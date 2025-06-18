from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index_view,name='index_view'),
    path('home',views.home_view,name='home_view')
]