import os

from django.core.exceptions import ValidationError


def validate_file_extension(value):
    valid_extensions = ['.xlsm', '.xlsx']
    ext = os.path.splitext(value.name)[1]

    if ext not in valid_extensions:
        raise ValidationError(u"Obsługowanie rozszerzenia ['.xlsm', '.xlsx']")
