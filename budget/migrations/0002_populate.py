# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from budget.models import Category


def populate(apps, schema_editor):
    Category.objects.create(name="Chemia", default_category=True)
    Category.objects.create(name="Kosmetyki", default_category=True)
    Category.objects.create(name="Kotecki", default_category=True)
    Category.objects.create(name="Domek", default_category=True)
    Category.objects.create(name="Inne", default_category=True)
    Category.objects.create(name="Rozrywka", default_category=True)
    Category.objects.create(name="Rachunki", default_category=True)
    Category.objects.create(name="Kredyty", default_category=True)
    Category.objects.create(name="Samochody", default_category=True)
    Category.objects.create(name="Transport", default_category=True)
    Category.objects.create(name="Dzieci", default_category=True)
    Category.objects.create(name="Prezenty", default_category=True)
    Category.objects.create(name="Lekarstwa", default_category=True)
    Category.objects.create(name="Higiena", default_category=True)
    Category.objects.create(name="Zachcianki", default_category=True)


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate),
    ]
