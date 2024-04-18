from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('create/', views.create_poll, name='create_poll'),
    path('list/', views.list_polls, name='list_polls'),
    path('poll_detail/<int:pk>/', views.poll_detail, name='poll_detail'),
]
