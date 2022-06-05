from django.urls import path
from . import views

urlpatterns = [
    path('inventory/', views.index_inventory, name = 'inventory'),
    path('breweries/', views.all_breweries, name = 'breweries'),
    path('brewery_details/<int:id>', views.brewery_details, name = 'details'),
    path('brewer_contacts/', views.brewer_contacts, name = 'brewer_contacts'),
    path('add_kegs/<int:id>', views.add_update_kegs, name = 'add'),
    path('update_kegs/<int:id>/<pk>', views.update_kegs, name = 'keg_update'),
    path('update_orders/<int:id>/<pk>', views.update_orders, name = 'order_update'),
    path('delete_keg/<int:id>/<pk>', views.delete_keg, name = 'remove'),
    path('delete_order/<int:id>/<pk>', views.delete_order, name = 'cancel'),
   ]