from django.contrib.auth import get_user_model
from django.db import models

from common.models.mixins import InfoMixin

User = get_user_model()


class DepartmentInfo(models.Model):
    department = models.OneToOneField(
        'organizations.department', models.CASCADE, related_name='vacations_info',
        verbose_name='Отдел', primary_key=True,
    )
    min_active_employees = models.PositiveSmallIntegerField(
        'Мин. число активных сотрудников', blank=True, null=True,
    )
    vacation_start = models.TimeField('Начало отпуска', blank=True, null=True,)
    vacation_end = models.TimeField('Окончание отпуска', blank=True, null=True,)
    vacation_max_duration = models.PositiveSmallIntegerField(
        'Макс. длительность отпуска', blank=True, null=True,
    )

    class Meta:
        verbose_name = 'Параметр отдела'
        verbose_name_plural = 'Параметры отделов'

    def __str__(self):
        return f'vacation Info'


class Watch(InfoMixin):
    department = models.ForeignKey(
        'vacations.DepartmentInfo', models.CASCADE, 'watches',
        verbose_name='Группа',
    )
    # todo  дату надо понять как назвать
    date = models.DateField('Дата xxx')
    vacation_start = models.TimeField('Начало отпуска', blank=True, null=True,)
    vacation_end = models.TimeField('Окончание отпуска', blank=True, null=True,)
    vacation_max_duration = models.PositiveSmallIntegerField(
        'Макс. длительность отпуска', blank=True, null=True,
    )
    min_active = models.PositiveSmallIntegerField(
        'Мин. число активных сотрудников', null=True, blank=True,
    )
    members = models.ManyToManyField(
        'organizations.Member', related_name='watches',
        verbose_name='Сотрудники на смене', through='WatchMember'
    )

    class Meta:
        verbose_name = 'Смена'
        verbose_name_plural = 'Смены'
        ordering = ('-date',)

    def __str__(self):
        return f'Смена №{self.pk} для {self.department})'


class WatchMember(models.Model):
    member = models.ForeignKey(
        'organizations.Member', models.CASCADE, 'watches_info',
        verbose_name='Участник смены',
    )
    watch = models.ForeignKey(
        'vacations.watch', models.CASCADE, 'members_info',
        verbose_name='Смена',
    )
    status = models.ForeignKey(
        'vacations.watchStatus', models.RESTRICT, 'members',
        verbose_name='Статус смены',
    )

    class Meta:
        verbose_name = 'Смена - участник смены'
        verbose_name_plural = 'Смены - участники смены'

    def __str__(self):
        return f'Участник смены {self.member.employee.user} ({self.pk})'
