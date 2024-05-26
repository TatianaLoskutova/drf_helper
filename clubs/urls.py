from django.urls import path, include
from rest_framework.routers import DefaultRouter

from clubs.views import dicts

router = DefaultRouter()

router.register(r'dicts/positions', dicts.PositionView, 'positions')

urlpatterns = [
    path('clubs/', include(router.urls)),
]
