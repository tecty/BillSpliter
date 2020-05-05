from django.shortcuts import render
from rest_framework import viewsets
from Bills.permissions import IsOwnerOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from .serializers import *
# Create your views here.


class GroupViewSet(viewsets.ModelViewSet):
    queryset = BillGroup.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)

    def get_queryset(self):
        return BillGroup.objects.filter(
            user = self.request.user
        )

    def perform_create(self, serializer):
        # save the object and add the
        serializer.save().addUser(
            self.request.user.id
        )

    @action(detail=True, methods=['POST'], name='add_user')
    def add_user(self, request, pk=None):
        self.get_object().addUser(self.request.data['user'])
        return self.retrieve(self.request)

    @action(detail=True, methods=['POST'], name='del_user')
    def del_user(self, request, pk=None):
        self.get_object().delUser(self.request.data['user'])
        return self.retrieve(self.request)
