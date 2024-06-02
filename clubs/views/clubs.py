from drf_spectacular.utils import extend_schema, extend_schema_view

from clubs.models.clubs import Club
from clubs.serializers.api import clubs
from common.views.mixins import CRUViewSet, ListViewSet


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
class ClubView(CRUViewSet):
    queryset = Club.objects.all()
    serializer_class = clubs.ClubListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return clubs.ClubRetrieveSerializer
        elif self.action == 'create':
            return clubs.ClubCreateSerializer
        elif self.action == 'update':
            return clubs.ClubUpdateSerializer
        elif self.action == 'partial_update':
            return clubs.ClubUpdateSerializer

        return self.serializer_class
