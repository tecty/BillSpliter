from django.shortcuts import render
from rest_framework import viewsets
from .permissions import *
from .serializers import *
from .models import PREPARE, SUSPEND

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated


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


class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
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
        bill = serialiizer.save()
        # pre_fetch the user_set to reduce db call 
        u_set =bill.group.user_set.values('id')
        u_set = [u['id'] for u in u_set]

        try:
            tr_list = []
            for tr in self.request.data['transactions']:
                # perform the from user validation checking
                if tr['from_u'] not in u_set:
                    raise serializers.ValidationError(
                        "User %d is not in the group", tr['from_u']
                    )

                # filling the missing information
                tr['bill'] = bill.id
                tr['to_u'] = self.request.user.id
                # use transaction serializer to perform this creation
                tr_s = TransactionSerializer(data=tr)
                tr_s.is_valid(raise_exception=True)
                # try to use bulk create 
                tr_list.append(tr_s)
                

            # bulk create to increase the performance 
            # Transaction.objects.bulk_create(tr_list)
            [tr.save() for tr in tr_list]
            
            # The request user must approve their bill 
            bill.approve( self.request.user)

        # except serializers.ValidationError as e:
        #     raise e
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
            .exclude(transaction__state=FINISH).distinct()
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
