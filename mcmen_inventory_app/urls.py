from django.urls import path
from . import views

urlpatterns = [
    path('index_inventory/', views.index_inventory, name = 'index_inventory'),
    path('inventory/', views.total_inventory, name = 'inventory'),
    path('brewery_details/<int:id>', views.brewery_details, name = 'brew_details'),
    path('add_kegs/<int:id>', views.add_update_kegs, name = 'add'),
    path('update_kegs/<int:id>/<pk>', views.update_kegs, name = 'keg_update'),
    path('update_orders/<int:id>/<pk>', views.update_orders, name = 'order_update'),
    path('delete_keg/<int:id>/<pk>', views.delete_keg, name = 'remove'),
    path('delete_order/<int:id>/<pk>', views.delete_order, name = 'cancel'),
    path('adj_view/<int:id>', views.inventory_view, name = 'adj_view'),
    path('adj_total_view/', views.total_inventory_view, name = 'adj_total_view'),
    path('all_brew_posts/', views.all_brew_posts, name = 'all_brew_posts'),
    path('brew_post_details/<int:id>', views.brew_post_details, name = 'brew_post_details'),
    path('add_brewer_post/', views.add_brewer_post, name = 'add_brewer_post'),
    path('search_inventory/', views.search_inventory, name = 'search_inventory'),
   ]