from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    club = models.ForeignKey(
        'practices.Club', models.CASCADE, 'clubs',
        verbose_name='Теннисный клуб',
    )
    name = models.CharField('Название', max_length=255)
    trainer = models.ForeignKey(
        User, models.RESTRICT, 'group_trainers',
        verbose_name='Тренер',
    )
    players = models.ManyToManyField(
        User, 'group_players', verbose_name='Игроки',
        blank=True,
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
