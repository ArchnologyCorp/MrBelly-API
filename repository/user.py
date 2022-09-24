from repository.db import openConnection, psycopg2
from helpers.json_helper import buildJson
from helpers.sql import *

def authLogin(phone, password):
    response = None
    try:
        conn = openConnection() 
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM tb_usuario WHERE numero_fone = %s and senha = %s', (f'55{phone}', password))
        authUser = cur.fetchall()
        response = buildJson({'id': 0, 'creation_date': None, 'updated_at': None, 'user': '', 'phone': '', 'password': ''}, authUser)[0]
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return response

def postUser(entity):
    response = {}
    try:
        conn = openConnection() 
        cur = conn.cursor()
        cur.execute(f'INSERT INTO tb_usuario (nome, numero_fone, senha) VALUES(%s,%s,%s) RETURNING id', (entity["name"], entity["phone"], entity["password"]))
        conn.commit()
        entity['id'] = int(cur.fetchone()[0])
        response = entity
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return response

def putUser(entity, id):
    response = {}
    try:
        conn = openConnection() 
        cur = conn.cursor()
        cur.execute('UPDATE tb_usuario SET nome=%s, numero_fone=%s WHERE id=%s', (entity["name"], entity["phone"], id))
        conn.commit()
        response = entity
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return response

def totalByUser(id):
    response = { }
    try:
        conn = openConnection() 
        cur = conn.cursor()
        cur.execute(getQuery(tableName=f'tb_cobranca CB INNER JOIN tb_devedor DV ON CB.id = dv.id_cobranca INNER JOIN tb_usuario Cob ON Cob.id = CB.id_usuario INNER JOIN tb_usuario Dev ON Dev.id = DV.id_usuario', 
                            properties=['Dev.id', 'Cob.id', 'Dev.nome', 'Cob.nome', 'SUM(DV.valor)'], 
                            alias=['id_devedor', 'id_cobrador', 'devedor', 'cobrador', 'total'], 
                            filter=f'Cob.id = {id} OR Dev.id = {id}',
                            group='Dev.Id, Dev.nome, Cob.Id, Cob.nome'))
        tot = cur.fetchall()
        response = buildJson({'id_debtor': 0, 'id_collector': 0, 'debtor': '', 'collector': '', 'total': 0}, tot)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return response