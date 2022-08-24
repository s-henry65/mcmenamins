from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from mcmen_inventory_app.models import Kegs
from mcmen_inventory_app.models import Brewery
from mcmen_dist_app.models import Property
from mcmen_order_app.models import OrderItem


@login_required
def index_inventory(request):
    breweries = Brewery.objects.all()
    # print('START')
    keg_totals = {}
    keg_data = Kegs.objects.all()
    # order_data = PropOrder.objects.all()
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
        'keg_totals' : keg_totals, 'breweries' : breweries,
    }
    return render(request, 'inventory/index_inventory.html', context)

@login_required
def all_breweries(request):
  breweries = Brewery.objects.all()
  return render(request, 'inventory/view_breweries.html', {'breweries': breweries})

@login_required
def brewery_details(request, id):
    breweries = Brewery.objects.all()
    orders = OrderItem.objects.filter(brewery = id)
    brew_prop = Brewery.objects.get(id = id)
    property = Property.objects.all()
    keg_data = Kegs.objects.filter(brewery = id)
    context = {
        'keg_data': keg_data, 'property' : property, 'brew_prop' : brew_prop,
        'orders' : orders, 'breweries' : breweries,
        }
    return render(request, 'inventory/brewery_details.html', context)

@login_required
def add_update_kegs(request, id):
    breweries = Brewery.objects.all()
    brewery = Brewery.objects.get(id = id)
    keg = Kegs.objects.get(id = id)
    keg_data = Kegs.objects.filter(brewery = id)
    context = {'brewery' : brewery, 'keg_data' : keg_data, 'keg': keg,
            'breweries' : breweries,
    }
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
        print('LOOK', kegs, brewery)
        kegs.brewery.add(brewery)
        return render(request, 'inventory/add_update_kegs.html', context)

@login_required
def update_kegs(request, id, pk):
    breweries = Brewery.objects.all()
    keg = Kegs.objects.get(id = id)
    context = {'keg' : keg, 'pk' : pk, 'breweries' : breweries,
    }
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
    order = OrderItem.objects.get(id = id)
    property = Property.objects.all()
    keg = Kegs.objects.get(id = order.beer.id)
    context = {'order' : order, 'pk' : pk, 'property' : property, 'keg_data' : keg_data}

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
    order = OrderItem.objects.get(id = id)
    # order_data = Order.objects.filter(order = id)
    order.delete()
    return redirect('brew_details', pk)

@login_required
def inventory_view(request, id):
    brewery = Brewery.objects.get(id = id)
    # print(brewery.id)
    brewery.inv_view = request.POST['inv_view']
    # print('HERE ',brewery.inv_view)
    brewery.save()
    return redirect('brew_details', id)