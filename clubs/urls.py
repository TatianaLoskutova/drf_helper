from django.urls import path, include
from rest_framework.routers import DefaultRouter

from clubs.views import dicts, clubs

router = DefaultRouter()

router.register(r'dicts/positions', dicts.PositionView, 'positions')
router.register(r'search', clubs.ClubSearchView, 'clubs-search')

urlpatterns = [
    path('clubs/', include(router.urls)),
]
