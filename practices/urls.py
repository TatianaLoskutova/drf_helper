from django.urls import include, path
from rest_framework.routers import DefaultRouter

from practices.views import dicts

router = DefaultRouter()

router.register(
    r'dicts/statuses/trainings', dicts.TrainingStatusView,
    'trainings-statuses',
)
router.register(
    r'dicts/statuses/courts', dicts.CourtStatusView, 'courts-statuses'
)

urlpatterns = [
    path('trainings/', include(router.urls)),
]
