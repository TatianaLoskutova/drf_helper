from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from crum import get_current_user
from clubs.constants import DIRECTOR_POSITION
from clubs.models.clubs import Club
from common.serializers.mixins import ExtendedModelSerializer, \
    InfoModelSerializer
from users.serializers.nested.users import UserShortSerializer
from rest_framework.exceptions import ParseError

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

    def validate_name(self, value):
        if self.Meta.model.objects.filter(name=value):
            raise ParseError(
                'Клуб с таким названием уже существует'
            )
        return value

    def validate(self, attrs):
        user = get_current_user()
        attrs['director'] = user
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            instance = super().create(validated_data)
            instance.players.add(
                validated_data['director'],
                through_defaults={'position_id': DIRECTOR_POSITION, }
            )
        return instance


class ClubUpdateSerializer(ExtendedModelSerializer):
    class Meta:
        model = Club
        fields = ('id', 'name')
