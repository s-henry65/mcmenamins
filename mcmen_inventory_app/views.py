from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from mcmen_inventory_app.models import Kegs
from mcmen_inventory_app.models import Brewery
from mcmen_inventory_app.models import BrewLog
from mcmen_inventory_app.models import BrewLogComment
from mcmen_inventory_app.models import ComingSoon
from mcmen_dist_app.models import Property
from mcmen_order_app.models import OrderItem
from mcmen_user_app.models import UserProfile
from django.contrib import messages


def index_inventory(request):
    breweries = Brewery.objects.all()
    current_user = request.user
    user_data = UserProfile.objects.get(user_name=current_user)
    context = {'user_data': user_data
               }
    if 'Brewer' in user_data.job_title or current_user.is_staff:
        return render(request, 'inventory/index_inventory.html', {'breweries': breweries})
    else:
        messages.warning(request, 'Sorry, you are not authorized.')
        return render(request, 'distribution/router.html', context)


@login_required
def total_inventory(request):
    current_user = request.user
    user_data = UserProfile.objects.get(user_name=current_user)
    breweries = Brewery.objects.all()
    keg_totals = {}
    keg_data = Kegs.objects.all()
    counter = 0
    for keg in keg_data:
        counter2 = counter + 1
        while counter2 <= (len(keg_data)) - 1:
            if (keg_data[counter].beer) == (keg_data[counter2].beer):
                (keg_data[counter2].quantity) = (
                    keg_data[counter2].quantity) + (keg_data[counter].quantity)
                counter2 += 1
            else:
                keg_totals[keg.beer] = keg.quantity
            counter2 += 1
        counter += 1
    context = {
        'keg_totals': keg_totals, 'breweries': breweries, 'user_data': user_data,
    }
    return render(request, 'inventory/total_inventory.html', context)


@login_required
def search_inventory(request):
    breweries = Brewery.objects.all()
    context = {
        'breweries': breweries,
    }
    if request.method == 'GET':
        return render(request, 'inventory/search_inventory.html', context)
    elif request.method == 'POST':
        criteria = request.POST['criteria']
        key_word = request.POST['key word']
        if criteria == 'beer':
            keg_totals = Kegs.objects.filter(beer=key_word)
            context = {
                'breweries': breweries, 'keg_totals': keg_totals,
            }
            if keg_totals.count() == 0:
                messages.warning(
                    request, (f'There is no inventory for {key_word}. Check spelling and capitalization.'))
                return render(request, 'inventory/search_inventory.html', context)
            else:
                return render(request, 'inventory/search_inventory.html', context)
        else:
            keg_totals = Kegs.objects.filter(sku=key_word)
            context = {
                'breweries': breweries, 'keg_totals': keg_totals,
            }
            if keg_totals.count() == 0:
                messages.warning(
                    request, (f'There is no inventory for {key_word}. Check spelling and capitalization.'))
            return render(request, 'inventory/search_inventory.html', context)


@login_required
def brewery_details(request, id):
    current_user = request.user
    user_data = UserProfile.objects.get(user_name=current_user)
    breweries = Brewery.objects.all()
    orders = OrderItem.objects.filter(brewery=id, archive=False)
    brew_prop = Brewery.objects.get(id=id)
    keg_totals = Kegs.objects.filter(brewery=id)
    upcoming = ComingSoon.objects.filter(brewery=id)
    context = {
        'keg_totals': keg_totals, 'property': property, 'brew_prop': brew_prop,
        'orders': orders, 'breweries': breweries, 'user_data': user_data, 'upcoming': upcoming,
    }
    if orders.count() == 0:
        messages.warning(request, 'There are no pending orders.')
        return render(request, 'inventory/brewery_details.html', context)
    else:
        return render(request, 'inventory/brewery_details.html', context)


@login_required
def add_update_kegs(request, id):
    breweries = Brewery.objects.all()
    brewery = Brewery.objects.get(id=id)
    keg_data = Kegs.objects.filter(brewery=id)
    context = {'brewery': brewery, 'keg_data': keg_data,
               'breweries': breweries,
               }
    if request.method == 'GET':
        return render(request, 'inventory/add_update_kegs.html', context)
    # Adding a new keg of beer
    elif request.method == 'POST':
        beer = request.POST['beer']
        brew_date = request.POST['brew_date']
        sku = request.POST['sku']
        quantity = request.POST['quantity']
        kegs = Kegs.objects.create(beer=beer, brew_date=brew_date,
                                   sku=sku, quantity=quantity)
        kegs.brewery.add(brewery)
        return render(request, 'inventory/add_update_kegs.html', context)


