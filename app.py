from traceback import print_tb
import repository.debit, repository.credit, repository.user
from flask import Flask, request, jsonify
from auth import validateToken, login
from helpers.response_helper import *

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    devs = ['Carlos', 'Teylor', 'Cleber', 'Leonardo', 'Railson']
    return devs

@app.route('/auth', methods=['POST'])
def auth():
    data = request.get_json()
    response = login(data['phone'], data['password'])
    
    if 'status_code' in response:
        return errorResponse(response['msg'], response['status_code'])
    
    return sucessResponse(response, 'Usuário autenticado com sucesso')

@app.route('/debits', methods=['GET', 'POST'])
@validateToken
def debitsEndPoint(user):
    if request.method == 'GET':
        return sucessResponse(repository.debit.getDebits(user['id']))
    elif request.method == 'POST':
        debit = request.get_json()
        return sucessResponse(repository.debit.postDebit(debit, user['id']))

@app.route('/debits/<id>', methods=['GET', 'PUT', 'DELETE'])
@validateToken
def debitEndPoint(user, id):
    if request.method == 'GET':
        return sucessResponse(repository.debit.getDebit(id, user['id']))
    elif request.method == 'PUT':
        debit = request.get_json()
        repository.debit.putDebit(id, debit)
        return sucessResponse()

# CARLOS
@app.route('/credit/<id>', methods=['GET'])
@validateToken
def debitEndPoint(user, id):
    return sucessResponse(repository.credit.getCredit(id, user['id']))

@app.route('/credits', methods=['GET'])
@validateToken
def debitEndPoint(user):
    return sucessResponse(repository.credit.getCredits(user))
    

@app.route('/credits/IPad/<id>', methods=['PATCH'])
@validateToken
def debitEndPoint(id):
        debit = request.get_json()
        repository.credit.patchPay(id, debit)
        return sucessResponse()

@app.route('/credits/IReceived/<pay>/<id>', methods=['PATCH'])
@validateToken
def debitEndPoint(received, id):
        debit = request.get_json()
        repository.credit.patchReceived(received, id, debit)
        return sucessResponse()






















































# LEONARDO 
@app.route('/auth/user', methods=['GET'])
@validateToken
def authEndpoint(user):
    if request.method == 'GET':
        return sucessResponse(user, 'Usuário resgatado com sucesso')

@app.route('/user', methods=['POST'])
def usersEndPoint():
    if request.method == 'POST':
        data = request.get_json()
        return sucessResponse(repository.user.postUser(data))

@app.route('/user/<id>', methods=['PUT'])
@validateToken
def userEndPoint(user, id):
    if user['id'] != int(id):
        return jsonify({'msg': 'Usuário não possui permissão para editar dados de outro usuário'}), 401
    if request.method == 'PUT':
        data = request.get_json()
        return sucessResponse(repository.user.putUser(data, id))

@app.route('/user/total', methods=['GET'])
@validateToken
def totalUser(user):
    if request.method == 'GET':
        transactions = repository.user.totalByUser(user['id'])
        collectors = []
        debtors = []
        for transaction in transactions:
            if transaction['id_debtor'] is not user['id']:
                debtors.append({'name': transaction['debtor'], 'amount': float(transaction['total'])})
            else: 
                collectors.append({'name': transaction['collector'], 'amount': float(transaction['total'])})

        return sucessResponse({'debtors': debtors, 'collectors': collectors}, 'Totalizadores calculados com sucesso')


































if __name__ == "__main__":
    app.run(debug=True)