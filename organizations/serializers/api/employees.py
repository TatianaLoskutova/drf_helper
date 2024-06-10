from crum import get_current_user
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from organizations.constants import MANAGER_POSITION
from organizations.models.organizations import Organization, Employee
from organizations.models.dicts import Position
from organizations.serializers.nested.dicts import PositionShortSerializer
from common.serializers.mixins import ExtendedModelSerializer
from users.serializers.nested.users import UserEmployeeSerializer

User = get_user_model()


class EmployeeSearchSerializer(ExtendedModelSerializer):
    user = UserEmployeeSerializer()
    position = PositionShortSerializer()

    class Meta:
        model = Employee
        fields = (
            'id',
            'position',
            'user',
        )


class EmployeeListSerializer(ExtendedModelSerializer):
    user = UserEmployeeSerializer()
    position = PositionShortSerializer()

    class Meta:
        model = Employee
        fields = (
            'id',
            'date_joined',
            'user',
            'position',
        )


class EmployeeRetrieveSerializer(ExtendedModelSerializer):
    user = UserEmployeeSerializer()
    position = PositionShortSerializer()

    class Meta:
        model = Employee
        fields = (
            'id',
            'date_joined',
            'user',
            'position',
        )


class EmployeeCreateSerializer(ExtendedModelSerializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
            'position',
        )

    def validate(self, attrs):
        current_user = get_current_user()

        organization_id = self.context['view'].kwargs.get('pk')
        organization = Organization.objects.filter(
            id=organization_id, director=current_user
        ).first()
        if not organization:
            raise ParseError(
                'Такой организации не найдено'
            )
        attrs['organization'] = organization

        return attrs

    def create(self, validated_data):
        user_data = {
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
            'email': validated_data.pop('email'),
            'password': validated_data.pop('password'),
            'is_corporate_account': True,
        }

        with transaction.atomic():
            user = User.objects.create_user(**user_data)
            validated_data['user'] = user
            instance = super().create(validated_data)
        return instance


class EmployeeUpdateSerializer(ExtendedModelSerializer):
    position = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.filter(is_active=True)
    )

    class Meta:
        model = Employee
        fields = (
            'position',
        )

    def validate(self, attrs):
        if self.instance.is_director:
            raise ParseError(
                'Руководитель организации недоступен для изменений.'
            )
        return attrs

    def validate_position(self, value):
        if value.code == MANAGER_POSITION:
            if self.instance.is_chief:
                employee_departments = self.instance.departments_chiefs.values_list('name', flat=True)
                if employee_departments:
                    error_department_text = ', '.join(employee_departments)
                    raise ParseError(
                        f'Невозможно сменить должность. Сотрудник является '
                        f'начальником в следующих отделах:  {error_department_text}.'
                    )
        return value


class EmployeeDeleteSerializer(serializers.Serializer):

    def validate(self, attrs):
        if self.instance.is_director:
            raise ParseError(
                'невозможно удалить руководителя из организации.'
            )
        departments_as_member = self.instance.departments_members.values_list('name', flat=True)
        departments_as_chief = self.instance.departments_chiefs.values_list('name', flat=True)
        departments_exists = set(departments_as_member).union(set(departments_as_chief))
        if departments_exists:
            error_department_text = ', '.join(list(departments_exists))
            raise ParseError(
                f'Удаление невозможно. Сотрудник находится в следующих отделах '
                f'начальником в следующих отделах:  {error_department_text}.'
            )

        return attrs
