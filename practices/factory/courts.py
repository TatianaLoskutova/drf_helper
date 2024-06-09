from django.db.models import Count, Q

from practices import constants
from practices.models.courts import Court


class CourtFactory:
    model = Court

    def list(self):
        all_statuses = constants.TRAINING_ALL_STATUSES

        annotates_stats = dict()
        for status in all_statuses:
            annotates_stats[f'{status}_pax'] = Count(
                'trainings', distinct=True, filter=Q(trainings__status_id=status),
            )

        qs = self.model.objects.prefetch_related(
            'group',
            'group__group__trainer',
            'group__group__trainer__user',
            'group__group__club',
            'members',
            'members__player',
            'members__player__user',
        ).annotate(
            all_pax=Count('trainings', distinct=True),
        ).annotate(**annotates_stats)
        return qs
