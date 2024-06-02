from crum import get_current_user
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from clubs.models.clubs import Club, Player
from clubs.serializers.nested.dicts import PositionShortSerializer
from common.serializers.mixins import ExtendedModelSerializer
from users.serializers.nested.users import UserPlayerSerializer

User = get_user_model()


class PlayerListSerializer(ExtendedModelSerializer):
    user = UserPlayerSerializer()
    position = PositionShortSerializer()

    class Meta:
        model = Player
        fields = (
            'id',
            'date_joined',
            'user',
            'position',
        )


class PlayerRetrieveSerializer(ExtendedModelSerializer):
    user = UserPlayerSerializer()
    position = PositionShortSerializer()

    class Meta:
        model = Player
        fields = (
            'id',
            'date_joined',
            'user',
            'position',
        )


class PlayerCreateSerializer(ExtendedModelSerializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Player
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
            'position',
        )

    def validate(self, attrs):
        current_user = get_current_user()

        club_id = self.context['view'].kwargs.get('pk')
        club = Club.objects.filter(
            id=club_id, director=current_user
        ).first()
        if not club:
            raise ParseError(
                'Такого клуба не найдено'
            )
        attrs['club'] = club

        return attrs

    def create(self, validated_data):
        user_data = {
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
            'email': validated_data.pop('email'),
            'password': validated_data.pop('password'),
            'is_corporate_account': True,
        }

        with transaction.atomic():
            user = User.objects.create_user(**user_data)
            validated_data['user'] = user
            instance = super().create(validated_data)
        return instance


class PlayerUpdateSerializer(ExtendedModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'
