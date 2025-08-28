# High Level Design (Mini Leave Management System)

## Architecture diagram (Frontend, Backend, Database).
                ┌─────────────────────────────┐
                │         Frontend            │
                │   Django + HTML templates.  |
                └──────────────┬──────────────┘
                               │ HTTP (REST API)
                               ▼
                ┌─────────────────────────────┐
                │          Backend            │
                │    Django + DRF (APIs)      │
                │   - Add Employee            │
                │   - Apply Leave             │
                │   - Approve/Reject Leave    │
                │   - Track Leave Balance     │
                └──────────────┬──────────────┘
                               │ ORM Queries
                               ▼
                ┌─────────────────────────────┐
                │         Database            |
                │    SQLite (dev) / Postgres  │
                │   Tables:                   │
                │   - Employee                │
                │   - LeaveRequest            │
                └─────────────────────────────┘

## Components
- Frontend: simple HTML pages that call the REST APIs.
- Backend: Django REST Framework (this project).
- Database: SQLite for local submission.

## API <-> DB Flow
1. Frontend sends HTTP request to Backend REST endpoint.
2. Backend validates request, runs business logic (edge-case checks).
3. Backend reads/writes to DB (Employee, LeaveRequest tables).
4. Backend returns JSON response.

## Scaling from 50 -> 500 employees
- Move DB from SQLite -> PostgreSQL.
- Deploy backend to a cloud provider (Heroku / Render / AWS).


