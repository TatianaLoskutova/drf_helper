from rest_framework.permissions import IsAuthenticated


class IsWatchManager(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if obj.group.organization.director == request.user:
            return True
        if obj.group.chief.user == request.user:
            return True
        return False
