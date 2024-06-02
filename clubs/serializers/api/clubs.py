from django.contrib.auth import get_user_model
from rest_framework import serializers

from clubs.models.clubs import Club
from common.serializers.mixins import ExtendedModelSerializer, \
    InfoModelSerializer
from users.serializers.nested.users import UserShortSerializer

User = get_user_model()


class ClubSearchListSerializer(ExtendedModelSerializer):
    director = UserShortSerializer()

    class Meta:
        model = Club
        fields = (
            'id',
            'name',
            'director',
        )


class ClubListSerializer(InfoModelSerializer):
    director = UserShortSerializer()
    pax = serializers.IntegerField()
    groups_count = serializers.IntegerField()
    can_manage = serializers.BooleanField()

    class Meta:
        model = Club
        fields = (
            'id',
            'name',
            'director',
            'pax',
            'groups_count',
            'created_at',
            'can_manage',
        )


class ClubRetrieveSerializer(InfoModelSerializer):
    director = UserShortSerializer()
    pax = serializers.IntegerField()
    groups_count = serializers.IntegerField()
    can_manage = serializers.BooleanField()

    class Meta:
        model = Club
        fields = (
            'id',
            'name',
            'director',
            'pax',
            'groups_count',
            'created_at',
            'can_manage',
        )


class ClubCreateSerializer(ExtendedModelSerializer):
    class Meta:
        model = Club
        fields = ('id', 'name')


class ClubUpdateSerializer(ExtendedModelSerializer):
    class Meta:
        model = Club
        fields = ('id', 'name')
