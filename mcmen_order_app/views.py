from django.shortcuts import render, redirect
import requests
from django.contrib.auth.decorators import login_required
from mcmen_order_app.models import OrderItem
from mcmen_order_app.models import Order
from django.contrib import messages
from mcmen_dist_app.models import User
from mcmen_inventory_app.models import Brewery
from mcmen_dist_app.models import Property
from mcmen_inventory_app.models import Kegs
from mcmen_user_app.models import UserProfile
from datetime import date

@login_required
def order(request, id):
    breweries = Brewery.objects.all()
    orders = Order.objects.filter(manager=id)
    context = {'orders': orders, 'breweries': breweries,
               }
    if orders.count() == 0:
        messages.warning(request, 'There are no current orders.')
        return render(request, 'order/order.html',)
    else:
        return render(request, 'order/order.html', context)

@login_required
def view_cart(request, id):
    current_user = request.user
    # print('USER', current_user)
    breweries = Brewery.objects.all()
    profile = UserProfile.objects.get(first_name=current_user)
    today = date.today()
    prop = profile.home_base
    item = OrderItem.objects.all()
    order = Order.objects.filter(
        manager=current_user, cart_status='Open')
    if order.count() == 0:
        order = Order.objects.create(
            manager=current_user, order_date=today, property=prop, cart_status='Open')
        context = {'order': order, 'breweries': breweries,
                   }
        return redirect('view_cart', id)
    else:
        # print('ORDER CT', item.count())
        context = {'order': order, 'breweries': breweries,
                   }
        return render(request, 'order/cart.html', context)

@login_required
def dist_admin(request):
    orders = Order.objects.all()
    # print(orders)
    context = {'orders': orders,
               }
    if orders.count() == 0:
        messages.warning(request, 'There are no current orders.')
        return render(request, 'user/dist_admin.html',)
    else:
        return render(request, 'user/dist_admin.html', context)

@login_required
def order_delivered(request, id):
    orders = Order.objects.all()
    context = {'orders': orders,
               }
    order = Order.objects.get(id=id)
    order.status = 'Delivered'
    order.save()
    return render(request, 'user/dist_admin.html', context)

@login_required
def place_order(request, id):
    current_user = request.user
    breweries = Brewery.objects.all()
    brew_prop = Brewery.objects.get(id=id)
    property = Property.objects.all()
    keg_data = Kegs.objects.filter(brewery=id)
    # Order/cart info
    profile = UserProfile.objects.get(first_name=current_user)
    today = date.today()
    prop = profile.home_base
    order = Order.objects.filter(manager=current_user, cart_status='Open')
    if request.method == 'GET':
        # Check for open cart
        if order.count() == 0:
            order = Order.objects.create(
            manager=current_user, order_date=today, property=prop, cart_status='Open')
            context = {'order': order, 'keg_data': keg_data, 'property': property, 'brew_prop': brew_prop,
                   'breweries': breweries,
                   }
            return render(request, 'order/place_order.html', context)
        else:
            context = {'order': order, 'keg_data': keg_data, 'property': property, 'brew_prop': brew_prop,
                   'breweries': breweries,
                   }
            return render(request, 'order/place_order.html', context)
    # Placing an order
    elif request.method == 'POST':
        beer = Kegs.objects.get(id=request.POST['beer'])
        quantity = request.POST['quantity']
        property = prop
        brewery = brew_prop
        manager = current_user
        keg_order = OrderItem.objects.create(beer = beer, quantity = quantity, property = property,
            brewery = brewery, manager = manager, order_date = today)
        order = Order.objects.get(manager=current_user, cart_status='Open')
        item = OrderItem.objects.get(id = keg_order.id)
        order.order_items.add(item)
        return redirect('place_order', id)

@login_required
def close_cart(request, id):
    orders = Order.objects.all()
    context = {'orders': orders,
               }
    order = Order.objects.get(id=id)
    order.cart_status = 'Closed'
    order.save()
    return render(request, 'order/order.html', context)

@login_required
def edit_cart(request, id):
    item = OrderItem.objects.get(id = id)
    print('ORDER ITEM', item)
    item.beer = request.POST['beer']
    
    item.quantity = request.POST['quantity']
    item.save()
    return redirect('view_cart', id)