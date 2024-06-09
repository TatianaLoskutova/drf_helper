from django.db.models import Count, Q

from practices import constants
from practices.models.courts import Court


class CourtFactory:
    model = Court

    def list(self):
        all_statuses = constants.TRAINING_ALL_STATUSES

        annotates = dict()
        for status in all_statuses:
            annotates[f'{status}_pax'] = Count(
                'trainings', distinct=True, filter=Q(breaks__status_id=status),
            )

        qs = self.model.objects.prefetch_related(
            'group',
            'members',
            'members__player',
            'members__player__user',
        ).annotate(
            all_pax=Count('trainings', distinct=True),
        ).annotate(**annotates)
        return qs
