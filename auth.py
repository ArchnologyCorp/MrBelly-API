
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
import jwt
from werkzeug.security import check_password_hash
from helpers.response_helper import errorResponse
import repository.user

def validateToken(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return errorResponse('Authorization não informado', 401)
        try:
            data = jwt.decode(token, 'pagueoaluguel', algorithms=['HS256'])
        except:
            return errorResponse('Token inválido ou expirado', 401)
        return f(data, *args, **kwargs)
    return decorated

def login(phone, password):
    auth = repository.user.authLogin(phone, password)
    if not auth or not auth['phone'] or not auth['password']:
        return {'msg': 'Usuário ou senha incorretos', 'status_code': 401}
        
    token = jwt.encode({'id': auth['id'], 'user': auth['user'], 'phone': phone, 'exp':datetime.now() + timedelta(hours=12)}, 'pagueoaluguel')
    return {'user': auth['user'], 'token': token}

    