import factory

from users import factories as users_factories

from transfers import models


class TransferFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Transfer

    from_user = factory.SubFactory(
        users_factories.UserFactory,
        username='paying_user',
    )
    to_user = factory.SubFactory(
        users_factories.UserFactory,
        username='receiving_user',
    )
    quantity = 35.79
