from rest_framework import serializers

from users.models.profiles import Profile


class ProfileShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile  # тут под вопросом
        fields = (
            'telegram_id',
        )


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile  # тут под вопросом
        fields = (
            'telegram_id',
        )
