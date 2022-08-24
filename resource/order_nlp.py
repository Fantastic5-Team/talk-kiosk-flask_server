from konlpy.tag import Mecab
import json
import utils

tagger = Mecab()

# 주문 딕셔너리 생성
my_order = {"ordered": {"menu": []} ,"situation":{}}
order_list={}

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
    #add_menu(sentence)
    #conflict_processing(sentence)
    #select_option(sentence)
    #conflict_menu_select(sentence)
    set_check(sentence)

    #print(my_order)
    


# 메뉴 추가 함수
# def add_menu(sentence):
#     menu_id_dict = {}  # {id:메뉴명}

#     for k, v in menu_dict.items():
#         if v in sentence:  # 메뉴 딕셔너리에 있는 메뉴가 문장에 있으면
#             menu_id_dict[utils.find_key(menu_dict, v)] = v.replace(
#                 " ", "")  # 메뉴명에서 공백 삭제

#     # 메뉴 문자열
#     temp_menu_string = ""

#     for word in tagger.pos(sentence):
#         if word[1] == "NNG":
#             temp_menu_string = temp_menu_string + word[0]
#         elif word[1] == "NR":
#             count_num = int(utils.find_key_value_list(num_dict, word[0]))
#             menu_num_dict(menu_id_dict, temp_menu_string, count_num)
#             temp_menu_string = ""
#         elif word[1] == "SN":
#             count = int(word[0])
#         elif utils.exist_key_value_list(num_dict, word[0]):
#             count = int(utils.find_key_value_list(num_dict, word[0]))
#         elif word[0] == "개":
#             menu_num_dict(menu_id_dict, temp_menu_string, count)
#             temp_menu_string = ""

#     # 수량이 언급 안 된 메뉴들을 하나씩 추가한다.
#     if len(temp_menu_string) != 0:
#         for k, v in menu_id_dict.items():
#             if v in temp_menu_string:
#                 insert_in_menu_dict(k)

#     # ordered 객체 menu 의 value로 추가
#     ordered = my_order["ordered"]
#     ordered["menu"] = order_menu_list

#     print(menu_id_dict)
#     print(my_order)

def erase_gap(sentence):
    before_pos = ""
    temp_sentence = sentence
    result_sentence = ""
    for word in tagger.pos(sentence):
        if word[1] == "NNG":
            if(before_pos == "NNG"):
                temp_sentence = temp_sentence[:temp_sentence.find(
                    word[0])-1]+temp_sentence[temp_sentence.find(
                        word[0]):]
                result_sentence = result_sentence + temp_sentence[:temp_sentence.find(
                    word[0])+len(word[0])]
                temp_sentence = temp_sentence[temp_sentence.find(
                    word[0])+len(word[0]):]
            before_pos = "NNG"

        else:
            before_pos = word[1]

    if temp_sentence != "":
        result_sentence = result_sentence + temp_sentence
    print(result_sentence)

# 메뉴 추가 함수


def add_menu(sentence):
    menu_id_dict = {}  # {id:메뉴명}

    for k, v in menu_dict.items():
        if v in sentence:  # 메뉴 딕셔너리에 있는 메뉴가 문장에 있으면
            temp_menu = v + "세트"
            print(temp_menu)
            if temp_menu in sentence:
                menu_id_dict[utils.find_key(menu_dict, v)] = temp_menu.replace(
                    " ", "")  # 메뉴명에서 공백 삭제
            else:
                menu_id_dict[utils.find_key(menu_dict, v)] = v.replace(
                    " ", "")  # 메뉴명에서 공백 삭제

    # 메뉴 문자열
    temp_menu_string = ""

    for word in tagger.pos(sentence):
        if word[1] == "NNG":
            temp_menu_string = temp_menu_string + word[0]
            temp_menu_name = word[0]
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
        count = 1
        for k, v in menu_id_dict.items():
            if v in temp_menu_string:
                insert_in_menu_dict(id, count, menu_id_dict)

    order_list["order_list"] = order_menu_list
    order_list["code"] = 1001
    print(menu_id_dict)
    print(order_list)


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
                insert_in_menu_dict(k, count, menu_id_dict)
            else:

                insert_in_menu_dict(k, count, menu_id_dict)


# 새로운 메뉴 딕셔너리 생성
def insert_in_menu_dict(id, count, menu_id_dict):
    menu = conflict_processing(menu_id_dict[id].replace('세트', ''))
    menu_dictionary = {"menu": menu, "option": [],
                       "set": [], "qty": count}  # 메뉴별 딕셔너리
    if "세트" in menu_id_dict[id]:
        menu_dictionary["set"] = [201, 301]

    order_menu_list.append(menu_dictionary)


# 해당 단어가 들어간 메뉴들 출력 함수
def conflict_processing(sentence):
    result_menu_list = []
    for menu in tagger.nouns(sentence):
        if menu != "버거":
            menu_list = utils.find_menu(menu_dict, menu)
            if len(menu_list) > 1:
                menu_list = [utils.find_value(menu_dict, k)
                             for k in menu_list.keys()]
                for i in menu_list:
                    result_menu_list.append(int(utils.find_key(menu_dict, i)))
                return result_menu_list
            elif len(menu_list) == 1:
                for i in menu_list:
                    result_menu_list.append(int(utils.find_key(menu_dict, i)))
                return result_menu_list


def choose_menu(sentence):
    return


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
# API NO.4 세트 메뉴 선택
# 선택을 안할 경우 2006, 세트 선택시 
def set_check(sentence):
    my_set={"set":[201,301],"code":{}}

    temp=[]
    a=0
    b=0

    for v in tagger.morphs(sentence):
        if(v =='아니' or v=='다음'):
            my_set["code"]=2006
            

    for k ,v in menu_dict.items():
        
        if v in sentence:
            # print(k,v)
            
            if int(k) < 200:
                continue
            elif int(k) < 300:
                temp.append(int(k))
            else:
                temp.append(int(k))

    #사이드 메뉴와 음료의 갯수의 입력을 확인한다.    
    for i in temp:
        if i//100 == 2:
            a+=1
        elif i//100 == 3:
            b+=1
    

    if(a>=2 or b>=2):
        my_set["code"]=2007
    else:
        my_set["code"]=2005
        for i in temp:
            if i//100 ==2:
                my_set["set"][0]=i
            elif i//100 ==3:
                my_set["set"][1]=i
    

    print(my_set)

main()
