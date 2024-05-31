from common.serializers.mixins import DictMixinSerializer
from clubs.models.dicts import Position


class PositionShortSerializer(DictMixinSerializer):
    class Meta:
        model = Position
