from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name = 'landing'),
    path('index/', views.index, name = 'index'),
    path('logout_user/', views.logout_user, name = 'logout_user'),
    path('login_user/', views.login_user, name = 'login_user'),
    path('admin_page/', views.admin_page, name = 'admin_page'),
    path('add_property/', views.add_property, name = 'add_property'),
    path('add_driver/', views.add_driver, name = 'add_driver'),
    path('add_route/', views.add_route, name = 'add_route'),
    path('view_routes/', views.all_routes, name = 'view_routes'),
    path('view_all_posts/', views.view_all_posts, name = 'view_all_posts'),
    path('post_details/<int:id>', views.post_details, name = 'details'),
    path('add_post/', views.add_driver_post, name = 'add_post'),
    path('view_props/', views.all_props, name = 'view_props'),
    path('prop_details/<int:id>', views.prop_details, name = 'prop_details'),
    path('api/property/<int:pk>', views.property_detail),
    path('search_routes/', views.search_routes, name = 'search_routes'),
    path('contacts/', views.contacts, name = 'contacts')
]