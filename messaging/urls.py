from django.urls import path
from . import views

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('compose/', views.compose_message, name='compose_message'),
    path('conversation/<int:pk>/', views.conversation_detail, name='conversation_detail'),
    path('announcements/', views.announcements, name='announcements'),
    path('announcements/create/', views.create_announcement, name='create_announcement'),
]
