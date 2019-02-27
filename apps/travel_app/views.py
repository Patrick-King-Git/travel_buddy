from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt

def login(request):
    return render(request, 'travel_app/login.html')

def register(request):
    print('at the register check')
    errors = User.objects.validate_register(request.POST)
    if len(errors) > 0:
        print(errors)
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/main')

    else:
        print('no errors')
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(name = request.POST['name'], username = request.POST['username'], password = hash1.decode())
        messages.success(request, 'User succcessfully registered!!')
        request.session['logged_in_name'] = user.name
        request.session['logged_in_id'] = user.id
        request.session['logged_in_username'] = user.username
        print(request.session['logged_in_name'])
        return redirect('/travels')

def checklogin(request):
    print('checking the login')
    errors = User.objects.validate_login(request.POST)
    if len(errors) >0:
        for key,value in errors.items():
            messages.error(request, value)
        return redirect('/main')
    else:
        messages.success (request, 'successfully logged in')
        user = User.objects.filter(username = request.POST['username'] )
        request.session['logged_in_name'] = user[0].name
        request.session['logged_in_id'] = user[0].id
        request.session['logged_in_username'] = user[0].username
        return redirect('/travels')

def travels(request):
    print('at the home page')
    if 'logged_in_id' not in request.session:
        messages.error(request, 'please login')
        return redirect('/main')
    else:
        user = User.objects.get(id = request.session['logged_in_id'])
        users_trips = user.trips.all()
        all_users = User.objects.exclude(id = request.session['logged_in_id'])
        all_trips = Trip.objects.all()
        print('$'*50)
        print(all_users)
        print(user)
        print(users_trips)
        context = {
            'trips': users_trips,
            'all_users': all_users,
            'all_trips': all_trips
        }
        return render(request, 'travel_app/travel.html', context)

def logout(request):
    request.session.clear()
    return redirect('/main')

def addtravelhome(request):
    if 'logged_in_id' not in request.session:
        messages.error(request, 'please login')
        return redirect('/main')
    else:
        return render(request, 'travel_app/add_travel.html')

def processadd(request):
    print('at process add')
    errors  = Trip.objects.validate_trip(request.POST)
    if len(errors) >0:
        for key,value in errors.items():
            messages.error(request, value)
        return redirect('/travels/add')
    else:
        this_user = User.objects.get(id= request.session['logged_in_id'])
        new_trip = Trip.objects.create(destination = request.POST['destination'],description = request.POST['description'], planned_by = request.session['logged_in_name'], travel_date_from = request.POST['travel_date_from'],travel_date_to = request.POST['travel_date_to'])
        this_user.trips.add(new_trip)
        print('*'* 50)
        print(new_trip.planned_by)
        print(new_trip.travel_date_from)
        print(this_user.trips.all())
        print('*'*50)
        return redirect('/travels')

def destination(request, num):
    print('at thr destination screen')
    if 'logged_in_id' not in request.session:
        messages.error(request, 'please login')
        return redirect('/main')
    else:
        this_trip = Trip.objects.get(id = num)
        print(this_trip)
        all_users = this_trip.users.all()
        context = {
            'this_trip': this_trip,
            'all_users': all_users
        }
        return render(request, 'travel_app/view_destination.html', context)

def jointrip(request, num):
    print('at the jointrip page')
    number = int(num)
    this_user = User.objects.get(id = request.session['logged_in_id'])
    this_trip = Trip.objects.get(id = num)
    this_trip.users.add(this_user)
    return redirect(f'/travels/destination/{number}')