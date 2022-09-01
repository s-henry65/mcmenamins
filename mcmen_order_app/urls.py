from django.urls import path
from . import views   
    
urlpatterns = [
    path('order/<int:id>', views.order, name = 'order'),
    path('view_cart/<int:id>', views.view_cart, name = 'view_cart'),
    path('order_delivered/<int:id>', views.order_delivered, name = 'order_delivered'),
    path('dist_admin/', views.dist_admin, name = 'dist_admin'),
    path('place_order/<int:id>', views.place_order, name = 'place_order'),
    path('close_cart/<int:id>', views.close_cart, name = 'close_cart'),
    path('remove_item/<int:id>/<pk>', views.remove_item, name = 'remove_item'),
    path('close_order/<int:id>', views.close_order, name = 'close_order'),
    path('archive_order/<int:id>', views.archive_order, name = 'archive_order'),
    path('order_archive/', views.order_archive, name = 'order_archive'),
    # path('open_cart/', views.open_cart, name = 'open_cart'),
]