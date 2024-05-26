from django.contrib import admin

from clubs.models import clubs, dicts, groups
from practices.models.courts import GroupInfo


#######################
# INLINES
#######################
class PlayerInline(admin.TabularInline):
    model = clubs.Player
    fields = ('user', 'position', 'date_joined')


class MemberInline(admin.TabularInline):
    model = groups.Member
    fields = ('user', 'date_joined')


class ProfileTrainingInline(admin.StackedInline):
    model = GroupInfo
    fields = (
        'min_active_players',
        'training_start',
        'training_end',
        'training_max_duration',
    )


#######################
# MODELS
#######################
@admin.register(dicts.Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'sort', 'is_active',)


@admin.register(clubs.Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'director',)
    filter_horizontal = ('players',)
    inlines = (PlayerInline,)
    readonly_fields = (
        'created_at', 'created_by', 'updated_at', 'updated_by',
    )


@admin.register(groups.Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'trainer',)
    list_display_links = ('id', 'name',)
    search_fields = ('name',)
    inlines = (
        MemberInline,
        ProfileTrainingInline,
    )
    readonly_fields = (
        'created_at', 'created_by', 'updated_at', 'updated_by',
    )
