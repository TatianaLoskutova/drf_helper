import django_filters
from django.db.models import Q, F
from organizations.models.organizations import Organization, Employee
from organizations.models.departments import Department
from organizations.models.offers import Offer
from organizations.constants import DIRECTOR_POSITION, CHIEF_POSITION


class OrganizationFilter(django_filters.FilterSet):
    can_manage = django_filters.BooleanFilter('can_manage', label='Can manage')

    class Meta:
        model = Organization
        fields = ('can_manage', 'id',)


class EmployeeFilter(django_filters.FilterSet):
    only_corporate = django_filters.BooleanFilter(
        'user__is_corporate_account', label='Is corporate account'
    )
    can_be_department_chief = django_filters.BooleanFilter(
        method='can_be_department_chief_filter', label='Can be department chief'
    )

    class Meta:
        model = Employee
        fields = ('only_corporate',)

    def can_be_department_chief_filter(self, queryset, name, value):
        return queryset.filter(position_id__in=[DIRECTOR_POSITION, CHIEF_POSITION])


class DepartmentFilter(django_filters.FilterSet):
    is_member = django_filters.BooleanFilter('is_member',)
    can_manage = django_filters.BooleanFilter('can_manage', )

    class Meta:
        model = Department
        fields = ('organization', 'chief',)


class OfferOrgFilter(django_filters.FilterSet):
    TYPE_CHOICES = (
        ('sent', 'Отправленные'),
        ('received', 'Полученные'),
    )
    DECISION_CHOICES = (
        ('accept', 'Принятые'),
        ('reject', 'Отклоненные'),
        ('unknown', 'На рассмотрении'),
    )

    can_accept = django_filters.BooleanFilter('can_accept',)
    can_reject = django_filters.BooleanFilter('can_reject',)

    type = django_filters.ChoiceFilter(
        method='type_filter',
        choices=TYPE_CHOICES,
        label='type',
    )

    decision = django_filters.ChoiceFilter(
        method='decision_filter',
        choices=DECISION_CHOICES,
        label='decision',
    )

    class Meta:
        model = Offer
        fields = ('user_accept',)

    def type_filter(self, queryset, name, value):
        if value == 'sent':
            return queryset.filter(~Q(created_by=F('user')))
        elif value == 'received':
            return queryset.filter(created_by=F('user'))
        return queryset

    def decision_filter(self, queryset, name, value):
        offer_type = self.data.get('type')
        if offer_type not in ('sent', 'received'):
            return queryset
        if value not in ('accept', 'reject', 'unknown'):
            return queryset

        sent_type = bool(offer_type == 'sent')
        decision_filter = {
            'accept': Q(user_accept=True) if sent_type else Q(org_accept=True),
            'reject': Q(user_accept=False) if sent_type else Q(org_accept=False),
            'unknown': Q(user_accept=None) if sent_type else Q(org_accept=None),
        }
        return queryset.filter(decision_filter[value])


class OfferUserFilter(django_filters.FilterSet):
    TYPE_CHOICES = (
        ('sent', 'Отправленные'),
        ('received', 'Полученные'),
    )
    DECISION_CHOICES = (
        ('accept', 'Принятые'),
        ('reject', 'Отклоненные'),
        ('unknown', 'На рассмотрении'),
    )

    can_accept = django_filters.BooleanFilter('can_accept',)
    can_reject = django_filters.BooleanFilter('can_reject',)

    type = django_filters.ChoiceFilter(
        method='type_filter',
        choices=TYPE_CHOICES,
        label='type',
    )

    decision = django_filters.ChoiceFilter(
        method='decision_filter',
        choices=DECISION_CHOICES,
        label='decision',
    )

    class Meta:
        model = Offer
        fields = ('user_accept',)

    def type_filter(self, queryset, name, value):
        if value == 'sent':
            return queryset.filter(created_by=F('user'))
        elif value == 'received':
            return queryset.filter(~Q(created_by=F('user')))
        return queryset

    def decision_filter(self, queryset, name, value):
        offer_type = self.data.get('type')
        if offer_type not in ['sent', 'received']:
            return queryset
        if value not in ['accept', 'reject', 'unknown']:
            return queryset

        sent_type = bool(offer_type == 'sent')
        decision_filter = {
            'accept': Q(user_accept=True) if sent_type else Q(org_accept=True),
            'reject': Q(user_accept=False) if sent_type else Q(org_accept=False),
            'unknown': Q(user_accept=None) if sent_type else Q(org_accept=None),
        }
        return queryset.filter(decision_filter[value])