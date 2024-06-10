from django.contrib import admin

from organizations.models import organizations, dicts, departments, offers
from vacations.models.watches import DepartmentInfo


#######################
# INLINES
#######################
class EmployeeInline(admin.TabularInline):
    model = organizations.Employee
    fields = ('user', 'position', 'date_joined')


class OfferInline(admin.TabularInline):
    model = offers.Offer
    fields = ('org_accept', 'user', 'user_accept',)


class MemberInline(admin.TabularInline):
    model = departments.Member
    fields = ('employee', 'date_joined')


class ProfileVacationInline(admin.StackedInline):
    model = DepartmentInfo
    fields = (
        'min_active_employees',
        'vacation_start',
        'vacation_end',
        'vacation_max_duration',
    )


#######################
# MODELS
#######################
@admin.register(dicts.Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'sort', 'is_active',)


@admin.register(organizations.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'director',)
    filter_horizontal = ('employees',)
    inlines = (EmployeeInline, OfferInline)
    readonly_fields = (
        'created_at', 'created_by', 'updated_at', 'updated_by',
    )


@admin.register(departments.Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'chief',)
    list_display_links = ('id', 'name',)
    search_fields = ('name',)
    inlines = (
        ProfileVacationInline,
        MemberInline,
    )
    readonly_fields = (
        'created_at', 'created_by', 'updated_at', 'updated_by',
    )


@admin.register(offers.Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'organization', 'org_accept', 'user', 'user_accept',)
    search_fields = ('organization__name', 'user__last_name',)

    readonly_fields = (
        'created_at', 'created_by', 'updated_at', 'updated_by',
    )
