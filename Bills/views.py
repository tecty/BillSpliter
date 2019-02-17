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
    permission_classes = (
        NoCreation, IsOwnerOrReadOnly,
        DelectionProtectedByState,
        UpdateProtectedByState,
    )


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
                # perform the from user validation checking
                if User.objects.get(pk=tr['from_u']) not in bill.group.user_set.all():
                    raise serializers.ValidationError(
                        "User %d is not in the group", tr['from_u']
                    )

                # filling the missing information
                tr['bill'] = bill.id
                tr['to_u'] = self.request.user.id
                # use transaction serializer to perform this creation
                tr_s = TransactionSerializer(data=tr)
                tr_s.is_valid(raise_exception=True)
                tr = tr_s.save()
                # wrap the transaction creation
                bill.transaction_set.add(tr)
        except serializers.ValidationError as e:
            raise e
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


class BriefTransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = BriefTransactionSerializer
    permission_classes = (NoCreation, IsRelatedOrReadOnly,)

    def get_queryset(self):
        return Transaction.get_waitng_tr(self.request.user)


class SettleTransactionViewSet(viewsets.ModelViewSet):
    queryset = SettleTransaction.objects.all()
    serializer_class = SettleTrSerializer
    permission_classes = (NoCreation, IsRelatedOrReadOnly,)


class SettlementViewSet(viewsets.ModelViewSet):
    queryset = Settlement.objects.all()
    serializer_class = SettleSerializer
    permission_classes = (IsOwnerOrReadOnly, DelectionProtectedByState,)

    @action(detail=True, methods=['GET'], name='waiting_bill')
    def waiting_bill(self, request, pk=None):
        query = Settlement.get_waiting_bill(self.get_object())

        return Response(BillSerializer(query, many=True).data)
