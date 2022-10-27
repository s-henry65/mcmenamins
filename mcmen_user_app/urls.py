from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name = 'landing'),
    path('logout_user/', views.logout_user, name = 'logout_user'),
    path('login_user/', views.login_user, name = 'login_user'),
    path('router/', views.router, name = 'router'),
    path('create_user_profile/<int:id>', views.create_user_profile, name = 'create_profile'),
    path('update_profile/', views.update_profile, name = 'update_profile'),
    path('create_user/', views.create_user, name = 'create_user'),
    path('view_users/', views.view_users, name = 'view_users'),
    path('delete_user/<int:id>', views.delete_user, name = 'delete_user'),
    path('contacts/', views.contacts, name = 'contacts'),
    path('user_manual/', views.user_manual, name = 'user_manual'),
]