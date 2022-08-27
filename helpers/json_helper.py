from helpers.value_helper import convertValue

def buildJson(obj, values):
    array = []
    for value in values:
        body = {}
        for index, key in enumerate(obj.keys()):
            body[key] = convertValue(value[index])
        array.append(body)
    return array