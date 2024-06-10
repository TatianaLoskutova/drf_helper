from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from common.serializers.mixins import ExtendedModelSerializer

from organizations.models.departments import Member, Department
from organizations.models.organizations import Employee
from organizations.serializers.nested.dicts import PositionShortSerializer
from organizations.serializers.nested.employees import EmployeeShortSerializer

User = get_user_model()


class MemberSearchSerializer(ExtendedModelSerializer):
    full_name = serializers.CharField(source='employee.user.full_name')
    username = serializers.CharField(source='employee.user.username')
    position = PositionShortSerializer(source='employee.position')

    class Meta:
        model = Member
        fields = (
            'id',
            'full_name',
            'username',
            'position',
        )


class MemberListSerializer(ExtendedModelSerializer):
    employee = EmployeeShortSerializer()

    class Meta:
        model = Member
        fields = (
            'id',
            'employee',
            'date_joined',
        )


class MemberRetrieveSerializer(ExtendedModelSerializer):
    employee = EmployeeShortSerializer()

    class Meta:
        model = Member
        fields = (
            'id',
            'employee',
            'date_joined',
        )


class MemberCreateSerializer(ExtendedModelSerializer):
    employees = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), many=True, write_only=True
    )

    class Meta:
        model = Member
        fields = (
            'id',
            'employees',
        )

    def validate(self, attrs):
        try:
            department = self.get_object_from_url(Department)
            organization = department.organization
        except:
            raise ParseError('Текущая организация не найдена.')

        attrs['department'] = department

        employees = attrs['employees']
        employees_id_set = {obj.pk for obj in employees}

        organization_employees = organization.employees_info.all()
        organization_employees_id_set = {obj.pk for obj in organization_employees}

        # Check employees from request exist in organization
        if employees_id_set - organization_employees_id_set:
            raise ParseError(
                'Некоторые из указанных сотрудников не существуют в организации. '
                'Проверьте введенные данные.'
            )

        return attrs

    def create(self, validated_data):
        employees = validated_data.pop('employees')
        department = validated_data.pop('department')
        department.members.set(employees)
        return department
