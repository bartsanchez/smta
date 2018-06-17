from django import test

from unittest import mock

from rest_framework import test as drf_test

from users import models
from users import factories
from smta import tests


class UserModelTests(test.TestCase):
    def test_str(self):
        user = factories.UserFactory(username='foo')

        self.assertEqual(str(user), 'foo')

    def test_get_balance__default(self):
        user = factories.UserFactory()

        self.assertEqual(user.get_balance(), 0.0)

    def test_get_balance__positive(self):
        user = factories.UserFactory(balance=1984.33)

        self.assertEqual(user.get_balance(), 1984.33)

    def test_get_balance__negative(self):
        user = factories.UserFactory(balance=-70.8)

        self.assertEqual(user.get_balance(), -70.8)


class NonAuthUserEndpointsPermsTests(test.TestCase):
    def setUp(self):
        self.client = test.Client()

    def test_is_forbidden_for_non_auth_users(self):
        response = self.client.get('/users/', follow=True)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()['detail'],
            'Authentication credentials were not provided.',
        )


class AuthUserEndpointsPermsTests(tests.AuthenticatedAPITestCase):
    def test_is_allowed_for_auth_users(self):
        response = self.client.get('/users/', follow=True)

        self.assertEqual(response.status_code, 200)


class UserViewsetTests(tests.AuthenticatedAPITestCase):
    def test_no_users(self):
        response = self.client.get('/users/', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.json(), [])

    def test_new_user(self):
        self.client.post('/users/', {'username': 'foo'})
        response = self.client.get('/users/', follow=True)

        self.assertEqual(response.status_code, 200)

        user = models.User.objects.get(username='foo')

        self.assertListEqual(
            response.json(),
            [{
                'username': 'foo',
                'url': 'http://testserver/users/{0}/'.format(user.pk),
            }]
        )

    def test_two_users(self):
        self.client.post('/users/', {'username': 'foo'})
        self.client.post('/users/', {'username': 'bar'})
        response = self.client.get('/users/', follow=True)

        response_json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_json), 2)
        self.assertEqual(response_json[0]['username'], 'foo')
        self.assertEqual(response_json[1]['username'], 'bar')

    def test_balance__user_does_not_exist(self):
        response = self.client.get('/users/8888/balance', follow=True)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['detail'], 'Not found.')

    @mock.patch('users.models.User.get_balance', return_value=-777.94)
    def test_balance__is_admin(self, balance_mock):
        self.client.post('/users/', {'username': 'foo'})

        user = models.User.objects.get(username='foo')

        response = self.client.get(
            '/users/{0}/balance'.format(user.pk),
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['balance'], -777.94)

        balance_mock.assert_called_once_with()


class NotSuperuserUserViewsetTests(drf_test.APITestCase):
    fixtures = ['example_users']

    def setUp(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token 19430615fbb3d69f1ad4dd5db6f9a7ddafa193a5'
        )
        self.user = models.User.objects.get(username='unprivileged_user')
        self.assertFalse(self.user.is_superuser)

    @mock.patch('users.models.User.get_balance', return_value=666.66)
    def test_balance__is_not_admin_but_it_is_its_balance(self, balance_mock):
        response = self.client.get(
            '/users/{0}/balance'.format(self.user.pk),
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['balance'], 666.66)

        balance_mock.assert_called_once_with()

    def test_balance__is_not_admin_and_is_not_its_balance(self):
        user = models.User.objects.get(username='another_user')

        response = self.client.get(
            '/users/{0}/balance'.format(user.pk),
            follow=True,
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()['detail'],
            'You don\'t have permissions to view this balance',
        )
