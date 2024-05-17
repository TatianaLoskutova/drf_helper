from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Club(models.Model):
    name = models.CharField('Название', max_length=255)
    director = models.ForeignKey(
        User, models.RESTRICT, 'club_directors',
        verbose_name='Директор',
    )
    players = models.ManyToManyField(
        User, 'club_players', verbose_name='Игроки',
        blank=True,
    )

    class Meta:
        verbose_name = 'Теннисный клуб'
        verbose_name_plural = 'Теннисные клубы'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} ({self.pk})'
