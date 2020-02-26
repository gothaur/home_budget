# from django.contrib.auth.models import AbstractUser
# from django.db import models
# from budget.models import (
#     Category,
# )
#
#
# class User(AbstractUser):
#     category = models.ManyToManyField(
#         Category,
#         through='UserCategory',
#     )
#
#
# class UserCategory(models.Model):
#     user_id = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#     )
#     category_id = models.ForeignKey(
#         Category,
#         on_delete=models.CASCADE,
#     )
#     default_category = models.BooleanField()
