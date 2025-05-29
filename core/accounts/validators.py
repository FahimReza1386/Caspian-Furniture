from django.core.exceptions import ValidationError
import re


def validate_iranian_phone_number(value):
    """
    Validates that the phone number is a valid Iranian cellphone number.
    It should start with '09' followed by 9 digits.
    """
    pattern = r'^09\d{9}$'
    if not re.match(pattern, value):
        raise ValidationError('Invalid Iranian cellphone number. It should start with "09" and be followed by 9 digits.')
