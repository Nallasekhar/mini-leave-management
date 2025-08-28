from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, LeaveRequestViewSet, LeaveActionViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'leaves', LeaveRequestViewSet, basename='leaverequest')

leave_action = LeaveActionViewSet.as_view({'put':'update'})

urlpatterns = [
    path('', include(router.urls)),
    path('leave-action/<int:pk>/', leave_action, name='leave-action'),
]
