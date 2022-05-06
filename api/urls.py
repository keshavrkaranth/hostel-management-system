
from django.urls import path
from .views import *

urlpatterns = [
    path('',homePage),
    path('createStudent',createStudent)
]
