from drf_spectacular.utils import extend_schema, extend_schema_view

from clubs.models.clubs import Player
from clubs.serializers.api import players as players_s
from common.views.mixins import CRUDViewSet


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

    lookup_url_kwarg = 'player_id'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return players_s.PlayerRetrieveSerializer
        elif self.action == 'create':
            return players_s.PlayerCreateSerializer
        elif self.action == 'update':
            return players_s.PlayerUpdateSerializer
        elif self.action == 'partial_update':
            return players_s.PlayerUpdateSerializer

        return self.serializer_class

    def get_queryset(self):
        club_id = self.request.parser_context['kwargs'].get('pk')
        queryset = Player.objects.filter(club_id=club_id)
        return queryset
