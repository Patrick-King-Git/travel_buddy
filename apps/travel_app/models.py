from __future__ import unicode_literals
from django.db import models
import bcrypt
import datetime



class TripManager(models.Manager):
    def validate_trip(request, postData):
        print('&'* 50)
        print('we are validating the trip')
        print (datetime.date.today())
        print (type(datetime.date.today()))
        day = postData['travel_date_from']
        print(type(day))
        errors= {}
        if len(postData['destination']) < 1:
            errors['destination'] = "Destination can't be blank"
        if len(postData['description']) < 1:
            errors['description'] = "Description can't be blank"
        if len(postData['travel_date_from']) < 1:
            errors['travel_date_from'] = "Travel Date From can't be blank"
        if len(postData['travel_date_to']) < 1:
            errors['travel_date_to'] = "Travel Date To can't be blank"
        if postData['travel_date_from'] < str(datetime.date.today()):
            errors['travel_date_leave'] = 'Trip must be set in the future'
        if postData['travel_date_from'] >= postData['travel_date_to']:
            errors['travel_dates'] = 'You must depart for your trip before you can arrive back'
        return errors
        
class Trip(models.Model):
    destination = models.CharField(max_length = 255)
    description = models.TextField(max_length = 1000)
    planned_by = models.CharField(max_length=255)
    travel_date_from = models.DateField()
    travel_date_to = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()

class UserManager(models.Manager):
    def validate_register(request, postData):
        errors = {}
        if len(postData['name'])< 3:
            errors['name'] = 'Name cannot be empty'
        if len(postData['username'])< 3:
            errors['username'] = 'Username cannot be empty'
        if len(postData['password'])< 8:
            errors['password'] = 'Password must be at least 8 characters'
        if postData['password'] != postData['password2']:
            errors['password2'] = 'Passwords must match'
        return errors

    def validate_login(self, postData):
        errors = {}
        matching_user = User.objects.filter(username = postData['username'] )
        if len(matching_user) <1:
            errors['username'] = 'Username does not exist, try a new username or register'
        else: 
            user = matching_user[0]
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors['password'] = 'Password is incorrect'
        return errors

class User(models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    password= models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    trips = models.ManyToManyField(Trip, related_name='users')
    objects = UserManager()
