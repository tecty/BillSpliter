from django.shortcuts import render
from rest_framework import viewsets
from .permissions import *
from .serializers import *
from .models import PREPARE, SUSPEND

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (NoCreation, IsOwnerOrReadOnly,)


class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = (
        IsOwnerOrReadOnly, DelectionProtectedByState,)

    def create(self, request):
        """
        Handle the model tagle at this level 
        """

        # pop the transaction data first
        trs = request.data.pop('transactions')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bill = serializer.save()

        try:
            for tr in trs:
                # filling the missing information
                tr['bill'] = bill.id
                tr_s = TransactionSerializer(data=tr)
                tr_s.is_valid(raise_exception=True)
                tr = tr_s.save()
                # wrap the transaction creation
                bill.transaction_set.add(tr)

        except Exception as e:
            bill.delete()
            print(e)
            raise serializers.ValidationError({
                'transactions': 'Error in createing transactions'
            })

        # try to approve a created bill
        # hence the request user nolonger need to approve
        # self transactions
        bill.approve()

        # wrap the transactions correctly and create success
        bill_s = BillSerializer(bill)
        headers = self.get_success_headers(bill_s)
        return Response(
            bill_s.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    # def perform_destroy(self, instance):
    #     if instance.state == PREPARE or instance.state == SUSPEND:
    #         instance.delete()
    #     else:
    #         # Couldn't delete a settled bill
    #         raise serializers.ValidationError({
    #             'above concencus stage bill could not be deleted'
    #         })

    @action(detail=True, methods=['POST'], name='Approve')
    def approve(self, request, pk=None):
        self.get_object().approve(request.user)
        headers = self.get_success_headers(
            BillSerializer(self.get_object())
        )
        return Response(
            bill_s.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    @action(detail=True, methods=['POST'], name='Reject')
    def reject(self, request, pk=None):
        self.get_object().reject(request.user)

        headers = self.get_success_headers(
            BillSerializer(self.get_object())
        )
        return Response(
            bill_s.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    @action(detail=True, methods=['POST'], name='Approve_all')
    def approve_all(self, request):
        Bill.approve_all(request.user)

        headers = self.get_success_headers(
            BillSerializer(self.get_object())
        )
        return Response(
            bill_s.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class SettleTransactionViewSet(viewsets.ModelViewSet):
    queryset = SettleTransaction.objects.all()
    serializer_class = SettleTrSerializer
    permission_classes = (NoCreation, IsRelatedOrReadOnly,)


class SettlementViewSet(viewsets.ModelViewSet):
    queryset = SettleTransaction.objects.all()
    serializer_class = SettleTrSerializer
    permission_classes = (IsOwnerOrReadOnly, DelectionProtectedByState,)

    def perform_destroy(self, instance):
        if instance.state == PREPARE or instance.state == SUSPEND:
            instance.delete()
        else:
            # Couldn't delete a settled bill
            raise serializers.ValidationError({
                'above concencus stage bill could not be deleted'
            })
