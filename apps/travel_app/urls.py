from django.urls import path
from . import views

urlpatterns = [
    path('main', views.login),
    path('register', views.register),
    path('checklogin', views.checklogin),
    path('travels', views.travels),
    path('logout', views.logout),
    path('travels/add', views.addtravelhome),
    path('processadd', views.processadd),
    path('travels/destination/<num>', views.destination),
    path('jointrip/<num>', views.jointrip),
]