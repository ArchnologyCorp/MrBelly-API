from datetime import datetime

def convertValue(value):
    match value:
        case datetime():
            return value.isoformat()
        case _:
            return value