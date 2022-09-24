def removeByList(entity = [], list=[]):
    _entity = entity
    for item in list:
        _entity.remove(item)
    return _entity