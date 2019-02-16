from django.shortcuts import render
from rest_framework import viewsets
from Bills.permissions import IsOwnerOrReadOnly
from .serializers import *
# Create your views here.


class GroupViewSet(viewsets.ModelViewSet):
    queryset = BillGroups.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        # save the object and add the
        serializer.save().addUser(
            self.request.user
        )
