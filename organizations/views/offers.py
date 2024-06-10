from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.filters import OrderingFilter

from organizations.backends import OwnedByOrganization
from organizations.factory.offers import OfferFactory
from organizations.filters import OfferOrgFilter, OfferUserFilter
from organizations.models.offers import Offer
from organizations.permissions import IsOfferChief
from organizations.serializers.api import offers as offers_s
from common.views.mixins import LCUViewSet


@extend_schema_view(
    list=extend_schema(summary='Список офферов организации', tags=['Организации: Офферы']),
    create=extend_schema(summary='Создать ооферы пользователям', tags=['Организации: Офферы']),
    partial_update=extend_schema(summary='Изменить оффер пользователя частично', tags=['Организации: Офферы']),
)
class OfferOrganizationView(LCUViewSet):
    permission_classes = [IsOfferChief]

    queryset = Offer.objects.all()
    serializer_class = offers_s.OfferOrgToUserListSerializer

    multi_serializer_class = {
        'list': offers_s.OfferOrgToUserListSerializer,
        'create': offers_s.OfferOrgToUserCreateSerializer,
        'partial_update': offers_s.OfferOrgToUserUpdateSerializer,
    }

    lookup_url_kwarg = 'offer_id'
    http_method_names = ('get', 'post', 'patch',)

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        OwnedByOrganization,
    )
    filterset_class = OfferOrgFilter
    ordering_fields = ('-created_at', 'updated_at',)

    def get_queryset(self):
        return OfferFactory().organization_list()


@extend_schema_view(
    list=extend_schema(summary='Список офферов пользователя', tags=['Организации: Офферы']),
    create=extend_schema(summary='Создать оффер в организацию', tags=['Организации: Офферы']),
    partial_update=extend_schema(summary='Изменить оффер в организацию частично', tags=['Организации: Офферы']),
)
class OfferUserView(LCUViewSet):
    queryset = Offer.objects.all()
    serializer_class = offers_s.OfferUserToOrgListSerializer

    multi_serializer_class = {
        'list': offers_s.OfferUserToOrgListSerializer,
        'create': offers_s.OfferUserToOrgCreateSerializer,
        'partial_update': offers_s.OfferUserToOrgUpdateSerializer,
    }

    http_method_names = ('get', 'post', 'patch',)

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_class = OfferUserFilter
    ordering_fields = ('created_at', 'updated_at',)

    def get_queryset(self):
        return OfferFactory().user_list()
