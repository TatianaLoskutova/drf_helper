from django.contrib.auth import get_user_model
from django.db import models

from common.models.mixins import BaseDictModelMixin

User = get_user_model()


class CourtStatus(BaseDictModelMixin):

    class Meta:
        verbose_name = 'Статус корта'
        verbose_name_plural = 'Статусы кортов'


class TrainingStatus(BaseDictModelMixin):

    class Meta:
        verbose_name = 'Статус тренировки'
        verbose_name_plural = 'Статусы тренировок'
