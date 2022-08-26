# 키로 딕셔너리의 값 반환
def find_value(_dict, _key):
    return _dict.get(_key)

# 값으로 딕셔너리의 키 반환


def find_key(_dict, _value):
    for k, v in _dict.items():
        if v == _value:
            return k

# 값으로 딕셔너리의 키 반환 (value가 list인 경우)


def find_key_value_list(_dict, _value):
    for k, v in _dict.items():
        if _value in v:
            return k

# value 존재 확인


def exist_key(_dict, _value):
    for k, v in _dict.items():
        if v == _value:
            return True
    return False

# value 존재 확인 (value가 list인 경우)


def exist_key_value_list(_dict, _value):
    for k, v in _dict.items():
        if _value in v:
            return True
    return False

# 키워드가 포함된 메뉴 딕셔너리 반환


def find_menu(_dict, _value):
    result = []
    for k, v in _dict.items():
        if _value in v:
            result.append(k)
    return result
