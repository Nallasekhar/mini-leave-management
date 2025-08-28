from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Employee, LeaveRequest
from .serializers import EmployeeSerializer, LeaveRequestSerializer
from django.db.models import Q
import datetime

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all().order_by('id')
    serializer_class = EmployeeSerializer


class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.all().order_by('-applied_at')
    serializer_class = LeaveRequestSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        # Basic validations
        try:
            emp = Employee.objects.get(id=data.get('employee'))
        except Employee.DoesNotExist:
            return Response({'error':'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

        start = data.get('start_date')
        end = data.get('end_date')
        if not start or not end:
            return Response({'error':'start_date and end_date are required'}, status=status.HTTP_400_BAD_REQUEST)
        if start > end:
            return Response({'error':'end_date cannot be before start_date'}, status=status.HTTP_400_BAD_REQUEST)

        # before joining
        start_date_obj = datetime.datetime.strptime(start, '%Y-%m-%d').date()
        end_date_obj = datetime.datetime.strptime(end, '%Y-%m-%d').date()
        if start_date_obj < emp.joining_date:
            return Response({'error':'Cannot apply leave before joining date'}, status=status.HTTP_400_BAD_REQUEST)

        # overlapping with approved leaves
        overlaps = LeaveRequest.objects.filter(employee=emp, status=LeaveRequest.STATUS_APPROVED).filter(
            Q(start_date__lte=end_date_obj) & Q(end_date__gte=start_date_obj)
        )
        if overlaps.exists():
            return Response({'error':'Overlapping approved leave exists'}, status=status.HTTP_400_BAD_REQUEST)

        # days count
        days = (end_date_obj - start_date_obj).days + 1
        if emp.leave_balance < days:
            return Response({'error':'Not enough leave balance'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LeaveActionViewSet(viewsets.ViewSet):
    def update(self, request, pk=None):
        lr = get_object_or_404(LeaveRequest, pk=pk)
        status_choice = request.data.get('status')
        if status_choice not in [LeaveRequest.STATUS_APPROVED, LeaveRequest.STATUS_REJECTED]:
            return Response({'error':'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        if lr.status == LeaveRequest.STATUS_APPROVED and status_choice == LeaveRequest.STATUS_APPROVED:
            return Response({'message':'Already approved'}, status=status.HTTP_200_OK)

        # Approve: deduct balance
        if status_choice == LeaveRequest.STATUS_APPROVED:
            days = lr.days_count()
            if lr.employee.leave_balance < days:
                return Response({'error':'Employee does not have enough balance'}, status=status.HTTP_400_BAD_REQUEST)
            lr.employee.leave_balance -= days
            lr.employee.save()

        # If changing from approved to rejected, restore balance
        if lr.status == LeaveRequest.STATUS_APPROVED and status_choice == LeaveRequest.STATUS_REJECTED:
            lr.employee.leave_balance += lr.days_count()
            lr.employee.save()

        lr.status = status_choice
        lr.save()
        return Response({'message':f'Leave {status_choice}'}, status=status.HTTP_200_OK)
