from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsMyClub(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.director == request.user:
            return True

        if request.method in SAFE_METHODS:
            return obj.players.all(user=request.user).exists()

        return False


class IsColleagues(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.club.director == request.user:
            return True

        if request.method in SAFE_METHODS:
            return obj.club.players.all(user=request.user).exists()
        return False


class IsMyGroup(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.club.director == request.user:
            return True

        if request.method in SAFE_METHODS:
            return obj.club.players.all(user=request.user).exists()

        return False


class IsOfferTrainer(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.club.director == request.user:
            return True

        return False
