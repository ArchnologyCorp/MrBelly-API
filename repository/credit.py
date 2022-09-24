from repository.db import openConnection, psycopg2
from helpers.json_helper import buildJson
from utils.array import removeByList
from helpers.sql import *
from datetime import datetime

_tableName = 'tb_devedor'

_propertiesSQl = [
    'id',
    'data_criacao',
    'data_atualizacao',
    'data_cobranca',
    'valor',
    'observacao',
    'is_pago',
    'is_recebido',
    'id_cobranca',
    'id_usuario']

_propertiesObj = {
    'id': 0,
    'creation_date': datetime.today(),
    'updated_at': None,
    'credit_date': datetime.today(),
    'value': 0.0,
    'observation': '',
    'is_paid_out': False,
    'is_debited': False,
    'id_credit': 0,
    'id_user': 0}

_properties = _propertiesObj.keys()


def getCredits(user):
    response = []
    try:
        sql = f'''{_tableName} cred 
                INNER JOIN tb_cobranca debit ON debit.id = cred.id_cobranca
                INNER JOIN tb_usuario usu ON usuD.id = debit.id_usuario 
                INNER JOIN tb_usuario usu ON usuC.id = cred.id_usuario 
                '''
        _properties_ = createProperties(
            [_propertiesSQl, ['id', 'nome'], ['id', 'nome']], ['cobr', 'usuC', 'usuD'])

        conn = openConnection()
        cur = conn.cursor()
        cur.execute(getQuery(tableName=sql, properties=_properties_, filter=f'id_usuario = {user}'))
        credits = cur.fetchall()
        response = buildJson(_propertiesObj.update({
            'id_user_credit': 0, 'name_user_credit': '', 'id_user_debit': 0, 'name_user_debit': ''}), credits)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return response


def getCredit(id, user):
    response = {}
    try:
        sql = f'''{_tableName} cred 
                INNER JOIN tb_cobranca debit ON debit.id = cred.id_cobranca
                INNER JOIN tb_usuario usu ON usuD.id = debit.id_usuario 
                INNER JOIN tb_usuario usu ON usuC.id = cred.id_usuario 
                '''
        _properties_ = createProperties(
            [_propertiesSQl, ['id', 'nome'], ['id', 'nome']], ['cobr', 'usuC', 'usuD'])

        conn = openConnection()
        cur = conn.cursor()
        cur.execute(getQuery(
            tableName=sql, properties=_properties_, filter=f'cred.id = {int(id)} and cred.id_usuario = {user}'))
        data = cur.fetchall()
        response = buildJson(_propertiesObj.update({
            'id_user_credit': 0, 'name_user_credit': '', 'id_user_debit': 0, 'name_user_debit': ''}), data)[0]
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return response


def postDebit(entity):
    response = {}
    try:
        _properties_ = removeByList(
            _propertiesSQl, ['id', 'data_criacao', 'data_atualizacao'])

        conn = openConnection()
        cur = conn.cursor()
        cur.execute(addQuery(tableName=_tableName, properties=_properties_, values=getPropertiesByProperties(
            entity, removeByList(_properties, ['id', 'creation_date', 'updated_at']))))
        conn.commit()
        entity['id'] = int(cur.fetchone()[0])
        response = entity
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return response

def patchPay(id, user):
    response = {}
    try:
        conn = openConnection()
        cur = conn.cursor()
        cur.execute(editQuery(tableName=_tableName, properties=['is_pago'], values=[True], param=f'id = {id} AND id_usuario = {user}'))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return response

def patchReceived(received, id, user):
    response = {}
    try:
        conn = openConnection()
        cur = conn.cursor()
        cur.execute(editQuery(tableName=_tableName, properties=['is_recebido', 'is_pago'], values=[received, received], param=f'id = {id} AND id_usuario = {user}'))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return response

def getPropertiesByProperties(entity, properties):
    return [entity[value] for value in properties]
