from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # тут под вопросом
        fields = (
            'id', 'username',
        )


