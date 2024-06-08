from crum import get_current_user
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from clubs.models.clubs import Club
from clubs.models.groups import Group
from clubs.serializers.nested.clubs import ClubShortSerializer
from common.serializers.mixins import ExtendedModelSerializer, \
    InfoModelSerializer
from users.serializers.nested.users import UserShortSerializer

User = get_user_model()


class GroupListSerializer(InfoModelSerializer):
    club = ClubShortSerializer()
    trainer = UserShortSerializer()
    pax = serializers.IntegerField()
    can_manage = serializers.BooleanField()
    is_member = serializers.BooleanField()

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'trainer',
            'club',
            'pax',
            'created_at',
            'can_manage',
            'is_member',
        )


class GroupRetrieveSerializer(InfoModelSerializer):
    club = ClubShortSerializer()
    trainer = UserShortSerializer()
    pax = serializers.IntegerField()
    can_manage = serializers.BooleanField()
    is_member = serializers.BooleanField()

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'club',
            'trainer',
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
            'trainer',
            'name',
        )
        extra_kwargs = {
            'trainer': {'required': False, 'allow_null': True, },
        }

    def validate_club(self, value):
        user = get_current_user()
        if value not in Club.objects.filter(director=user,):
            return ParseError(
                'Клуб выбран неверно.'
            )
        return value

    def validate(self, attrs):
        org = attrs['club']

        # specified trainer or club director
        attrs['trainer'] = attrs.get('trainer') or org.director_player
        trainer = attrs['trainer']
        # Check trainer
        if trainer not in org.players_info.all():
            raise ParseError(
                'Администратором может быть только тренер клуба или руководитель.'
            )
        # Check name duplicate
        if self.Meta.model.objects.filter(
                club=org, name=attrs['name']
        ).exists():
            raise ParseError(
                'Группа с таким названием уже существует.'
            )
        return attrs


class GroupUpdateSerializer(ExtendedModelSerializer):

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'members',
        )

    def validate(self, attrs):
        # Check name duplicate
        if self.instance.club.groups.filter(name=attrs['name']).exists():
            raise ParseError(
                'Группа с таким названием уже существует.'
            )
        return attrs
