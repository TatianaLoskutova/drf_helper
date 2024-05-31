from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsNotCorporate(BasePermission):
    message = (
        'У вас корпоративный аккаунт. Данное действие недоступно. '
        'Обратитесь к администратору.'
    )

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)

        return (
            bool(request.user and request.user.is_authenticated
                 and not request.user.is_corporate_account)
        )

    # def has_object_permission(self, request, view, obj):
    #     """
    #     Return `True` if permission is granted, `False` otherwise.
    #     """
    #     return True
