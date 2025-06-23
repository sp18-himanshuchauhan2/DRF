from home.views import index
from django.urls import path
from home.views import person, login, PersonAPI

urlpatterns = [
    path('index/', index),
    path('person/', person),
    path('login/', login),
    path('person-api/', PersonAPI.as_view())
]
