from drf_spectacular.utils import extend_schema, extend_schema_view

from clubs.models.clubs import Club
from clubs.serializers.api.clubs import ClubSearchListSerializer
from common.views.mixins import ListViewSet


@extend_schema_view(
    list=extend_schema(summary='Список клубов Search', tags=['Теннисные клубы']),
)
class ClubSearchView(ListViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSearchListSerializer
