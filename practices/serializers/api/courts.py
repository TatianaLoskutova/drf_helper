from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from clubs.models.groups import Group, Member
from clubs.serializers.nested.groups import GroupShortSerializer
from common.serializers.mixins import InfoModelSerializer
from practices.models.courts import Court, GroupInfo
from practices.serializers.internal.courts import CourtStatsSerializer

User = get_user_model()


class CourtListSerializer(InfoModelSerializer):
    group = GroupShortSerializer(source='group.group')
    stats = CourtStatsSerializer(source='*')

    class Meta:
        model = Court
        fields = (
            'id',
            'group',
            'date',
            'training_start',
            'training_end',
            'training_max_duration',
            'min_active',
            'stats',
        )


class CourtRetrieveSerializer(InfoModelSerializer):
    group = GroupShortSerializer(source='group.group')
    stats = CourtStatsSerializer(source='*')

    class Meta:
        model = Court
        fields = (
            'id',
            'group',
            'date',
            'training_start',
            'training_end',
            'training_max_duration',
            'min_active',
            'stats',
        )


class CourtCreateSerializer(InfoModelSerializer):
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all()
    )
    members = serializers.PrimaryKeyRelatedField(
        queryset=Member.objects.all(), many=True, allow_null=True,
        required=False,
    )
    all_group_members = serializers.BooleanField(default=False)
    remember_default_data = serializers.BooleanField(default=False)

    class Meta:
        model = Court
        fields = (
            'id',
            'group',
            'date',
            'training_start',
            'training_end',
            'training_max_duration',
            'min_active',
            'members',
            'all_group_members',
            'remember_default_data',
        )
        extra_kwargs = {
            'training_start': {'required': False, 'allow_null': True},
            'training_end': {'required': False, 'allow_null': True},
            'training_max_duration': {'required': False, 'allow_null': True},
            'min_active': {'required': False, 'allow_null': True},
        }

    def create(self, validated_data):
        remember_data = validated_data.pop('remember_default_data', False)
        all_group_members = validated_data.pop('all_group_members', False)

        with transaction.atomic():
            if hasattr(validated_data['group'], 'trainings_info'):
                validated_data['group'] = validated_data['group'].trainings_info
            else:
                validated_data['group'] = GroupInfo.objects.create(
                    group=validated_data['group'],
                )

            if all_group_members:
                validated_data.pop('members', list())
                members = validated_data['group'].group.members_info.all()
            else:
                members = validated_data.pop('members')
            instance = super().create(validated_data)

            instance.members.set(members)

            if remember_data:
                defaults = {
                    'training_start': validated_data['training_start'],
                    'training_end': validated_data['training_end'],
                    'training_max_duration': validated_data['training_max_duration'],
                    'min_active': validated_data['min_active'],
                }
                group = instance.group
                for key, value in defaults.items():
                    setattr(group, key, value)
                group.save()

            return instance

    def validate(self, attrs):

        # Check params
        required_fields = (
            'training_start', 'training_end', 'training_max_duration',
            'min_active',
        )
        for field in required_fields:
            try:
                from_default = getattr(attrs['group'].trainings_info, field)
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
        if attrs.get('training_start') and attrs.get('training_end'):
            if attrs.get('training_start') >= attrs.get('training_end'):
                raise ParseError(
                    'Время начала тренировки должно быть меньше времени окончания.'
                )

        # Check duplicates
        if self.Meta.model.objects.filter(
            group_id=attrs['group'].pk, date=attrs['date']
        ).exists():
            raise ParseError(
                'На этот день уже существует тренировка.'
            )
        return attrs

    def validate_group(self, value):
        my_groups = Group.objects.my_groups_admin()
        if value not in my_groups:
            raise ParseError(
                'У вас нет полномочий создавать смены в этой группе.'
            )
        return value

    def validate_date(self, value):
        now = timezone.now().date()
        if value < now:
            raise ParseError(
                'Дата тренировки должна быть больше или равна текущей дате.'
            )
        return value

    def validate_training_start(self, value):
        if value.minute % 15 > 0:
            raise ParseError(
                'Время начала тренировки должно быть кратно 15 минутам.'
            )
        return value

    def validate_training_end(self, value):
        if value.minute % 15 > 0:
            raise ParseError(
                'Время окончания тренировки должно быть кратно 15 минутам.'
            )
        return value


class CourtUpdateSerializer(InfoModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        queryset=Member.objects.all(), many=True, allow_null=True,
        required=False,
    )
    all_group_members = serializers.BooleanField(default=False)
    remember_default_data = serializers.BooleanField(default=False)

    class Meta:
        model = Court
        fields = (
            'id',
            'date',
            'training_start',
            'training_end',
            'training_max_duration',
            'min_active',
            'members',
            'all_group_members',
            'remember_default_data',
        )

    def update(self, instance, validated_data):
        remember_data = validated_data.pop('remember_default_data', False)
        all_group_members = validated_data.pop('all_group_members', False)

        with transaction.atomic():
            if all_group_members:
                validated_data.pop('members', list())
                members = self.instance.group.members_info.all()
            else:
                members = validated_data.pop('members', None)
            instance = super().update(instance, validated_data)

            if members:
                instance.members.set(members)

            if remember_data:
                defaults = {
                    'training_start': (
                            validated_data.get('training_start')
                            or self.instance.training_start
                    ),
                    'training_end': (
                            validated_data.get('training_end')
                            or self.instance.training_end
                    ),
                    'training_max_duration': (
                            validated_data.get('training_max_duration')
                            or self.instance.training_max_duration
                    ),
                    'min_active': (
                            validated_data.get('min_active')
                            or self.instance.min_active
                    ),
                }
                group = instance.group
                for key, value in defaults.items():
                    setattr(group, key, value)
                group.save()

            return instance

    def validate(self, attrs):
        # Check times
        if attrs.get('training_start') and attrs.get('training_end'):
            if attrs.get('training_start') >= attrs.get('training_end'):
                raise ParseError(
                    'Время начала тренировки должно быть меньше времени окончания.'
                )
        # Check duplicates
        if attrs.get('date') and self.Meta.model.objects.filter(
                group_id=self.instance.group.pk, date=attrs['date']
        ).exists():
            raise ParseError(
                'На этот день уже корт забронирован.'
            )
        return attrs

    def validate_date(self, value):
        now = timezone.now().date()
        if value < now:
            raise ParseError(
                'Дата корта должна быть больше или равна текущей дате.'
            )
        return value

    def validate_training_start(self, value):
        if value.minute % 15 > 0:
            raise ParseError(
                'Время начала тренировки должно быть кратно 15 минутам.'
            )
        return value

    def validate_training_end(self, value):
        if value.minute % 15 > 0:
            raise ParseError(
                'Время окончания тренировки должно быть кратно 15 минутам.'
            )
        return value
