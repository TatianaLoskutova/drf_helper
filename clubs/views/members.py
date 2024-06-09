from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import action

from clubs.backends import OwnedByGroup
from clubs.models.groups import Member
from clubs.permissions import IsColleagues
from clubs.serializers.api import members as members_s
from common.views.mixins import LCDViewSet


@extend_schema_view(
    list=extend_schema(summary='Список участников группы', tags=['Теннисные клубы: Группы: Участники']),
    # retrieve=extend_schema(summary='Деталка участника группы', tags=['Теннисные клубы: Группы: Участники']),
    create=extend_schema(summary='Создать участника группы', tags=['Теннисные клубы: Группы: Участники']),
    destroy=extend_schema(summary='Удалить участника из группы', tags=['Теннисные клубы: Группы: Участники']),
    search=extend_schema(filters=True, summary='Список участников группы Search', tags=['Словари']),
)
class MemberView(LCDViewSet):
    permission_classes = [IsColleagues]

    queryset = Member.objects.all()
    serializer_class = members_s.MemberListSerializer

    multi_serializer_class = {
        'list': members_s.MemberListSerializer,
        # 'retrieve': members_s.MemberRetrieveSerializer,
        'create': members_s.MemberCreateSerializer,
        'search': members_s.MemberSearchSerializer,
    }

    lookup_url_kwarg = 'member_id'

    filter_backends = (OwnedByGroup,)

    def get_queryset(self):
        qs = Member.objects.select_related(
            'player',
        ).prefetch_related(
            'group',
            'player__user',
            'player__club',
            'player__position',
        )
        return qs

    @action(methods=['GET'], detail=False, url_path='search')
    def search(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
