import psycopg2
from datetime import datetime

def openConnection():
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(
        host="ec2-3-223-242-224.compute-1.amazonaws.com", 
        database="dcusk4ojn43g3h",
        user="txtfgbvmfpcowk",
        password="a1696082d98712652af6daeafb7eae810e09817056ce48f37b5a39687ca6689c")
    return conn

def getDebits():
    response = []
    try:
        conn = openConnection() 
        cur = conn.cursor()
        cur.execute('SELECT * FROM tb_cobranca')
        users = cur.fetchall()
        response = buildJson({'id': 0, 'creation_date': None, 'updated_at': None, 'description': '', 'id_user': 0}, users)
            
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return response

def buildJson(obj, values):
    array = []
    for value in values:
        body = {}
        for index, key in enumerate(obj.keys()):
            body[key] = convertValue(value[index])
        array.append(body)
    return array

def convertValue(value):
    match value:
        case datetime():
            return value.isoformat()
        case _:
            return value