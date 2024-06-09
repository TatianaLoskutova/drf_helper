from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from clubs.trainers.groups import GroupTrainer
from common.models.mixins import InfoMixin

User = get_user_model()


class Group(InfoMixin):
    club = models.ForeignKey(
        'Club', models.CASCADE, 'groups',
        verbose_name='Теннисный клуб',
    )
    name = models.CharField('Название', max_length=255)
    trainer = models.ForeignKey(
        'Player', models.RESTRICT, 'groups_trainers',
        verbose_name='Тренер',
    )
    members = models.ManyToManyField(
        'Player', 'groups_members', verbose_name='Игроки групп',
        blank=True, through='Member',
    )

    objects = GroupTrainer()

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
    player = models.ForeignKey(
        'Player', models.CASCADE, 'groups_info',
    )
    date_joined = models.DateField('Date joined', default=timezone.now)

    class Meta:
        verbose_name = 'Участник группы'
        verbose_name_plural = 'Участники групп'
        ordering = ('-date_joined',)
        unique_together = (('group', 'player'),)

    def __str__(self):
        return f'Member {self.player}'
