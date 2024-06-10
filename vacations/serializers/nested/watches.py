from vacations.models.watches import DepartmentInfo
from common.serializers.mixins import ExtendedModelSerializer


class VacationSettingsSerializer(ExtendedModelSerializer):
    class Meta:
        model = DepartmentInfo
        exclude = ('department',)
