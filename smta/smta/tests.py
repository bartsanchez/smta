from django.contrib import auth
from django.contrib.auth import hashers

from rest_framework import test
from rest_framework.authtoken import models


class AuthenticatedAPITestCase(test.APITestCase):
    def setUp(self):
        user = auth.get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password=hashers.UNUSABLE_PASSWORD_PREFIX,
        )
        token = models.Token.objects.create(user=user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token {0}'.format(token),
        )
