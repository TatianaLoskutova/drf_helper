from django.contrib.auth import get_user_model
from django.db import models

from common.models.mixins import InfoMixin

User = get_user_model()


class GroupInfo(models.Model):
    group = models.OneToOneField(
        'clubs.Group', models.CASCADE, related_name='trainings_info',
        verbose_name='Группа', primary_key=True,
    )
    min_active_players = models.PositiveSmallIntegerField(
        'Мин. число активных игроков', blank=True, null=True,
    )
    training_start = models.TimeField('Начало тренировки', blank=True, null=True,)
    training_end = models.TimeField('Окончание тренировки', blank=True, null=True,)
    training_max_duration = models.PositiveSmallIntegerField(
        'Макс. длительность тренировки', blank=True, null=True,
    )

    class Meta:
        verbose_name = 'Параметры тренировочных групп'
        verbose_name_plural = 'Параметры тренировочных групп'

    def __str__(self):
        return f'{self.group}'


class Court(InfoMixin):
    group = models.ForeignKey(
        'practices.GroupInfo', models.CASCADE, 'courts',
        verbose_name='Группа',
    )
    date = models.DateField('Дата аренды корта')
    training_start = models.TimeField('Начало тренировки', blank=True, null=True,)
    training_end = models.TimeField('Окончание тренировки', blank=True, null=True,)
    training_max_duration = models.PositiveSmallIntegerField(
        'Макс. длительность тренировки', blank=True, null=True,
    )
    min_active = models.PositiveSmallIntegerField(
        'Мин. число активных игроков', null=True, blank=True,
    )
    members = models.ManyToManyField(
        'clubs.Member', related_name='courts',
        verbose_name='Участники смены', through='CourtMember'
    )

    class Meta:
        verbose_name = 'Корт'
        verbose_name_plural = 'Корты'
        ordering = ('-date',)

    def __str__(self):
        return f'Корт №{self.pk} для {self.group})'


class CourtMember(models.Model):
    member = models.ForeignKey(
        'clubs.Member', models.CASCADE, 'courts_info',
        verbose_name='Участник',
    )
    court = models.ForeignKey(
        'practices.Court', models.CASCADE, 'members_info',
        verbose_name='Корт',
    )
    status = models.ForeignKey(
        'practices.CourtStatus', models.RESTRICT, 'members',
        verbose_name='Статус корта',
    )

    class Meta:
        verbose_name = 'Корт - участник группы'
        verbose_name_plural = 'Корты - участники группы'

    def __str__(self):
        return f'Участник корта {self.member.player.user} ({self.pk})'
