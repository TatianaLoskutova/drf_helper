from common.serializers.mixins import ExtendedModelSerializer
from clubs.models.groups import Group
from clubs.serializers.nested.players import PlayerShortSerializer
from clubs.serializers.nested.clubs import \
    ClubShortSerializer


class GroupShortSerializer(ExtendedModelSerializer):
    club = ClubShortSerializer()
    trainer = PlayerShortSerializer()

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'club',
            'trainer',
        )
