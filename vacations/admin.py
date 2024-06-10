from django.contrib import admin
from django.contrib.admin import TabularInline
from django.urls import reverse
from django.utils.html import format_html

from vacations.models import watches, dicts, vacations


#######################
# INLINES
#######################
class WatchMemberInline(TabularInline):
    model = watches.WatchMember
    fields = ('member', 'status')


#######################
# MODELS
#######################
@admin.register(dicts.WatchStatus)
class WatchStatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'sort', 'is_active',)


@admin.register(dicts.VacationStatus)
class VacationStatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'sort', 'is_active',)


@admin.register(watches.Watch)
class WatchAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'department', 'date', 'vacation_start', 'vacation_end',
        'vacation_max_duration',
    )
    inlines = (
        WatchMemberInline,
    )


@admin.register(vacations.Vacation)
class VacationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'watch_link', 'vacation_start', 'vacation_end', 'status',
    )
    list_filter = ('status',)
    radio_fields = {'status': admin.VERTICAL}

    def court_link(self, obj):
        link = reverse(
            'admin:vacations_watch_change', args=[obj.watch.id],
        )
        return format_html('<a href="{}">{}</a>', link, obj.watch)
