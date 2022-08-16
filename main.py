from flask import Flask
# from flask_cors import CORS, cross_origin 
import json

app = Flask(__name__)

@app.route('/')
def hello():
    devs = ['Carlos', 'Teylor', 'Cleber', 'Leonardo', 'Railson']
    print('Devs: {}'.format(json.dumps(devs)))
    print('Hello Word!')
    return devs
