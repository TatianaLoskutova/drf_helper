from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.filters import OrderingFilter

from vacations.factory.watches import WatchFactory
from vacations.models.watches import Watch
from common.views.mixins import LCRUViewSet
from vacations.serializers.api import watches as watches_s


@extend_schema_view(
    list=extend_schema(summary='Список смен', tags=['Отпуска: Смены']),
    retrieve=extend_schema(summary='Деталка смены', tags=['Отпуска: Смены']),
    create=extend_schema(summary='Создать смену', tags=['Отпуска: Смены']),
    partial_update=extend_schema(summary='Изменить смену частично', tags=['Отпуска: Смены']),
)
class WatchView(LCRUViewSet):
    # permission_classes = [IsMyCourt]

    queryset = Watch.objects.all()
    serializer_class = watches_s.WatchListSerializer

    multi_serializer_class = {
        'list': watches_s.WatchListSerializer,
        'retrieve': watches_s.WatchRetrieveSerializer,
        'create': watches_s.WatchCreateSerializer,
        'partial_update': watches_s.WatchUpdateSerializer,
    }

    http_method_names = ('get', 'post', 'patch')

    filter_backends = (
        OrderingFilter,
        DjangoFilterBackend,
        # MyRCourt,
    )
    # filterset_class = CourtFilter

    def get_queryset(self):
        return WatchFactory().list()

