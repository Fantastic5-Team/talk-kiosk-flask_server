# 키로 딕셔너리의 값 반환
def find_value(_dict, _key):
    return _dict.get(_key)

# 값으로 딕셔너리의 키 반환
def find_key(_dict, _value):
    for k, v in _dict.items():
        if v == _value:
            return k

#value 존재 확인
def exist_key(_dict, _value):
    for k, v in _dict.items():
        if v == _value:
            return True

# 키워드가 포한된 메뉴 딕셔너리 반환


def find_menu(_dict, _value):
    result = {}
    for k, v in _dict.items():
        if _value in v:
            result[k] = v
    return result
