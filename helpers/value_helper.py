from datetime import datetime
from decimal import Decimal

def convertValue(value):
   if isinstance(value, (float, Decimal)):
    return float(value)
   elif isinstance(value, datetime):
        return value.isoformat()
   else:
    return value