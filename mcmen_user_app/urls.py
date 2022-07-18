from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name = 'landing'),
    path('logout_user/', views.logout_user, name = 'logout_user'),
    path('login_user/', views.login_user, name = 'login_user'),
    path('router/', views.router, name = 'router'),
    path('create_user_profile/', views.create_user_profile, name = 'create_profile'),
    path('update_profile/', views.update_profile, name = 'update_profile'),
]