from django import test

from users import factories


class UserModelTests(test.TestCase):
    def test_str(self):
        user = factories.UserFactory(username='foo')

        self.assertEqual(str(user), 'foo')
