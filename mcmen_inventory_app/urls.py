from django.urls import path
from . import views

urlpatterns = [
    path('inventory/', views.index_inventory, name = 'inventory'),
    path('breweries/', views.all_breweries, name = 'breweries'),
    path('brewery_details/<int:id>', views.brewery_details, name = 'details'),
    path('brewer_contacts/', views.brewer_contacts, name = 'brewer_contacts')
   ]