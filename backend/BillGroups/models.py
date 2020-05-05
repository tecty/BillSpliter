from django.db import models
from django.db.utils import IntegrityError
from django.contrib.auth.models import User, Group
# Create your models here.


# class BillGroup(Group):
#     owner = models.ForeignKey(User, models.PROTECT)

#     def addUser(self, user_id):
#         self.user_set.add(
#             User.objects.get(pk=user_id))

#     def delUser(self, user_id):
#         self.user_set.remove(
#             User.objects.get(pk=user_id))

#     @classmethod
#     # filter out the instance of user's bill groups
#     def get_bill_group(cls, user):
#         return cls.objects.filter(user=user)

#     def getKey(self, user_id):
#         # generate the key if the key is expire or validate too many
#         # person
#         self.user_set.remove(
#             User.objects.get(pk=user_id))

#     @classmethod
#     def join(cls, user, key):
#         # use key and user to join the group
#         # key is the time limit and amount limit numbers 
#         return cls.objects.filter(user=user)


class GroupMember(models.Model):
    user = models.ForeignKey(User, models.PROTECT)
    status = models.CharField(max_length = 1, choices = (
        ('I', "Invited"),
        # Reckon
        ('R', "Accepted"),
        ('A', "Applied")
    ))
    group = models.ForeignKey('BillGroup', models.CASCADE)
    class Meta: 
        unique_together = [['group', 'user']]

    def __str__(self):
        return str(self.user) + ' in ' + self.group.name 

# class BillGroupManager(models.Manager):
#     def user_set(self):
#         qs = self.get_queryset()
#         return GroupMember.objects.filter(
#             group = qs.get(),
#             status = 'R'
#         )

class BillGroup(models.Model):
    owner = models.ForeignKey(User,models.PROTECT)
    name  = models.CharField(max_length = 511, unique=True)

    @property
    def user_set(self):
        return GroupMember.objects.filter(
            group = self, 
            status = 'R'
        ).only('user_id')

    def isMember(self, user:User):
        return self.owner == user or self.groupmember_set.filter(user = user).count() == 1

    def invite(self, actor: User, username:str):
        if not self.isMember(actor): 
            raise PermissionError("You are not in the group.")
        u = User.objects.get(username = username)
        try:
            GroupMember(user = u, group = self, status = 'I').save()
        except IntegrityError as e:
            pass


    def approve (self,actor:User ,username:str):
        gm = self.groupmember_set.get(user__username = username)
        if gm.status =='R':
            return 
        if (gm.status == 'A' and self.owner == actor) or \
            (gm.status == 'I' and actor.username == str(username)):
            # different actor has different effect
            gm.status = 'R'
            gm.save()
        else: 
            raise PermissionError("You have not right to approve the request")

    def delUser(self, actor:User, username:str):
        if not self.owner == actor:
            raise PermissionError()
        self.groupmember_set.filter(user__username = username).delete()

    @classmethod
    def join(cls, user:User, groupName:str):
        cls.objects.get(name = groupName)

    @classmethod
    def get_bill_group(cls, user:str):
        # both user approved can be in the correct group
        return cls.objects.filter(
            groupmember__user = user, 
            groupmember__status = 'R')

    def __str__(self):
        return self.name + ' by ' +  str(self.owner)
