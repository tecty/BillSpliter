from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import *
# Create your views here.


class GroupViewSet(viewsets.ModelViewSet):
    queryset = BillGroups.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        # add a owner
        request.data.pop('owner', None)
        request.data['owner'] = request.user
        group = GroupSerializer().create(request.data)
        group.addUser(request.user)
        return group
