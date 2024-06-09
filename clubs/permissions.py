from rest_framework.permissions import BasePermission, IsAuthenticated, \
    SAFE_METHODS


class IsMyClub(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if obj.director == request.user:
            return True

        if request.method in SAFE_METHODS:
            return request.user in obj.players.all()

        return False


class IsColleagues(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if obj.club.director == request.user:
            return True

        if request.method in SAFE_METHODS:
            return request.user in obj.club.players.all()
        return False


class IsMembers(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if (
            obj.group.club.director == request.user
            or obj.group.trainer.user == request.user
        ):
            return True

        if request.method in SAFE_METHODS:
            return request.user in obj.group.club.players.all()
        return False


class IsMyGroup(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if obj.club.director == request.user:
            return True

        if request.method in SAFE_METHODS:
            return request.user in obj.club.players.all()

        return False


class IsOfferTrainer(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if obj.club.director == request.user:
            return True

        return False
