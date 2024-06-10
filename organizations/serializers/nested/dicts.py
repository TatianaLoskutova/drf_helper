from common.serializers.mixins import DictMixinSerializer
from organizations.models.dicts import Position


class PositionShortSerializer(DictMixinSerializer):
    class Meta:
        model = Position
