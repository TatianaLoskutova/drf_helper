from common.serializers.mixins import ExtendedModelSerializer
from organizations.models.departments import Department
from organizations.serializers.nested.employees import EmployeeShortSerializer
from organizations.serializers.nested.organizations import \
    OrganizationShortSerializer


class DepartmentShortSerializer(ExtendedModelSerializer):
    organization = OrganizationShortSerializer()
    chief = EmployeeShortSerializer()

    class Meta:
        model = Department
        fields = (
            'id',
            'name',
            'organization',
            'chief',
        )
