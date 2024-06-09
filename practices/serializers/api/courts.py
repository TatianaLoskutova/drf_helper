from django.contrib.auth import get_user_model
from rest_framework import serializers

from practices.models.courts import Court
from practices.serializers.internal.courts import CourtStatsSerializer
from common.serializers.mixins import InfoModelSerializer

User = get_user_model()


class CourtListSerializer(InfoModelSerializer):
    all_pax = serializers.IntegerField()
    stats = CourtStatsSerializer(source='*')

    class Meta:
        model = Court
        fields = '__all__'


class CourtRetrieveSerializer(InfoModelSerializer):
    class Meta:
        model = Court
        fields = '__all__'


class CourtCreateSerializer(InfoModelSerializer):
    class Meta:
        model = Court
        fields = '__all__'


class CourtUpdateSerializer(InfoModelSerializer):
    class Meta:
        model = Court
        fields = '__all__'
