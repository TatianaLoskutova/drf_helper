from django.urls import include, path
from rest_framework.routers import DefaultRouter

from vacations.views import dicts, watches

router = DefaultRouter()

router.register(r'watches', watches.WatchView, 'watches')
router.register(
    r'dicts/statuses/vacations', dicts.VacationStatusView,
    'vacations-statuses',
)
router.register(
    r'dicts/statuses/watches', dicts.WatchStatusView, 'watch-statuses'
)

urlpatterns = [
    path('vacations/', include(router.urls)),
]
