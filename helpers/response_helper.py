import json

def sucessResponse(data = {}, msg = 'Função realizada com sucesso'):
    return ({'success': True, 'msg': msg, 'data': data})

def errorResponse(msg, statusCode = 400):
    return {'sucess': False, 'msg': msg}, statusCode
