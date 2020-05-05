from .models import BillGroup
from rest_framework import serializers
from Bills.serializers import UserSerializer

# TODO: Redo the groupserializer 
class GroupSerializer(serializers.ModelSerializer):
    users = UserSerializer(
        source='user_set', many=True, read_only=True
    )

    owner = UserSerializer(
        # source='owner',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = BillGroup
        fields = (
            "id",
            "owner",
            "users",
            "name"
        )
