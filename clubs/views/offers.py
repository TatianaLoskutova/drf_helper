from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.filters import OrderingFilter

from clubs.backends import OwnedByClub
from clubs.factory.offers import OfferFactory
from clubs.filters import OfferOrgFilter, OfferUserFilter
from clubs.models.offers import Offer
from clubs.permissions import IsOfferTrainer
from clubs.serializers.api import offers as offers_s
from common.views.mixins import LCUViewSet


@extend_schema_view(
    list=extend_schema(summary='Список офферов клуба', tags=['Теннисные клубы: Офферы']),
    create=extend_schema(summary='Создать ооферы пользователям', tags=['Теннисные клубы: Офферы']),
    partial_update=extend_schema(summary='Изменить оффер пользователя частично', tags=['Теннисные клубы: Офферы']),
)
class OfferClubView(LCUViewSet):
    permission_classes = [IsOfferTrainer]

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
        OwnedByClub,
    )
    filterset_class = OfferOrgFilter
    ordering_fields = ('-created_at', 'updated_at',)

    def get_queryset(self):
        return OfferFactory().club_list()


@extend_schema_view(
    list=extend_schema(summary='Список офферов пользователя', tags=['Теннисные клубы: Офферы']),
    create=extend_schema(summary='Создать оффер в клуб', tags=['Теннисные клубы: Офферы']),
    partial_update=extend_schema(summary='Изменить оффер в клуб частично', tags=['Теннисные клубы: Офферы']),
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
