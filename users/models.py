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


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
