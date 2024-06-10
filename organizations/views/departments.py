from django.db.models import Case, Count, Q, When
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter

from organizations.backends import MyDepartment
from organizations.filters import DepartmentFilter
from organizations.models.departments import Department
from organizations.permissions import IsMyDepartment
from organizations.serializers.api import departments as departments_s
from common.views.mixins import LCRUViewSet


@extend_schema_view(
    list=extend_schema(summary='Список отделов', tags=['Организации: Отделы']),
    retrieve=extend_schema(summary='Деталка отдела', tags=['Организации: Отделы']),
    create=extend_schema(summary='Создать отдел', tags=['Организации: Отделы']),
    update=extend_schema(summary='Изменить отдел', tags=['Организации: Отделы']),
    partial_update=extend_schema(summary='Изменить отдел частично', tags=['Организации: Отделы']),
    update_settings=extend_schema(summary='Изменить настройки отдела', tags=['Организации: Отделы']),
)
class DepartmentView(LCRUViewSet):
    permission_classes = [IsMyDepartment]

    queryset = Department.objects.all()
    serializer_class = departments_s.DepartmentListSerializer

    multi_serializer_class = {
        'list': departments_s.DepartmentListSerializer,
        'retrieve': departments_s.DepartmentRetrieveSerializer,
        'create': departments_s.DepartmentCreateSerializer,
        'update': departments_s.DepartmentUpdateSerializer,
        'partial_update': departments_s.DepartmentUpdateSerializer,
        'update_settings': departments_s.DepartmentSettingsUpdateSerializer,
    }

    http_method_names = ('get', 'post', 'patch')

    filter_backends = (
        OrderingFilter,
        SearchFilter,
        DjangoFilterBackend,
        MyDepartment,
    )
    search_fields = ('name',)
    filterset_class = DepartmentFilter
    ordering = ('name', 'id',)

    def get_queryset(self):
        queryset = Department.objects.select_related(
            'chief',
        ).prefetch_related(
            'organization',
            'organization__director',
            'members',
        ).annotate(
            pax=Count('members', distinct=True),
            can_manage=Case(
                When(
                    Q(chief__user=self.request.user) |
                    Q(organization__director=self.request.user),
                    then=True
                ),
                default=False,
            ),
            _is_member_count=Count(
                'members', filter=(Q(members__user=self.request.user)),
                distinct=True,
            ),
            is_member=Case(
                When(Q(_is_member_count__gt=0), then=True), default=False,
            ),
        )
        return queryset

    @action(methods=['PATCH'], detail=True, url_path='settings')
    def update_settings(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
