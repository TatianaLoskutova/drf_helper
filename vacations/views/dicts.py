from drf_spectacular.utils import extend_schema, extend_schema_view

from common.views.mixins import DictListMixin
from vacations.models.dicts import WatchStatus, VacationStatus


@extend_schema_view(
    list=extend_schema(
        summary='Список статусов смен', tags=['Словари']
    ),
)
class WatchStatusView(DictListMixin):
    queryset = WatchStatus.objects.filter(is_active=True)


@extend_schema_view(
    list=extend_schema(summary='Список статусов отпусков', tags=['Словари']),
)
class VacationStatusView(DictListMixin):
    queryset = VacationStatus.objects.filter(is_active=True)
