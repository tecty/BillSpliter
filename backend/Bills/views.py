from django.shortcuts import render
from rest_framework import viewsets
from .permissions import *
from .serializers import *
from .models import PREPARE, SUSPEND

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated

from traceback import print_exc


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    """
    Get method could only get the element of current user
    """

    def list(self, request):
        if request.user and request.user.is_authenticated:
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        # else: not authenticated
        # raise not authenticated
        raise NotAuthenticated()

    def retrieve(self, request, pk=None):
        return self.list(request)


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (
        NoCreation, IsOwnerOrReadOnly,
        DelectionProtectedByState,
        UpdateProtectedByState,
        IsAuthenticated,
    )


def tr_helper(tr, bill_id, to_u):
    tr['bill'] = bill_id
    if 'to_u' not in tr:
        tr['to_u'] = to_u
    tr = TransactionSerializer(data=tr)
    tr.is_valid(raise_exception=True)
    return tr


class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.select_related('owner')\
        .prefetch_related('transaction_set').all()
    serializer_class = BillSerializer
    permission_classes = (
        IsAuthenticated,
        IsOwnerOrReadOnly,
        IsInGroupOrNotPermit,
        DelectionProtectedByState,
    )

    def validate_trs(self, trs):
        # each from_u can be seen only once
        seen = set()
        for tr in trs:
            if tr.from_u in seen:
                # this tr list is invalidate
                raise serializers.ValidationError(
                    {
                        'transactions':
                            "User %d has seen at least twice " %
                            tr.from_u
                    }
                )
            seen.add(tr.from_u)

    def perform_create(self, serialiizer):
        if not self.request.data['transactions'] or \
                len(self.request.data['transactions']) == 0:
            raise serializers.ValidationError({
                'transactions': 'Empty transaction list.'
            })
        if len(set(t['from_u'] for t in self.request.data['transactions'])) != \
                len(self.request.data['transactions']):
            raise serializers.ValidationError({
                'transactions': 'Duplicated transaction is not allowed.'
            })

        try:
            bill = serialiizer.save()

            # optimisation
            group = set(bill.group.user_set.values_list('id', flat=True))
            group_filter = [int(tr['from_u'])
                            for tr in self.request.data['transactions']
                            if int(tr['from_u']) not in group]
            if any(group_filter):
                raise serializers.ValidationError(
                    "Users %s is not in the group" % str(group_filter)
                )
            trs = (
                Transaction(
                    **(
                        tr_helper(
                            tr, bill.id, self.request.user.id).validated_data
                    )
                )
                for tr in self.request.data['transactions']
            )
            # list of validated data dict
            trs = Transaction.objects.bulk_create(trs)
            bill.approve(self.request.user)
        except serializers.ValidationError as e:
            bill.delete()
            raise e
        except Exception as e:
            print_exc(e)
            bill.delete()
            print(e)
            raise e

    @action(detail=True, methods=['GET'], name='Approve')
    def approve(self, request, pk=None):
        self.get_object().approve(request.user)
        return self.retrieve(self.request)

    @action(detail=True, methods=['GET'], name='Reject')
    def reject(self, request, pk=None):
        self.get_object().reject(request.user)
        return self.retrieve(self.request)

    @action(detail=True, methods=['GET'], name='Resume')
    def resume(self, request, pk=None):
        self.get_object().resume(request.user)
        return self.retrieve(self.request)

    @action(detail=False, methods=['GET'], name='Approve_all')
    def approve_all(self, request):
        Bill.approve_all(request.user)
        return Response(
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=['GET'])
    def current(self, request, *args, **kwargs):
        # only include the finished bills
        self.queryset = Bill.filter_user_bills(self.request.user)\
            .exclude(transaction__state=FINISH).distinct()\
            .select_related('owner')\
            .prefetch_related('transaction_set')
        return self.list(request, *args, **kwargs)

    @action(detail=False, methods=['GET'])
    def balance(self, request):
        return Response(
            {'balance': Transaction.get_balance(self.request.user)}
        )


class BriefTransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = BriefTransactionSerializer
    permission_classes = (
        NoCreation,
        IsRelatedOrReadOnly,
        IsAuthenticated,
    )

    def get_queryset(self):
        return Transaction.filter_user(self.request.user).exclude(state=FINISH)


class SettleTransactionViewSet(viewsets.ModelViewSet):
    queryset = SettleTransaction.objects.all()
    serializer_class = SettleTrSerializer
    permission_classes = (
        NoCreation,
        IsRelatedOrReadOnly,
        IsAuthenticated,
    )

    @action(detail=True, methods=['GET'], name='Approve')
    def approve(self, request, pk=None):
        self.get_object().approve(request.user)
        return self.retrieve(self.request)

    @action(detail=True, methods=['GET'], name='Reject')
    def reject(self, request, pk=None):
        self.get_object().reject(request.user)
        return self.retrieve(self.request)


class SettlementViewSet(viewsets.ModelViewSet):
    queryset = Settlement.objects.order_by('-id')
    serializer_class = SettleSerializer
    permission_classes = (
        IsOwnerOrReadOnly,
        DelectionProtectedByState,
        IsAuthenticated,
    )

    @action(detail=True, methods=['GET'], name='waiting_bill')
    def waiting_bill(self, request, pk=None):
        query = Settlement.get_waiting_bill(self.get_object())

        return Response(BillSerializer(query, many=True).data)

    @action(detail=True, methods=['GET'])
    def include_bill(self, request, pk=None):
        return Response(BillSerializer(
            self.get_object().bill_set, many=True
        ).data)

    @action(detail=True, methods=['GET'])
    def statistic(self, request, pk=None):
        """
        Some worthknowing statistics about this transaction
        Including actual pay, balance, GDP, tr_count 
        """
        settle = self.get_object()
        return Response({
            'gdp': settle.gdp,
            'tr_count': settle.tr_count,
            'balance': settle.get_balance_by_user(self.request.user),
            'actual_pay': settle.get_actual_pay_by_user(self.request.user),
        })
