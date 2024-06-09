from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from common.serializers.mixins import ExtendedModelSerializer

from clubs.models.groups import Member, Group
from clubs.models.clubs import Player
from clubs.serializers.nested.dicts import PositionShortSerializer
from clubs.serializers.nested.players import PlayerShortSerializer

User = get_user_model()


class MemberSearchSerializer(ExtendedModelSerializer):
    full_name = serializers.CharField(source='player.user.full_name')
    username = serializers.CharField(source='player.user.username')
    position = PositionShortSerializer(source='player.position')

    class Meta:
        model = Member
        fields = (
            'id',
            'full_name',
            'username',
            'position',
        )


class MemberListSerializer(ExtendedModelSerializer):
    player = PlayerShortSerializer()

    class Meta:
        model = Member
        fields = (
            'id',
            'player',
            'date_joined',
        )


class MemberRetrieveSerializer(ExtendedModelSerializer):
    player = PlayerShortSerializer()

    class Meta:
        model = Member
        fields = (
            'id',
            'player',
            'date_joined',
        )


class MemberCreateSerializer(ExtendedModelSerializer):
    players = serializers.PrimaryKeyRelatedField(
        queryset=Player.objects.all(), many=True, write_only=True
    )

    class Meta:
        model = Member
        fields = (
            'id',
            'players',
        )

    def validate(self, attrs):
        try:
            group = self.get_object_from_url(Group)
            club = group.club
        except:
            raise ParseError('Ой, что-то не так. Текущий клуб не найден.')

        attrs['group'] = group

        players = attrs['players']
        players_id_set = {obj.pk for obj in players}

        club_players = club.employees_info.all()
        club_players_id_set = {obj.pk for obj in club_players}

        # Check players from request exist in club
        if players_id_set - club_players_id_set:
            raise ParseError(
                'Некоторые из указанных игроков не существуют в клубе. '
                'Проверьте введенные данные.'
            )

        return attrs

    def create(self, validated_data):
        players = validated_data.pop('players')
        group = validated_data.pop('group')
        group.members.set(players)
        return group
