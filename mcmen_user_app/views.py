from django.shortcuts import render, redirect
import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from mcmen_user_app.models import UserProfile
from mcmen_dist_app.models import Property
from django.contrib.auth.forms import UserCreationForm
from mcmen_dist_app.models import User
from .forms import CreateUserForm
from mcmen_order_app.models import Order
from mcmen_order_app.models import OrderItem

def landing(request):
    return render(request, 'distribution/landing.html')

@login_required
def router(request):
    try:
        current_user = request.user
        id = current_user.id
        user_data = UserProfile.objects.get(user_name = id)
        # print(user_data, id)
        context = { 'user_data' : user_data
        }
        return render(request, 'distribution/router.html', context)
    except:
        messages.warning(request, 'Please setup a User Profile to continue')
        return redirect('create_profile',)

def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('router')
    else:
        messages.warning(request, 'User Name or Password is incorrect')
        return render(request, 'distribution/landing.html')

def logout_user(request):
    logout(request)
    return redirect('landing')

def create_user_profile(request):
    props = Property.objects.all()
    current_user = request.user
    id = current_user.id
    user_info = User.objects.get(id=id)
    print(id, user_info.first_name)
    context = { 'props' : props, 'user_info' : user_info
    }
    if request.method == 'GET':
        return render(request, 'user/user_profile.html', context)
    elif request.method == 'POST':
        user_name = current_user
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_num = request.POST['phone_num']
        email = request.POST['email']
        job_title = request.POST['job_title']
        home_base = Property.objects.get(id=request.POST['home_base'])
        
        UserProfile.objects.create(first_name = first_name, last_name = last_name, phone_num = phone_num, 
                                    email = email, job_title = job_title, home_base = home_base,
                                    user_name = user_name)
        return redirect('router')

def update_profile(request):
    current_user = request.user
    id = current_user.id
    user_data = UserProfile.objects.get(id = id)
    props = Property.objects.all()
    # print(user_data.id)
    context = { 'props' : props, 'user_data' : user_data
    }
    if request.method == 'GET':
        return render(request, 'user/update_profile.html', context)
    elif request.method == 'POST':
        user_data.first_name = request.POST['first_name']
        user_data.last_name = request.POST['last_name']
        user_data.phone_num = request.POST['phone_num']
        user_data.email = request.POST['email']
        user_data.job_title = request.POST['job_title']
        user_data.home_base = Property.objects.get(id=request.POST['home_base'])
        user_data.save()
        return redirect('router')

@login_required
def create_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.warning(request, 'New user successfully added!')
            return redirect(create_user) 
        else:
            return render(request, "user/create_user.html", {'form': form}) 
    else:
        form = CreateUserForm()
        context = {
            'form': form,
        }
        return render(request, 'user/create_user.html', context)

@login_required
def view_users(request):
  staff= User.objects.order_by('username')
  context = {
        'staff': staff,
    }
  return render(request, 'user/view_all_users.html', context)

@login_required
def delete_user(request, id):
    user = User.objects.get(id = id)
    # order_data = Order.objects.filter(order = id)
    user.delete()
    return redirect('view_users')


@login_required
def contacts(request):
  drive_staff = UserProfile.objects.filter(job_title = 'Driver')
  brew_staff = UserProfile.objects.filter(job_title = 'Brewer')
  pub_manager = UserProfile.objects.filter(job_title = 'Manager, Pub')
  admin_staff = UserProfile.objects.filter(job_title = 'Administration')
  brew_manager = UserProfile.objects.filter(job_title = 'Manager, Brewery')
  dist_manager = UserProfile.objects.filter(job_title = 'Manager, Distribution')
  
  context = {
        'drive_staff': drive_staff, 'brew_staff' : brew_staff, 'pub_manger' : pub_manager,
        'pub_manager' : pub_manager, 'admin_staff' : admin_staff, 'brew_manager' : brew_manager,
        'dist_manager' : dist_manager
        }
  return render(request, 'user/contacts.html', context)