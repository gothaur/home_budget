from django.contrib.auth.models import (
    User,
)
from django.db import (
    models,
)


class Category(models.Model):
    name = models.CharField(
        max_length=32,
        unique=True,
    )
    default_category = models.BooleanField()

    def __str__(self):
        return self.name


class Income(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    comment = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Expenses(models.Model):
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    comment = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
