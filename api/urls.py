from home.views import index
from django.urls import path, include
from home.views import person, login, PersonAPI, PersonViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'people', PersonViewSet, basename='people')
urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('index/', index),
    path('person/', person),
    path('login/', login),
    path('person-api/', PersonAPI.as_view()),
]
