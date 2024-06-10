from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from organizations.chiefs.departments import DepartmentChief
from common.models.mixins import InfoMixin

User = get_user_model()


class Department(InfoMixin):
    organization = models.ForeignKey(
        'Organization', models.CASCADE, 'departments',
        verbose_name='Организация',
    )
    name = models.CharField('Название', max_length=255)
    chief = models.ForeignKey(
        'Employee', models.RESTRICT, 'department_chief',
        verbose_name='Начальник',
    )
    members = models.ManyToManyField(
        'Employee', 'department_members', verbose_name='Сотрудники отдела',
        blank=True, through='Member',
    )

    objects = DepartmentChief()

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} ({self.pk})'


class Member(models.Model):
    department = models.ForeignKey(
        'department', models.CASCADE, 'members_info',
    )
    employee = models.ForeignKey(
        'employee', models.CASCADE, 'departments_info',
    )
    date_joined = models.DateField('Date joined', default=timezone.now)

    class Meta:
        verbose_name = 'Сотрудник отдела'
        verbose_name_plural = 'Сотрудники отдела'
        ordering = ('-date_joined',)
        unique_together = (('department', 'employee'),)

    def __str__(self):
        return f'Member {self.employee}'
