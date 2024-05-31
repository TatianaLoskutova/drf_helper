from clubs.models.clubs import Club
from common.serializers.mixins import ExtendedModelSerializer


class ClubSearchListSerializer(ExtendedModelSerializer):
    directors = ser
    class Meta:
        model = Club
        fields = (
            'id',
            'name',
            'director',
        )
