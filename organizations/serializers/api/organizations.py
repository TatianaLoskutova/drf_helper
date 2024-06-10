from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from crum import get_current_user
from organizations.constants import DIRECTOR_POSITION
from organizations.models.organizations import Organization
from common.serializers.mixins import ExtendedModelSerializer, \
    InfoModelSerializer
from users.serializers.nested.users import UserShortSerializer
from rest_framework.exceptions import ParseError

User = get_user_model()


class OrganizationSearchListSerializer(ExtendedModelSerializer):
    director = UserShortSerializer()

    class Meta:
        model = Organization
        fields = (
            'id',
            'name',
            'director',
        )


class OrganizationListSerializer(InfoModelSerializer):
    director = UserShortSerializer()
    pax = serializers.IntegerField()
    departments_count = serializers.IntegerField()
    can_manage = serializers.BooleanField()

    class Meta:
        model = Organization
        fields = (
            'id',
            'name',
            'director',
            'pax',
            'departments_count',
            'created_at',
            'can_manage',
        )


class OrganizationRetrieveSerializer(InfoModelSerializer):
    director = UserShortSerializer()
    pax = serializers.IntegerField()
    departments_count = serializers.IntegerField()
    can_manage = serializers.BooleanField()

    class Meta:
        model = Organization
        fields = (
            'id',
            'name',
            'director',
            'pax',
            'departments_count',
            'created_at',
            'can_manage',
        )


class OrganizationCreateSerializer(ExtendedModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'name')

    def validate_name(self, value):
        if self.Meta.model.objects.filter(name=value):
            raise ParseError(
                'Организация с таким названием уже существует'
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


class OrganizationUpdateSerializer(ExtendedModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'name')
