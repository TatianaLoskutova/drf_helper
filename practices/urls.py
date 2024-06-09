from django.urls import include, path
from rest_framework.routers import DefaultRouter

from practices.views import dicts, courts

router = DefaultRouter()

router.register(r'courts', courts.CourtView, 'courts')
router.register(
    r'dicts/statuses/trainings', dicts.TrainingStatusView,
    'trainings-statuses',
)
router.register(
    r'dicts/statuses/courts', dicts.CourtStatusView, 'court-statuses'
)

urlpatterns = [
    path('trainings/', include(router.urls)),
]
