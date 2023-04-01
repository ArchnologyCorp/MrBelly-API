from queue import Empty
from repository.db import openConnection, psycopg2
from repository.credit import deleteCreditByDebit, postCredit
from helpers.json_helper import buildJson
from helpers.sql import *

_tableName = 'tb_cobranca'

def getDebits(user):
    response = []
    try:
        conn = openConnection() 
        cur = conn.cursor()
        cur.execute(getQuery(tableName=f'''{_tableName} Cobr 
                                        INNER JOIN tb_devedor Dv ON Dv.id_cobranca = Cobr.id
                                        INNER JOIN tb_usuario Dev ON Dev.id = Dv.id_usuario 
                                        INNER JOIN tb_usuario Cob ON Cob.id = Cobr.id_usuario''', properties=['Cobr.id', 'Cobr.data_criacao', 'Cobr.data_atualizacao', 'Cobr.descricao', 'Dev.id', 'Dev.nome', 'Dv.valor', 'Dv.data_cobranca', 'Dv.is_pago', 'Dv.is_recebido'], filter=f'Cobr.id_usuario = {user}'))
        users = cur.fetchall()
        response = buildJson({'id': 0, 'creation_date': None, 'updated_at': None, 'description': '', 'debtor_id': 0, 'debtor_name': '', 'amount_value': 0.0, 'credit_date': None, 'is_paid_out': False, 'is_debited': False}, users)
        debits = []

        for debit in response:
            currentDebit = next(item for item in response if item["id"] == debit["id"])
            
            if not 'debtors' in currentDebit:
                currentDebit['debtors'] = [] 
                
            currentDebit['debtors'].append({'id': debit['debtor_id'], 'name': debit['debtor_name'], 'amount': debit['amount_value'], 'credit_date': debit['credit_date'], 'is_paid_out': debit['is_paid_out'], 'is_debited': debit['is_debited']})
            is_duplicate = any(single_debit["id"] == debit["id"] or "id" in debits for single_debit in debits)

            if not is_duplicate:
                debits.append({
                    'id': debit['id'],
                    'creation_date': debit['creation_date'],
                    'updated_at': debit['updated_at'],
                    'description': debit['description'],
                    'debtors': currentDebit['debtors']
                })
        
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        conn.close()
    return debits


def getDebit(id, user):
    response = {}
    try:
        conn = openConnection() 
        cur = conn.cursor()
        cur.execute(getQuery(tableName=f'''{_tableName} Cobr 
                                        INNER JOIN tb_devedor Dv ON Dv.id_cobranca = Cobr.id
                                        INNER JOIN tb_usuario Dev ON Dev.id = Dv.id_usuario 
                                        INNER JOIN tb_usuario Cob ON Cob.id = Cobr.id_usuario''', properties=['Cobr.id', 'Cobr.data_criacao', 'Cobr.data_atualizacao', 'Cobr.descricao', 'Dev.id', 'Dev.nome', 'Dv.valor'], filter=f'Cobr.id = {int(id)} and Cobr.id_usuario = {user}'))
        data = cur.fetchall()
        response = buildJson({'id': 0, 'creation_date': None, 'updated_at': None, 'description': '', 'debtor_id': 0, 'debtor_name': '', 'amount_value': 0.0}, data)
        
        debtors = []
        for debit in response:
            debtors.append({'id': debit['debtor_id'], 'name': debit['debtor_name'], 'amount': debit['amount_value']})
        
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        conn.close()
    return {
        'id': debit['id'],
        'creation_date': debit['creation_date'],
        'updated_at': debit['updated_at'],
        'description': debit['description'],
        'debtors': debtors
    }


def postDebit(entity, user):
    response = {}
    try:
        conn = openConnection() 
        cur = conn.cursor()
        cur.execute(addQuery(tableName=_tableName, properties=['descricao, id_usuario'], values=(entity["description"], user)))
        conn.commit()
        entity['id'] = int(cur.fetchone()[0])
        for credit in entity["credits"]:
            credit["id_credit"] = entity['id']
            credit["is_debited"] = False
            credit["is_paid_out"] = False
            postCredit(credit)
        response = entity
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        conn.close()
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
        deleteCreditByDebit(id)
        conn = openConnection() 
        cur = conn.cursor()
        cur.execute(deleteQuery(tableName=_tableName, param=f'id = {int(id)}'))
        conn.commit()
        response = True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return response
