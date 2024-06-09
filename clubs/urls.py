from django.urls import path, include
from rest_framework.routers import DefaultRouter

from clubs.views import dicts, clubs, players, groups, offers, members

router = DefaultRouter()

router.register(r'dicts/positions', dicts.PositionView, 'positions')
router.register(r'search', clubs.ClubSearchView, 'clubs-search')
router.register(r'(?P<pk>\d+)/players', players.PlayerView, 'players')
router.register(r'offers', offers.OfferUserView, 'user-offers')
router.register(r'(?P<pk>\d+)/offers', offers.OfferClubView, 'org-offers')
router.register(r'groups/(?P<pk>\d+)/members', members.MemberView, 'members')
router.register(r'groups', groups.GroupView, 'groups')
router.register(r'', clubs.ClubView, 'clubs')


urlpatterns = [
    path('clubs/', include(router.urls)),
]
