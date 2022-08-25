from flask import Flask, request
# from flask_cors import CORS, cross_origin
import json
import db

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello():
    devs = ['Carlos', 'Teylor', 'Cleber', 'Leonardo', 'Railson']
    print('Devs: {}'.format(json.dumps(devs)))
    print('Hello Word!')
    return devs

@app.route('/debits', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def debitsEndPoint():
    if request.method == 'GET':
        return db.getDebits()
    elif request.method == 'POST':
        debit = request.get_json()
        return db.postDebit(debit)
    elif request.method == 'DELETE':
        debit = request.get_json()
        response = db.deleteDebit(debit['id'])
        return {'success':  response}
    elif request.method == 'PATCH':
        debit = request.get_json()
        return db.getDebit(debit['id'])
    elif request.method == 'PUT':
        debit = request.get_json()
        # _debit['id'] = debit or _debit['id']
        response = db.putDebit(debit)
        return {'success': response}


if __name__ == "__main__":
    app.run(debug=True)
