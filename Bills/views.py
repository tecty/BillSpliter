from django.shortcuts import render
from rest_framework import viewsets
from .permissions import *
from .serializers import *
from .models import FINISH

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (AllowAny,)

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
    permission_classes = (IsOwnerOrReadOnly,)

    def create(self, request):
        """
        Handle the model tagle at this level 
        """

        # pop the transaction data first
        trs = request.data.pop('transactions')

        # add a owner
        request.data['owner'] = request.user
        # create the bill instance
        bill = BillSerializer().create(request.data)

        try:
            for tr in trs:
                # filling the missing information
                tr['bill'] = bill
                tr['to_u'] = request.user
                tr['from_u'] = User.objects.get(pk=tr['from_u'])
                tr = TransactionSerializer().create(tr)
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

    def perform_destroy(self, instance):
        if instance.state != FINISH:
            instance.delete()
        else:
            # Couldn't delete a settled bill
            raise serializers.ValidationError({
                'Finished Bill could not be deleted.'
            })

    @action(detail=True, methods=['GET'], name='Approve')
    def approve(self, request, pk=None):
        pass
