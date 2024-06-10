from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import action

from organizations.backends import OwnedByDepartment
from organizations.models.departments import Member
from organizations.permissions import IsColleagues
from organizations.serializers.api import members as members_s
from common.views.mixins import LCDViewSet


@extend_schema_view(
    list=extend_schema(summary='Список сотрудников отдела', tags=['Организации: Отделы: Сотрудники']),
    # retrieve=extend_schema(summary='Деталка участника группы', tags=['Теннисные клубы: Группы: Участники']),
    create=extend_schema(summary='Создать сотрудника отдела', tags=['Организации: Отделы: Сотрудники']),
    destroy=extend_schema(summary='Удалить сотрудника из отдела', tags=['Организации: Отделы: Сотрудники']),
    search=extend_schema(filters=True, summary='Список сотрудников отдела Search', tags=['Словари']),
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

    filter_backends = (OwnedByDepartment,)

    def get_queryset(self):
        qs = Member.objects.select_related(
            'employee',
        ).prefetch_related(
            'group',
            'employee__user',
            'employee__organization',
            'employee__position',
        )
        return qs

    @action(methods=['GET'], detail=False, url_path='search')
    def search(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
