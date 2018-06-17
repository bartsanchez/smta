from django import test

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
