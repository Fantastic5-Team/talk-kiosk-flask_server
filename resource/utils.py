def find_value(_dict, _key):
    return _dict.get(_key)

def find_key(_dict, _value):
    for k, v in _dict.items():
        if v == _value:
            return k