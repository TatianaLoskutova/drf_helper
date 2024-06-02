from drf_spectacular.utils import extend_schema, extend_schema_view

from clubs.backends import OwnedByClub
from clubs.filters import PlayerFilter
from clubs.models.clubs import Player
from clubs.permissions import IsColleagues
from clubs.serializers.api import players as players_s
from common.views.mixins import CRUDViewSet
from rest_framework.filters import OrderingFilter, SearchFilter


@extend_schema_view(
    list=extend_schema(summary='Список игроков клуба', tags=['Теннисные клубы: Игроки']),
    retrieve=extend_schema(summary='Деталка игрока клуба', tags=['Теннисные клубы: Игроки']),
    create=extend_schema(summary='Создать игрока клуба', tags=['Теннисные клубы: Игроки']),
    update=extend_schema(summary='Изменить игрока клуба', tags=['Теннисные клубы: Игроки']),
    partial_update=extend_schema(summary='Частично изменить игрока клуба', tags=['Теннисные клубы: Игроки']),
    destroy=extend_schema(summary='Удалить игрока клуба', tags=['Теннисные клубы: Игроки']),
)
class PlayerView(CRUDViewSet):
    queryset = Player.objects.all()
    serializer_class = players_s.PlayerListSerializer
    permission_classes = [IsColleagues]

    multi_serializer_class = {
        'list': players_s.PlayerListSerializer,
        'retrieve': players_s.PlayerRetrieveSerializer,
        'create': players_s.PlayerCreateSerializer,
        'update': players_s.PlayerUpdateSerializer,
        'partial_update': players_s.PlayerUpdateSerializer,
    }

    lookup_url_kwarg = 'player_id'
    http_method_names = ('get', 'post', 'patch', 'delete',)

    filter_backends = (
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
