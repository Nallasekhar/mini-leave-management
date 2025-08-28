from django.shortcuts import render, redirect
from .models import Employee, LeaveRequest

def employee_form(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        department = request.POST.get("department")
        joining_date = request.POST.get("joining_date")
        Employee.objects.create(
            name=name, email=email,
            department=department,
            joining_date=joining_date
        )
        return redirect("employee_form")
    return render(request, "leavemgr/employee_form.html")


def leave_form(request):
    employees = Employee.objects.all()
    if request.method == "POST":
        emp_id = request.POST.get("employee")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        reason = request.POST.get("reason")
        LeaveRequest.objects.create(
            employee_id=emp_id,
            start_date=start_date,
            end_date=end_date,
            reason=reason
        )
        return redirect("leave_list")
    return render(request, "leavemgr/leave_form.html", {"employees": employees})


def leave_list(request):
    leaves = LeaveRequest.objects.all().select_related("employee")
    return render(request, "leavemgr/leave_list.html", {"leaves": leaves})
