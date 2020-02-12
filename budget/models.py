from django.db import models


# class User(models.Model):
#     username = models.CharField(max_length=32, unique=True)
#     password = models.CharField(max_length=32)


class Category(models.Model):
    name = models.CharField(max_length=32)


class Income(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    comment = models.CharField(max_length=255)


class Expenses(models.Model):
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    comment = models.CharField(max_length=255)
