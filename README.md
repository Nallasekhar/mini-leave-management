# Mini Leave Management System 

This is a simple Django REST project skeleton for the **Mini Leave Management System** assignment.
It is easy to understand, run locally.
## Admin Login:

Username: admin
Password: Admin123@

## What is included
- Django app `leavemgr` with models, serializers, views and URLs.
- Basic project configuration (`project`).
- `requirements.txt`.
- `HLD.md` — high level design and scaling.

## Setup (local, simple)
1. Create & activate a virtualenv (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   
   ```
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations and start server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
4. Use the API (examples below) — by default it runs at `http://127.0.0.1:8000/`.

## API Endpoints (examples)
- `POST /api/employees/` — Add employee.
  ```json
  {
    "name": "Sekhar Nalla",
    "email": "sekhar@example.com",
    "department": "Engineering",
    "joining_date": "2024-07-01",
    "leave_balance": 20
  }
  ```
- `POST /api/leaves/` — Apply for leave.
  ```json
  {
    "employee": 1,
    "start_date": "2025-09-10",
    "end_date": "2025-09-12",
    "reason": "Personal"
  }
  ```
- `PUT /api/leave-action/{id}/` — Approve or reject leave.
  ```json
  { "status": "Approved" }
  ```
## Assumptions

- Each employee gets a default leave balance (20 days) unless specified.
- Leaves are full-day only (no half-days).
- HR is the one who approves/rejects leaves via the leave-action endpoint.
- No overlapping with already APPROVED leaves.


## Edge cases handled in code

- Applying for leave before joining date -> rejected.
- Applying for more days than available balance -> rejected.
- Overlapping leave requests -> rejected.
- Employee not found -> 404.
- Invalid dates (e.g., end date before start date) -> rejected.
- Approving when employee has insufficient balance -> rejected.
- Re-approving an already approved leave handled gracefully.
- Changing approved -> rejected restores balance.

## Potential improvements. 

- Partial leaves / half-day / hourly leaves.
- Public holidays calculation and exclusion.

