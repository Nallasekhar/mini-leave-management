# API Documentation (sample inputs/outputs)

Base URL: http://127.0.0.1:8000/api/

## Create Employee
POST /employees/
Request:
{
  "name":"Sekhar N",
  "email":"sekhar@example.com",
  "department":"Engineering",
  "joining_date":"2024-07-01",
  "leave_balance":20
}
Response: 201 Created (employee object)

## Apply Leave
POST /leaves/
Request:
{
  "employee": 1,
  "start_date":"2025-09-10",
  "end_date":"2025-09-12",
  "reason":"Vacation"
}
Response: 201 Created (leave object)

## Approve / Reject
PUT /leave-action/{id}/
Request:
{ "status": "Approved" }
Response: { "message": "Leave Approved" }

## HTML + Bootstrap frontend(sample inputs/outputs)

Add Employee: http://127.0.0.1:8000/employee/add/

Apply Leave: http://127.0.0.1:8000/leave/apply/

Leave List: http://127.0.0.1:8000/leave/list/