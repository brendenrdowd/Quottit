# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Q
from .models import *
from ..LR.models import User
from django.contrib import messages
import bcrypt

def index(request):
    context = {
        'contents': Quote.objects.all(),
        'user': User.objects.get(id=request.session['user_id']),
        'favorites': Favorite.objects.filter(user=User.objects.get(id=request.session['user_id']))
    }
    return render(request, 'main/index.html', context)

def add(request):
    user = User.objects.get(id=request.session['user_id'])
    user_id = request.session['user_id']
    create = Quote.objects.validate(request.POST, user_id) #validation
    if not create['status']:
        for err in create['errors']:
            messages.error(request, err)
            return redirect('/dashboard')
    return redirect('/dashboard')

def favorite(request,number):
    user_id = request.session['user_id']
    quote_id = number
    fave = Quote.objects.favVal(number, user_id)
    if not fave['status']:
        for err in fave['errors']:
            messages.error(request, err)
    return redirect('/dashboard')

def display(request,number):
    print 'in display'
    user = User.objects.get(id=number)
    context = {
        'contents': Quote.objects.filter(user = user),
        'user': user
    }
    return render(request, 'main/display.html', context)

def remove(request,number):
    d = Favorite.objects.get(id=number)
    d.delete()
    return redirect('/dashboard')
