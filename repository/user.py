from repository.db import openConnection, psycopg2
from helpers.json_helper import buildJson

def authLogin(phone, password):
    response = None
    try:
        print(phone)
        print(password)
        conn = openConnection() 
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM tb_usuario WHERE numero_fone = %s and senha = %s', (f'55{phone}', password))
        authUser = cur.fetchall()
        response = buildJson({'id': 0, 'creation_date': None, 'updated_at': None, 'user': '', 'phone': '', 'password': ''}, authUser)[0]
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return response