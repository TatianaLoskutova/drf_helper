from django.contrib import admin
from django.contrib.admin import TabularInline

from practices.models import clubs, groups, courts

#######################
# INLINES
#######################


class CourtPlayerInline(TabularInline):
    model = courts.CourtPlayer
    fields = ('player', 'status')

#######################
# MODELS
#######################


@admin.register(clubs.Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'director',)


@admin.register(groups.Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'trainer', 'min_active_players',)


@admin.register(courts.CourtStatus)
class CourtStatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'sort', 'is_booked',)


@admin.register(courts.Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'group', 'date', 'training_start', 'training_end',
        'training_max_duration',
    )
    inlines = (
        CourtPlayerInline,
    )
