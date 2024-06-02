from django.contrib.auth import get_user_model
from rest_framework import serializers

from common.serializers.mixins import ExtendedModelSerializer, \
    InfoModelSerializer
from clubs.models.groups import Group
from users.serializers.nested.users import UserShortSerializer
from crum import get_current_user
from rest_framework.exceptions import ParseError
from clubs.models.clubs import Club

User = get_user_model()


class GroupListSerializer(InfoModelSerializer):
    pax = serializers.IntegerField()
    can_manage = serializers.BooleanField()
    is_member = serializers.BooleanField()

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'pax',
            'created_at',
            'can_manage',
            'is_member',
        )


class GroupRetrieveSerializer(InfoModelSerializer):
    pax = serializers.IntegerField()
    can_manage = serializers.BooleanField()
    is_member = serializers.BooleanField()

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'pax',
            'created_at',
            'can_manage',
            'is_member',
        )


class GroupCreateSerializer(ExtendedModelSerializer):
    class Meta:
        model = Group
        fields = (
            'id',
            'club',
            'name',
            'members_info',
        )

    def validate_organisation(self, value):
        user = get_current_user()
        if value not in Club.objects.filter(director=user,):
            return ParseError(
                'Организация выбрана ошибочно.'
            )
        return value


class GroupUpdateSerializer(ExtendedModelSerializer):

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'members',
        )
