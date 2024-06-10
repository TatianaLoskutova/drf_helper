from django.contrib.auth import get_user_model

from common.models.mixins import BaseDictModelMixin

User = get_user_model()


class WatchStatus(BaseDictModelMixin):

    class Meta:
        verbose_name = 'Статус смены'
        verbose_name_plural = 'Статусы смен'


class VacationStatus(BaseDictModelMixin):

    class Meta:
        verbose_name = 'Статус отпуска'
        verbose_name_plural = 'Статусы отпусков'
