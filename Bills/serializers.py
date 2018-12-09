from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Transaction, Bill


class GroupSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        source='user_set', many=True, read_only=True)

    class Meta:
        model = Group
        fields = (
            "id",
            "user"
        )


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


class BillSerializer(serializers.ModelSerializer):
    transactions = serializers.PrimaryKeyRelatedField(
        source='transaction_set',
        many=True,
        read_only=True
    )

    class Meta:
        model = Bill
        fields = (
            'title',
            'owner',
            'group',
            'description',
            'transactions'
        )
