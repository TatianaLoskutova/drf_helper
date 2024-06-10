from django.contrib.auth import get_user_model
from django.db import models

from vacations.constants import VACATION_CREATED_DEFAULT, \
    VACATION_CREATED_STATUS
from vacations.models.dicts import VacationStatus

User = get_user_model()


class Vacation(models.Model):
    watch = models.ForeignKey(
        'vacations.Watch', models.CASCADE, 'vacations',
        verbose_name='Смена',
    )
    employee = models.ForeignKey(
        User, models.CASCADE, 'vacations',
        verbose_name='Сотрудник',
    )
    member = models.ForeignKey(
        'organizations.Member', models.CASCADE, 'vacations', verbose_name='Сотрудник отдела',
    )
    vacation_start = models.TimeField('Начало отпуска', blank=True, null=True,)
    vacation_end = models.TimeField('Окончание отпуска', blank=True, null=True,)
    status = models.ForeignKey(
        'vacations.VacationStatus', models.RESTRICT, 'vacations',
        verbose_name='Статус отпуска', blank=True,
    )

    class Meta:
        verbose_name = 'Отпуск'
        verbose_name_plural = 'Отпуска'
        ordering = ('-watch__date', 'vacation_start')

    def __str__(self):
        return f'Отпуск пользователя {self.employee} ({self.pk})'

    def save(self, *args, **kwargs):
        if not self.pk:
            status, created = VacationStatus.objects.get_or_create(
                code=VACATION_CREATED_STATUS,
                defaults=VACATION_CREATED_DEFAULT,
            )
            self.status = status
        return super().save(*args, **kwargs)
