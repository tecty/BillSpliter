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
        return BillGroup.objects.filter(groupmember__user = self.request.user)

    def perform_create(self, serializer):
        # save the object and add the
        g = serializer.save()
        g.invite(
            self.request.user,self.request.user
        )
        g.approve(self.request.user,self.request.user)

    @action(detail=True, methods=['POST'], name='invite')
    def invite_user(self, request, pk=None):
        self.get_object().addUser(self.request.user, self.request.data['user'])
        return self.retrieve(self.request)

    @action(detail=True, methods=['POST'], name='approve')
    def approve_user(self, request, pk=None):
        self.get_object().approve(self.request.user, self.request.data['user'])
        return self.retrieve(self.request)

    @action(detail=True, methods=['POST'], name='delete_user')
    def approve_user(self, request, pk=None):
        self.get_object().delUser(self.request.user, self.request.data['user'])
        return self.retrieve(self.request)
