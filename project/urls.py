from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


urlpatterns = [
    path('', lambda request: redirect('admin/')),
    path("admin/", admin.site.urls),                   # Django admin
    path("api/", include("leavemgr.urls")),            # REST API endpoints
    path("", include("leavemgr.urls_frontend")),       # Frontend HTML pages
]
admin.site.site_header = "Mini Leave Management System"
admin.site.site_title = "Mini Leave Management Admin"