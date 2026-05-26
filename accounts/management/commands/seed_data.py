"""
Management command to seed the database with example data.
Usage: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seeds the database with example church data'

    def handle(self, *args, **kwargs):
        from accounts.models import CustomUser
        from members.models import Member, Family, Visitor
        from attendance.models import ServiceType, AttendanceRecord, AttendanceEntry
        from finance.models import FundCategory, Transaction
        from ministries.models import Ministry, MinistryMembership
        from events.models import Event
        from communication.models import Announcement

        self.stdout.write('Seeding database...')

        # ── Super Admin ──
        admin, _ = CustomUser.objects.get_or_create(username='admin', defaults={
            'email': 'admin@gracechurch.org', 'first_name': 'System', 'last_name': 'Admin',
            'role': 'super_admin', 'is_staff': True, 'is_superuser': True,
        })
        admin.set_password('admin123')
        admin.save()
        self.stdout.write('  Created admin user (admin/admin123)')

        # ── Role users ──
        roles = [
            ('pastor', 'Rev. John', 'Mensah', 'pastor@gracechurch.org', 'pastor'),
            ('finance_officer', 'Grace', 'Asante', 'finance@gracechurch.org', 'finance_officer'),
            ('ministry_leader', 'Abena', 'Boateng', 'ministry@gracechurch.org', 'ministry_leader'),
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

        # ── Families ──
        fam_names = ['Mensah Family', 'Asante Family', 'Boateng Family', 'Owusu Family', 'Appiah Family']
        families = []
        for name in fam_names:
            f, _ = Family.objects.get_or_create(name=name)
            families.append(f)

        # ── Members ──
        member_data = [
            ('kofi', 'Kofi', 'Owusu', 'kofi@email.com'), ('ama', 'Ama', 'Appiah', 'ama@email.com'),
            ('kwame', 'Kwame', 'Darko', 'kwame@email.com'), ('akosua', 'Akosua', 'Frempong', 'akosua@email.com'),
            ('yaw', 'Yaw', 'Adusei', 'yaw@email.com'), ('adwoa', 'Adwoa', 'Sarpong', 'adwoa@email.com'),
            ('kojo', 'Kojo', 'Antwi', 'kojo@email.com'), ('abena2', 'Abena', 'Kyei', 'abena2@email.com'),
        ]
        member_users = []
        for username, fn, ln, email in member_data:
            u, _ = CustomUser.objects.get_or_create(username=username, defaults={
                'first_name': fn, 'last_name': ln, 'email': email, 'role': 'member',
                'is_active_member': True, 'join_date': date(2021, random.randint(1, 12), 1),
            })
            u.set_password('password123')
            u.save()
            Member.objects.get_or_create(user=u, defaults={
                'family': random.choice(families),
                'membership_status': 'active',
                'membership_date': date(2021, random.randint(1, 12), 1),
                'is_baptised': random.choice([True, True, False]),
                'is_confirmed': random.choice([True, False]),
                'occupation': random.choice(['Teacher', 'Engineer', 'Nurse', 'Accountant', 'Trader']),
            })
            member_users.append(u)

        # Create member profiles for staff too
        for u in staff_users:
            Member.objects.get_or_create(user=u, defaults={
                'family': random.choice(families),
                'membership_status': 'active',
                'membership_date': date(2020, 1, 1),
                'is_baptised': True,
            })

        self.stdout.write(f'  Created {len(member_data)} members + {len(staff_users)} staff members')

        # ── Service Types ──
        for name in ['Sunday Service', 'Wednesday Bible Study', 'Prayer Meeting', 'Youth Service']:
            ServiceType.objects.get_or_create(name=name)

        # ── Attendance Records ──
        sunday = ServiceType.objects.get(name='Sunday Service')
        all_users = list(CustomUser.objects.filter(is_active_member=True))
        for weeks_ago in range(1, 9):
            record_date = date.today() - timedelta(weeks=weeks_ago)
            # Make it a Sunday
            # ensure it is a Sunday (weekday 6)
            days_to_sunday = (record_date.weekday() + 1) % 7
            record_date -= timedelta(days=days_to_sunday)
            record, created = AttendanceRecord.objects.get_or_create(
                service_type=sunday, date=record_date,
                defaults={'recorded_by': admin}
            )
            if created:
                present = random.sample(all_users, k=min(len(all_users), random.randint(8, len(all_users))))
                for u in present:
                    AttendanceEntry.objects.get_or_create(record=record, member=u, defaults={'is_present': True})

        # ── Fund Categories ──
        for name in ['General Fund', 'Building Fund', 'Missions', 'Benevolence', 'Youth Ministry']:
            FundCategory.objects.get_or_create(name=name)
        general = FundCategory.objects.get(name='General Fund')

        # ── Transactions ──
        for i in range(20):
            t_date = date.today() - timedelta(days=random.randint(0, 90))
            t_type = random.choice(['tithe', 'offering', 'donation', 'tithe', 'offering'])
            Transaction.objects.create(
                transaction_type=t_type,
                member=random.choice(all_users),
                amount=round(random.uniform(20, 500), 2),
                fund_category=general,
                payment_method=random.choice(['cash', 'mobile_money', 'bank_transfer']),
                date=t_date,
                recorded_by=admin,
            )

        # ── Ministries ──
        ministry_data = [
            ('Choir Ministry', 'Music and worship through song', staff_users[0]),
            ('Youth Ministry', 'Engaging the next generation', staff_users[2]),
            ('Ushering Ministry', 'Welcoming and seating congregation', staff_users[0]),
            ("Women's Fellowship", 'Empowering women in faith', staff_users[1]),
        ]
        for name, desc, leader in ministry_data:
            m, _ = Ministry.objects.get_or_create(name=name, defaults={
                'description': desc, 'leader': leader, 'is_active': True,
                'meeting_schedule': 'Every Saturday 9am',
            })
            # Add some members
            for u in random.sample(member_users, k=min(4, len(member_users))):
                MinistryMembership.objects.get_or_create(ministry=m, member=u)

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
                'location': 'Grace Church Auditorium',
                'organizer': admin,
                'is_public': True,
                'requires_registration': etype == 'conference',
                'max_capacity': 200 if etype == 'conference' else None,
            })

        # ── Visitors ──
        visitor_data = [
            ('Emmanuel', 'Asare', 'new'), ('Felicia', 'Oteng', 'returning'),
            ('George', 'Mensah', 'interested'), ('Helen', 'Darko', 'converted'),
        ]
        for fn, ln, status in visitor_data:
            Visitor.objects.get_or_create(first_name=fn, last_name=ln, defaults={
                'visit_date': date.today() - timedelta(days=random.randint(1, 30)),
                'status': status,
                'assigned_to': staff_users[0],
                'how_heard': 'Friend invitation',
            })

        # ── Announcement ──
        Announcement.objects.get_or_create(title='Welcome to Grace Church CMS', defaults={
            'content': 'This system is live! Use the sidebar to navigate all modules. '
                       'Contact the admin if you need help with your role or permissions.',
            'author': admin, 'priority': 'high', 'is_published': True,
        })

        self.stdout.write(self.style.SUCCESS('✓ Database seeded successfully!'))
        self.stdout.write('\nLogin credentials:')
        self.stdout.write('  admin / admin123  (Super Admin)')
        self.stdout.write('  pastor / password123  (Pastor)')
        self.stdout.write('  finance_officer / password123  (Finance Officer)')
        self.stdout.write('  ministry_leader / password123  (Ministry Leader)')
        self.stdout.write('  kofi / password123  (Member)')
