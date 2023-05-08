
from django.urls import path,include
from .views import *
from rest_framework import routers
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register('login',Login, basename="login")


urlpatterns = [ 
    path('', include(router.urls)),     
    path('register/', Register.as_view()),
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post-retrieve-update-destroy'),
]


