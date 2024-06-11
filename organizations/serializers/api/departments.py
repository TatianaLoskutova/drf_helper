from crum import get_current_user
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from organizations.models.organizations import Organization
from organizations.models.departments import Department
from organizations.serializers.nested.organizations import OrganizationShortSerializer
from organizations.serializers.nested.employees import EmployeeShortSerializer
from common.serializers.mixins import ExtendedModelSerializer, \
    InfoModelSerializer
from vacations.serializers.nested.watches import VacationSettingsSerializer

User = get_user_model()


class DepartmentListSerializer(InfoModelSerializer):
    organization = OrganizationShortSerializer()
    chief = EmployeeShortSerializer()
    pax = serializers.IntegerField()
    can_manage = serializers.BooleanField()
    is_member = serializers.BooleanField()

    class Meta:
        model = Department
        fields = (
            'id',
            'name',
            'chief',
            'organization',
            'pax',
            'created_at',
            'can_manage',
            'is_member',
        )


class DepartmentRetrieveSerializer(InfoModelSerializer):
    vacations_info = VacationSettingsSerializer(allow_null=True)
    organization = OrganizationShortSerializer()
    chief = EmployeeShortSerializer()
    pax = serializers.IntegerField()
    can_manage = serializers.BooleanField()
    is_member = serializers.BooleanField()

    class Meta:
        model = Department
        fields = (
            'id',
            'vacations_info',
            'name',
            'organization',
            'chief',
            'pax',
            'created_at',
            'can_manage',
            'is_member',
        )


class DepartmentCreateSerializer(ExtendedModelSerializer):
    class Meta:
        model = Department
        fields = (
            'id',
            'organization',
            'chief',
            'name',
        )
        extra_kwargs = {
            'chief': {'required': False, 'allow_null': True, },
        }

    def validate_organization(self, value):
        user = get_current_user()
        if value not in Organization.objects.filter(director=user,):
            return ParseError(
                'Организация выбрана неверно.'
            )
        return value

    def validate(self, attrs):
        org = attrs['organization']

        # specified chief or organization director
        attrs['chief'] = attrs.get('chief') or org.director_employee
        chief = attrs['chief']
        # Check chief
        if chief not in org.employees_info.all():
            raise ParseError(
                'Администратором может быть только начальник или руководитель.'
            )
        # Check name duplicate
        if self.Meta.model.objects.filter(
                organization=org, name=attrs['name']
        ).exists():
            raise ParseError(
                'Отдел с таким названием уже существует.'
            )
        return attrs


class DepartmentUpdateSerializer(ExtendedModelSerializer):

    class Meta:
        model = Department
        fields = (
            'id',
            'name',
            'members',
        )

    def validate(self, attrs):
        # Check name duplicate
        if self.instance.organization.departments.filter(name=attrs['name'])\
                .exists():
            raise ParseError(
                'Отдел с таким названием уже существует.'
            )
        return attrs


class DepartmentSettingsUpdateSerializer(ExtendedModelSerializer):
    vacations_info = VacationSettingsSerializer()

    class Meta:
        model = Department
        fields = (
            'id',
            'vacations_info',
        )

    def update(self, instance, validated_data):
        with transaction.atomic():
            for key, value in validated_data.items():
                self._update_department_profile(key, value)
        return instance

    def _update_department_profile(self, param, validated_data):
        if param in self.fields:
            serializer = self.fields[param]
            instance, c = serializer.Meta.model.objects.get_or_create(
                department_id=self.get_from_url('pk')
            )
            serializer.update(instance, validated_data)
        return
