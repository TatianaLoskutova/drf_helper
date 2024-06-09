from django.contrib.auth import get_user_model
from django.db import models

from practices.constants import TRAINING_CREATED_DEFAULT, \
    TRAINING_CREATED_STATUS
from practices.models.dicts import TrainingStatus

User = get_user_model()


class Training(models.Model):
    court = models.ForeignKey(
        'practices.Court', models.CASCADE, 'trainings',
        verbose_name='Корт',
    )
    player = models.ForeignKey(
        User, models.CASCADE, 'trainings',
        verbose_name='Игрок',
    )
    member = models.ForeignKey(
        'clubs.Member', models.CASCADE, 'trainings', verbose_name='Участник группы',
    )
    training_start = models.TimeField('Начало тренировки', blank=True, null=True,)
    training_end = models.TimeField('Окончание тренировки', blank=True, null=True,)
    status = models.ForeignKey(
        'practices.TrainingStatus', models.RESTRICT, 'trainings',
        verbose_name='Статус тренировки', blank=True,
    )

    class Meta:
        verbose_name = 'Тренировка'
        verbose_name_plural = 'Тренировки'
        ordering = ('-court__date', 'training_start')

    def __str__(self):
        return f'Тренировка пользователя {self.player} ({self.pk})'

    def save(self, *args, **kwargs):
        if not self.pk:
            status, created = TrainingStatus.objects.get_or_create(
                code=TRAINING_CREATED_STATUS,
                defaults=TRAINING_CREATED_DEFAULT,
            )
            self.status = status
        return super().save(*args, **kwargs)
