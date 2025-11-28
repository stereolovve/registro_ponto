# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a complete time tracking and payroll management system with a Django REST API backend and React TypeScript frontend. The system allows employees to clock in/out, track work hours, and supervisors to approve timesheets and calculate salaries.

## Architecture

### Backend (Django)
- **Django 4.2.7** with Django REST Framework
- **JWT Authentication** using `djangorestframework-simplejwt`
- **SQLite database** for development
- Two main Django apps:
  - `accounts` - User management, profiles, authentication
  - `timetrack` - Time records, work codes, salary calculations

### Frontend (React)
- **React 19.1.1** with TypeScript
- **React Router** for navigation
- **Tailwind CSS** for styling with Radix UI components
- **Axios** for API communication
- **Context API** for authentication and theme management

### Key Models
- `Profile` (accounts/models.py:6) - Extended user profile with hourly rates
- `TimeRecord` (timetrack/models.py:22) - Time tracking with up to 3 periods per day
- `WorkCode` (timetrack/models.py:8) - Project/work classification codes
- `Salary` (timetrack/models.py:95) - Monthly salary calculations

## Development Commands

### Backend (Django)
```bash
# Start Django development server
python manage.py runserver

# Run database migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Create test data (users, work codes, sample records)
python create_test_data.py

# Access Django admin
# http://localhost:8000/admin/
```

### Frontend (React)
```bash
# Install dependencies
cd frontend
npm install

# Start development server
npm start
# Runs on http://localhost:3000

# Build production bundle
npm run build

# Run tests
npm run test
```

### API Endpoints Structure

The API follows REST conventions with these main routes:
- `/api/accounts/` - Authentication, user profiles
- `/api/timetrack/` - Time records, work codes, dashboard data

Key endpoints:
- `POST /api/accounts/login/` - JWT authentication
- `GET /api/timetrack/dashboard/` - Dashboard statistics
- `POST /api/timetrack/time-records/` - Create time records
- `GET /api/timetrack/salaries/` - Salary calculations

## Development Guidelines

### Time Record Validation
The `TimeRecord.clean()` method (timetrack/models.py:54) enforces logical time constraints:
- Exit times must be after entry times
- No overlapping periods
- Maximum 3 periods per day

### Frontend Authentication
- JWT tokens stored in localStorage via `AuthContext` (frontend/src/contexts/AuthContext.tsx)
- `PrivateRoute` component protects authenticated routes
- Automatic token refresh handling

### Database Relationships
- Users have one Profile (one-to-one)
- TimeRecords belong to User and WorkCode (foreign keys)
- Approval system: TimeRecords can be approved by supervisors
- Salary calculations aggregate TimeRecord hours per month

## Testing & Data

### Test Credentials
Run `python create_test_data.py` to create:
- **Admin:** username=`admin`, password=`admin123`
- **Employee:** username=`funcionario`, password=`func123`

### Test Interface
A standalone HTML test interface exists at `frontend/public/test.html` for API testing without the React app.

## Configuration Notes

### CORS Settings
The Django backend is configured to accept requests from:
- localhost:3000, localhost:3001, localhost:3006 (React dev servers)
- Both 127.0.0.1 and localhost variants

### Environment
- Uses `python-decouple` for environment variables
- Brazilian locale (pt-br) and São Paulo timezone
- SQLite database in development (db.sqlite3)

### File Structure
```
app/                     # Django project config
├── accounts/            # User management app
├── timetrack/          # Time tracking app  
├── frontend/           # React TypeScript app
├── manage.py           # Django CLI
├── requirements.txt    # Python dependencies
└── create_test_data.py # Test data generator
```

## Important Business Logic

### Time Calculation
Hours are calculated using `calcular_horas_trabalhadas()` method (timetrack/models.py:75) which sums all periods and returns decimal hours.

### Salary Processing  
Monthly salaries auto-calculate as `hours_worked * hourly_rate` when saved (timetrack/models.py:120).

### User Roles
- `funcionario` (employee) - Can record time, view own records
- `supervisor` - Can approve records, access all user data