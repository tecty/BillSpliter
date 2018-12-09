from .models import BillGroups
from rest_framework import serializers


class GroupSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        source='user_set', many=True, read_only=True)

    class Meta:
        model = BillGroups
        fields = (
            "id",
            "owner",
            "user",
            "name"
        )

