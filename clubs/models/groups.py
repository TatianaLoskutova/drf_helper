from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Group(models.Model):
    club = models.ForeignKey(
        'Club', models.CASCADE, 'groups',
        verbose_name='Теннисный клуб',
    )
    name = models.CharField('Название', max_length=255)
    trainer = models.ForeignKey(
        User, models.RESTRICT, 'groups_trainers',
        verbose_name='Тренер',
    )
    members = models.ManyToManyField(
        User, 'groups_members', verbose_name='Участники групп',
        blank=True, through='Member',
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
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} ({self.pk})'


class Member(models.Model):
    group = models.ForeignKey(
        'Group', models.CASCADE, 'members_info',
    )
    user = models.ForeignKey(
        User, models.CASCADE, 'groups_info',
    )
    date_joined = models.DateField('Date joined', default=timezone.now)

    class Meta:
        verbose_name = 'Участник группы'
        verbose_name_plural = 'Участники групп'
        ordering = ('-date_joined',)
        unique_together = (('group', 'user'),)

    def __str__(self):
        return f'Member {self.user}'
