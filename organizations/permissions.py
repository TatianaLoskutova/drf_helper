from rest_framework.permissions import IsAuthenticated, \
    SAFE_METHODS


class IsMyOrganization(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if obj.director == request.user:
            return True

        if request.method in SAFE_METHODS:
            return request.user in obj.employees.all()

        return False


class IsColleagues(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if obj.organization.director == request.user:
            return True

        if request.method in SAFE_METHODS:
            return request.user in obj.organization.employees.all()
        return False


class IsMembers(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if (
            obj.group.organization.director == request.user
            or obj.group.trainer.user == request.user
        ):
            return True

        if request.method in SAFE_METHODS:
            return request.user in obj.group.organization.employees.all()
        return False


class IsMyDepartment(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if obj.organization.director == request.user:
            return True

        if request.method in SAFE_METHODS:
            return request.user in obj.organization.employees.all()

        if obj.trainer.user == request.user:
            return True

        return False


class IsOfferChief(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if obj.organization.director == request.user:
            return True

        return False
