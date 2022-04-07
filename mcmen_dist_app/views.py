
from turtle import title
from django.shortcuts import render, redirect
import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from mcmen_dist_app.models import PostComment, Property
from mcmen_dist_app.models import Driver
from mcmen_dist_app.models import Route
from mcmen_dist_app.models import Article, PostComment
from mcmen_dist_app.models import Images
from decouple import config

#--> Rest
from rest_framework.decorators import api_view
from rest_framework import serializers, status
from .serializers import PropertySerializer
from rest_framework.response import Response
#-->


def landing(request):
    return render(request, 'pages/landing.html')

@login_required
def index(request):
    return render(request, 'pages/index.html')

def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('index')
    else:
        messages.warning(request, 'User Name or Password is incorrect')
        return render(request, 'pages/landing.html')

def logout_user(request):
    logout(request)
    return redirect('landing')

def admin_page(request):
    return render(request, 'pages/admin_page.html')

def add_property(request):
    if request.method == 'GET': 
        return render(request, 'pages/add_property.html')
    elif request.method == 'POST': 
        code = request.POST['code']
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']   
        name = request.POST['name']
        phone_num = request.POST['phone_num']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zipcode = request.POST['zipcode']
        manager = request.POST['manager']
        brewer = request.POST['brewer']
        delivery = request.POST['delivery']
        notes = request.POST['notes']
        Property.objects.create(code = code, latitude = latitude, longitude = longitude, name = name, address = address,
        city = city, state = state, zipcode = zipcode, manager = manager, 
        brewer = brewer, delivery = delivery, notes = notes, phone_num = phone_num)
        return redirect('admin_page')

def add_driver(request):
    if request.method == 'GET': 
        return render(request, 'pages/add_driver.html')
    elif request.method == 'POST': 
        first_name = request.POST['first_name']  
        last_name = request.POST['last_name']
        name = list(last_name)
        nick_name = first_name + '.' + name[0]
        phone_num = request.POST['phone_num']
        Driver.objects.create(first_name = first_name, last_name = last_name, 
        nick_name = nick_name, phone_num = phone_num)
        return redirect('admin_page')

def add_route(request):
    props = Property.objects.all()
    drivers = Driver.objects.all()
    context = {'props': props, 'drivers': drivers}
    if request.method == 'GET':
        return render(request, 'pages/add_route.html', context) 
    elif request.method == 'POST':
        truck_num = request.POST['truck_num']
        day = request.POST['day']
        # for x in drivers:
        drivers = Driver.objects.get(id=request.POST['drivers'])
        properties = Property.objects.get(id=request.POST['properties'])
        print('LOOK HERE!',drivers, properties)
        Route.objects.create(truck_num = truck_num, drivers = drivers, 
        day = day, properties = properties)
        return redirect('admin_page')

def all_routes(request):
  routes = Route.objects.all()
  props = Property.objects.all()
  return render(request, 'pages/view_routes.html', {'routes': routes, 'props': props})

def search_routes(request):
    if request.method == 'GET':
        return render(request, 'pages/search_routes.html') 
    elif request.method == 'POST':
        props = Property.objects.all()
        routes = Route.objects.all()
        # print(routes)
        route_truck = request.POST['truck_num']
        route_day = request.POST['day']
        # print(route_truck, route_day)
        day_route = Route.objects.filter(truck_num=route_truck, day=route_day)
        # print(day_route)
    return render(request, 'pages/search_routes.html', {'day_route': day_route, 'props': props})

def add_driver_post(request):
    authors = Driver.objects.all()
    context = {'authors': authors} 
    if request.method == 'GET':
        return render(request, 'pages/add_driver_post.html', context)
    elif request.method == 'POST':
        title = request.POST['title']
        text = request.POST['text']
        pub_date = request.POST['pub_date']
        author = Driver.objects.get(id=request.POST['author'])
        Article.objects.create(author = author, title = title, text = text, pub_date = pub_date)
        return redirect('view_all_posts')

def view_all_posts(request):
  articles = Article.objects.all()
  comments = PostComment.objects.all()
  context = {'articles': articles, 'comments': comments}
#   print(comments)
  return render(request, 'pages/view_posts.html', context)

def post_details(request, id):
    authors = Driver.objects.all()
    article = Article.objects.get(id = id)
    comments = PostComment.objects.filter(post_connected=article.id) 
    if request.method == 'GET':
        return render(request, 'pages/post_details.html', {"authors": authors, "article": article, "comments": comments})
    elif request.method == 'POST':
        content = request.POST['content']
        date_posted = request.POST['date_posted']
        author = Driver.objects.get(id=request.POST['author'])  
        post_connected = article
        PostComment.objects.create(author = author, post_connected = post_connected, content = content, date_posted = date_posted)
        return redirect('view_all_posts')

def all_props(request):
  props = Property.objects.all()
  return render(request, 'pages/view_props.html', {'props': props})

def prop_details(request, id):
    prop = Property.objects.get(id = id)
    latX= prop.latitude
    lngX= prop.longitude
    key= config("WEATHER_KEY")
    note_list= prop.notes.split("#")
    # print('coordinates ',latX, lngX)
    response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?lat={latX}&lon={lngX}&units=imperial&appid={key}')
    weather_data = response.json()
    # print(weather_data)
    main= weather_data['main']
    weather= weather_data['weather'][0]
    context= {'prop': prop, 'main': main, 'weather': weather, 'note_list': note_list}
    return render(request, 'pages/prop_details.html', context)

@api_view(['GET'])
def property_detail(request, pk, format=None):
    """
    Retrieve a property by id.
    """
    try:
        property = Property.objects.get(pk=pk)
    except Property.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PropertySerializer(property)
        return Response(serializer.data)

def contacts(request):
  staff = Driver.objects.all()
  return render(request, 'pages/contacts.html', {'staff': staff})