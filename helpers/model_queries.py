import datetime

def addQuery(tableName, properties, values):
    return f'INSERT INTO {tableName}({",".join(properties)}) VALUES({[mappingTypeValue(value) for value in values]})'

def editQuery(tableName, properties, values, param):
    return f'UPDATE {tableName} SET ({",".join(properties)} = {[mappingTypeValue(value) for value in values]} WHERE {param or "1 = 1"}'

def deleteQuery(tableName, param):
    return f'DELETE FROM {tableName} WHERE {param or "1 <> 1"}'

def getQuery(tableName, properties, alias, filter):
    return f'SELECT {",".join(properties) or "*"} FROM {tableName} WHERE 1 = 1 AND {filter}'

def mappingTypeValue(value):
    if type(value) is str:
        return '"' + value + '"'
    elif type(value) is datetime.datetime:
        return value.isoformat()
    return str(value)
