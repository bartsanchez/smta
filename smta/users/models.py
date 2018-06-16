from django.contrib.auth import models as auth_models
from django.db import models


class User(auth_models.User):
    balance = models.FloatField(default=0)

    def __str__(self):
        return self.username

    def get_balance(self):
        return self.balance
