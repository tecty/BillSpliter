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

    def get_queryset(self):
        return Bill.filter_user_bills(self.request.user)

    def perform_create(self, serialiizer):
        bill = serialiizer.save()
        try:
            for tr in self.request.data['transactions']:
                # filling the missing information
                tr['bill'] = bill.id
                tr['to_u'] = self.request.user.id
                # use transaction serializer to perform this creation
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

    @action(detail=True, methods=['GET'], name='Approve')
    def approve(self, request, pk=None):
        self.get_object().approve(request.user)
        return self.retrieve(self.request)

    @action(detail=True, methods=['GET'], name='Reject')
    def reject(self, request, pk=None):
        self.get_object().reject(request.user)
        return self.retrieve(self.request)

    @action(detail=False, methods=['GET'], name='Approve_all')
    def approve_all(self, request):
        Bill.approve_all(request.user)
        return Response(
            status=status.HTTP_200_OK,
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
