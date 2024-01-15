from django.core.exceptions import ValidationError
from django.utils.timezone import now, timedelta

import re

def defaut_date():
    # Next 2 days if it is Saturday
    return now() + timedelta(days=1) if now().weekday() != 5 else now() + timedelta(days=2)

def validate_alphanumeric(value: str) -> None:
    if not re.match('^[a-zA-Z0-9]+$', value):
        raise ValidationError('Not an alphanumeric text')
    
def validate_po(value: str) -> None:
    if not re.match('^[a-zA-Z0-9-]+$', value):
        raise ValidationError('Not a valid PO')
