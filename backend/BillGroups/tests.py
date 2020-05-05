from django.test import TestCase
from .models import *
# Create your tests here.


class GroupCase(TestCase):
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

        self.group = BillGroup.objects.create(
            owner=self.user001,
            name="test"
        )

        self.user_list = [
            self.user001,
            self.user002,
            self.user003,
            self.user004,
        ]

    def test_owner_invite(self):
        self.group.invite(self.user001,self.user002)
        self.group.approve(self.user002,self.user002)
        self.assertEqual(
            self.group.isMember(self.user002), True
        )

    def test_member_invite(self):
        self.group.invite(self.user001,self.user002)
        self.group.approve(self.user002,self.user002)

        self.group.invite(self.user002,self.user003)
        self.group.approve(self.user003,self.user003)

        self.assertEqual(
            self.group.isMember(self.user003), True
        )

    def test_del_user(self):
        self.group.invite(self.user001,self.user002)
        self.group.approve(self.user002,self.user002)

        self.group.delUser(self.user001,self.user002)
        self.assertEqual(
            self.group.isMember(self.user002), False
        )
