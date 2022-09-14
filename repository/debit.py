from pydoc import resolve
from repository.db import openConnection, psycopg2
from helpers.json_helper import buildJson

def getDebits(user):
    response = []
    try:
        conn = openConnection() 
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM tb_cobranca WHERE id_usuario = {user}')
        users = cur.fetchall()
        response = buildJson({'id': 0, 'creation_date': None, 'updated_at': None, 'description': '', 'id_user': 0}, users)
            
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return response

def getDebit(id, user):
    response = {}
    try:
        conn = openConnection() 
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM tb_cobranca WHERE id = {int(id)} and id_usuario = {user}')
        data = cur.fetchall()
        response = buildJson({'id': 0, 'creation_date': None, 'updated_at': None, 'description': '', 'id_user': 0}, data)[0]
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return response

def postDebit(entity, user):
    response = {}
    try:
        conn = openConnection() 
        cur = conn.cursor()
        cur.execute(f'INSERT INTO tb_cobranca (descricao, id_usuario) VALUES(%s,%s) RETURNING id', (entity["description"], user))
        conn.commit()
        entity['id'] = int(cur.fetchone()[0])
        response = entity
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return response

def putDebit(id, entity):
    response = False
    try:
        conn = openConnection() 
        cur = conn.cursor()
        cur.execute(f'UPDATE tb_cobranca SET descricao = %s, data_atualizacao = now() WHERE id = %s', (entity["description"], id))
        conn.commit()
        response = True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return response

def deleteDebit(id):
    response = False
    try:
        conn = openConnection() 
        cur = conn.cursor()
        cur.execute(f'DELETE FROM tb_cobranca WHERE id = {int(id)}')
        conn.commit()
        response = True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return response
