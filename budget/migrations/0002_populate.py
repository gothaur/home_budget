# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from budget.models import Category


def populate(apps, schema_editor):
    Category.objects.create(name="Chemia")
    Category.objects.create(name="Kosmetyki")
    Category.objects.create(name="Kotecki")
    Category.objects.create(name="Domek")
    Category.objects.create(name="Inne")
    Category.objects.create(name="Rozrywka")
    Category.objects.create(name="Rachunki")
    Category.objects.create(name="Kredyty")
    Category.objects.create(name="Samochody")
    Category.objects.create(name="Transport")
    Category.objects.create(name="Dzieci")
    Category.objects.create(name="Prezenty")
    Category.objects.create(name="Lekarstwa")
    Category.objects.create(name="Higiena")
    Category.objects.create(name="Zachcianki")


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate),
    ]
