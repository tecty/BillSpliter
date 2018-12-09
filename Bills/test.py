from django.test import TestCase
from Bills.models import *
# Create your tests here.


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

        self.group = Group.objects.create(name="test")
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
