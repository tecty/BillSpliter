from django.db import models
from django.contrib.auth.models import User, Group
# Create your models here.


class BillGroups(Group):
    owner = models.ForeignKey(User, models.PROTECT)

    def addUser(self, user):
        self.user_set.add(user)

    def delUser(self, user):
        self.user_set.remove(user)
