from django.urls import path
from . import views

urlpatterns = [
    path('management/', views.student_management, name='student_management'),
    path('consultation/save/', views.consultation_save, name='consultation_save'),
    path('consultation/delete/', views.consultation_delete, name='consultation_delete'),
    path('attendance/', views.attendance_management, name='attendance_management'),
    path('api/attendance/update/', views.api_attendance_update, name='api_attendance_update'),
    path('api/schedules/', views.api_schedule_list, name='api_schedule_list'),
    path('api/schedules/save/', views.api_schedule_save, name='api_schedule_save'),
    path('api/schedules/delete/', views.api_schedule_delete, name='api_schedule_delete'),
    path('', views.home, name='home'),
]
