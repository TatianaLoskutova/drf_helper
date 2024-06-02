import django_filters

from clubs.models.clubs import Club, Player
from clubs.models.groups import Group


class ClubFilter(django_filters.FilterSet):
    can_manage = django_filters.BooleanFilter('can_manage', label='Can manage')

    class Meta:
        model = Club
        fields = ('can_manage', 'id',)


class PlayerFilter(django_filters.FilterSet):
    only_corporate = django_filters.BooleanFilter(
        'user__is_corporate_account', label='Is corporate account'
    )

    class Meta:
        model = Player
        fields = ('only_corporate',)


class GroupFilter(django_filters.FilterSet):
    is_member = django_filters.BooleanFilter('is_member',)

    class Meta:
        model = Group
        fields = ('club', 'trainer', 'is_member')
