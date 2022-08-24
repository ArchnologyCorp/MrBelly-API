from flask import Flask
# from flask_cors import CORS, cross_origin 
import json
import db

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def hello():
    devs = ['Carlos', 'Teylor', 'Cleber', 'Leonardo', 'Railson']
    print('Devs: {}'.format(json.dumps(devs)))
    print('Hello Word!')
    return devs

@app.route('/debits', methods = ['GET'])
def getDebits():
    return db.getDebits()
       
if __name__ == "__main__":
    app.run(debug=True)