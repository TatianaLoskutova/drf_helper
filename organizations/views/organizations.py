from django.db.models import Case, Count, When
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.filters import OrderingFilter, SearchFilter

from organizations.backends import MyOrganization
from organizations.filters import OrganizationFilter
from organizations.models.organizations import Organization
from organizations.permissions import IsMyOrganization
from organizations.serializers.api import organizations
from common.views.mixins import LCRUViewSet, ListViewSet


@extend_schema_view(
    list=extend_schema(summary='Список организаций Search', tags=['Словари']),
)
class OrganizationSearchView(ListViewSet):
    queryset = Organization.objects.all()
    serializer_class = organizations.OrganizationSearchListSerializer


@extend_schema_view(
    list=extend_schema(summary='Список организаций', tags=['Организации']),
    retrieve=extend_schema(summary='Деталка организации', tags=['Организации']),
    create=extend_schema(summary='Создать организацию', tags=['Организации']),
    update=extend_schema(summary='Изменить организацию', tags=['Организации']),
    partial_update=extend_schema(summary='Частично изменить организацию', tags=['Организации']),
)
class OrganizationView(LCRUViewSet):
    permission_classes = [IsMyOrganization]
    queryset = Organization.objects.all()
    serializer_class = organizations.OrganizationListSerializer

    multi_serializer_class = {
        'list': organizations.OrganizationListSerializer,
        'retrieve': organizations.OrganizationRetrieveSerializer,
        'create': organizations.OrganizationCreateSerializer,
        'update': organizations.OrganizationUpdateSerializer,
        'partial_update': organizations.OrganizationUpdateSerializer,
    }

    http_method_names = ('get', 'post', 'patch')

    filter_backends = (
        OrderingFilter,
        SearchFilter,
        DjangoFilterBackend,
        MyOrganization,
    )
    filterset_class = OrganizationFilter
    ordering = ('name', 'id',)

    def get_queryset(self):
        queryset = Organization.objects.select_related(
            'director',
        ).prefetch_related(
            'employees',
            'departments',
        ).annotate(
            pax=Count('employees', distinct=True),
            departments_count=Count('departments', distinct=True),
            can_manage=Case(
                When(director=self.request.user, then=True),
                default=False,
            )
        )
        return queryset
