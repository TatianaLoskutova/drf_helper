from crum import get_current_user
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from clubs.constants import PLAYER_POSITION, TRAINER_POSITION, DIRECTOR_POSITION
from clubs.models.clubs import Club, Player
from clubs.models.dicts import Position
from clubs.serializers.nested.dicts import PositionShortSerializer
from common.serializers.mixins import ExtendedModelSerializer
from users.serializers.nested.users import UserPlayerSerializer

User = get_user_model()


class PlayerSearchSerializer(ExtendedModelSerializer):
    user = UserPlayerSerializer()
    position = PositionShortSerializer()

    class Meta:
        model = Player
        fields = (
            'id',
            'position',
            'user',
        )


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
    position = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.filter(is_active=True)
    )

    class Meta:
        model = Player
        fields = (
            'position',
        )

    def validate(self, attrs):
        if self.instance.is_director:
            raise ParseError(
                'Руководитель клуба недоступен для изменений.'
            )
        return attrs

    def validate_position(self, value):
        if value.code == PLAYER_POSITION:
            if self.instance.is_trainer:
                player_groups = self.instance.groups_trainers.values_list('name', flat=True)
                if player_groups:
                    error_group_text = ', '.join(player_groups)
                    raise ParseError(
                        f'Невозможно сменить должность. Игрок является '
                        f'тренером в следующих группах:  {error_group_text}.'
                    )
        return value


class PlayerDeleteSerializer(serializers.Serializer):

    def validate(self, attrs):
        if self.instance.is_director:
            raise ParseError(
                'невозможно удалить руководителя из клуба.'
            )
        groups_as_member = self.instance.groups_members.values_list('name', flat=True)
        groups_as_trainer = self.instance.groups_trainers.values_list('name', flat=True)
        groups_exists = set(groups_as_member).union(set(groups_as_trainer))
        if groups_exists:
            error_group_text = ', '.join(list(groups_exists))
            raise ParseError(
                f'Удаление невозможно. Игрок находится в следующих группах '
                f'тренером в следующих группах:  {error_group_text}.'
            )

        return attrs
