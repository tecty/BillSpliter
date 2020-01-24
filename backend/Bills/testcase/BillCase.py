from .util import *

class BillCase(UserCaseEnv):

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
        bill = create_bill(self.ul, 10)

        self.assertEqual(bill.transaction_set.count(), len(self.ul))
        self.assertEqual(
            bill.transaction_set.first().amount, 10/len(self.ul))
        self.assertEqual(
            bill.transaction_set.first().state, CONCENCUS)

    def test_create_bill_util_with_prepare(self):
        bill = create_bill(self.ul, 10, PREPARE)

        self.assertEqual(bill.transaction_set.count(), len(self.ul))
        self.assertEqual(
            bill.transaction_set.first().amount, 10/len(self.ul))
        self.assertEqual(
            bill.transaction_set.first().state, PREPARE)

    def test_approve_all(self):

        bill1 = create_bill(
            [self.ul[0], self.ul[1]], 10, PREPARE)
        bill2 = create_bill(
            [self.ul[0], self.ul[1], self.ul[2]], 10, PREPARE)

        Bill.approve_all(self.ul[0])
        Bill.approve_all(self.ul[1])

        # update bills
        bill1.refresh_from_db()
        bill2.refresh_from_db()

        # bill1 get all member approved, so it's concencus
        # bill2 need to get user2 concencus, so it still preparing
        self.assertEqual(bill1.state, CONCENCUS)
        self.assertEqual(bill2.state, PREPARE)

    def test_get_process(self):
        bill = create_bill(self.ul, 10, PREPARE)
        self.assertEqual(bill, Bill.get_process(self.user001).first())

    # def test_concencus_bill_prevent_delete(self):
    #     bill1 = create_bill(
    #         [self.ul[0], self.ul[1]], 10, CONCENCUS)
    #     bill_id = bill1.id
    #     try:
    #         bill1.delete()
    #     except Exception as e:
    #         pass
    #     bill1.refresh_from_db()
    #     self.assertEqual(bill1.id, bill_id)

