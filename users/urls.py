from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import users

urlpatterns = [
    path('users/reg/', users.RegistrationView.as_view(), name='reg')
]
