from django.test import TestCase
from Bills.models import *
# from .testcase.SettleCase import SettleCase
# from .testcase.BillCase import BillCase
from .testcase import * 
# Create your tests here.


class BillViewCase(TestCase):

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

        self.ul = [
            self.user001,
            self.user002,
            self.user003,
            self.user004,
        ]

        # for the view test part 

