from django.urls import path
from . import views

urlpatterns = [
    path('inventory/', views.index_inventory, name = 'inventory'),
    path('breweries/', views.all_breweries, name = 'breweries'),
    path('brewery_details/<int:id>', views.brewery_details, name = 'brew_details'),
    path('add_kegs/<int:id>', views.add_update_kegs, name = 'add'),
    path('update_kegs/<int:id>/<pk>', views.update_kegs, name = 'keg_update'),
    path('update_orders/<int:id>/<pk>', views.update_orders, name = 'order_update'),
    path('delete_keg/<int:id>/<pk>', views.delete_keg, name = 'remove'),
    path('delete_order/<int:id>/<pk>', views.delete_order, name = 'cancel'),
    path('adj_view/<int:id>', views.inventory_view, name = 'adj_view'),
   ]