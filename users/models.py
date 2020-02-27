from django.contrib.auth.models import (
    User
)
from django.db import (
    models,
)
from budget.models import (
    Category,
)


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        parent_link=True,
        primary_key=True,
        unique=True,
        )
    categories = models.ManyToManyField(
        Category,
    )
