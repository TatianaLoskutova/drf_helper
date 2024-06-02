from django.urls import path, include
from rest_framework.routers import DefaultRouter

from clubs.views import dicts, clubs, players, groups

router = DefaultRouter()

router.register(r'dicts/positions', dicts.PositionView, 'positions')
router.register(r'search', clubs.ClubSearchView, 'clubs-search')
router.register(r'(?P<pk>\d+)/players', players.PlayerView, 'players')
router.register(r'groups', groups.GroupView, 'groups')
router.register(r'', clubs.ClubView, 'clubs')


urlpatterns = [
    path('clubs/', include(router.urls)),
]
