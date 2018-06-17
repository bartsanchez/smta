from django import dispatch
from django.core import exceptions
from django.db.models import signals

from transfers import models


@dispatch.receiver(
    signals.pre_save,
    sender=models.Transfer,
    dispatch_uid='transfer_should_have_different_users',
)
def transfer_should_have_different_users(sender, instance, **kwargs):
    if instance.from_user.pk == instance.to_user.pk:
        raise exceptions.ValidationError(
            'It is not possible to make transfers to the same person who send '
            'the money.'
        )
