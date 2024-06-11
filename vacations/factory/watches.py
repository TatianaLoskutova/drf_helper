import pdb

from django.db.models import Count, Q

from vacations import constants
from vacations.models.watches import Watch


class WatchFactory:
    model = Watch

    def list(self):
        all_statuses = constants.VACATION_ALL_STATUSES

        annotates_stats = dict()
        for status in all_statuses:
            annotates_stats[f'{status}_pax'] = Count(
                'vacations', distinct=True,
                filter=Q(vacations__status_id=status),
            )
        qs = self.model.objects.prefetch_related(
            'department',
            'department__department__chief',
            'department__department__chief__user',
            'department__department__organization',
            'members',
            'members__employee',
            'members__employee__user',
        ).annotate(
            all_pax=Count('vacations', distinct=True),
        ).annotate(**annotates_stats)
        return qs
