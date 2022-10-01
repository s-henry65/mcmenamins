from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from mcmen_order_app.models import OrderItem
from mcmen_order_app.models import Order
from django.contrib import messages
from mcmen_inventory_app.models import Brewery
from mcmen_inventory_app.models import ComingSoon
from mcmen_dist_app.models import Property
from mcmen_inventory_app.models import Kegs
from mcmen_user_app.models import UserProfile
from datetime import date


@login_required
def order_index(request):
    breweries = Brewery.objects.all()
    current_user = request.user
    user_data = UserProfile.objects.get(user_name=current_user)
    context = {
        'breweries': breweries, 'user_data': user_data,
    }
    if 'Manager' in user_data.job_title or current_user.is_staff:
        return render(request, 'order/order_index.html', context)
    else:
        messages.warning(request, 'Sorry, you are not authorized.')
        return render(request, 'distribution/router.html', context)


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
            messages.warning(
                request, 'There are no pending orders. Check your cart.')
            return render(request, 'order/order.html', context)
        else:
            return render(request, 'order/order.html', context)
    except:
        cart = 0
        context = {'orders': orders, 'breweries': breweries, 'prop': prop, 'cart': cart,
                   }
        if orders.count() == 0:
            messages.warning(
                request, 'There are no pending orders. Check your cart.')
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
        cart = Order.objects.get(manager=current_user,
                                 archive=False, cart_status='Open')
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
    upcoming = ComingSoon.objects.filter(brewery=id)
    profile = UserProfile.objects.get(user_name=current_user)
    today = date.today()
    prop = profile.home_base
    order = Order.objects.filter(manager=current_user, cart_status='Open')
    if request.method == 'GET':
        # Check for open cart
        try:
            cart = Order.objects.get(
                manager=current_user, archive=False, cart_status='Open')
            context = {'order': order, 'keg_data': keg_data, 'property': property, 'brew_prop': brew_prop,
                       'breweries': breweries, 'cart': cart, 'upcoming': upcoming,
                       }
            return render(request, 'order/place_order.html', context)
        except:
            order = Order.objects.create(
                manager=current_user, order_date=today, property=prop, cart_status='Open')
            context = {'order': order, 'keg_data': keg_data, 'property': property, 'brew_prop': brew_prop,
                       'breweries': breweries, 'upcoming': upcoming,
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
        keg_order = OrderItem.objects.create(beer=beer, quantity=quantity, property=property,
                                             brewery=brewery, manager=manager, order_date=today, notes=notes)
        order = Order.objects.get(manager=current_user, cart_status='Open')
        item = OrderItem.objects.get(id=keg_order.id)
        order.order_items.add(item)
        order.keg_count += item.quantity
        # print(order.keg_count)
        order.save()
        messages.warning(request, 'Keg(s) successfully added!')
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
    order = Order.objects.get(id=pk)
    keg = OrderItem.objects.get(id=id)
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


@login_required
def search_order_archive(request):
    # orders = Order.objects.filter(archive=True)
    if request.method == 'GET':
        return render(request, 'user/search_order_archive.html')
    elif request.method == 'POST':
        criteria = request.POST['criteria']
        if criteria == 'property':
            key_word = request.POST['property']
            try:
                prop_id = Property.objects.get(name=key_word)
                orders = Order.objects.filter(archive=True, property=prop_id)
                context = {
                    'orders': orders,
                }
                return render(request, 'user/search_order_archive.html', context)
            except:
                messages.warning(request, (f'There are no orders for {key_word}. Check spelling and capitalization.'))
                return render(request, 'user/search_order_archive.html')

        elif criteria == 'date':
            order_month = request.POST['order_month']
            order_year = request.POST['order_year']
            if order_month == 'all':
                orders = Order.objects.filter(archive=True, order_date__year=order_year)
                context = {
                    'orders': orders,
                }
                if orders.count() == 0:
                    messages.warning(
                        request, (f'There are no orders for {order_year}. Check date.'))
                    return render(request, 'user/search_order_archive.html')
                else:
                    return render(request, 'user/search_order_archive.html', context)
            else:
                orders = Order.objects.filter(archive=True, order_date__year=order_year,
                                                  order_date__month=order_month)
                context = {
                    'orders': orders,
                }
                if orders.count() == 0:
                    messages.warning(
                        request, (f'There are no orders for {order_month}, {order_year}. Check date.'))
                    return render(request, 'user/search_order_archive.html')
                else:
                    return render(request, 'user/search_order_archive.html', context)

        elif criteria == 'prop_date':
            key_word = request.POST['property']
            order_month = request.POST['order_month']
            order_year = request.POST['order_year']
            if order_month == 'all':
                try:
                    prop_id = Property.objects.get(name=key_word)
                    orders = Order.objects.filter(archive=True, property=prop_id, order_date__year=order_year)
                    context = {
                        'orders': orders,
                    }
                    if orders.count() == 0:
                        messages.warning(
                        request, (f'There are no orders for {key_word}, {order_year}. Check date, spelling and capitalization.'))
                        return render(request, 'user/search_order_archive.html')
                    else:
                        return render(request, 'user/search_order_archive.html', context)
                except:
                    messages.warning(
                    request, (f'There are no orders for {key_word}, {order_year}. Check date, spelling and capitalization.'))
                    return render(request, 'user/search_order_archive.html')
            else:
                try:
                    prop_id = Property.objects.get(name=key_word)
                    orders = Order.objects.filter(archive=True, order_date__year=order_year,
                             property=prop_id, order_date__month=order_month)
                    context = {
                        'orders': orders,
                    }
                    if orders.count() == 0:
                        messages.warning(
                        request, (f'There are no orders for {key_word}, {order_month}, {order_year}. Check date, spelling and capitalization.'))
                        return render(request, 'user/search_order_archive.html')
                    else:
                        return render(request, 'user/search_order_archive.html', context)
                except:
                    messages.warning(
                    request, (f'There are no orders for {key_word}, {order_month}, {order_year}. Check date, spelling and capitalization.'))
                    return render(request, 'user/search_order_archive.html')


@login_required
def search_pub_orders(request, id):
    current_user = request.user
    breweries = Brewery.objects.all()
    # orders = Order.objects.filter(manager=id, archive=True,)
    profile = UserProfile.objects.get(user_name=current_user)
    prop = profile.home_base.name
    context = {'prop': prop, 'breweries': breweries,
    }
    if request.method == 'GET':
        return render(request, 'order/search_pub_orders.html', context)
    elif request.method == 'POST':
        order_month = request.POST['order_month']
        order_year = request.POST['order_year']
        if order_month == 'all':
            orders = Order.objects.filter(manager=id, archive=True, order_date__year=order_year)
            context = {
                'prop': prop, 'orders': orders, 'breweries': breweries,
            }
            if orders.count() == 0:
                messages.warning(request, (f'There are no orders for {order_year}. Check date.'))
                return render(request, 'order/search_pub_orders.html', context)
            else:
                return render(request, 'order/search_pub_orders.html', context)
        else:
            orders = Order.objects.filter(manager=id, archive=True, order_date__year=order_year,
                order_date__month=order_month)
            context = {
                'prop': prop, 'orders': orders, 'breweries': breweries,
            }
            if orders.count() == 0:
                messages.warning(request, (f'There are no orders for {order_month}, {order_year}. Check date.'))
                return render(request, 'order/search_pub_orders.html', context)
            else:
                return render(request, 'order/search_pub_orders.html', context)
