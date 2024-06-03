from common.serializers.mixins import ExtendedModelSerializer
from clubs.models.clubs import Club


class ClubShortSerializer(ExtendedModelSerializer):
    class Meta:
        model = Club
        fields = (
            'id',
            'name',
        )
