from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Transaction, Bill, SettleTransaction, Settlement
from BillGroups.models import BillGroups


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
        queryset=BillGroups.objects.all()
    )

    def validate_group(self, value):
        return BillGroups.objects.get(pk=value)

    class Meta:
        model = Bill
        fields = (
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
            'settle',
            'from_u',
            'to_u',
            'modified'
            'amount',
            'state'
        )


class SettleSerializer(serializers.ModelSerializer):
    settle_tr = SettleTrSerializer(
        source='settletransaction_set',
        many=True,
        read_only=True
    )

    class Meta:
        model = Settlement
        fields = (
            'title',
            'owner',
            'created',
            'group',
            'description',
            'settle_tr'
        )
