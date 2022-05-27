
from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from mcmen_inventory_app.models import Kegs
from mcmen_inventory_app.models import Brewer, Brewery
from mcmen_dist_app.models import Driver
from mcmen_dist_app.models import Property
from mcmen_inventory_app.models import Order

@login_required
def index_inventory(request):
    # print('START')
    keg_totals = {}
    keg_data = Kegs.objects.all()
    # print('DATA ',keg_data)
    
    counter = 0
    for keg in keg_data:
        # print('FOR ', counter, ' ', keg_data[counter].beer)
        counter2 = counter + 1
        # print('WHILE ', counter2)
        while counter2 <= (len(keg_data)) -1:
            if (keg_data[counter].beer) == (keg_data[counter2].beer):
                (keg_data[counter2].quantity) = (keg_data[counter2].quantity) + (keg_data[counter].quantity)   
                counter2 += 1
                # print('MATCH')
            else:
                keg_totals[keg.beer] = keg.quantity     
            counter2 += 1      
        counter += 1
    # print('DICT ', keg_totals)

    context = {
        'keg_totals' : keg_totals,
    }
    return render(request, 'inventory/index_inventory.html', context)

@login_required
def all_breweries(request):
  breweries = Brewery.objects.all()
  return render(request, 'inventory/view_breweries.html', {'breweries': breweries})

@login_required
def brewery_details(request, id):
    current_user = request.user
    brew_prop = Brewery.objects.get(id = id)
    property = Property.objects.all()
    keg_data = Kegs.objects.filter(brewery = id)
    context = {'keg_data': keg_data, 'property' : property, 'brew_prop' : brew_prop}
    if request.method == 'GET':
        return render(request, 'inventory/brewery_details.html', context)
    elif request.method == 'POST':
        beer = Kegs.objects.get(id=request.POST['beer'])
        quantity = request.POST['quantity']
        property = Property.objects.get(id=request.POST['property']) 
        order_date = request.POST['order_date']
        brewery = brew_prop
        manager = (current_user.first_name + ' ' + current_user.last_name)
        Order.objects.create(beer = beer, quantity = quantity, property = property,
        brewery = brewery, manager = manager, order_date = order_date,)
    return redirect('breweries')

@login_required
def brewer_contacts(request):
    current_user = request.user
    print(current_user.first_name)
    
    drive_staff = Driver.objects.all()
    brew_staff = Brewer.objects.all()
    context = {'drive_staff': drive_staff, 'brew_staff' : brew_staff}
    return render(request, 'inventory/brewer_contacts.html', context)