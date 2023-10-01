from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('register_user/', register_user,name='register_user'),
    path('apply_loan/', apply_loan,name='apply_loan'),
    path('make_payment/', make_payment,name='make_payment'),
    path('get_statement/', get_statement,name='get_statement'),
  
]
