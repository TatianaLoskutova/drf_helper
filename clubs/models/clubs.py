from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from clubs.constants import DIRECTOR_POSITION, TRAINER_POSITION, \
    PLAYER_POSITION
from common.models.mixins import InfoMixin

User = get_user_model()


class Club(InfoMixin):
    name = models.CharField('Название', max_length=255)
    director = models.ForeignKey(
        User, models.RESTRICT, 'clubs_directors',
        verbose_name='Директор',
    )
    players = models.ManyToManyField(
        User, 'clubs_players', verbose_name='Игроки',
        blank=True, through='Player',
    )

    class Meta:
        verbose_name = 'Теннисный клуб'
        verbose_name_plural = 'Теннисные клубы'
        ordering = ('name', 'id',)

    def __str__(self):
        return f'{self.name} ({self.pk})'

    @property
    def director_player(self):
        obj, create = self.players_info.get_or_create(
            position_id=DIRECTOR_POSITION, defaults={'user': self.director, }
        )
        return obj


class Player(models.Model):
    club = models.ForeignKey(
        'Club', models.CASCADE, 'players_info',
    )
    user = models.ForeignKey(
        User, models.CASCADE, 'clubs_info',
    )
    position = models.ForeignKey(
        'Position', models.RESTRICT, 'players',
    )
    date_joined = models.DateField('Date joined', default=timezone.now)

    class Meta:
        verbose_name = 'Игрок клуба'
        verbose_name_plural = 'Игроки клубов'
        ordering = ('-date_joined',)
        unique_together = (('club', 'user'),)

    def __str__(self):
        return f'Player #{self.pk} {self.user}'

    @property
    def is_director(self):
        if self.position_id == DIRECTOR_POSITION:
            return True
        return False

    @property
    def is_trainer(self):
        if self.position_id == TRAINER_POSITION:
            return True
        return False

    @property
    def is_player(self):
        if self.position_id == PLAYER_POSITION:
            return True
        return False
