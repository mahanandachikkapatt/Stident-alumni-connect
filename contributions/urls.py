from django.urls import path
from . import views

urlpatterns = [
    path('', views.contribution_list, name='contribution_list'),
    path('add/', views.contribution_add, name='contribution_add'),
    path('my-contributions/', views.my_contributions, name='my_contributions'),
    path('feedback/', views.feedback_list, name='feedback_list'),
    path('feedback/add/', views.feedback_add, name='feedback_add'),
    path('feedback/<int:pk>/respond/', views.feedback_respond, name='feedback_respond'),
]
