from django.contrib.auth.models import (
    AbstractUser,
)
from django.db import models
from budget.models import (
    Category
)


class User(AbstractUser):
    categories = models.ManyToManyField(
        Category,
    )
