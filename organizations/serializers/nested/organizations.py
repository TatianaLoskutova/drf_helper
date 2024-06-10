from common.serializers.mixins import ExtendedModelSerializer
from organizations.models.organizations import Organization


class OrganizationShortSerializer(ExtendedModelSerializer):
    class Meta:
        model = Organization
        fields = (
            'id',
            'name',
        )
