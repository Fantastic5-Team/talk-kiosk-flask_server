from konlpy.tag import Mecab
import json
import utils

tagger = Mecab()

# 주문 딕셔너리 생성
my_order = {"ordered": {"menu": []} ,"situation":{}}

# 메뉴 주문 리스트
order_menu_list = []

# json 파일 불러오기
with open("/home/workspace/talk-kiosk-flask_server/json/intent.json", "r") as f:
    data = json.load(f)
f.close()

order = data["order"]

with open("/home/workspace/talk-kiosk-flask_server/json/menu-table.json", "r") as f:
    data = json.load(f)
f.close

menu_dict = data

with open("/home/workspace/talk-kiosk-flask_server/json/number.json", "r") as f:
    data = json.load(f)
f.close

num_dict = data

with open("/home/workspace/talk-kiosk-flask_server/json/option-sel.json","r") as f:
    data = json.load(f)
f.close

opt_dict = data


def main():

    sentence = input("sentence > ")
    print(tagger.pos(sentence))
    # print(tagger.nouns(sentence))
    # add_menu(sentence)
    #conflict_processing(sentence)
    #select_option(sentence)
    #conflict_menu_select(sentence)
    set_check(sentence)

    #print(my_order)
    


# 메뉴 추가 함수
def add_menu(sentence):
    menu_id_dict = {}  # {id:메뉴명}

    for k, v in menu_dict.items():
        if v in sentence:  # 메뉴 딕셔너리에 있는 메뉴가 문장에 있으면
            menu_id_dict[utils.find_key(menu_dict, v)] = v.replace(
                " ", "")  # 메뉴명에서 공백 삭제

    # 메뉴 문자열
    temp_menu_string = ""

    for word in tagger.pos(sentence):
        if word[1] == "NNG":
            temp_menu_string = temp_menu_string + word[0]
        elif word[1] == "NR":
            count_num = int(utils.find_key_value_list(num_dict, word[0]))
            menu_num_dict(menu_id_dict, temp_menu_string, count_num)
            temp_menu_string = ""
        elif word[1] == "SN":
            count = int(word[0])
        elif utils.exist_key_value_list(num_dict, word[0]):
            count = int(utils.find_key_value_list(num_dict, word[0]))
        elif word[0] == "개":
            menu_num_dict(menu_id_dict, temp_menu_string, count)
            temp_menu_string = ""

    # 수량이 언급 안 된 메뉴들을 하나씩 추가한다.
    if len(temp_menu_string) != 0:
        for k, v in menu_id_dict.items():
            if v in temp_menu_string:
                insert_in_menu_dict(k)

    # ordered 객체 menu 의 value로 추가
    ordered = my_order["ordered"]
    ordered["menu"] = order_menu_list

    print(menu_id_dict)
    print(my_order)


def menu_num_dict(menu_id_dict, temp_menu_string, count):
    # 메뉴 순서 딕셔너리 {id : temp_menu_string에서 위치}
    menu_sequence_dict = {}

    for k, v in menu_id_dict.items():
        menu_sequence_dict[k] = temp_menu_string.find(v)

    plural_menu = max(menu_sequence_dict,
                      key=menu_sequence_dict.get)

    for k, v in menu_sequence_dict.items():
        if v != -1:
            if k == plural_menu:
                for num in range(count):
                    insert_in_menu_dict(k)
            else:
                insert_in_menu_dict(k)


# 새로운 메뉴 딕셔너리 생성
def insert_in_menu_dict(id):
    menu_dictionary = {"id": id}  # 메뉴별 딕셔너리
    order_menu_list.append(menu_dictionary)


# 해당 단어가 들어간 메뉴들 출력 함수
def conflict_processing(sentence):
    for menu in tagger.nouns(sentence):
        if menu != "버거":
            menu_list = utils.find_menu(menu_dict, menu)
            if len(menu_list) > 1:
                print("다음의 메뉴 중 선택: ", [utils.find_value(
                    menu_dict, k) for k in menu_list.keys()])
                my_order["situation"]="2002" #situation 2002
                print(my_order)
                    
            elif len(menu_list) == 1:
                print("다음의 메뉴 추가: ", menu_list)
            else:
                print("error: 메뉴 없음")

def select_option(sentence):
    opt_select={}
    opt_select["option"]=[]
    for v in tagger.morphs(sentence):
        if(v =='아니' or v=='다음'):
            opt_select["code"]=2004
    else:
        for v in opt_dict.values():
            if v in sentence:
                opt_select["option"].append(utils.find_key(opt_dict,v))
                opt_select["code"]=2003
    if "code" not in opt_select:
        opt_select["code"]=1002
    print(opt_select)
    # return opt_select

def conflict_menu_select(sentence):
    second_menuchoice={}
    for k, v in menu_dict.items():
        if v in sentence:  # 메뉴 딕셔너리에 있는 메뉴가 문장에 있으면
            second_menuchoice[utils.find_key(menu_dict, v)] = v.replace(" ", "")  # 메뉴명에서 공백 삭제
            print(v)

def set_check(sentence):
    my_set={"set":[201,301],"code":{}}

    for v in tagger.morphs(sentence):
        if(v =='아니' or v=='다음'):
            my_set["code"]=2006

    for k ,v in menu_dict.items():
        
        if v in sentence:
            # print(k,v)
            
            if int(k) < 200:
                continue
            elif int(k) < 300:
                my_set["set"][0]=int(k)
                my_set["code"]=2006
            else:
                if(my_set["code"]==2006):
                    print("Warning")
                    my_set["code"]=2007
                    break
                my_set["set"][1]=int(k)
                my_set["code"]=2006

    print(my_set)

main()
