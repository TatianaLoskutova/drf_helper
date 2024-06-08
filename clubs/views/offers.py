from django.db.models import Case, Q, When
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.filters import OrderingFilter

from clubs.backends import OwnedByClub
from clubs.filters import OfferOrgFilter, OfferUserFilter
from clubs.models.offers import Offer
from clubs.permissions import IsOfferTrainer
from clubs.serializers.api import offers as offers_s
from common.views.mixins import ListCreateUpdateViewSet


@extend_schema_view(
    list=extend_schema(summary='Список офферов клуба', tags=['Теннисные клубы: Офферы']),
    create=extend_schema(summary='Создать ооферы пользователям', tags=['Теннисные клубы: Офферы']),
    partial_update=extend_schema(summary='Изменить оффер пользователя частично', tags=['Теннисные клубы: Офферы']),
)
class OfferClubView(ListCreateUpdateViewSet):
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
        qs = Offer.objects.select_related(
            'user',
        ).prefetch_related(
            'club',
        ).annotate(
            can_accept=Case(
                When(Q(user_accept__isnull=True, org_accept=False), then=True,),
                default=False,
            ),
            can_reject=Case(
                When(Q(user_accept__isnull=True, org_accept=True), then=True,),
                default=False,
            ),
        )
        return qs


@extend_schema_view(
    list=extend_schema(summary='Список офферов пользователя', tags=['Теннисные клубы: Офферы']),
    create=extend_schema(summary='Создать оффер в клуб', tags=['Теннисные клубы: Офферы']),
    partial_update=extend_schema(summary='Изменить оффер в клуб частично', tags=['Теннисные клубы: Офферы']),
)
class OfferUserView(ListCreateUpdateViewSet):
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
        qs = Offer.objects.select_related(
            'user',
        ).prefetch_related(
            'club',
        ).filter(
            user=self.request.user,
        ).annotate(
            can_accept=Case(
                When(Q(org_accept__isnull=True, user_accept=False), then=True,),
                default=False,
            ),
            can_reject=Case(
                When(Q(org_accept__isnull=True, user_accept=True), then=True,),
                default=False,
            ),
        )
        return qs
