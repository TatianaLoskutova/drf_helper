from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter

from clubs.backends import OwnedByClub
from clubs.filters import PlayerFilter
from clubs.models.clubs import Player
from clubs.permissions import IsColleagues
from clubs.serializers.api import players as players_s
from common.views.mixins import LCRUDViewSet, ListViewSet


@extend_schema_view(
    list=extend_schema(summary='Список игроков клуба', tags=['Теннисные клубы: Игроки']),
    retrieve=extend_schema(summary='Деталка игрока клуба', tags=['Теннисные клубы: Игроки']),
    create=extend_schema(summary='Создать игрока клуба', tags=['Теннисные клубы: Игроки']),
    update=extend_schema(summary='Изменить игрока клуба', tags=['Теннисные клубы: Игроки']),
    partial_update=extend_schema(summary='Частично изменить игрока клуба', tags=['Теннисные клубы: Игроки']),
    destroy=extend_schema(summary='Удалить игрока из клуба', tags=['Теннисные клубы: Игроки']),
    search=extend_schema(filters=True, summary='Список игроков клуба Search',tags=['Словари']),
)
class PlayerView(LCRUDViewSet):
    permission_classes = [IsColleagues]
    queryset = Player.objects.all()
    serializer_class = players_s.PlayerListSerializer


    multi_serializer_class = {
        'list': players_s.PlayerListSerializer,
        'retrieve': players_s.PlayerRetrieveSerializer,
        'create': players_s.PlayerCreateSerializer,
        'update': players_s.PlayerUpdateSerializer,
        'partial_update': players_s.PlayerUpdateSerializer,
        'search': players_s.PlayerSearchSerializer,
        'destroy': players_s.PlayerDeleteSerializer,
    }

    lookup_url_kwarg = 'player_id'
    http_method_names = ('get', 'post', 'patch', 'delete',)

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
        OwnedByClub,
    )
    filterset_class = PlayerFilter
    ordering = ('position', 'date_joined', 'id',)

    def get_queryset(self):
        qs = Player.objects.select_related(
            'user',
            'position',
        ).prefetch_related(
            'club',
        )
        return qs

    @action(methods=['GET'], detail=False, url_path='search')
    def search(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=dict())
        serializer.is_valid(raise_exception=True)
        return super().destroy(request, *args, **kwargs)
