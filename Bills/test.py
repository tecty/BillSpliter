from django.test import TestCase
from Bills.models import *
# Create your tests here.


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

    def test_user_concencus(self):
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
        self.assertEqual(
            bill.transaction_set.first().state, CONCENCUS)

    def test_create_bill_util_with_prepare(self):
        bill = create_bill(self.user_list, 10, PREPARE)

        self.assertEqual(bill.transaction_set.count(), len(self.user_list))
        self.assertEqual(
            bill.transaction_set.first().amount, 10/len(self.user_list))
        self.assertEqual(
            bill.transaction_set.first().state, PREPARE)

    def test_approve_all(self):

        bill1 = create_bill(
            [self.user_list[0], self.user_list[1]], 10, PREPARE)
        bill2 = create_bill(
            [self.user_list[0], self.user_list[1], self.user_list[2]], 10, PREPARE)

        Bill.approve_all(self.user_list[0])
        Bill.approve_all(self.user_list[1])

        # update bills
        bill1.refresh_from_db()
        bill2.refresh_from_db()

        # bill1 get all member approved, so it's concencus
        # bill2 need to get user2 concencus, so it still preparing
        self.assertEqual(bill1.state, CONCENCUS)
        self.assertEqual(bill2.state, PREPARE)


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
        self.group.addUser(self.user001)
        self.group.addUser(self.user002)
        self.group.addUser(self.user003)
        self.group.addUser(self.user004)
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

    def create_settlement(self):
        return Settlement.objects.create(
            title="Feb,2019",
            owner=self.ul[0],
            group=self.group
        )

    def test_null_create(self):
        # test whether all the environment is created
        self.assertEqual(
            Bill.objects.filter(owner=self.ul[0]).count(), 3
        )
        # all the default bill is share as 2.5, 5, and 7.5
        self.assertEqual(
            Bill.objects.get(pk=1).transaction_set.first().amount,
            2.5
        )
        self.assertEqual(
            Bill.objects.get(pk=2).transaction_set.first().amount,
            5
        )
        self.assertEqual(
            Bill.objects.get(pk=3).transaction_set.first().amount,
            7.5
        )

    def test_calculate_balance(self):
        """
        This method is not belong to here. but I don't wanna write another
        settup function
        """

        self.assertEqual(Transaction.get_balance(self.ul[0]), 45)
        self.assertEqual(Transaction.get_balance(self.ul[1]), -15)
        self.assertEqual(Transaction.get_balance(self.ul[2]), -15)
        self.assertEqual(Transaction.get_balance(self.ul[3]), -15)

    def test_s_tr_creation(self):
        """
        Test all the settle transaction is setted up correctly
        """
        s = self.create_settlement()
        self.assertEqual(s.wait_count, 0)

        # s_tr will be setted
        self.assertEqual(s.settletransaction_set.all().count(), 3)

        self.assertEqual(s.settletransaction_set.get(id=1).amount, 15)
        self.assertEqual(s.settletransaction_set.get(id=2).amount, 15)
        self.assertEqual(s.settletransaction_set.get(id=3).amount, 15)

    def test_s_tr_lock_aquire_creation(self):
        """
        Create the settlement after the lock is acquire.
        (Async S_tr creation)
        Test all the settle transaction is setted up correctly
        """
        create_bill(self.ul, 10)

        s = self.create_settlement()

        self.assertEqual(s.wait_count, 0)

        # s_tr will be setted
        self.assertEqual(s.settletransaction_set.all().count(), 3)

        self.assertEqual(s.settletransaction_set.get(id=1).amount, 17.5)
        self.assertEqual(s.settletransaction_set.get(id=2).amount, 17.5)
        self.assertEqual(s.settletransaction_set.get(id=3).amount, 17.5)

    def test_s_tr_approve_by_from_user(self):
        s = self.create_settlement()

        s_tr = s.settletransaction_set.get(id=1)

        s_tr.approve(s_tr.from_u)

        self.assertEqual(s_tr.state, APPROVED)
        self.assertEqual(s.state, PREPARE)

    def test_s_tr_success_payment(self):
        s = self.create_settlement()

        s_tr = s.settletransaction_set.get(id=1)

        # both user has agree to this payment
        s_tr.approve(s_tr.from_u)
        s_tr.approve(s_tr.to_u)

        # concence this bill
        self.assertEqual(s_tr.state, CONCENCUS)
        self.assertEqual(s.state, PREPARE)

    def test_s_tr_success_finish(self):
        """
        No only need to test all the s_tr is finished,
        but also all the bill state is swith to finsh
        """
        s = self.create_settlement()

        for s_tr in s.settletransaction_set.all():

            # both user has agree to this payment
            s_tr.approve(s_tr.from_u)
            s_tr.approve(s_tr.to_u)

        self.assertEqual(s.state, FINISH)
        self.assertEqual(s.bill_set.first().state, FINISH)

    def test_s_tr_reject(self):

        s = self.create_settlement()

        s_tr = s.settletransaction_set.get(id=1)

        # from user didn't finished his payment
        s_tr.approve(s_tr.from_u)
        s_tr.reject(s_tr.to_u)

        self.assertEqual(s_tr.state, PREPARE)

    def test_bill_tr_commit(self):
        s = self.create_settlement()
        self.assertEqual(Transaction.objects.first().state, COMMITED)

    def test_settlment_is_attached_to_bill(self):
        s = self.create_settlement()

        self.assertEqual(Bill.objects.first().settlement, s)
        self.assertEqual(Bill.objects.filter(settlement=s).count(), 3)

    def test_settlement_is_attached_to_async_bill(self):
        """
        prepare bill will be attached to ongoing attachment 
        """
        bill = create_bill(self.ul, 10, PREPARE)
        s = self.create_settlement()
        # update the object, the object will be attach the settlment
        bill.refresh_from_db()
        self.assertEqual(bill.settlement, s)

    def test_s_tr_async_concencus_s_tr_create(self):
        """
        Async tr is concencus will be directly
        going to concencus state
        """
        bill = create_bill(self.ul, 10, PREPARE)

        s = self.create_settlement()

        self.assertEqual(s.wait_count, 1)

        # sync to update bill with settlment attached
        bill.refresh_from_db()

        # call the internal method, approved by all the user
        bill.approve(self.ul[0])
        bill.approve(self.ul[1])
        bill.approve(self.ul[2])
        bill.approve(self.ul[3])

        # I should be observed all the bill will be directly to
        # committed, all the s_tr will be setted up
        s.refresh_from_db()
        self.assertEqual(s.wait_count, 0)
        self.assertEqual(bill.state, COMMITED)
        self.assertEqual(s.settletransaction_set.all().count(), 3)

    def test_get_balance_by_settlement(self):
        s = self.create_settlement()
        self.assertEqual(Transaction.get_balance(self.ul[0], s), 45)
        self.assertEqual(Transaction.get_balance(self.ul[1], s), -15)
        self.assertEqual(Transaction.get_balance(self.ul[2], s), -15)
        self.assertEqual(Transaction.get_balance(self.ul[3], s), -15)

        create_bill(self.ul, 10)

        # uneffected even create more bill
        self.assertEqual(Transaction.get_balance(self.ul[0], s), 45)
        self.assertEqual(Transaction.get_balance(self.ul[1], s), -15)
        self.assertEqual(Transaction.get_balance(self.ul[2], s), -15)
        self.assertEqual(Transaction.get_balance(self.ul[3], s), -15)

    def test_get_waiting_bill(self):
        bill1 = create_bill(self.ul, 10, PREPARE)
        bill2 = create_bill(self.ul, 10, PREPARE)

        s = self.create_settlement()

        # should be waiting for two bill
        self.assertEqual(s.get_waiting_bill().count(), 2)
        # these two should be first and second bill
        self.assertEqual(s.get_waiting_bill()[0], bill1)
        self.assertEqual(s.get_waiting_bill()[1], bill2)

    def test_delete_waiting_bill_start_up_settlement(self):
        bill1 = create_bill(self.ul, 10, PREPARE)
        s = self.create_settlement()
        self.assertEqual(s.state, SUSPEND)
        bill1.refresh_from_db()
        bill1.delete()
        s.refresh_from_db()
        self.assertEqual(s.wait_count, 0)
        self.assertEqual(s.state, PREPARE)
        self.assertEqual(s.settletransaction_set.count(), 3)
