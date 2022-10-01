from django.urls import path
from . import views   
    
urlpatterns = [
    path('order_index/', views.order_index, name = 'order_index'),
    path('order/<int:id>', views.order, name = 'order'),
    path('view_cart/<int:id>', views.view_cart, name = 'view_cart'),
    path('order_delivered/<int:id>', views.order_delivered, name = 'order_delivered'),
    path('dist_admin/', views.dist_admin, name = 'dist_admin'),
    path('place_order/<int:id>', views.place_order, name = 'place_order'),
    path('close_cart/<int:id>', views.close_cart, name = 'close_cart'),
    path('remove_item/<int:id>/<pk>', views.remove_item, name = 'remove_item'),
    path('close_order/<int:id>', views.close_order, name = 'close_order'),
    path('archive_order/<int:id>', views.archive_order, name = 'archive_order'),
    path('search_pub_orders/<int:id>', views.search_pub_orders, name = 'search_pub_orders'),
    path('search_order_archive/', views.search_order_archive, name = 'search_order_archive'),
]