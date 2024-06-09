from clubs.models.clubs import Player
from clubs.serializers.nested.dicts import PositionShortSerializer
from common.serializers.mixins import ExtendedModelSerializer
from users.serializers.nested.users import UserShortSerializer


class PlayerShortSerializer(ExtendedModelSerializer):
    user = UserShortSerializer()
    position = PositionShortSerializer()

    class Meta:
        fields = (
            'id',
            'user',
            'position',
        )
        model = Player
