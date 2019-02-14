from django.db import models
from django.db.models import CharField, DateTimeField,\
    ForeignKey, DecimalField, PositiveIntegerField, \
    Sum, Value, Q
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User
from BillGroups.models import BillGroups
from django.dispatch import receiver
from django.db.models.signals import post_save

"""
Three-phase-commit
https://en.wikipedia.org/wiki/Three-phase_commit_protocol
Prepare -> Approved -(all)-> Concencus -(settle)-> Committed-> Finished
↑                   -(rejected)-> Suspend -> (deleted)
-----------------------------------|
"""
# state reference
PREPARE = 'PR'
APPROVED = 'AP'
REJECTED = 'RJ'
CONCENCUS = 'CS'
COMMITED = 'CD'
FINISH = 'FN'
SUSPEND = 'SP'


class TimestampModel(models.Model):
    """
    Abstract model which will record timestamp
    while doing operation
    """
    # timestamp for modify and creation
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class StatefulTransactionModel(models.Model):
    """
    all those model will share these five stages
    Prepare, Approve, Concencus, Finished
             Reject,  Suspend
    """
    class Meta:
        abstract = True
    """
    This related name will be name by class, more about this at:
    https://docs.djangoproject.com/en/1.7/topics/db/models/#abstract-related-name
    So, if I want to get this value, I need to use
    st.SettlementTransaction_from_user
    """
    from_u = ForeignKey(User, on_delete=models.PROTECT,
                        related_name="%(class)s_from_user")
    to_u = ForeignKey(User, on_delete=models.PROTECT,
                      related_name="%(class)s_to_user")
    # how much money is performed in this transaction
    amount = DecimalField(max_digits=16, decimal_places=2)
    # current state of this transaction
    state = CharField(
        max_length=2,
        # state is limited to these type
        choices=(
            (PREPARE, "Prepare"),
            (APPROVED, "Approved"),
            (REJECTED, "Recected"),
            (CONCENCUS, "Concencus"),
            (FINISH, "Finish"),
            (SUSPEND, "Suspend"),
        ),
        default=PREPARE
    )


class Bill(TimestampModel):
    # informaqtion about this bill
    title = CharField(max_length=255)
    description = CharField(max_length=2048, blank=True)
    # creator of this bill
    owner = ForeignKey(User, on_delete=models.PROTECT)
    group = ForeignKey(BillGroups, on_delete=models.PROTECT)

    """
    Settlement will be attach to a bill 
    Nullable foreign key will require both nullable and blankable 
    https://stackoverflow.com/questions/16589069/foreignkey-does-not-allow-null-values
    Blankable is for validator, nullable is for database creation 
    """
    settlement = ForeignKey(
        'Settlement', on_delete=models.PROTECT, null=True, blank=True)

    @property
    def state(self):
        # maping of the state from transaction
        s = {
            PREPARE: PREPARE,
            APPROVED: PREPARE,
            REJECTED: SUSPEND,
            CONCENCUS: CONCENCUS,
            COMMITED: COMMITED,
            FINISH: FINISH,
            SUSPEND: SUSPEND,
            None: SUSPEND
        }
        # get random one of tr
        # and return its mapping
        return s[self.transaction_set.first().state]

    def tr_state_update(self, request_uesr, to_state):
        """
        @request_user: who make this request 
        @to_state: which state is this request is make to 

        @pre: tr update is successful 

        @post: if forall tr.state == APPROVE and \
                tr.bill.settlement == NULL
                then all tr.state == CONCENCUS 
        @post: if forall tr.state == APPROVE and \
                tr.bill.settlement != NULL
                then all tr.state == COMMITED
        @post: if to_state == REJECTED and \
                then for all tr.state != REJECTED, tr.state = REJECTED and 
                this.exclude(tr__state = REJECTED).count() == 1
        """
        # filter out the transaction set might need to update
        trs = self.transaction_set.all()

        if to_state == APPROVED:
            if trs.exclude(state=APPROVED).count() == 0:

                # decrease the lock of settlement
                # if there's any
                if self.settlement != None:
                    self.settlement.wait_count -= 1
                    self.settlement.save()

                    # if the settelment is attached,
                    # then the state is directly to COMMITED
                    trs.update(state=COMMITED)
                    return

                # ELSE
                # all transations are approved
                # push to next stage for all the transactions
                trs.update(state=CONCENCUS)

            else:
                # need more waiting
                return
        elif to_state == REJECTED:
            # push all the bill to suspend state
            for tr in trs.exclude(from_u=request_uesr):
                tr.state = SUSPEND
                tr.save()

    @classmethod
    def approve_all(cls, request_user):
        # find all the pending bill he need to pay,
        # then pay them all
        bills = cls.objects\
            .filter(
                transaction__state=PREPARE,
                transaction__from_u=request_user
            )

        """
        O(n^2) operation, no way to get faster 
        """
        for b in bills:
            b.approve(request_user)

    def approve(self, request_uesr):
        # the transactions need to approved by request user
        if self.transaction_set.get(from_u=request_uesr).approve():
            self.tr_state_update(request_uesr, APPROVED)

    def reject(self, request_uesr):
        if self.transaction_set.get(
                from_u=request_uesr
        ).reject():
            self.tr_state_update(request_uesr, REJECTED)

    def resume(self, request_user):
        if request_user == self.owner:
            for tr in self.transaction_set.all():
                tr.resume()
                if tr.from_u == request_user:
                    tr.approve()
            return True
        return False

    def commit(self):
        """
        Non 'public' method, it's called by Settlement class 
        """
        if self.state == CONCENCUS:
            for tr in self.transaction_set.all():
                # update all it's transaction to commit
                tr.commit()
            return True
        return False

    def revoke(self):
        if self.state == COMMITED:
            for tr in self.transaction_set.all():
                # update all it's transaction to CONCENCUS
                tr.revoke()
            return True
        return False


