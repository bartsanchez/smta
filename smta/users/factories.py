import factory

from users import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    username = 'Fake User'
