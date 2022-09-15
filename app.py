import json
from flask import Flask, request, jsonify
from auth import validateToken, login 
app = Flask(__name__)
import repository.debit, repository.user

@app.route('/', methods=['GET'])
def hello():
    devs = ['Carlos', 'Teylor', 'Cleber', 'Leonardo', 'Railson']
    return devs

@app.route('/auth', methods=['POST'])
def auth():
    data = request.get_json()
    return login(data['phone'], data['password'])

@app.route('/debits', methods=['GET', 'POST'])
@validateToken
def debitsEndPoint(user):
    if request.method == 'GET':
        return json.dumps(repository.debit.getDebits(user['id']), indent=4)
    elif request.method == 'POST':
        debit = request.get_json()
        return repository.debit.postDebit(debit, user['id'])

@app.route('/debits/<id>', methods=['GET', 'PUT', 'DELETE'])
@validateToken
def debitEndPoint(user, id):
    if request.method == 'GET':
        return repository.debit.getDebit(id, user['id'])
    elif request.method == 'PUT':
        debit = request.get_json()
        response = repository.debit.putDebit(id, debit)
        return {'success': response}
    elif request.method == 'DELETE':
        response = repository.debit.deleteDebit(id)
        return {'success':  response}

# CARLOS
























































# LEONARDO 
@app.route('/auth/user', methods=['GET'])
@validateToken
def authEndpoint(user):
    if request.method == 'GET':
        return user

@app.route('/user', methods=['POST'])
def usersEndPoint():
    if request.method == 'POST':
        data = request.get_json()
        return repository.user.postUser(data)

@app.route('/user/<id>', methods=['PUT'])
@validateToken
def userEndPoint(user, id):
    if user['id'] != int(id):
        return jsonify({'msg': 'Usuário não possui permissão para editar dados de outro usuário'}), 401
    if request.method == 'PUT':
        data = request.get_json()
        return repository.user.putUser(data, id)


































if __name__ == "__main__":
    app.run(debug=True)