from django.test import TestCase
from Bills.models import *


# a helper function for creating of a set of tr
# owner = ul[0]
# @pre: forall i,j in ul.length =>
#           ul[i].group == ul[j].group
# @post: forall i,j in bill.tr.length =>
#           bill.tr[i].amount == bill.tr[j].amount
# @post: forall bill => bill.state == concencus
# @post: forall tr => tr.state == concencus
def create_bill(ul, total, state=CONCENCUS):
    bill = Bill.objects.create(
        title="dinner",
        description="nothing",
        owner=ul[0],
        group=BillGroups.get_bill_group(ul[0]).first()
    )

    for u in ul:
        # setted up the transaction to owner
        bill.transaction_set.create(
            from_u=u,
            to_u=ul[0],
            state=state,
            amount=total/len(ul)
        )

    return bill


class UserCaseEnv(TestCase):
    def setUp(self):
        """Create a list of User to be test environment"""
        self.user001 = User.objects.create_user(
            'u001', "u001@example.cn", "tt")
        self.user002 = User.objects.create_user(
            'u002', "u002@example.cn", "tt")
        self.user003 = User.objects.create_user(
            'u003', "u003@example.cn", "tt")
        self.user004 = User.objects.create_user(
            'u004', "u004@example.cn", "tt")

        # dummy billing groups
        self.group = BillGroups.objects.create(name="test", owner=self.user001)
        self.group.addUser(self.user001.id)
        self.group.addUser(self.user002.id)
        self.group.addUser(self.user003.id)
        self.group.addUser(self.user004.id)
        self.user001.groups.add(self.group)

        # ul for user_list
        self.ul = [
            self.user001,
            self.user002,
            self.user003,
            self.user004,
        ]

        # creating a lot of finished tr

        create_bill(self.ul, 10)
        create_bill(self.ul, 20)
        create_bill(self.ul, 30)