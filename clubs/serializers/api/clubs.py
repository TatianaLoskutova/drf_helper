import pdb

from crum import get_current_user
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ParseError

from clubs.models.clubs import Club
from common.serializers.mixins import ExtendedModelSerializer
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


class ClubListSerializer(ExtendedModelSerializer):
    director = UserShortSerializer()

    class Meta:
        model = Club
        fields = '__all__'


class ClubRetrieveSerializer(ExtendedModelSerializer):
    director = UserShortSerializer()

    class Meta:
        model = Club
        fields = '__all__'


class ClubCreateSerializer(ExtendedModelSerializer):
    class Meta:
        model = Club
        fields = ('id', 'name')


class ClubUpdateSerializer(ExtendedModelSerializer):
    class Meta:
        model = Club
        fields = ('id', 'name')
