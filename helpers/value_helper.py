from datetime import datetime
from decimal import Decimal

def convertValue(value):
    match value:
        case float() | Decimal():
            return float(value)
        case datetime():
            return value.isoformat()
        case _:
            return value