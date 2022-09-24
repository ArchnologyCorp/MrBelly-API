from repository.db import openConnection, psycopg2
from helpers.json_helper import buildJson
from helpers.sql import *

_tableName = 'tb_cobranca'

def getDebits(user):
    response = []
    try:
        conn = openConnection() 
        cur = conn.cursor()
        cur.execute(getQuery(tableName=f'{_tableName} cobr INNER JOIN tb_usuario usu ON cobr.id_usuario = usu.id', properties=['cobr.id', 'cobr.data_criacao', 'cobr.data_atualizacao', 'cobr.descricao', 'usu.id', 'usu.nome'], filter=f'id_usuario = {user}'))
        users = cur.fetchall()
        response = buildJson({'id': 0, 'creation_date': None, 'updated_at': None, 'description': '', 'id_user': 0, 'name_user': ''}, users)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return response

def getDebit(id, user):
    response = {}
    try:
        conn = openConnection() 
        cur = conn.cursor()
        cur.execute(getQuery(tableName=_tableName, filter=f'id = {int(id)} and id_usuario = {user}'))
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
        cur.execute(addQuery(tableName=_tableName, properties=['descricao, id_usuario'], values=(entity["description"], user)))
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
        cur.execute(editQuery(tableName=_tableName, properties=['descricao', 'data_atualizacao'], values=(entity["description"], 'now()'), param=f'id = {int(id)}'))
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
        cur.execute(deleteQuery(tableName=_tableName, param=f'id = {int(id)}'))
        conn.commit()
        response = True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return response
