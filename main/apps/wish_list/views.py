# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from .models import User, Item

import bcrypt

from django.contrib import messages

# Create your views here.

def index(request):
    return render(request, 'wish_list/index.html')

def logout(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')

def register(request):
    errors = User.objects.reg_validator(request.POST)
    if type(errors) == list:
        for error in errors:
            messages.error(request, error)
        return redirect('/')
    
    request.session['first_name'] = errors.first_name
    request.session['id'] = errors.id
    return redirect('/dashboard')

def login(request):
    errors = User.objects.validate_login(request.POST)
    if type(errors) == list:
        for error in errors:
            messages.error(request, error)
        return redirect('/')
    else:
        request.session['first_name'] = errors.first_name
        request.session['id'] = errors.id
        return redirect('/dashboard')

def success(request):
    try:
        request.session['id']
    except KeyError:
        return redirect('/')
    
    this_user= User.objects.get(id=request.session['id'])
    content = {
        'items_added': this_user.items_added.all(),
        'your_list': this_user.wishlist.exclude(added_by = this_user),
        'other_items': Item.objects.exclude(users = this_user),
        'logged_in': this_user
    }
    return render(request, 'wish_list/dashboard.html', content)

def add(request):
    content = {
        'logged_in': User.objects.get(id=request.session['id'])
    }
    return render(request, 'wish_list/add.html', content)

def create(request):
    result = Item.objects.item_validator(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)
        return redirect('/wish_items/new')
    else:
        return redirect("/dashboard")

def item_info(request, item_id):
    this_item = Item.objects.get(id=item_id)
    content = {
        'item': this_item,
        'lists': this_item.users.all()
    }
    return render(request, 'wish_list/item_info.html', content)

def join(request, item_id):
    this_user = User.objects.get(id=request.session['id'])
    this_item = Item.objects.get(id=item_id)
    this_item.users.add(this_user)
    
    return redirect('/dashboard')

def remove(request, item_id):
    # 'your_list': this_user.wishlist.exclude(added_by = this_user),
    this_user=User.objects.get(id=request.session['id'])
    this_item = Item.objects.get(id=item_id)
    this_user.wishlist.remove(this_item)

    return redirect('/dashboard')


def delete(request, item_id):
    this_item = Item.objects.get(id=item_id)
    this_item.delete()
    return redirect('/dashboard')
    