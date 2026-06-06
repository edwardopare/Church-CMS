"""
Seed command — updated to match new Member model (no user FK, no Family).
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seeds the database with example church data'

    def handle(self, *args, **kwargs):
        from accounts.models import CustomUser
        from members.models import Member, Visitor
        from attendance.models import ServiceType, AttendanceRecord, AttendanceEntry
        from finance.models import FundCategory, Transaction
        from ministries.models import Ministry, MinistryMembership
        from events.models import Event
        from communication.models import Announcement

        self.stdout.write('Seeding database...')

        # ── Super Admin ──
        admin, _ = CustomUser.objects.get_or_create(username='admin', defaults={
            'email': 'admin@churchofchrist-redtop.org', 'first_name': 'System', 'last_name': 'Admin',
            'role': 'super_admin', 'is_staff': True, 'is_superuser': True,
        })
        admin.set_password('admin123')
        admin.save()

        # ── Staff users ──
        roles = [
            ('pastor', 'Rev. John', 'Mensah', 'pastor@churchofchrist-redtop.org', 'pastor'),
            ('finance_officer', 'Grace', 'Asante', 'finance@churchofchrist-redtop.org', 'finance_officer'),
            ('ministry_leader', 'Abena', 'Boateng', 'ministry@churchofchrist-redtop.org', 'ministry_leader'),
        ]
        staff_users = []
        for username, fn, ln, email, role in roles:
            u, _ = CustomUser.objects.get_or_create(username=username, defaults={
                'first_name': fn, 'last_name': ln, 'email': email, 'role': role,
                'is_active_member': True, 'join_date': date(2020, 1, 1),
            })
            u.set_password('password123')
            u.save()
            staff_users.append(u)

        # ── Members (standalone, no user account) ──
        members_data = [
            ('Kofi', 'Owusu', 'kofi@email.com', '0244000001', 'M'),
            ('Ama', 'Appiah', 'ama@email.com', '0244000002', 'F'),
            ('Kwame', 'Darko', 'kwame@email.com', '0244000003', 'M'),
            ('Akosua', 'Frempong', 'akosua@email.com', '0244000004', 'F'),
            ('Yaw', 'Adusei', 'yaw@email.com', '0244000005', 'M'),
            ('Adwoa', 'Sarpong', 'adwoa@email.com', '0244000006', 'F'),
            ('Kojo', 'Antwi', 'kojo@email.com', '0244000007', 'M'),
            ('Abena', 'Kyei', 'abena@email.com', '0244000008', 'F'),
            ('Nana', 'Asare', 'nana@email.com', '0244000009', 'M'),
            ('Efua', 'Mensah', 'efua@email.com', '0244000010', 'F'),
        ]
        created_members = []
        for fn, ln, email, phone, gender in members_data:
            m, _ = Member.objects.get_or_create(first_name=fn, last_name=ln, defaults={
                'email': email, 'phone': phone, 'gender': gender,
                'membership_status': 'active',
                'membership_date': date(2021, random.randint(1, 12), 1),
                'is_baptised': random.choice([True, True, False]),
                'is_confirmed': random.choice([True, False]),
                'occupation': random.choice(['Teacher', 'Engineer', 'Nurse', 'Accountant', 'Trader']),
            })
            created_members.append(m)

        self.stdout.write(f'  Created {len(created_members)} members')

        # ── Service Types ──
        for name in ['Sunday Service', 'Wednesday Bible Study', 'Prayer Meeting', 'Youth Service']:
            ServiceType.objects.get_or_create(name=name)

        # ── Attendance ──
        sunday = ServiceType.objects.get(name='Sunday Service')
        all_users = list(CustomUser.objects.filter(is_active_member=True))
        for weeks_ago in range(1, 9):
            record_date = date.today() - timedelta(weeks=weeks_ago)
            days_to_sunday = (record_date.weekday() + 1) % 7
            record_date -= timedelta(days=days_to_sunday)
            record, created = AttendanceRecord.objects.get_or_create(
                service_type=sunday, date=record_date,
                defaults={'recorded_by': admin}
            )
            if created and all_users:
                present = random.sample(all_users, k=min(len(all_users), random.randint(3, len(all_users))))
                for u in present:
                    AttendanceEntry.objects.get_or_create(record=record, member=u, defaults={'is_present': True})

        # ── Fund Categories ──
        for name in ['General Fund', 'Building Fund', 'Missions', 'Benevolence', 'Youth Ministry']:
            FundCategory.objects.get_or_create(name=name)
        general = FundCategory.objects.get(name='General Fund')

        # ── Transactions ──
        for i in range(25):
            t_date = date.today() - timedelta(days=random.randint(0, 90))
            Transaction.objects.create(
                transaction_type=random.choice(['tithe', 'offering', 'donation', 'tithe', 'offering']),
                member=random.choice(all_users) if all_users else None,
                amount=round(random.uniform(20, 500), 2),
                fund_category=general,
                payment_method=random.choice(['cash', 'mobile_money', 'bank_transfer']),
                date=t_date,
                recorded_by=admin,
            )

        # ── Ministries ──
        ministry_data = [
            ('Choir Ministry', 'Music and worship through song'),
            ('Youth Ministry', 'Engaging the next generation'),
            ('Ushering Ministry', 'Welcoming and seating congregation'),
            ("Women's Fellowship", 'Empowering women in faith'),
        ]
        for name, desc in ministry_data:
            Ministry.objects.get_or_create(name=name, defaults={
                'description': desc, 'leader': staff_users[0], 'is_active': True,
                'meeting_schedule': 'Every Saturday 9am',
            })

        # ── Events ──
        event_data = [
            ('Sunday Worship Service', 'service', 7),
            ('Annual Convention 2025', 'conference', 30),
            ('Youth Retreat', 'youth', 14),
            ('Community Outreach', 'outreach', 3),
        ]
        for title, etype, days_ahead in event_data:
            Event.objects.get_or_create(title=title, defaults={
                'event_type': etype,
                'start_datetime': timezone.now() + timedelta(days=days_ahead),
                'end_datetime': timezone.now() + timedelta(days=days_ahead, hours=3),
                'location': 'Church of Christ - RedTop Auditorium',
                'organizer': admin,
                'is_public': True,
                'requires_registration': etype == 'conference',
                'max_capacity': 200 if etype == 'conference' else None,
            })

        # ── Visitors ──
        for fn, ln, status in [
            ('Emmanuel', 'Asare', 'new'), ('Felicia', 'Oteng', 'returning'),
            ('George', 'Mensah', 'interested'), ('Helen', 'Darko', 'converted'),
        ]:
            Visitor.objects.get_or_create(first_name=fn, last_name=ln, defaults={
                'visit_date': date.today() - timedelta(days=random.randint(1, 30)),
                'status': status,
                'assigned_to': staff_users[0],
                'how_heard': 'Friend invitation',
                'converted_member_name': 'Kofi Owusu' if status == 'converted' else '',
            })

        # ── Announcement ──
        Announcement.objects.get_or_create(title='Welcome to Church of Christ - RedTop CMS', defaults={
            'content': 'The system is live! Use the sidebar to navigate. Contact admin for role or permissions help.',
            'author': admin, 'priority': 'high', 'is_published': True,
        })

        self.stdout.write(self.style.SUCCESS('\n✓ Database seeded successfully!'))
        self.stdout.write('\nLogin credentials:')
        self.stdout.write('  admin / admin123  (Super Admin)')
        self.stdout.write('  pastor / password123  (Pastor)')
        self.stdout.write('  finance_officer / password123  (Finance Officer)')
        self.stdout.write('  ministry_leader / password123  (Ministry Leader)')
