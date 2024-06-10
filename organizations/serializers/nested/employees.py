from organizations.models.organizations import Employee
from organizations.serializers.nested.dicts import PositionShortSerializer
from common.serializers.mixins import ExtendedModelSerializer
from users.serializers.nested.users import UserShortSerializer


class EmployeeShortSerializer(ExtendedModelSerializer):
    user = UserShortSerializer()
    position = PositionShortSerializer()

    class Meta:
        fields = (
            'id',
            'user',
            'position',
        )
        model = Employee
