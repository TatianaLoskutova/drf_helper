from django.db.models import Q
from rest_framework.filters import BaseFilterBackend


class OwnedByOrganization(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        org_id = request.parser_context['kwargs'].get('pk')
        return queryset.filter(organization_id=org_id)


class OwnedByDepartment(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        department_id = request.parser_context['kwargs'].get('pk')
        return queryset.filter(department_id=department_id)


class MyOrganization(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        return queryset.filter(
            Q(director=user) | Q(employees=user)
        ).distinct()


class MyDepartment(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        return queryset.filter(
            Q(organization__director=user) | Q(organization__employees=user)
        ).distinct()
