from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = 'users.User' # тут под вопросом
        fileds = (
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
        )
