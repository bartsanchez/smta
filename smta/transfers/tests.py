from django import test

from users import factories as user_factories

from transfers import factories
from transfers import models

from smta import tests


class TransferModelTests(test.TestCase):
    def test_str(self):
        transfer = factories.TransferFactory()

        self.assertEqual(
            str(transfer),
            'paying_user transfers 35.79 to receiving_user'
        )

    def test_execute_transfer(self):
        from_user = user_factories.UserFactory(
            username='paying_user',
            balance=150,
        )
        to_user = user_factories.UserFactory(
            username='receiving_user',
            balance=25,
        )
        transfer = factories.TransferFactory(
            from_user=from_user,
            to_user=to_user,
            quantity=50,
        )

        self.assertTrue(transfer.execute_transfer())
        self.assertEqual(from_user.get_balance(), 100)
        self.assertEqual(to_user.get_balance(), 75)

    def test_execute_transfer__negative(self):
        from_user = user_factories.UserFactory(
            username='paying_user',
            balance=-250.33,
        )
        to_user = user_factories.UserFactory(
            username='receiving_user',
            balance=-1500.708,
        )
        transfer = factories.TransferFactory(
            from_user=from_user,
            to_user=to_user,
            quantity=285.49,
        )

        self.assertTrue(transfer.execute_transfer())
        self.assertEqual(from_user.get_balance(), -535.82)
        self.assertEqual(to_user.get_balance(), -1215.218)


class TransferViewsetTests(tests.AuthenticatedAPITestCase):
    fixtures = ['example_users']

    def test_no_users(self):
        response = self.client.get('/transfers/', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.json(), [])

    def test_new_transfer(self):
        transfer_data = {
            'from_user': 'http://testserver/users/2/',
            'to_user': 'http://testserver/users/3/',
            'quantity': 80486.2,
        }
        self.client.post('/transfers/', transfer_data)

        response = self.client.get('/transfers/', follow=True)

        self.assertEqual(response.status_code, 200)

        transfer = models.Transfer.objects.first()
        url = 'http://testserver/transfers/{0}/'.format(transfer.pk)
        transfer_data.update({'url': url}),

        self.assertListEqual(response.json(), [transfer_data])
