from django.db import models
from django.contrib.auth.models import User, Group
# Create your models here.


class BillGroups(Group):
    owner = models.ForeignKey(User, models.PROTECT)

    def addUser(self, user_id):
        self.user_set.add(
            User.objects.get(pk=user_id))

    def delUser(self, user_id):
        self.user_set.remove(
            User.objects.get(pk=user_id))

    @classmethod
    # filter out the instance of user's bill groups
    def get_bill_group(cls, user):
        return cls.objects.filter(user=user)

    def getKey(self, user_id):
        # generate the key if the key is expire or validate too many
        # person
        self.user_set.remove(
            User.objects.get(pk=user_id))

    @classmethod
    def join(cls, user, key):
        # use key and user to join the group
        # key is the time limit and amount limit numbers 
        return cls.objects.filter(user=user)
