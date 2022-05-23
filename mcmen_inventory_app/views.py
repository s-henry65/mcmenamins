from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from mcmen_inventory_app.models import Kegs


# @login_required
# def index_inventory(request):
#     keg_data = Kegs.objects.all()
#     context = {
#         'keg_data' : keg_data,
#     }
#     print('DATA:' ,keg_data)
#     return render(request, 'pages/index_inventory.html', context)
