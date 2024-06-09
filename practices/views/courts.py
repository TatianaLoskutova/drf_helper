from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.filters import OrderingFilter

from practices.factory.courts import CourtFactory
from practices.models.courts import Court
from common.views.mixins import LCRUViewSet
from practices.serializers.api import courts as courts_s


@extend_schema_view(
    list=extend_schema(summary='Список кортов', tags=['Тренировки: Корты']),
    retrieve=extend_schema(summary='Деталка корта', tags=['Тренировки: Корты']),
    create=extend_schema(summary='Создать корт', tags=['Тренировки: Корты']),
    partial_update=extend_schema(summary='Изменить корт частично', tags=['Тренировки: Корты']),
)
class CourtView(LCRUViewSet):
    # permission_classes = [IsMyCourt]

    queryset = Court.objects.all()
    serializer_class = courts_s.CourtListSerializer

    multi_serializer_class = {
        'list': courts_s.CourtListSerializer,
        'retrieve': courts_s.CourtRetrieveSerializer,
        'create': courts_s.CourtCreateSerializer,
        'partial_update': courts_s.CourtUpdateSerializer,
    }

    http_method_names = ('get', 'post', 'patch')

    filter_backends = (
        OrderingFilter,
        DjangoFilterBackend,
        # MyRCourt,
    )
    # filterset_class = CourtFilter

    def get_queryset(self):
        return CourtFactory().list()

