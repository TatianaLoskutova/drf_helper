from django.contrib import admin
from django.contrib.admin import TabularInline
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html

from practices.models import clubs, courts, dicts, groups, trainings


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
    filter_horizontal = ('players',)


@admin.register(groups.Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'trainer', 'min_active_players',
        'court_count',
    )
    list_display_links = ('id', 'name',)
    search_fields = ('name',)

    def court_count(self, obj):
        return obj.court_count

    court_count.short_description = 'Кол-во кортов'

    def get_queryset(self, request):
        queryset = groups.Group.objects.annotate(
            court_count=Count('courts__id')
        )
        return queryset


@admin.register(dicts.CourtStatus)
class CourtStatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'sort', 'is_booked',)


@admin.register(dicts.TrainingStatus)
class TrainingStatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'sort', 'is_booked',)


@admin.register(courts.Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'group', 'date', 'training_start', 'training_end',
        'training_max_duration',
    )
    autocomplete_fields = ('group',)
    inlines = (
        CourtPlayerInline,
    )


@admin.register(trainings.Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'court_link', 'training_start', 'training_end', 'status',
    )
    list_filter = ('status',)
    radio_fields = {'status': admin.VERTICAL}

    def court_link(self, obj):
        link = reverse(
            'admin:practices_court_change', args=[obj.court.id],
        )
        return format_html('<a href="{}">{}</a>', link, obj.court)
