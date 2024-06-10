from crum import get_current_user
from django.db import models
from django.db.models import Q


class DepartmentChief(models.Manager):
    def my_departments(self):
        user = get_current_user()
        return self.filter(
            Q(organization__director=user)
            | Q(organization__employees=user)
        )

    def my_departments_admin(self):
        user = get_current_user()
        return self.filter(
            Q(organization__director=user)
            | Q(chief__user=user)
        )
