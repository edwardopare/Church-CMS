# Church of Christ West Hills City Management System

A complete, production-ready Church Management System built with Django, Bootstrap 5, and PostgreSQL.

---

## Features

| Module | Features |
|---|---|
| **Auth & Users** | Registration, login, password reset, profile photos, role-based permissions |
| **Members** | Directory, family groups, baptism/confirmation records, membership tracking |
| **Attendance** | Service attendance, analytics, 8-week trends |
| **Finance** | Tithes, offerings, donations, pledges, expenses, 12-month reports |
| **Ministries** | Create ministries, assign leaders, manage members |
| **Events** | Event creation, calendar view, registration with capacity limits |
| **Communication** | Announcements, internal messaging inbox |
| **Reports** | Membership growth, attendance, financial, visitor conversion |
| **Visitor Management** | Record visitors, follow-up tracking, convert to members |

---

## User Roles

| Role | Access |
|---|---|
| **Super Admin** | Full access to everything |
| **Church Admin** | Manage members, users, all modules |
| **Pastor** | View members, take attendance, post announcements |
| **Finance Officer** | Full finance module access |
| **Ministry Leader** | Manage ministries and events |
| **Member** | View dashboard, events, announcements, inbox |
| **Guest** | Minimal access |

---

## Quick Start

### 1. Clone / extract the project

```bash
cd church_cms
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install django pillow
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Seed example data

```bash
python manage.py seed_data
```

### 6. Run development server

```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000** and log in with:

| Username | Password | Role |
|---|---|---|
| `admin` | `admin123` | Super Admin |
| `pastor` | `password123` | Pastor |
| `finance_officer` | `password123` | Finance Officer |
| `ministry_leader` | `password123` | Ministry Leader |
| `kofi` | `password123` | Member |

---

## Project Structure

```
church_cms/
├── church_management/     # Project config (settings, urls, wsgi)
├── accounts/              # Custom user model, roles, auth
├── members/               # Members, families, visitors
├── attendance/            # Service attendance, analytics
├── finance/               # Transactions, pledges, reports
├── ministries/            # Ministry groups
├── events/                # Events, calendar, registration
├── communication/         # Announcements, inbox
├── reports/               # Analytics dashboard
├── templates/             # All HTML templates
├── static/                # CSS, JS, images
└── media/                 # User-uploaded files
```

---

## Upgrading to PostgreSQL

In `church_management/settings.py`, replace the `DATABASES` block:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'church_cms'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

Then run: `pip install psycopg2-binary && python manage.py migrate`

---

## Production Deployment Checklist

- [ ] Set `DEBUG = False` in settings
- [ ] Set a strong `SECRET_KEY` (use environment variable)
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Switch to PostgreSQL
- [ ] Configure SMTP email backend
- [ ] Run `python manage.py collectstatic`
- [ ] Use Gunicorn + Nginx (or similar)
- [ ] Set up SSL/HTTPS

```bash
pip install gunicorn
gunicorn church_management.wsgi:application --bind 0.0.0.0:8000
```

---

## Tech Stack

- **Backend**: Django 4+
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Frontend**: Bootstrap 5, Font Awesome 6, Chart.js 4
- **Fonts**: Playfair Display + DM Sans
- **Calendar**: FullCalendar 3
