from datetime import datetime
from decimal import Decimal

def convertValue(value):
    if value == float() | Decimal(): 
        return float(value)
    elif value == datetime():
        return value.isoformat()
    else:
        return value