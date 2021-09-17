from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='account')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    username = models.CharField(max_length=20)
    idn = models.CharField(max_length=10)
    balance = models.FloatField(default=0)

    def __str__(self):
        return f'{self.username} - {self.balance}'