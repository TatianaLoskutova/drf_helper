from django.contrib import admin
from django.contrib.admin import TabularInline
from django.urls import reverse
from django.utils.html import format_html

from practices.models import courts, dicts, trainings


#######################
# INLINES
#######################
class CourtMemberInline(TabularInline):
    model = courts.CourtMember
    fields = ('member', 'status')


#######################
# MODELS
#######################
@admin.register(dicts.CourtStatus)
class CourtStatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'sort', 'is_active',)


@admin.register(dicts.TrainingStatus)
class TrainingStatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'sort', 'is_active',)


@admin.register(courts.Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'group', 'date', 'training_start', 'training_end',
        'training_max_duration',
    )
    inlines = (
        CourtMemberInline,
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
