from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from mcmen_order_app.models import OrderItem
from mcmen_order_app.models import Order
from django.contrib import messages
from mcmen_inventory_app.models import Brewery
from mcmen_dist_app.models import Property
from mcmen_inventory_app.models import Kegs
from mcmen_user_app.models import UserProfile
from datetime import date

@login_required
def order_index(request):
    breweries = Brewery.objects.all()
    context = { 
        'breweries': breweries,
    }
    return render(request, 'order/order_index.html', context)

@login_required
def order(request, id):
    current_user = request.user
    breweries = Brewery.objects.all()
    orders = Order.objects.filter(manager=id, archive=False, cart_status='Closed')
    profile = UserProfile.objects.get(user_name=current_user)
    prop = profile.home_base.name
    try:
        cart = Order.objects.get(manager=id, archive=False, cart_status='Open')
        context = {'orders': orders, 'breweries': breweries, 'prop': prop, 'cart': cart,
               }
        if orders.count() == 0:
            messages.warning(request, 'There are no closed orders. Check your cart.')
            return render(request, 'order/order.html', context)
        else:
            return render(request, 'order/order.html', context)
    except:
        cart = 0
        context = {'orders': orders, 'breweries': breweries, 'prop': prop, 'cart': cart,
               }
        if orders.count() == 0:
            messages.warning(request, 'There are no closed orders. Check your cart.')
            return render(request, 'order/order.html', context)
        else:
            return render(request, 'order/order.html', context)
@login_required
def view_cart(request, id):
    current_user = request.user
    breweries = Brewery.objects.all()
    profile = UserProfile.objects.get(user_name=current_user)
    today = date.today()
    prop = profile.home_base
    order = Order.objects.filter(manager=current_user, cart_status='Open')
    try:
        cart = Order.objects.get(manager=current_user, archive=False, cart_status='Open')
        context = {'order': order, 'breweries': breweries, 'prop': prop, 'cart': cart,
                   }
        return render(request, 'order/cart.html', context)
    except:
        # order.count() == 0:
        order = Order.objects.create(
        manager=current_user, order_date=today, property=prop, cart_status='Open')
        context = {'order': order, 'breweries': breweries, 'prop': prop,
                   }
        return redirect('view_cart', id)
        # print('ORDER CT', item.count())


@login_required
def place_order(request, id):
    current_user = request.user
    breweries = Brewery.objects.all()
    brew_prop = Brewery.objects.get(id=id)
    property = Property.objects.all()
    keg_data = Kegs.objects.filter(brewery=id)
    profile = UserProfile.objects.get(user_name=current_user)
    today = date.today()
    prop = profile.home_base
    order = Order.objects.filter(manager=current_user, cart_status='Open')
    if request.method == 'GET':
        # Check for open cart
        try:
            cart = Order.objects.get(manager=current_user, archive=False, cart_status='Open')
            context = {'order': order, 'keg_data': keg_data, 'property': property, 'brew_prop': brew_prop,
                   'breweries': breweries, 'cart': cart,
                   }
            return render(request, 'order/place_order.html', context)
        except:
            order = Order.objects.create(
            manager=current_user, order_date=today, property=prop, cart_status='Open')
            context = {'order': order, 'keg_data': keg_data, 'property': property, 'brew_prop': brew_prop,
                   'breweries': breweries,
                   }
            return redirect('place_order', id)
    # Placing an order
    elif request.method == 'POST':
        beer = Kegs.objects.get(id=request.POST['beer'])
        quantity = request.POST['quantity']
        notes = request.POST['text']
        property = prop
        brewery = brew_prop
        manager = current_user
        keg_order = OrderItem.objects.create(beer = beer, quantity = quantity, property = property,
            brewery = brewery, manager = manager, order_date = today, notes = notes)
        order = Order.objects.get(manager=current_user, cart_status='Open')
        item = OrderItem.objects.get(id = keg_order.id)
        order.order_items.add(item)
        order.keg_count += item.quantity
        # print(order.keg_count)
        order.save()
        return redirect('place_order', id)

@login_required
def close_cart(request, id):
    order = Order.objects.get(id=id)
    notes = request.POST['text']
    order.notes = notes
    order.cart_status = 'Closed'
    order.save()
    current_user = request.user
    id = current_user.id
    return redirect('order', id)

@login_required
def remove_item(request, id, pk):
    order = Order.objects.get(id = pk)
    keg = OrderItem.objects.get(id = id)
    order.keg_count -= keg.quantity
    # print(order.keg_count)
    order.save()
    keg.delete()
    return redirect('view_cart', pk)

@login_required
def dist_admin(request):
    orders = Order.objects.filter(archive=False)
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
    orders = Order.objects.filter(archive=False)
    context = {'orders': orders,
               }
    order = Order.objects.get(id=id)
    order.status = 'Delivered'
    order.save()
    return render(request, 'user/dist_admin.html', context)

@login_required
def order_archive(request):
    orders = Order.objects.filter(archive=True)
    context = {'orders': orders,
               }
    return render(request, 'user/order_archive.html', context)

@login_required
def close_order(request, id):
    orders = Order.objects.filter(archive=False)
    context = {'orders': orders,
               }
    order = Order.objects.get(id=id)
    order.status = 'Delivered'
    order.save()
    return render(request, 'user/dist_admin.html', context)

@login_required
def archive_order(request, id):
    orders = Order.objects.filter(archive=False)
    context = {'orders': orders,
               }
    order = Order.objects.get(id=id)
    order.archive = True
    order.save()
    return render(request, 'user/dist_admin.html', context)