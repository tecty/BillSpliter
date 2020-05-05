from .models import BillGroup, GroupMember
from rest_framework import serializers
from Bills.serializers import UserSerializer

# TODO: Redo the groupserializer 
class MemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(
        read_only=True
    )
    class Meta: 
        model = GroupMember
        fields = (
            'id', 
            'user',
            'status'
        )

class GroupSerializer(serializers.ModelSerializer):
    members = MemberSerializer(source = 'groupmember_set',many = True, read_only=True)

    owner = UserSerializer(
        # source='owner',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = BillGroup
        fields = (
            "id",
            "owner",
            "members",
            "name"
        )
