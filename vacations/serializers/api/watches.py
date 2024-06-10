from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from organizations.models.departments import Department, Member
from organizations.serializers.nested.departments import DepartmentShortSerializer
from common.serializers.mixins import InfoModelSerializer
from vacations.models.watches import Watch, DepartmentInfo
from vacations.serializers.internal.watches import WatchStatsSerializer

User = get_user_model()


class WatchListSerializer(InfoModelSerializer):
    department = DepartmentShortSerializer(source='department.department')
    stats = WatchStatsSerializer(source='*')

    class Meta:
        model = Watch
        fields = (
            'id',
            'department',
            'date',
            'vacation_start',
            'vacation_end',
            'vacation_max_duration',
            'min_active',
            'stats',
        )


class WatchRetrieveSerializer(InfoModelSerializer):
    department = DepartmentShortSerializer(source='department.department')
    stats = WatchStatsSerializer(source='*')

    class Meta:
        model = Watch
        fields = (
            'id',
            'department',
            'date',
            'vacation_start',
            'vacation_end',
            'vacation_max_duration',
            'min_active',
            'stats',
        )


class WatchCreateSerializer(InfoModelSerializer):
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all()
    )
    members = serializers.PrimaryKeyRelatedField(
        queryset=Member.objects.all(), many=True, allow_null=True,
        required=False,
    )
    all_department_members = serializers.BooleanField(default=False)
    remember_default_data = serializers.BooleanField(default=False)

    class Meta:
        model = Watch
        fields = (
            'id',
            'department',
            'date',
            'vacation_start',
            'vacation_end',
            'vacation_max_duration',
            'min_active',
            'members',
            'all_department_members',
            'remember_default_data',
        )
        extra_kwargs = {
            'vacation_start': {'required': False, 'allow_null': True},
            'vacation_end': {'required': False, 'allow_null': True},
            'vacation_max_duration': {'required': False, 'allow_null': True},
            'min_active': {'required': False, 'allow_null': True},
        }

    def create(self, validated_data):
        remember_data = validated_data.pop('remember_default_data', False)
        all_department_members = validated_data.pop('all_department_members', False)

        with transaction.atomic():
            if hasattr(validated_data['department'], 'vacations_info'):
                validated_data['department'] = validated_data['department'].vacations_info
            else:
                validated_data['department'] = DepartmentInfo.objects.create(
                    department=validated_data['department'],
                )

            if all_department_members:
                validated_data.pop('members', list())
                members = validated_data['department'].department.members_info.all()
            else:
                members = validated_data.pop('members')
            instance = super().create(validated_data)

            instance.members.set(members)

            if remember_data:
                defaults = {
                    'vacation_start': validated_data['vacation_start'],
                    'vacation_end': validated_data['vacation_end'],
                    'vacation_max_duration': validated_data['vacation_max_duration'],
                    'min_active': validated_data['min_active'],
                }
                department = instance.department
                for key, value in defaults.items():
                    setattr(department, key, value)
                department.save()

            return instance

    def validate(self, attrs):

        # Check params
        required_fields = (
            'vacation_start', 'vacation_end', 'vacation_max_duration',
            'min_active',
        )
        for field in required_fields:
            try:
                from_default = getattr(attrs['department'].vacations_info, field)
            except:
                from_default = None

            from_request = attrs.get(field)
            field_data = from_request or from_default

            if not field_data:
                field_name = getattr(self.Meta.model, field).field.verbose_name
                raise ParseError(
                    f'{field_name} - обязательное поле для заполнения.'
                )
            else:
                attrs[field] = field_data

        # Check times
        if attrs.get('vacation_start') and attrs.get('vacation_end'):
            if attrs.get('vacation_start') >= attrs.get('vacation_end'):
                raise ParseError(
                    'Время начала отпуска должно быть меньше времени окончания.'
                )

        # Check duplicates
        if self.Meta.model.objects.filter(
            department_id=attrs['department'].pk, date=attrs['date']
        ).exists():
            raise ParseError(
                'На этот день уже существует отпуск.'
            )
        return attrs

    def validate_department(self, value):
        my_departments = Department.objects.my_departments_admin()
        if value not in my_departments:
            raise ParseError(
                'У вас нет полномочий создавать смены в этом отделе.'
            )
        return value

    def validate_date(self, value):
        now = timezone.now().date()
        if value < now:
            raise ParseError(
                'Дата отпуска должна быть больше или равна текущей дате.'
            )
        return value

    def validate_vacation_start(self, value):
        if value.minute % 15 > 0:
            raise ParseError(
                'Время начала отпуска должно быть кратно 15 минутам.'
            )
        return value

    def validate_vacation_end(self, value):
        if value.minute % 15 > 0:
            raise ParseError(
                'Время окончания отпуска должно быть кратно 15 минутам.'
            )
        return value


class WatchUpdateSerializer(InfoModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        queryset=Member.objects.all(), many=True, allow_null=True,
        required=False,
    )
    all_department_members = serializers.BooleanField(default=False)
    remember_default_data = serializers.BooleanField(default=False)

    class Meta:
        model = Watch
        fields = (
            'id',
            'date',
            'vacation_start',
            'vacation_end',
            'vacation_max_duration',
            'min_active',
            'members',
            'all_department_members',
            'remember_default_data',
        )

    def update(self, instance, validated_data):
        remember_data = validated_data.pop('remember_default_data', False)
        all_department_members = validated_data.pop('all_department_members', False)

        with transaction.atomic():
            if all_department_members:
                validated_data.pop('members', list())
                members = self.instance.department.members_info.all()
            else:
                members = validated_data.pop('members', None)
            instance = super().update(instance, validated_data)

            if members:
                instance.members.set(members)

            if remember_data:
                defaults = {
                    'vacation_start': (
                            validated_data.get('vacation_start')
                            or self.instance.vacation_start
                    ),
                    'vacation_end': (
                            validated_data.get('vacation_end')
                            or self.instance.vacation_end
                    ),
                    'vacation_max_duration': (
                            validated_data.get('vacation_max_duration')
                            or self.instance.vacation_max_duration
                    ),
                    'min_active': (
                            validated_data.get('min_active')
                            or self.instance.min_active
                    ),
                }
                department = instance.department
                for key, value in defaults.items():
                    setattr(department, key, value)
                department.save()

            return instance

    def validate(self, attrs):
        # Check times
        if attrs.get('vacation_start') and attrs.get('vacation_end'):
            if attrs.get('vacation_start') >= attrs.get('vacation_end'):
                raise ParseError(
                    'Время начала отпуска должно быть меньше времени окончания.'
                )
        # Check duplicates
        if attrs.get('date') and self.Meta.model.objects.filter(
                department_id=self.instance.department.pk, date=attrs['date']
        ).exists():
            raise ParseError(
                'На этот день уже корт забронирован.'
            )
        return attrs

    def validate_date(self, value):
        now = timezone.now().date()
        if value < now:
            raise ParseError(
                'Дата смены должна быть больше или равна текущей дате.'
            )
        return value

    def validate_vacation_start(self, value):
        if value.minute % 15 > 0:
            raise ParseError(
                'Время начала отпуска должно быть кратно 15 минутам.'
            )
        return value

    def validate_vacation_end(self, value):
        if value.minute % 15 > 0:
            raise ParseError(
                'Время окончания отпуска должно быть кратно 15 минутам.'
            )
        return value
