from django.contrib import admin

from clubs.models import clubs, dicts, groups, offers
from practices.models.courts import GroupInfo


#######################
# INLINES
#######################
class PlayerInline(admin.TabularInline):
    model = clubs.Player
    fields = ('user', 'position', 'date_joined')


class OfferInline(admin.TabularInline):
    model = offers.Offer
    fields = ('org_accept', 'user', 'user_accept',)


class MemberInline(admin.TabularInline):
    model = groups.Member
    fields = ('player', 'date_joined')


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
    inlines = (PlayerInline, OfferInline)
    readonly_fields = (
        'created_at', 'created_by', 'updated_at', 'updated_by',
    )


@admin.register(groups.Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'trainer',)
    list_display_links = ('id', 'name',)
    search_fields = ('name',)
    inlines = (
        ProfileTrainingInline,
        MemberInline,
    )
    readonly_fields = (
        'created_at', 'created_by', 'updated_at', 'updated_by',
    )


@admin.register(offers.Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'club', 'org_accept', 'user', 'user_accept',)
    search_fields = ('club__name', 'user__last_name',)

    readonly_fields = (
        'created_at', 'created_by', 'updated_at', 'updated_by',
    )
