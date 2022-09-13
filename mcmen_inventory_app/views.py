from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from mcmen_inventory_app.models import Kegs
from mcmen_inventory_app.models import Brewery
from mcmen_inventory_app.models import BrewLog
from mcmen_inventory_app.models import BrewLogComment
from mcmen_dist_app.models import Property
from mcmen_order_app.models import OrderItem
from mcmen_user_app.models import UserProfile
from django.contrib import messages

@login_required
def index_inventory(request):
  breweries = Brewery.objects.all()
  return render(request, 'inventory/index_inventory.html', {'breweries': breweries})

@login_required
def total_inventory(request):
    current_user = request.user
    user_id = current_user.id
    user_data = UserProfile.objects.get(user_name = user_id)
    breweries = Brewery.objects.all()
    keg_totals = {}
    keg_data = Kegs.objects.all()
    counter = 0
    for keg in keg_data:
        counter2 = counter + 1
        while counter2 <= (len(keg_data)) -1:
            if (keg_data[counter].beer) == (keg_data[counter2].beer):
                (keg_data[counter2].quantity) = (keg_data[counter2].quantity) + (keg_data[counter].quantity)   
                counter2 += 1
            else:
                keg_totals[keg.beer] = keg.quantity     
            counter2 += 1      
        counter += 1
    context = {
        'keg_totals' : keg_totals, 'breweries' : breweries, 'user_data': user_data,
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
                messages.warning(request, (f'There is currently no inventory for {key_word}. Check spelling and capitalization.'))
                return render(request, 'inventory/search_inventory.html', context)
            else:
                return render(request, 'inventory/search_inventory.html', context)
        else:
            keg_totals = Kegs.objects.filter(category=key_word)
            context = {
                'breweries': breweries, 'keg_totals': keg_totals,
            }
            if keg_totals.count() == 0:
                messages.warning(request, (f'There is currently no inventory for {key_word}. Check spelling and capitalization.'))
            return render(request, 'inventory/search_inventory.html', context)
    
@login_required
def brewery_details(request, id):
    current_user = request.user
    user_id = current_user.id
    user_data = UserProfile.objects.get(user_name = user_id)
    breweries = Brewery.objects.all()
    orders = OrderItem.objects.filter(brewery = id)
    brew_prop = Brewery.objects.get(id = id)
    property = Property.objects.all()
    keg_totals = Kegs.objects.filter(brewery = id)
    context = {
        'keg_totals': keg_totals, 'property' : property, 'brew_prop' : brew_prop,
        'orders' : orders, 'breweries' : breweries, 'user_data': user_data,
        }
    return render(request, 'inventory/brewery_details.html', context)

@login_required
def add_update_kegs(request, id):
    breweries = Brewery.objects.all()
    brewery = Brewery.objects.get(id = id)
    keg_data = Kegs.objects.filter(brewery = id)
    context = {'brewery' : brewery, 'keg_data' : keg_data,
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
    current_user = request.user
    user_id = current_user.id
    user_data = UserProfile.objects.get(id = user_id)
    user_data.view_pref = request.POST['inv_view']
    user_data.save()
    return redirect('brew_details', id)

@login_required
def total_inventory_view(request):
    current_user = request.user
    user_id = current_user.id
    user_data = UserProfile.objects.get(id = user_id)
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
        # pub_date = request.POST['pub_date']
        author = (current_user.first_name + ' ' + current_user.last_name)
        BrewLog.objects.create(author = author, title = title, text = text)
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
    article = BrewLog.objects.get(id = id)
    comments = BrewLogComment.objects.filter(post_connected=article.id)
    context = { "article": article, "comments": comments, 'breweries': breweries,}
    current_user = request.user
    if request.method == 'GET':
        return render(request, 'inventory/brewer_post_details.html', context)
    elif request.method == 'POST':
        content = request.POST['content']
        author = (current_user.first_name + ' ' + current_user.last_name)
        post_connected = article
        BrewLogComment.objects.create(author = author, post_connected = post_connected, content = content)
        return redirect('all_brew_posts')