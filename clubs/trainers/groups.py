from crum import get_current_user
from django.db import models
from django.db.models import Q


class GroupTrainer(models.Manager):
    def my_groups(self):
        user = get_current_user()
        return self.filter(
            Q(club__director=user)
            | Q(club__players=user)
        )

    def my_groups_admin(self):
        user = get_current_user()
        return self.filter(
            Q(club__director=user)
            | Q(trainer__user=user)
        )
