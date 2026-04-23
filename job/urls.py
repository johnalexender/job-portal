from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),

    path('job/<int:pk>/', views.job_detail, name='job_detail'),
    path('job/new/', views.job_create, name='job_create'),
    path('job/<int:pk>/edit/', views.job_edit, name='job_edit'),
    path('job/<int:pk>/delete/', views.job_delete, name='job_delete'),

    # ✅ APPLY
    path('job/<int:pk>/apply/', views.job_apply, name='job_apply'),

    path('job/<int:pk>/applications/', views.job_applications, name='job_applications'),

    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    path('applications/', views.my_applications, name='my_applications'),
    path('applications/status/', views.application_status, name='application_status'),
]