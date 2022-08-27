
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
import jwt
from werkzeug.security import check_password_hash
import repository.user

def validateToken(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'msg': 'Authorization não informado', 'data': []}), 401

        try:
            data = jwt.decode(token, 'pagueoaluguel', algorithms=['HS256'])
        except:
            return jsonify({'msg': 'token is invalid or expired', 'data': []}), 401
        return f(data, *args, **kwargs)
    return decorated

def login(user, password):
    auth = repository.user.authLogin(user, password)
    print(auth)
    if not auth or not auth['user'] or not auth['password']:
        return jsonify({'msg': 'Usuário ou senha incorretos'}), 401

    token = jwt.encode({'user': user, 'exp':datetime.now() + timedelta(hours=12)}, 'pagueoaluguel')
    return jsonify({'msg': 'Usuário autenticado com sucesso', 'user': user, 'token': token})

    