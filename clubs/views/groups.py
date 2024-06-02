from django.db.models import Case, Count, Q, When
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.filters import OrderingFilter, SearchFilter

from clubs.backends import MyClub, MyGroup
from clubs.filters import GroupFilter
from clubs.models.groups import Group
from clubs.permissions import IsColleagues, IsMyGroup
from clubs.serializers.api import groups as groups_s
from common.views.mixins import CRUViewSet


@extend_schema_view(
    list=extend_schema(summary='Список групп', tags=['Теннисные клубы: Группы']),
    retrieve=extend_schema(summary='Деталка группы', tags=['Теннисные клубы: Группы']),
    create=extend_schema(summary='Создать группу', tags=['Теннисные клубы: Группы']),
    update=extend_schema(summary='Изменить группу', tags=['Теннисные клубы: Группы']),
    partial_update=extend_schema(summary='Изменить группу частично', tags=['Теннисные клубы: Группы']),
)
class GroupView(CRUViewSet):
    permission_classes = [IsMyGroup]

    queryset = Group.objects.all()
    serializer_class = groups_s.GroupListSerializer

    multi_serializer_class = {
        'list': groups_s.GroupListSerializer,
        'retrieve': groups_s.GroupRetrieveSerializer,
        'create': groups_s.GroupCreateSerializer,
        'update': groups_s.GroupUpdateSerializer,
        'partial_update': groups_s.GroupUpdateSerializer,
    }

    http_method_names = ('get', 'post', 'patch')

    filter_backends = (
        OrderingFilter,
        SearchFilter,
        DjangoFilterBackend,
        MyGroup,
    )
    search_fields = ('name',)
    filterset_class = GroupFilter
    ordering = ('name', 'id',)

    def get_queryset(self):
        queryset = Group.objects.select_related(
            'trainer',
        ).prefetch_related(
            'club',
            'club__director',
            'members',
        ).annotate(
            pax=Count('members', distinct=True),
            can_manage=Case(
                When(
                    Q(trainer__user=self.request.user) |
                    Q(club__director=self.request.user),
                    then=True
                ),
                default=False,
            ),
            is_member=Case(
                When(Q(members_info__player__user=self.request.user)),
                default=False,
            ),
        )
        return queryset