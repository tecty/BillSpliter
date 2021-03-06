from .models import BillGroups
from rest_framework import serializers
from Bills.serializers import UserSerializer


class GroupSerializer(serializers.ModelSerializer):
    users = UserSerializer(
        source='user_set', many=True, read_only=True
    )

    owner = UserSerializer(
        # source='owner',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = BillGroups
        fields = (
            "id",
            "owner",
            "users",
            "name"
        )
