# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request,'LR/index.html')

def register(request):
    result = User.objects.regVal(request.POST) #make sure this matches on models.py
    if result['status'] == False:
        for err in result['errors']:
            messages.error(request, err)
            return redirect('/')
    else:
        password = request.POST['password']
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        request.session['user_id'] = result['user'].id
        print User.objects.all()
        return redirect('/dashboard')

def login(request):
    password = request.POST['password']
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    #check if they exist against what I have in the database?
    try:
        user = User.objects.get(email = email)
        hash1 = user.password
    except:
        hash1 = request.POST['email']
    result = User.objects.logVal(request.POST) #make sure this matches on models.py
    if result['status'] == False:
        print 'error on LR views'
        for err in result['errors']:
            messages.error(request, err)
        return redirect('/')
    else:
        print 'success'
        request.session['user_id'] = result['user'].id
        print request.session['user_id']
        return redirect('/dashboard/')

def logout(request):
    request.session.clear()
    return redirect('/')
