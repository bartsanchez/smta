from django import test

from users import models
from users import factories
from smta import tests


class UserModelTests(test.TestCase):
    def test_str(self):
        user = factories.UserFactory(username='foo')

        self.assertEqual(str(user), 'foo')


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
