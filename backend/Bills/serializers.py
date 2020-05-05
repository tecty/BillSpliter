from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Transaction, Bill, SettleTransaction, Settlement
from BillGroups.models import BillGroup


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "last_name"
        )

    def update(self, instance, validated_data):
        # update the user by given validated data
        user = super(UserSerializer, self)\
            .update(instance, validated_data)
        # update it's password
        user.set_password(validated_data['password'])
        user.save()
        return user

    def create(self, validated_data):
        # create user and udpate it's password
        user = super(UserSerializer, self)\
            .create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = (
            'bill',
            'from_u',
            'to_u',
            'amount',
            'state'
        )


class BriefTransactionSerializer(serializers.ModelSerializer):
    title = serializers.StringRelatedField(
        source='bill.title'
    )
    description = serializers.StringRelatedField(
        source='bill.description'
    )

    class Meta:
        model = Transaction
        fields = (
            'bill',
            'title',
            'description',
            'from_u',
            'to_u',
            'amount',
            'state'
        )


class BillSerializer(serializers.ModelSerializer):

    owner = UserSerializer(
        default=serializers.CurrentUserDefault()
    )

    transactions = TransactionSerializer(
        source='transaction_set',
        many=True,
        read_only=True
    )

    group = serializers.PrimaryKeyRelatedField(
        queryset=BillGroup.objects.all()
    )

    class Meta:
        model = Bill
        fields = (
            'id',
            'title',
            'owner',
            'state',
            'created',
            'group',
            'description',
            'transactions'
        )


class SettleTrSerializer(serializers.ModelSerializer):
    class Meta:
        model = SettleTransaction
        fields = (
            'id',
            'settle',
            'from_u',
            'to_u',
            'modified',
            'amount',
            'state'
        )


class SettleSerializer(serializers.ModelSerializer):
    settle_tr = SettleTrSerializer(
        source='settletransaction_set',
        many=True,
        read_only=True
    )

    owner = UserSerializer(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Settlement
        fields = (
            'id',
            'title',
            'description',
            'owner',
            'created',
            'state',
            'group',
            'description',
            'settle_tr'
        )

    def validate_group(self, group):
        if group.owner != self.context['request'].user:
            raise serializers.ValidationError(
                'Only group owner can create settlement'
            )
        return group
