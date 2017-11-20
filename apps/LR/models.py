# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core import validators
import re
import bcrypt
from datetime import datetime, date, time


class UserManager(models.Manager):
    def regVal(self,postData):
        response = {
        'status': True,
        'errors': [],
        }
        EMAIL_regex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
        NoNum = re.compile(r'^[a-zA-Z_ ]*$')
        if not len(postData['name']) > 2 or not NoNum.match(postData['name']):
            response['errors'].append('Please enter a valid name')
        if not EMAIL_regex.match(postData['email']) or not len(postData['email']) > 2:
            response['errors'].append('please enter a valid email')
        if postData['password'] == None or len(postData["password"]) < 8:
            print 'password fails'
            response["errors"].append("Password must be at least 8 characters!")
        if not postData['password'] == postData['confirm']:
            response['errors'].append('passwords do not match')
        if postData['birthday'] == "" or datetime.strptime(postData['birthday'], '%Y-%m-%d') > datetime.now():
            response['errors'].append('Birthday is not valid')

        emailObject = self.filter(email = postData["email"])
        if len(emailObject) > 0:
            response["errors"].append("Email is already in database!")
        if len(response["errors"]) == 0:
            hashed = bcrypt.hashpw((postData['password'].encode()), bcrypt.gensalt(12))
            user = self.create(name = postData["name"], email = postData["email"], password = hashed)
            response["user"] = user
            print user
            return response
        response["status"] = False
        return response

    def logVal(self,postData):
        response = {
            'status' : True,
            'errors' : []
            }
        try:
            user = self.get(email = postData["email"])
        except:
            user = None
        if not user:
            response["errors"].append("Email is not registered!")
        if user:
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                response["errors"].append("Password does not match registered email.")
        if len(response["errors"]) == 0:
            response["user"] = user
            return response
        response["status"] = False
        return response

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    birthday = models.DateTimeField(null=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return "User: \n{}\n{}\n{}\n{}\n{}\n{}".format(self.id,self.name,self.birthday,self.username,self.email,self.password)
    def __str__(self):
        return "User: \n{}\n{}\n{}\n{}\n{}\n{}".format(self.id,self.name,self.birthday,self.username,self.email,self.password)
