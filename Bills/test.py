from django.test import TestCase
from Bills.models import *
# Create your tests here.


# a helper function for creating of a set of tr
# owner = ul[0]
# @pre: forall i,j in ul.length =>
#           ul[i].group == ul[j].group
# @post: forall i,j in bill.tr.length =>
#           bill.tr[i].amount == bill.tr[j].amount
def create_bill(ul, total):
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
            amount=total/len(ul)
        )

    return bill


class BillCase(TestCase):
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
        self.user001.groups.add(self.group)

        self.user_list = [
            self.user001,
            self.user002,
            self.user003,
            self.user004,
        ]

    def test_create_bill(self):
        bill = Bill.objects.create(
            title="dinner",
            description="nothing",
            owner=self.user001,
            group=self.group
        )
        self.assertEquals(bill.title, "dinner")
        self.assertEquals(bill.description, "nothing")
        self.assertEquals(bill.owner, self.user001)
        self.assertEquals(bill.group, self.group)

    def test_create_bill_and_self_paid(self):
        bill = Bill.objects.create(
            title="dinner",
            description="nothing",
            owner=self.user001,
            group=self.group
        )
        tr = bill.transaction_set.create(
            from_u=self.user001,
            to_u=self.user001,
            amount=1.0
        )
        # this state must be prepare
        self.assertEqual(PREPARE, bill.state)

        bill.approve(self.user001)

        # this state must be concencus
        self.assertEqual(CONCENCUS, bill.state)

    def test_bill_reject(self):
        bill = Bill.objects.create(
            title="dinner",
            description="nothing",
            owner=self.user001,
            group=self.group
        )
        tr = bill.transaction_set.create(
            from_u=self.user002,
            to_u=self.user001,
            amount=1.0
        )
        # this state must be prepare
        self.assertEqual(PREPARE, bill.state)
        bill.reject(self.user002)
        self.assertEqual(SUSPEND, bill.state)

    def test_reject_multiple_user(self):
        bill = Bill.objects.create(
            title="dinner",
            description="nothing",
            owner=self.user001,
            group=self.group
        )
        tr1 = bill.transaction_set.create(
            from_u=self.user002,
            to_u=self.user001,
            amount=1.0
        )
        tr2 = bill.transaction_set.create(
            from_u=self.user001,
            to_u=self.user001,
            amount=1.0
        )
        bill.approve(self.user001)
        # this state must be prepare
        self.assertEqual(PREPARE, bill.state)
        bill.reject(self.user002)
        self.assertEqual(SUSPEND, bill.state)

        # all should be suspend
        self.assertEqual(
            SUSPEND,
            bill.transaction_set.get(
                from_u=self.user001
            ).state
        )
        self.assertEqual(
            REJECTED,
            bill.transaction_set.get(
                from_u=self.user002
            ).state
        )

    def test_approve_multiple_user(self):
        bill = Bill.objects.create(
            title="dinner",
            description="nothing",
            owner=self.user001,
            group=self.group
        )
        tr1 = bill.transaction_set.create(
            from_u=self.user002,
            to_u=self.user001,
            amount=1.0
        )
        tr2 = bill.transaction_set.create(
            from_u=self.user001,
            to_u=self.user001,
            amount=1.0
        )
        bill.approve(self.user001)
        # this state must be prepare
        self.assertEqual(PREPARE, bill.state)
        bill.approve(self.user002)
        self.assertEqual(CONCENCUS, bill.state)

        # all should be suspend
        self.assertEqual(
            CONCENCUS,
            bill.transaction_set.get(
                from_u=self.user001
            ).state
        )
        self.assertEqual(
            CONCENCUS,
            bill.transaction_set.get(
                from_u=self.user002
            ).state
        )

    def test_resume_other_user(self):
        bill = Bill.objects.create(
            title="dinner",
            description="nothing",
            owner=self.user001,
            group=self.group
        )
        tr1 = bill.transaction_set.create(
            from_u=self.user002,
            to_u=self.user001,
            amount=1.0
        )
        tr2 = bill.transaction_set.create(
            from_u=self.user001,
            to_u=self.user001,
            amount=1.0
        )
        bill.approve(self.user001)
        bill.reject(self.user002)

        # only owner can try to resume it
        bill.resume(self.user002)
        self.assertEqual(SUSPEND, bill.state)

    def test_resume_by_other_user(self):
        bill = Bill.objects.create(
            title="dinner",
            description="nothing",
            owner=self.user001,
            group=self.group
        )
        tr1 = bill.transaction_set.create(
            from_u=self.user002,
            to_u=self.user001,
            amount=1.0
        )
        tr2 = bill.transaction_set.create(
            from_u=self.user001,
            to_u=self.user001,
            amount=1.0
        )
        bill.approve(self.user001)
        bill.reject(self.user002)

        # only owner can try to resume it
        bill.resume(bill.owner)
        self.assertEqual(PREPARE, bill.state)
        bill.approve(self.user002)
        self.assertEqual(CONCENCUS, bill.state)

    def test_create_bill_util(self):
        bill = create_bill(self.user_list, 10)

        self.assertEqual(bill.transaction_set.count(), len(self.user_list))
        self.assertEqual(
            bill.transaction_set.first().amount, 10/len(self.user_list))


class SettleCase(TestCase):
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
        self.user001.groups.add(self.group)

        # ul for user_list
        self.ul = [
            self.user001,
            self.user002,
            self.user003,
            self.user004,
        ]

        # creating a lot of finished tr
