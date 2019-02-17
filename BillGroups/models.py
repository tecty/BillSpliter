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