class Transaction(StatefulTransactionModel):
    # user who participate in this transaction

    # to_u = ForeignKey(
    #     User, on_delete=models.PROTECT, related_name="to_user")
    # we can assume every transaction has a bill
    bill = ForeignKey(Bill, on_delete=models.CASCADE)

    @property
    def owner(self):
        # is the the bill owner can setup this transactions
        return self.bill.owner

    def approve(self):
        """
        @pre: request user == self.from_u 
        """
        if self.state == PREPARE:
            # only the prepare state can go be approved
            self.state = APPROVED
            self.save()
            return True
        return False

    def reject(self):
        """
        @pre: request_uesr = self.from_u
        """
        # push this transaction to reject state
        if self.state == PREPARE:
            self.state = REJECTED
            self.save()
            return True
        return False

    def resume(self):
        if self.state in [REJECTED, SUSPEND]:
            self.state = PREPARE
            self.save()
            return True
        return False

    def commit(self):
        """
        @pre self.state == CONCENCUS
        """
        self.state = COMMITED
        self.save()

    def revoke(self):
        """
        @pre self.state == COMMITED
        """
        self.state = CONCENCUS
        self.save()

    @classmethod
    def get_balance(cls, user, settle=None):
        """
        @post: settle== None ==> return == balance with all unfinished and concus bill
        @post: settle!= None ==> 
            return == balance with all unfinished and concus bill
            and bill == settle
        """
        # construct the basic query
        query = cls.objects
        if settle != None:
            # update the query and filter
            # filter by the given settle
            query = query.filter(bill__settlement=settle)

        # calculate the given user's balance
        # Coalesce is to provide a 0 when the none type is occour
        return query.filter(to_u=user).aggregate(
            asum=Coalesce(Sum('amount'), Value(0))
        )['asum']\
            - query.filter(from_u=user).aggregate(
            asum=Coalesce(Sum('amount'), Value(0))
        )['asum']


