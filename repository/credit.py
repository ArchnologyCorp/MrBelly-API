from repository.db import openConnection, psycopg2
from helpers.json_helper import buildJson
from utils.array import removeByList
from utils.dict import removeByDict
from helpers.sql import *
from datetime import datetime

_tableName = 'tb_devedor'

_defaultPropertiesSQl = [
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

_defaultPropertiesObj = {
    'id': 0,
    'creation_date': datetime.today(),
    'updated_at': None,
    'credit_date': datetime.today(),
    'value': 0.0,
    'observation': '',
    'is_paid_out': False,
    'is_debited': False,
    'id_debit': 0,
    'id_user': 0}

_properties = _defaultPropertiesObj.keys()


def getCredits(user):
    response = []
    _propertiesSQl = _defaultPropertiesSQl.copy()
    _propertiesObj = _defaultPropertiesObj.copy()

    try:
        sql = f'''{_tableName} cred 
                INNER JOIN tb_cobranca cobr ON cobr.id = cred.id_cobranca
                INNER JOIN tb_usuario usuD ON usuD.id = cobr.id_usuario 
                '''

        _properties_ = createProperties(
            [_propertiesSQl, ['descricao'], ['id', 'nome']], ['cred', 'cobr', 'usuD'])

        conn = openConnection()
        cur = conn.cursor()
        cur.execute(getQuery(tableName=sql, properties=_properties_, filter=f'cred.id_usuario = {user}'))
        credits = cur.fetchall()

        _propertiesObj.update({
            'description': '', 'id_user_debit': 0, 'name_user_debit': ''})
        response = buildJson(_propertiesObj, credits)

        for credit in response:
            credit.update({
                'debit':{
                    'id': credit['id_debit'],
                    'description': credit['description'],
                    'collector':{
                        'id': credit['id_user_debit'],
                        'name': credit['name_user_debit'],
                    },
                }
            }) 
            removeByDict(credit, ['id_user', 'id_debit', 'description', 'id_user_debit','name_user_debit'])

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        conn.close()
    return response


def getCredit(id, user):
    response = {}
    _propertiesSQl = _defaultPropertiesSQl.copy()
    _propertiesObj = _defaultPropertiesObj.copy()
    try:
        sql = f'''{_tableName} cred 
                INNER JOIN tb_cobranca cobr ON cobr.id = cred.id_cobranca
                INNER JOIN tb_usuario usuD ON usuD.id = cobr.id_usuario 
                '''
        _properties_ = createProperties(
            [_propertiesSQl, ['descricao'], ['id', 'nome']], ['cred', 'cobr', 'usuD'])

        conn = openConnection()
        cur = conn.cursor()
        cur.execute(getQuery(
            tableName=sql, properties=_properties_, filter=f'cred.id = {int(id)} and cred.id_usuario = {user}'))
        data = cur.fetchall()
        _propertiesObj.update({
            'description': '', 'id_user_debit': 0, 'name_user_debit': ''})
        response = buildJson(_propertiesObj, data)[0]
 
        response.update({
            'debit':{
                'id': response['id_debit'],
                'description': response['description'],
                'collector':{
                    'id': response['id_user_debit'],
                    'name': response['name_user_debit'],
                },
            }
        })

        removeByDict(response, ['id_user', 'id_debit', 'description', 'id_user_debit','name_user_debit'])

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        conn.close()
    return response


def postCredit(entity):
    response = {}
    _propertiesSQl = _defaultPropertiesSQl.copy()
    try:
        _properties_ = removeByList(
            _propertiesSQl, ['id', 'data_criacao', 'data_atualizacao'])
    
        conn = openConnection()
        cur = conn.cursor()
        cur.execute(addQuery(tableName=_tableName, properties=_properties_, values=getPropertiesByProperties(
            entity, removeByList(list(_properties), ['id', 'creation_date', 'updated_at']))))
        conn.commit()
        entity['id'] = int(cur.fetchone()[0])
        response = entity
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        conn.close()
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
    finally:
        conn.close()
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
    finally:
        conn.close()
    return response

def deleteCreditByDebit(id):
    response = False
    try:
        conn = openConnection() 
        cur = conn.cursor()
        cur.execute(deleteQuery(tableName=_tableName, param=f'id_cobranca = {int(id)}'))
        conn.commit()
        response = True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        conn.close()
    return response

def getPropertiesByProperties(entity, properties):
    return [entity[value] for value in properties]
