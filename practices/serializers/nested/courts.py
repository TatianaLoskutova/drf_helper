from practices.models.courts import GroupInfo
from common.serializers.mixins import ExtendedModelSerializer


class TrainingSettingsSerializer(ExtendedModelSerializer):
    class Meta:
        model = GroupInfo
        exclude = ('group',)
