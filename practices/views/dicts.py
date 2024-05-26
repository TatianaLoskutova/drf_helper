from drf_spectacular.utils import extend_schema, extend_schema_view

from common.views.mixins import DictListMixin
from practices.models.dicts import CourtStatus, TrainingStatus


@extend_schema_view(
    list=extend_schema(
        summary='Список статусов кортов', tags=['Словари']
    ),
)
class CourtStatusView(DictListMixin):
    queryset = CourtStatus.objects.filter(is_active=True)


@extend_schema_view(
    list=extend_schema(summary='Список статусов тренировок', tags=['Словари']),
)
class TrainingStatusView(DictListMixin):
    queryset = TrainingStatus.objects.filter(is_active=True)
