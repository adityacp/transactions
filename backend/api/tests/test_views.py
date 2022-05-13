from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from api.models import Account, Transaction


class AccountTestCase(TestCase):
    """ Test login and get the account information"""

    def setUp(self):
        self.client = APIClient()
        self.username = 'demo_test'
        self.password = 'demo_test'
        self.user = User.objects.create_user(username=self.username,
                                             password=self.password)
        self.account = Account.objects.create(user=self.user, balance=100)

    def tearDown(self):
        self.client.logout()
        User.objects.all().delete()
        Account.objects.all().delete()

    def test_success_login(self):
        data = {'username': 'demo_test', 'password': 'demo_test'}
        response = self.client.post(reverse('api:login'), data)
        response_data = response.json()
        self.assertTrue(Token.objects.filter(user_id=self.user.id).exists())
        self.assertEqual(
            response_data.get("account").get("id"), self.account.id
        )
        self.assertEqual(
            response_data.get("account").get("balance"), self.account.balance
        )

    def test_failed_login(self):
        data = {'username': 'demo_test1', 'password': 'demo_test'}
        response = self.client.post(reverse('api:login'), data)
        response_data = response.json()
        self.assertFalse(response_data.get("success"))


class TransactionTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        # User 1 Account
        self.username1 = 'demo_test1'
        self.password1 = 'demo_test1'
        self.user1 = User.objects.create_user(username=self.username1,
                                             password=self.password1)
        self.token1 = Token.objects.create(user=self.user1)
        self.account1 = Account.objects.create(user=self.user1, balance=100)

        # User 2 Account
        self.username2 = 'demo_test2'
        self.password2 = 'demo_test2'
        self.user2 = User.objects.create_user(username=self.username2,
                                              password=self.password2)
        self.token2 = Token.objects.create(user=self.user2)
        self.account2 = Account.objects.create(user=self.user2, balance=200)

    def test_success_add_transaction(self):
        data = {
            "sender_id": self.account1.id,
            "receiver_id": self.account2.id,
            "reason": "Test Reason",
            "type": "borrow",
            "status": "unpaid",
            "amount": "50"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        response = self.client.post(reverse('api:add_transaction'), data)
        response_data = response.json()
        transaction = Transaction.objects.filter(
            transaction_from_id=self.account1.id
        )
        self.assertTrue(response_data.get("success"))
        self.assertTrue(transaction.exists())
        self.assertEqual(transaction.first().amount, 50)

    def test_fail_add_transaction(self):
        data = {
            "sender_id": self.account1.id,
            "receiver_id": self.account2.id,
            "reason": "Test Reason",
            "type": "borrow",
            "status": "unpaid",
            "amount": "150"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        response = self.client.post(reverse('api:add_transaction'), data)
        response_data = response.json()
        transaction = Transaction.objects.filter(
            transaction_from_id=self.account1.id
        )
        self.assertFalse(response_data.get("success"))
        self.assertFalse(transaction.exists())
        self.assertEqual(response_data.get("message"), "Bearer has low balance")

    def test_get_transactions(self):
        data = {
            "transaction_from_id": self.account1.id,
            "transaction_to_id": self.account2.id,
            "reason": "Test Reason 1",
            "type": "lend",
            "status": "unpaid",
            "amount": "70"
        }
        transaction = Transaction.objects.create(**data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        response = self.client.get(reverse('api:get_transactions'))
        response_data = response.json()
        res_transaction = response_data.get("transactions")[0].get("transaction_id")
        self.assertEqual(str(transaction.transaction_id), res_transaction)
        self.assertTrue(response_data.get("success"))

    def test_get_transactions_with_filter(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        filters = {"filters": {"status": "paid"}}
        response = self.client.post(reverse('api:get_transactions'), filters)
        response_data = response.json()
        self.assertEqual(len(response_data.get("transactions")), 0)

    def test_mark_paid(self):
        data = {
            "transaction_from_id": self.account1.id,
            "transaction_to_id": self.account2.id,
            "reason": "Test Reason 1",
            "type": "lend",
            "status": "unpaid",
            "amount": "70"
        }
        transaction = Transaction.objects.create(**data)
        data = {
            "transaction_id": transaction.transaction_id
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        self.client.post(reverse('api:mark_paid'), data)
        transaction = Transaction.objects.get(
            transaction_id=transaction.transaction_id
        )
        self.assertEqual(transaction.status, "paid")
