from django.conf import settings
from django.db import (
    models,
)
from django.urls import (
    reverse,
)


class Category(models.Model):
    name = models.CharField(
        max_length=32,
        # unique=True,
    )
    default_category = models.BooleanField()

    def __str__(self):
        return self.name


class Income(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("income-detail", kwargs={'income_id': self.id})


class Expenses(models.Model):
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


# class Message(models.Model):
#     subject = models.CharField(
#         max_length=64,
#     )
#     message = models.TextField()
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE
#     )