@login_required
def update_kegs(request, id, pk):
    breweries = Brewery.objects.all()
    keg = Kegs.objects.get(id=id)
    context = {'keg': keg, 'pk': pk, 'breweries': breweries,
               }
    if request.method == 'GET':
        return render(request, 'inventory/update_inventory.html', context)
    elif request.method == 'POST':
        keg.beer = request.POST['beer']
        keg.sku = request.POST['sku']
        keg.quantity = request.POST['quantity']
        keg.save()
        return redirect('add', pk)


@login_required
def add_upcoming(request, id):
    breweries = Brewery.objects.all()
    brewery = Brewery.objects.get(id=id)
    keg_data = ComingSoon.objects.filter(brewery=id)
    context = {'brewery': brewery, 'keg_data': keg_data,
               'breweries': breweries,
               }
    if request.method == 'GET':
        return render(request, 'inventory/add_coming_soon.html', context)
    elif request.method == 'POST':
        beer = request.POST['beer']
        finish_date = request.POST['finish_date']
        sku = request.POST['sku']
        description = request.POST['text']
        kegs = ComingSoon.objects.create(beer=beer, finish_date=finish_date,
                                         sku=sku, description=description)
        kegs.brewery.add(brewery)
        return render(request, 'inventory/add_coming_soon.html', context)


@login_required
def delete_upcoming(request, id, pk):
    beer = ComingSoon.objects.get(id=id)
    beer.delete()
    return redirect('add_upcoming', pk)


@login_required
def update_orders(request, id, pk):
    keg_data = Kegs.objects.filter(brewery=pk)
    order = OrderItem.objects.get(id=id)
    property = Property.objects.all()
    keg = Kegs.objects.get(id=order.beer.id)
    context = {'order': order, 'pk': pk,
               'property': property, 'keg_data': keg_data}

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
    keg = Kegs.objects.get(id=id)
    keg.delete()
    return redirect('add', pk)


@login_required
def delete_order(request, id, pk):
    order = OrderItem.objects.get(id=id)
    order.delete()
    return redirect('brew_details', pk)


@login_required
def inventory_view(request, id):
    current_user = request.user
    user_data = UserProfile.objects.get(user_name=current_user)
    user_data.view_pref = request.POST['inv_view']
    user_data.save()
    return redirect('brew_details', id)


@login_required
def total_inventory_view(request):
    current_user = request.user
    user_data = UserProfile.objects.get(user_name=current_user)
    user_data.view_pref = request.POST['inv_view']
    user_data.save()
    return redirect('inventory')


@login_required
def add_brewer_post(request):
    current_user = request.user
    breweries = Brewery.objects.all()
    context = {
        'breweries': breweries,
    }
    if request.method == 'GET':
        return render(request, 'inventory/add_brewer_post.html', context)
    elif request.method == 'POST':
        title = request.POST['title']
        text = request.POST['text']
        author = (current_user.first_name + ' ' + current_user.last_name)
        BrewLog.objects.create(author=author, title=title, text=text)
        return redirect('all_brew_posts')


@login_required
def all_brew_posts(request):
    breweries = Brewery.objects.all()
    articles = BrewLog.objects.all()
    comments = BrewLogComment.objects.all()
    context = {
        'articles': articles, 'comments': comments, 'breweries': breweries,
    }
    return render(request, 'inventory/view_brew_posts.html', context)


@login_required
def brew_post_details(request, id):
    breweries = Brewery.objects.all()
    article = BrewLog.objects.get(id=id)
    comments = BrewLogComment.objects.filter(post_connected=article.id)
    context = {"article": article,
               "comments": comments, 'breweries': breweries, }
    current_user = request.user
    if request.method == 'GET':
        return render(request, 'inventory/brewer_post_details.html', context)
    elif request.method == 'POST':
        content = request.POST['content']
        author = (current_user.first_name + ' ' + current_user.last_name)
        post_connected = article
        BrewLogComment.objects.create(
            author=author, post_connected=post_connected, content=content)
        return redirect('all_brew_posts')


