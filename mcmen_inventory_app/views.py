
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
from mcmen_inventory_app.models import PropOrder

@login_required
def index_inventory(request):
    # print('START')
    keg_totals = {}
    keg_data = Kegs.objects.all()
    order_data = PropOrder.objects.all()
    # print(keg_data)
    # print(keg_data.count())
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
        'keg_totals' : keg_totals, 'order_data' : order_data,
    }
    return render(request, 'inventory/index_inventory.html', context)

@login_required
def all_breweries(request):
  breweries = Brewery.objects.all()
  return render(request, 'inventory/view_breweries.html', {'breweries': breweries})

@login_required
def brewery_details(request, id):
    orders = Order.objects.filter(brewery = id)
    current_user = request.user
    brew_prop = Brewery.objects.get(id = id)
    property = Property.objects.all()
    keg_data = Kegs.objects.filter(brewery = id)
    context = {
        'keg_data': keg_data, 'property' : property, 'brew_prop' : brew_prop,
        'orders' : orders
        }
    # Placing an order
    if request.method == 'GET':
        return render(request, 'inventory/brewery_details.html', context)
    elif request.method == 'POST':
        beer = Kegs.objects.get(id=request.POST['beer'])
        quantity = request.POST['quantity']
        property = Property.objects.get(id=request.POST['property']) 
        brewery = brew_prop
        manager = (current_user.first_name + ' ' + current_user.last_name)
        Order.objects.create(beer = beer, quantity = quantity, property = property,
        brewery = brewery, manager = manager)
    return render(request, 'inventory/brewery_details.html', context)

@login_required
def brewer_contacts(request):
    drive_staff = Driver.objects.all()
    brew_staff = Brewer.objects.all()
    context = {'drive_staff': drive_staff, 'brew_staff' : brew_staff}
    return render(request, 'inventory/brewer_contacts.html', context)

@login_required
def add_update_kegs(request, id):
    brewery = Brewery.objects.get(id = id)
    keg_data = Kegs.objects.filter(brewery = id)
    context = {'brewery' : brewery, 'keg_data' : keg_data}
    # print('BREWERY 1 :', brewery.id)
    # print('DATA 1 :', keg_data)
    if request.method == 'GET':
        return render(request, 'inventory/add_update_kegs.html', context)
    # Adding a new keg of beer
    elif request.method == 'POST':
        beer = request.POST['beer']
        brew_date = request.POST['brew_date']
        category = request.POST['category']
        quantity = request.POST['quantity']
        kegs = Kegs.objects.create(beer = beer, brew_date = brew_date, 
        category = category, quantity = quantity)
        kegs.brewery.add(brewery)
        return render(request, 'inventory/add_update_kegs.html', context)

@login_required
def update_kegs(request, id, pk):
    keg = Kegs.objects.get(id = id)
    context = {'keg' : keg, 'pk' : pk}
    if request.method == 'GET':
        return render(request, 'inventory/update_inventory.html', context)
    elif request.method == 'POST':
        keg.beer = request.POST['beer']
        keg.category = request.POST['category']
        keg.quantity = request.POST['quantity']
        keg.save()
        return redirect('add', pk)

@login_required
def update_orders(request, id, pk):
    keg_data = Kegs.objects.filter(brewery = pk)
    order = Order.objects.get(id = id)
    property = Property.objects.all()
    keg = Kegs.objects.get(id = order.beer.id)
    context = {'order' : order, 'pk' : pk, 'property' : property, 'keg_data' : keg_data}
    # print('BEER :', order.beer, order.beer.id)
    # print('QUANT :', order.quantity)
    # print(keg_data)
    # print(id, pk)
    # print(keg.quantity)
    if request.method == 'GET':
        return render(request, 'inventory/update_orders.html', context)
    elif request.method == 'POST':
        order.quantity = request.POST['quantity']
        order.status = request.POST['status']
        order.save()
        if order.status == 'Approved':
            keg.quantity -= int(order.quantity)
            keg.save()
        return redirect('brew_details', pk)

@login_required
def delete_keg(request, id, pk):
    keg = Kegs.objects.get(id = id)
    # keg_data = Kegs.objects.filter(brewery = id)
    keg.delete()
    return redirect('add', pk)

@login_required
def delete_order(request, id, pk):
    order = Order.objects.get(id = id)
    # order_data = Order.objects.filter(order = id)
    order.delete()
    return redirect('brew_details', pk)