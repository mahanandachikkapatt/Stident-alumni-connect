from django.urls import path
from . import views

urlpatterns = [
    path('', views.mentorship_list, name='alumni_list'),
    path('request/', views.mentorship_request, name='alumni_request'),
    path('requests/', views.mentorship_requests, name='alumni_requests'),
    path('request/<int:pk>/accept/', views.accept_request, name='accept_alumni_request'),
    path('request/<int:pk>/reject/', views.reject_request, name='reject_alumni_request'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/create/', views.job_create, name='job_create'),
    path('jobs/<int:pk>/apply/', views.job_apply, name='job_apply'),
    path('my-jobs/', views.my_jobs, name='my_jobs'),
]
