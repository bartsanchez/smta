from django import test
from django.contrib.auth import models as auth_models
from django.core import exceptions

from rest_framework import test as drf_test

from users import factories as user_factories
from users import models as user_models

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

    def test_execute_transfer__do_not_allow_twice(self):
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
        self.assertFalse(transfer.execute_transfer())


class TransferSignalTests(test.TestCase):
    def test_same_origin_and_destiny(self):
        user = user_factories.UserFactory()
        self.assertRaisesRegex(
            exceptions.ValidationError,
            'It is not possible to make transfers to the same person who send '
            'the money.',
            factories.TransferFactory,
            from_user=user,
            to_user=user,
            quantity=10
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
            'state': 'PENDING',
        }
        self.client.post('/transfers/', transfer_data)

        response = self.client.get('/transfers/', follow=True)

        self.assertEqual(response.status_code, 200)

        transfer = models.Transfer.objects.first()
        url = 'http://testserver/transfers/{0}/'.format(transfer.pk)
        execute_url = '{0}execute/'.format(url)
        transfer_data.update({'url': url, 'execute_url': execute_url})

        self.assertListEqual(response.json(), [transfer_data])

    def test_execute__OK(self):
        transfer = factories.TransferFactory()

        response = self.client.post(
            '/transfers/{0}/execute/'.format(transfer.pk),
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['detail'], 'Success')

    def test_execute__twice(self):
        transfer = factories.TransferFactory()

        response = self.client.post(
            '/transfers/{0}/execute/'.format(transfer.pk),
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['detail'], 'Success')

        response = self.client.post(
            '/transfers/{0}/execute/'.format(transfer.pk),
            follow=True
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()['detail'],
            'The order is not ready to be sent.',
        )

    def test_execute__transfer_does_not_exist(self):
        response = self.client.post('/transfers/2022/execute/', follow=True)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['detail'], 'Not found.')

    def test_execute_state_is_not_pending(self):
        transfer = factories.TransferFactory(state='COMPLETED')

        response = self.client.post(
            '/transfers/{0}/execute/'.format(transfer.pk),
            follow=True
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()['detail'],
            'The order is not ready to be sent.',
        )


class NotSuperuserTransferViewsetTests(drf_test.APITestCase):
    fixtures = ['example_users']

    def setUp(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token 19430615fbb3d69f1ad4dd5db6f9a7ddafa193a5'
        )
        self.user = user_models.User.objects.get(username='unprivileged_user')
        self.perm = auth_models.Permission.objects.get(codename='add_transfer')
        self.user.user_permissions.add(self.perm)
        self.assertFalse(self.user.is_superuser)

    def test_execute__is_not_admin_but_he_is_the_sender(self):
        user_receiving = user_models.User.objects.get(
            username='another_user',
        )
        transfer = factories.TransferFactory(
            from_user=self.user,
            to_user=user_receiving,
        )

        response = self.client.post(
            '/transfers/{0}/execute/'.format(transfer.pk),
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['detail'], 'Success')

    def test_execute__is_not_admin_and_he_is_not_the_sender(self):
        user = user_models.User.objects.get(username='another_user')
        user.user_permissions.add(self.perm)

        transfer = factories.TransferFactory(
            from_user=user,
            to_user=self.user,
        )

        response = self.client.post(
            '/transfers/{0}/execute/'.format(transfer.pk),
            follow=True,
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()['detail'],
            'You don\'t have permissions to execute this transfer',
        )
