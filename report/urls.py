from django.urls import path
from . import views

urlpatterns = [
    path('report/new/', views.report_create, name='report_create'),
    path('report/my/', views.report_user_list, name='report_user_list'),
    path('report/my/<int:pk>/', views.report_user_detail, name='report_user_detail'),

    # admin/superuser
    path('admin/reports/', views.admin_report_list, name='admin_report_list'),
    path('admin/reports/<int:pk>/', views.admin_report_detail, name='admin_report_detail'),
]
