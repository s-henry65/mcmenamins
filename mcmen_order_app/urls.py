from django.urls import path
from . import views   
    
urlpatterns = [
    path('order/<int:id>', views.order, name = 'order'),
    path('view_cart/<int:id>', views.view_cart, name = 'view_cart'),
    path('order_delivered/<int:id>', views.order_delivered, name = 'order_delivered'),
    path('dist_admin/', views.dist_admin, name = 'dist_admin'),
    path('place_order/<int:id>', views.place_order, name = 'place_order'),
    path('edit_cart/<int:id>', views.edit_cart, name = 'edit_cart'),
    path('close_cart/<int:id>', views.close_cart, name = 'close_cart'),
]