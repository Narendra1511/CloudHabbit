# CloudHabit ☁️

CloudHabit is a cloud-based microhabit tracking web application built with Django. Users can register, create habits, track daily completions, update existing habits, delete habits, and review progress from a modern cloud-style dashboard.

## Features
- User registration, login, and logout
- Create, read, update, and delete habits
- Daily log tracking with notes and count
- Dashboard cards for total habits, active habits, completed logs, and today's progress
- Streak and completion-rate calculations
- AWS-ready Django configuration using environment variables
- Production support for PostgreSQL, Gunicorn, and WhiteNoise
- GitHub Actions workflow for linting, security scan, migration check, and test execution

## Local setup
1. Create a virtual environment
2. Install requirements
3. Copy `.env.example` to `.env`
4. Run migrations
5. Create a superuser
6. Start the server

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## AWS deployment outline without IAM roles
This project can be deployed to **AWS EC2** without IAM roles by using direct SSH deployment and environment variables stored in an `.env` file.

### Recommended stack
- EC2 Ubuntu instance
- PostgreSQL on Amazon RDS
- Nginx reverse proxy
- Gunicorn app server
- GitHub Actions for CI/CD

### EC2 steps
```bash
sudo apt update && sudo apt install -y python3-venv python3-pip nginx git
```

Clone the project, create a virtual environment, install requirements, set your `.env`, run:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn cloudhabit.wsgi:application --bind 0.0.0.0:8000
```

Then point Nginx to Gunicorn and open port 80 in the EC2 security group.

### Example production environment values
```env
DJANGO_SECRET_KEY=your-production-secret
DEBUG=False
ALLOWED_HOSTS=your-ec2-public-dns,localhost
CSRF_TRUSTED_ORIGINS=http://your-ec2-public-dns,https://your-domain.com
DATABASE_URL=postgresql://username:password@rds-endpoint:5432/cloudhabit
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=False
```

## CI/CD notes
The included GitHub Actions workflow:
- installs dependencies
- runs `flake8`
- runs `bandit`
- runs `pip-audit`
- runs Django checks and tests

For CD to AWS EC2 without IAM roles, store these GitHub secrets:
- `EC2_HOST`
- `EC2_USERNAME`
- `EC2_SSH_KEY`
- `APP_DIR`

Then extend the workflow with SSH deployment commands.

## Suggested report screenshots
- Landing page
- Dashboard with habits
- Habit create/edit form
- GitHub Actions successful run
- Bandit or pip-audit findings
- AWS hosted app URL in browser

## Default demo idea
Create habits such as:
- Drink 8 glasses of water
- Read 10 pages
- Walk 20 minutes
- Sleep before 11 PM
