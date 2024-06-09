from rest_framework.permissions import IsAuthenticated


class IsCourtManager(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if obj.group.club.director == request.user:
            return True
        if obj.group.trainer.user == request.user:
            return True
        return False
