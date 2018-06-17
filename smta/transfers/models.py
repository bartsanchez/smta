from django.db import models

from users import models as users_models


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

    def __str__(self):
        return '{0} transfers {1} to {2}'.format(
            self.from_user,
            self.quantity,
            self.to_user,
        )
