import json

def sucessResponse(data = {}, msg = 'Função realizada com sucesso'):
    return json.dumps({'success': True, 'msg': msg, 'data': data}, default=str, indent=4)

def errorResponse(msg, statusCode = 400):
    return json.dumps({'sucess': False, 'msg': msg}, default=str), statusCode
