from django import test

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
