import datetime
from enums.methods import Method 

def addQuery(tableName, properties, values):
    return f'INSERT INTO {tableName}({",".join(properties)}) VALUES({",".join([mappingTypeValue(value) for value in values])}) RETURNING id'

def editQuery(tableName, properties, values, param):
    return f'UPDATE {tableName} SET {mappingFields(properties, values, Method.PUT)} WHERE {param or "1 <> 1"}'

def deleteQuery(tableName, param):
    return f'DELETE FROM {tableName} WHERE {param or "1 <> 1"}'

def getQuery(tableName, properties= '*', alias = [], filter = '', group = ''):
    return f"SELECT {mappingFields(properties, alias, Method.GET)} FROM {tableName} WHERE 1 = 1 AND {filter} {group is not '' and f'GROUP BY {group}' or ''}"

def mappingTypeValue(value):
    if type(value) is str:
        return f"'{value}'"
    elif type(value) is datetime.datetime:
        return value.isoformat().replace('"', "'")
    return str(value)

def mappingFields(properties, values, type):
    query = []
    for index, prop in enumerate(properties):
        if(type == Method.PUT):
            query.append(f'{prop} = {mappingTypeValue(values[index])}')
        else:
            if len(values) > 0:
                query.append(f'{prop} {values[index]}')
            else:
                query.append(f'{prop}') 
    return ','.join(query)
    
def createProperties(tupleFields, arrayTables):
    array = []
    for index, fields in enumerate(tupleFields):
        for field in fields:
            array.append(f'{f"{arrayTables[index]}." if arrayTables[index] != "" else ""}{field}')
    return array