class Settlement(TimestampModel):
    """

    Settle transaction is created when the settlement class gain the lock 
    The lock is provided by wait_count, when wait_count count the waiting bill
    is become 0, this settlement gain the lock. 

    Then it will call the method at the end of this file, to creat all the settle 
    transactions.
    """
    title = CharField(max_length=255)
    description = CharField(max_length=2048, blank=True)
    owner = ForeignKey(User, on_delete=models.PROTECT)
    group = ForeignKey(BillGroups, on_delete=models.PROTECT)
    # counter of unfinished integer
    # first save will not trigger s_tr creation
    # after it calculate how many bills it should wait
    wait_count = PositiveIntegerField(default=1)

    @property
    def state(self):
        # before the s_tr is set up, all is suspend
        if self.settletransaction_set.count() == 0:
            return SUSPEND
        # maping of the state from transaction
        s = {
            PREPARE: PREPARE,
            APPROVED: PREPARE,
            REJECTED: SUSPEND,  # Not exist
            CONCENCUS: PREPARE,
            COMMITED: FINISH,  # Not exist
            FINISH: FINISH,
            SUSPEND: PREPARE,  # Not exist in mapping
            None: PREPARE
        }
        # get random one of tr
        # and return its mapping
        return s[self.settletransaction_set.first().state]

    def try_finish(self):
        """
        When all the s_tr is concencus, finish all the tr,
        and finish all the bills
        """

        if self.settletransaction_set.exclude(
                state=CONCENCUS).count() == 0:
            # there's no more s_tr to wait, end this s_tr and
            # finish all the bills
            self.settletransaction_set.filter(
                state=CONCENCUS).update(state=FINISH)
            Transaction.objects.filter(
                state=COMMITED,
                bill__settlement__id=self.id
            ).update(state=FINISH)

    def get_waiting_bill(self):
        """
        return:list<bill> 
        @post:  forall bill in return ==> bill.state != COMMITED && bill.state != FINISHED
        """
        return Bill.objects\
            .exclude(transaction__state=COMMITED)\
            .exclude(transaction__state=FINISH)\
            .distinct()


@receiver(post_save, sender=Settlement)
def attach_settle_transactions(sender, instance, created, *args, **kwargs):
    """
    Use post save signal to setup a lock,
    s_tr will be setted until the lock is 0
    """
    if created:
        # set up the lock counter
        pending_bill = Bill.objects.filter(
            group=instance.group
        ).exclude(
            Q(transaction__state=FINISH) |
            Q(transaction__state=COMMITED)
        ).distinct()
        # these are the bill need to attach to this settlemnt
        pending_bill.update(settlement=instance)

        # remove the concencus bill, these bill we don't need to wait
        instance.wait_count = pending_bill.exclude(
            transaction__state=CONCENCUS
        ).count()
        instance.save()

        # Commit all the concencus tr
        Transaction.objects.filter(
            state=CONCENCUS,
            bill__group=instance.group
        ).update(state=COMMITED)

    # we gain the lock to start s_tr
    if instance.wait_count == 0 and instance.settletransaction_set.count() == 0:
        # user list for this group
        # there's no need for owner transfer money to owner
        ul = instance.group.user_set.all().exclude(
            pk=instance.group.owner.id)
        for u in ul:
            assert(ul.count() == 3)
            # amount of this tr
            amount = Transaction.get_balance(u)

            """
            base on the balance to decide the transfer direction
            """
            if amount < 0:
                instance.settletransaction_set.create(
                    from_u=u,
                    to_u=instance.group.owner,
                    amount=-amount
                )
                continue
            if amount > 0:
                instance.settletransaction_set.create(
                    to_u=u,
                    from_u=instance.group.owner,
                    amount=-amount
                )


class SettleTransaction(StatefulTransactionModel):
    """
    Because the behaviour of stage changes is different
    And included stage is different 
    @invariant: from_u != to_u
    """
    modified = DateTimeField(auto_now=True)
    settle = ForeignKey(Settlement, on_delete=models.CASCADE)

    def approve(self, request_user):
        """
        Approve the transaction by from_u then concencus by to_u
        Or error 
        """
        if self.state == PREPARE and request_user == self.from_u:
            self.state = APPROVED
            self.save()
            return True
        if self.state == APPROVED and request_user == self.to_u:
            self.state = CONCENCUS
            self.save()

            # this method is probe to wrong,
            # circular call is shown
            self.settle.try_finish()
            return True
        # else
        return False

    def reject(self, request_user):
        """
        to_user reject this is to revoke back to waiting 
        """
        if self.state == APPROVED and request_user == self.to_u:
            self.state = PREPARE
            self.save()
            return True
        return False
