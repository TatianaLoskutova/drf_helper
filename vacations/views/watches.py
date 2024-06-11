from crum import get_current_user
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404

from common.views.mixins import ExtendedRetrieveUpdateAPIView, LCRUViewSet
from vacations.factory.watches import WatchFactory
from vacations.models.watches import Watch, WatchMember
from vacations.serializers.api import watches as watches_s


@extend_schema_view(
    list=extend_schema(summary='Список смен', tags=['Отпуска: Смены']),
    retrieve=extend_schema(summary='Деталка смены', tags=['Отпуска: Смены']),
    create=extend_schema(summary='Создать смену', tags=['Отпуска: Смены']),
    partial_update=extend_schema(summary='Изменить смену частично', tags=['Отпуска: Смены']),
)
class WatchView(LCRUViewSet):
    # permission_classes = [IsMyCourt]

    queryset = Watch.objects.all()
    serializer_class = watches_s.WatchListSerializer

    multi_serializer_class = {
        'list': watches_s.WatchListSerializer,
        'retrieve': watches_s.WatchRetrieveSerializer,
        'create': watches_s.WatchCreateSerializer,
        'partial_update': watches_s.WatchUpdateSerializer,
    }

    http_method_names = ('get', 'post', 'patch')

    filter_backends = (
        OrderingFilter,
        DjangoFilterBackend,
        # MyRCourt,
    )
    # filterset_class = CourtFilter

    def get_queryset(self):
        return WatchFactory().list()


@extend_schema_view(
    get=extend_schema(summary='Данные участника смены', tags=['Отпуска: Смены']),
    patch=extend_schema(summary='Изменить участника смены', tags=['Отпуска: Смены']),
)
class MeWatchMemberView(ExtendedRetrieveUpdateAPIView):
    queryset = WatchMember.objects.all()
    serializer_class = watches_s.WatchMemberListSerializer
    multi_serializer_class = {
        'GET': watches_s.WatchMemberListSerializer,
        'PATCH': watches_s.WatchMemberUpdateSerializer,
    }

    def get_object(self):
        user = get_current_user()
        watch_id = self.request.parser_context['kwargs'].get('pk')
        member = get_object_or_404(
            WatchMember,
            Q(watch_id=watch_id, member__employee__user=user)
        )
        return member
