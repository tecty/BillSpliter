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

        self.group = BillGroups.objects.create(
            owner=self.user001,
            name="test"
        )
        self.user001.groups.add(self.group)

        self.user_list = [
            self.user001,
            self.user002,
            self.user003,
            self.user004,
        ]

    def test_add_user(self):
        self.group.addUser(self.user002.id)
        self.assertEqual(
            self.user001,
            self.group.user_set.filter(pk=self.user001.id).get()
        )

    def test_del_user(self):
        self.group.addUser(self.user002.id)
        self.group.delUser(self.user002.id)
        self.assertEqual(
            0,
            self.group.user_set.filter(
                pk=self.user002.id
            ).count()
        )
