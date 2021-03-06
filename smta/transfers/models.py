import threading

from django.db import models
from django.db import transaction

from users import models as users_models


TRANSFER_STATE_CHOICES = (
    ('PENDING', 'Pending'),
    ('COMPLETED', 'Completed'),
)


class Transfer(models.Model):
    from_user = models.ForeignKey(
        users_models.User,
        on_delete=models.CASCADE,
        related_name='sent_transfers',
    )
    to_user = models.ForeignKey(
        users_models.User,
        on_delete=models.CASCADE,
        related_name='received_transfers',
    )
    quantity = models.FloatField()
    state = models.CharField(
        max_length=10,
        choices=TRANSFER_STATE_CHOICES,
        default='PENDING',
        editable=False,
    )

    def __str__(self):
        return '{0} transfers {1} to {2}'.format(
            self.from_user,
            self.quantity,
            self.to_user,
        )

    @transaction.atomic
    def execute_transfer(self):
        lock = threading.Lock()
        with lock:
            if self.state == 'COMPLETED':
                return False

            self.from_user.balance -= self.quantity
            self.to_user.balance += self.quantity
            self.from_user.save()
            self.to_user.save()

            self.state = 'COMPLETED'
            self.save()

        return True
