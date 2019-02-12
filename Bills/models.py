from django.db import models
from django.db.models import CharField, DateTimeField,\
    ForeignKey, DecimalField
from django.contrib.auth.models import User
from BillGroups.models import BillGroups

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


class Settlement(TimestampModel):
    title = CharField(max_length=255)
    description = CharField(max_length=2048, blank=True)
    owner = ForeignKey(User, on_delete=models.PROTECT)
    group = ForeignKey(BillGroups, on_delete=models.PROTECT)


class SettleTransaction(StatefulTransactionModel):
    """
    Because the behaviour of stage changes is different
    And included stage is different 
    """
    settle = ForeignKey(Settlement, on_delete=models.CASCADE)


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
        Settlement, on_delete=models.PROTECT, null=True, blank=True)

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
        """
        # filter out the transaction set might need to update
        trs = self.transaction_set.all()

        if to_state == APPROVED:
            if trs.exclude(from_u=request_uesr).count() == \
                    trs.exclude(from_u=request_uesr)\
                    .filter(state=APPROVED).count():
                # all transations are approved
                # push to next stage for all the transactions
                for tr in trs:
                    tr.state = CONCENCUS
                    tr.save()
            else:
                # need more waiting
                return
        elif to_state == REJECTED:
            # push all the bill to suspend state
            for tr in trs.exclude(from_u=request_uesr):
                tr.state = SUSPEND
                tr.save()

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