@login_required
def archive_order_item(request, id, pk):
    order = OrderItem.objects.get(id=id)
    order.archive = True
    order.save()
    return redirect('brew_details', pk)


@login_required
def order_item_archive(request):
    orders = OrderItem.objects.filter(archive=True)
    context = {'orders': orders,
               }
    return render(request, 'inventory/brewery_details.html', context)


@login_required
def search_order_items(request, id):
    breweries = Brewery.objects.all()
    brew_prop = Brewery.objects.get(id=id)
    context = {
        'breweries': breweries, 'brew_prop': brew_prop,
    }
    if request.method == 'GET':
        return render(request, 'inventory/search_order_items.html', context)
    elif request.method == 'POST':
        criteria = request.POST['criteria']

        if criteria == 'property':
            key_word = request.POST['property']
            try:
                prop_id = Property.objects.get(name=key_word)
                orders = OrderItem.objects.filter(
                    brewery=id, archive=True, property=prop_id)
                context = {
                    'breweries': breweries, 'brew_prop': brew_prop, 'orders': orders,
                }
                return render(request, 'inventory/search_order_items.html', context)
            except:
                messages.warning(
                    request, (f'There are no orders for {key_word}. Check spelling and capitalization.'))
                return render(request, 'inventory/search_order_items.html', context)

        elif criteria == 'date':
            order_month = request.POST['order_month']
            order_year = request.POST['order_year']
            if order_month == 'all':
                orders = OrderItem.objects.filter(
                    brewery=id, archive=True, order_date__year=order_year)
                context = {
                    'breweries': breweries, 'brew_prop': brew_prop, 'orders': orders,
                }
                if orders.count() == 0:
                    messages.warning(
                        request, (f'There are no orders for {order_year}. Check date.'))
                    return render(request, 'inventory/search_order_items.html', context)
                else:
                    return render(request, 'inventory/search_order_items.html', context)
            else:
                orders = OrderItem.objects.filter(brewery=id, archive=True, order_date__year=order_year,
                                                  order_date__month=order_month)
                context = {
                    'breweries': breweries, 'brew_prop': brew_prop, 'orders': orders,
                }
                if orders.count() == 0:
                    messages.warning(
                        request, (f'There are no orders for {order_month}, {order_year}. Check date.'))
                    return render(request, 'inventory/search_order_items.html', context)
                else:
                    return render(request, 'inventory/search_order_items.html', context)

        elif criteria == 'prop_date':
            key_word = request.POST['property']
            order_month = request.POST['order_month']
            order_year = request.POST['order_year']
            if order_month == 'all':
                try:
                    prop_id = Property.objects.get(name=key_word)
                    orders = OrderItem.objects.filter(brewery=id, archive=True, property=prop_id, order_date__year=order_year)
                    context = {
                    'breweries': breweries, 'brew_prop': brew_prop, 'orders': orders,
                    }
                    if orders.count() == 0:
                        messages.warning(
                        request, (f'There are no orders for {key_word}, {order_year}. Check date, spelling and capitalization.'))
                        return render(request, 'inventory/search_order_items.html', context)
                    else:
                        return render(request, 'inventory/search_order_items.html', context)
                except:
                    messages.warning(
                    request, (f'There are no orders for {key_word}, {order_year}. Check date, spelling and capitalization.'))
                    return render(request, 'inventory/search_order_items.html', context)
            else:
                try:
                    prop_id = Property.objects.get(name=key_word)
                    orders = OrderItem.objects.filter(brewery=id, archive=True, order_date__year=order_year,
                             property=prop_id, order_date__month=order_month)
                    context = {
                        'breweries': breweries, 'brew_prop': brew_prop, 'orders': orders,
                    }
                    if orders.count() == 0:
                        messages.warning(
                        request, (f'There are no orders for {key_word}, {order_month}, {order_year}. Check date, spelling and capitalization.'))
                        return render(request, 'inventory/search_order_items.html', context)
                    else:
                        return render(request, 'inventory/search_order_items.html', context)
                except:
                    messages.warning(
                    request, (f'There are no orders for {key_word}, {order_month}, {order_year}. Check date, spelling and capitalization.'))
                    return render(request, 'inventory/search_order_items.html', context)