import datetime
from traceback import print_tb
from enums.methods import Method 

def addQuery(tableName, properties, values):
    return f'INSERT INTO {tableName}({",".join(properties)}) VALUES({",".join([mappingTypeValue(value) for value in values])}) RETURNING id'

def editQuery(tableName, properties, values, param):
    return f'UPDATE {tableName} SET {mappingFields(properties, values, Method.PUT)} WHERE {param or "1 <> 1"}'

def deleteQuery(tableName, param):
    return f'DELETE FROM {tableName} WHERE {param or "1 <> 1"}'

def getQuery(tableName, properties= '*', alias = [], filter = ''):
    return f'SELECT {mappingFields(properties, alias, Method.GET)} FROM {tableName} WHERE 1 = 1 AND {filter}'

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
            # Tratar ele, tá dodói
            # query.append(f'{prop} as {prop}') 
            query.append(f'{prop}') 
    print(','.join(query))
    return ','.join(query)
    
