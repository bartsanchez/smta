from django.contrib.auth import models


class User(models.User):
    pass

    def __str__(self):
        return self.username
