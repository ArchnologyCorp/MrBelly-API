from flask import Flask, request
from auth import validateToken, login 
app = Flask(__name__)
import repository.debit

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
    print(user)
    if request.method == 'GET':
        return repository.debit.getDebits()
    elif request.method == 'POST':
        debit = request.get_json()
        return repository.debit.postDebit(debit)

@app.route('/debits/<id>', methods=['GET', 'PUT', 'DELETE'])
@validateToken
def debitEndPoint(user, id):
    print(user)
    if request.method == 'GET':
        return repository.debit.getDebit(id)
    elif request.method == 'PUT':
        debit = request.get_json()
        response = repository.debit.putDebit(debit, id)
        return {'success': response}
    elif request.method == 'DELETE':
        response = repository.debit.deleteDebit(id)
        return {'success':  response}


if __name__ == "__main__":
    app.run(debug=True)