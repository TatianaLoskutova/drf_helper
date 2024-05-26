from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class GroupInfo(models.Model):
    group = models.OneToOneField(
        'clubs.Group', models.CASCADE,
        verbose_name='Корт', primary_key=True,
    )
    min_active_players = models.PositiveSmallIntegerField(
        'Минимальное количество активных игроков', blank=True, null=True,
    )
    training_start = models.TimeField('Начало тренировки', blank=True, null=True,)
    training_end = models.TimeField('Окончание тренировки', blank=True, null=True,)
    training_max_duration = models.PositiveSmallIntegerField(
        'Максимальная длительность тренировки', blank=True, null=True,
    )

    class Meta:
        verbose_name = 'Параметры тренировочных групп'
        verbose_name_plural = 'Параметры тренировочных групп'

    def __str__(self):
        return f'{self.group}'


class Court(models.Model):
    group = models.ForeignKey(
        'practices.GroupInfo', models.CASCADE, 'courts',
        verbose_name='Группа',
    )
    date = models.DateField('Дата аренды корта')
    training_start = models.TimeField('Начало тренировки', blank=True, null=True,)
    training_end = models.TimeField('Окончание тренировки', blank=True, null=True,)
    training_max_duration = models.PositiveSmallIntegerField(
        'Максимальная длительность тренировки', blank=True, null=True,
    )

    class Meta:
        verbose_name = 'Корт'
        verbose_name_plural = 'Корты'
        ordering = ('-date',)

    def __str__(self):
        return f'Корт №{self.pk} для {self.group})'


class CourtPlayer(models.Model):
    player = models.ForeignKey(
        User, models.CASCADE, 'courts',
        verbose_name='Игрок',
    )
    cort = models.ForeignKey(
        'practices.Court', models.CASCADE, 'players',
        verbose_name='Корт',
    )
    status = models.ForeignKey(
        'practices.CourtStatus', models.RESTRICT, 'court_players',
        verbose_name='Статус корта',
    )

    class Meta:
        verbose_name = 'Корт - Игрок'
        verbose_name_plural = 'Корты - Игроки'

    def __str__(self):
        return f'Корт {self.cort} для {self.player})'
