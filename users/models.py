from django.contrib.auth.models import (
    User
)
from django.db import models
from budget.models import (
    Category,
)


class UsersCategory(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE, parent_link=True)
    category = models.ManyToManyField(
        Category,
    )
