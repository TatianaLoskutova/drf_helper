from django.db.models import Q
from rest_framework.filters import BaseFilterBackend


class OwnedByClub(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        org_id = request.parser_context['kwargs'].get('pk')
        return queryset.filter(club_id=org_id)


class OwnedByGroup(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        group_id = request.parser_context['kwargs'].get('pk')
        return queryset.filter(group_id=group_id)


class MyClub(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        return queryset.filter(
            Q(director=user) | Q(players=user)
        )


class MyGroup(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        return queryset.filter(
            Q(club__director=user) | Q(club__players=user)
        )
