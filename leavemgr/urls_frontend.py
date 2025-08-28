from django.urls import path
from . import views_frontend

urlpatterns = [
    path("employee/add/", views_frontend.employee_form, name="employee_form"),
    path("leave/apply/", views_frontend.leave_form, name="leave_form"),
    path("leave/list/", views_frontend.leave_list, name="leave_list"),
]
