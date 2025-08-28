from django.db import models
from django.core.exceptions import ValidationError
class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    joining_date = models.DateField()
    leave_balance = models.IntegerField(default=20)

    def __str__(self):
        return f"{self.name} ({self.email})"


class LeaveRequest(models.Model):
    STATUS_PENDING = 'Pending'
    STATUS_APPROVED = 'Approved'
    STATUS_REJECTED = 'Rejected'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leaves')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    applied_at = models.DateTimeField(auto_now_add=True)

    def days_count(self):
        return (self.end_date - self.start_date).days + 1
    
    def clean(self):
        # Employee must exist
        if not self.employee_id:
            raise ValidationError("Employee not found")

        # Leave before joining date
        if self.start_date < self.employee.joining_date:
            raise ValidationError("Leave cannot be before joining date")

        # Invalid dates
        if self.end_date < self.start_date:
            raise ValidationError("End date cannot be before start date")

        # Check overlapping leaves
        overlap = LeaveRequest.objects.filter(
            employee=self.employee,
            status="Approved",
            start_date__lte=self.end_date,
            end_date__gte=self.start_date
        ).exclude(id=self.id)
        if overlap.exists():
            raise ValidationError("Overlapping leave request found")

        # Balance check (only on approval)
        if self.status == "Approved":
            days = (self.end_date - self.start_date).days + 1
            if days > self.employee.leave_balance:
                raise ValidationError("Not enough leave balance")
            self.employee.leave_balance -= days
            self.employee.save()

        super().save(*args, **kwargs)


    def __str__(self):
        return f"Leave {self.id} for {self.employee}"
