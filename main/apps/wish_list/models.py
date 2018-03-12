# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import bcrypt

import re

from django.contrib import messages

from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

# Create your models here.
class UserManager(models.Manager):
    def reg_validator(self, post_data):
        errors = []
        if len(post_data['first_name']) < 2 or len(post_data['last_name']) < 2:
            errors.append("name fields must be at least 3 characters")
        if len(post_data['pass']) < 8:
            errors.append("password must be at least 8 characters")       
        if not re.match(NAME_REGEX, post_data['first_name']):
            errors.append('name fields must be letter characters only')
        if not re.match(NAME_REGEX, post_data['last_name']):
            errors.append('name fields must be letter characters only')
        if not re.match(EMAIL_REGEX, post_data['email']):
            errors.append("invalid email")
        if len(User.objects.filter(email=post_data['email'])) > 0:
            errors.append("email already in use")
        if post_data['pass'] != post_data['pass_conf']:
            errors.append("passwords do not match")

        if not errors:
            hashed = bcrypt.hashpw((post_data['pass'].encode()), bcrypt.gensalt(5))

            new_user = self.create(
                first_name=post_data['first_name'],
                last_name=post_data['last_name'],
                email=post_data['email'],
                password=hashed
            )
            return new_user
        return errors

    def validate_login(self, post_data):
        errors = []
        if len(self.filter(email=post_data['email2'])) > 0:
            this_user = self.filter(email=post_data['email2'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(), this_user.password.encode()):
                errors.append('email/password incorrect')
        else:
            errors.append('email/password incorrect')

        if errors:
            return errors
        return this_user

class ItemManager(models.Manager):
    def item_validator(self, post_data):
        errors = []
        if len(post_data['item']) < 3:
            errors.append('fields are required and should be more than 3 characters')
        # if len(Item.objects.filter(name=post_data['item'])) > 0:
        #     errors.append('this item already exists')


        if not errors: 
            this_item = Item.objects.create(
                added_by = User.objects.get(id=post_data['id']),
                name = post_data['item']
            )
            this_item.users.add(User.objects.get(id=post_data['id']))
            
            return this_item
        else:
            return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Item(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name = "wishlist")
    added_by = models.ForeignKey(User, related_name = "items_added")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ItemManager()


