from django.db import models
from django.db.models import CharField, DateTimeField,\
    ForeignKey, DecimalField
from django.contrib.auth.models import User, Group


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


class Bill(TimestampModel):
    # informaqtion about this bill
    title = CharField(max_length=255)
    description = CharField(max_length=2048, blank=True)
    # creator of this bill
    owner = ForeignKey(User, on_delete=models.PROTECT)
    group = ForeignKey(Group, on_delete=models.PROTECT)

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
                tr.sate = SUSPEND
                tr.save()

    def approve(self, request_uesr):
        # the transactions need to approved by request user
        if self.transaction_set.get(from_u=request_uesr).approve():
            self.tr_state_update(request_uesr, APPROVED)

    def reject(self, request_uesr):
        if self.transaction_set.get(from_u=request_uesr).reject():
            self.tr_state_update(request_uesr, REJECTED)

    def resume(self, request_user):
        if request_user == self.owner:
            for tr in self.transaction_set.all():
                tr.resume()
                if tr.from_u == request_user:
                    tr.approve()
            return True
        return False


class Transaction(TimestampModel):
    # we can assume every transaction has a bill
    bill = ForeignKey(Bill, on_delete=models.CASCADE)
    # user who participate in this transaction
    from_u = ForeignKey(User, on_delete=models.PROTECT, related_name="from_u")
    to_u = ForeignKey(User, on_delete=models.PROTECT, related_name="to_u")
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
            (COMMITED, "Commited"),
            (FINISH, "Finish"),
            (SUSPEND, "Suspend"),
        ),
        default=PREPARE
    )

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
