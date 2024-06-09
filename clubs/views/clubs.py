from django.db.models import Case, Count, When
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.filters import OrderingFilter, SearchFilter

from clubs.backends import MyClub
from clubs.filters import ClubFilter
from clubs.models.clubs import Club
from clubs.permissions import IsMyClub
from clubs.serializers.api import clubs
from common.views.mixins import LCRUViewSet, ListViewSet


@extend_schema_view(
    list=extend_schema(summary='Список теннисных клубов Search', tags=['Словари']),
)
class ClubSearchView(ListViewSet):
    queryset = Club.objects.all()
    serializer_class = clubs.ClubSearchListSerializer


@extend_schema_view(
    list=extend_schema(summary='Список клубов', tags=['Теннисные клубы']),
    retrieve=extend_schema(summary='Деталка клубов', tags=['Теннисные клубы']),
    create=extend_schema(summary='Создать клуб', tags=['Теннисные клубы']),
    update=extend_schema(summary='Изменить клуб', tags=['Теннисные клубы']),
    partial_update=extend_schema(summary='Частично изменить клуб', tags=['Теннисные клубы']),
)
class ClubView(LCRUViewSet):
    permission_classes = [IsMyClub]
    queryset = Club.objects.all()
    serializer_class = clubs.ClubListSerializer

    multi_serializer_class = {
        'list': clubs.ClubListSerializer,
        'retrieve': clubs.ClubRetrieveSerializer,
        'create': clubs.ClubCreateSerializer,
        'update': clubs.ClubUpdateSerializer,
        'partial_update': clubs.ClubUpdateSerializer,
    }

    http_method_names = ('get', 'post', 'patch')

    filter_backends = (
        OrderingFilter,
        SearchFilter,
        DjangoFilterBackend,
        MyClub,
    )
    filterset_class = ClubFilter
    ordering = ('name', 'id',)

    def get_queryset(self):
        queryset = Club.objects.select_related(
            'director',
        ).prefetch_related(
            'players',
            'groups',
        ).annotate(
            pax=Count('players', distinct=True),
            groups_count=Count('groups', distinct=True),
            can_manage=Case(
                When(director=self.request.user, then=True),
                default=False,
            )
        )
        return queryset
