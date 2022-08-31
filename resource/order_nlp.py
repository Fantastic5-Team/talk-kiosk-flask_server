from konlpy.tag import Mecab
import json
import utils

tagger = Mecab()

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

with open("/home/workspace/talk-kiosk-flask_server/json/option-sel.json", "r") as f:
    data = json.load(f)
f.close

opt_dict = data

# api 1 :메뉴 추가 함수

def add_menu(sentence):
    try:
        result_dict = {"order_list": [], "code": ""}

        if sentence == "아니오" or sentence == "다음":
            result_dict["code"] = 2001
        elif sentence == "":
            result_dict["code"] = 1002
        else:
            temp_string = ""

            for word in tagger.pos(sentence):
                if word[1] == "NNG":
                    temp_string = temp_string + word[0]
                    menu_id = utils.find_key(menu_dict, temp_string)
                    if menu_id != None:
                        conflict_menu_list = utils.find_menu(
                            menu_dict, temp_string)
                        result_dict["order_list"].append(
                            {"menu": conflict_menu_list, "option": [], "set": [], "qty": 1})
                        temp_string = ""

                    if temp_string == "라지세트" or temp_string == "세트라지":
                        result_dict["order_list"][-1]["set"] = [202, 302]
                        temp_string = ""
                    elif "세트" in temp_string and len(temp_string) != 2:
                        result_dict["order_list"][-1]["set"] = [201, 301]
                        temp_string = temp_string.replace("세트", "")

                elif word[1] == "NR":
                    count_num = int(
                        utils.find_key_value_list(num_dict, word[0]))
                    result_dict["order_list"][-1]["qty"] = count_num
                elif word[1] == "SN":
                    count = int(word[0])
                elif utils.exist_key_value_list(num_dict, word[0]):
                    count = int(utils.find_key_value_list(num_dict, word[0]))
                elif word[0] == "개":
                    result_dict["order_list"][-1]["qty"] = count

            if temp_string == "세트":
                result_dict["order_list"][-1]["set"] = [201, 301]

            if result_dict["order_list"] != []:
                result_dict["code"] = 1001
            else:
                result_dict["code"] = 1002

        return result_dict
    except:
        return {"order_list": [], "code": 1002}


# API NO.2 여러 메뉴 중 하나 선택
def conflict_menu_select(sentence, conflict_list):
    try:
        temp_string = ""
        for word in tagger.pos(sentence):
            if word[1] == "NNG":
                temp_string = temp_string + word[0]
                menu_id = utils.find_key(menu_dict, temp_string)
            elif word[1] == "SN":
                menu_id = conflict_list[int(word[0]) - 1]

        if int(menu_id) in conflict_list:
            return {"resolve": int(menu_id), "code": 2002}
        else:
            return {"resolve": int(menu_id), "code": 2009}
    except:
        return {"resolve": "", "code": 1002}


# API NO.3 옵션 선택
def select_option(sentence):
    try:
        opt_select = {}
        opt_select["option"] = []
        for v in tagger.morphs(sentence):
            if(v == '아니' or v == '다음'):
                opt_select["code"] = 2004
        else:
            for v in opt_dict.values():
                if v in sentence:
                    opt_select["option"].append(utils.find_key(opt_dict, v))
                    opt_select["code"] = 2003
        if "code" not in opt_select:
            opt_select["code"] = 1002
        print(opt_select)
        return opt_select
    except:
        return {"option": [], "code": 1002}


# API NO.4 세트 메뉴 선택
# 선택을 안할 경우 2006, 세트 선택
def set_check(sentence, set):
    my_set={"set":set, "code":{}}
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
        if i//100 == 2:#사이드라면
            a+=1
        elif i//100 == 3:#음료라면
            b+=1
    if(a>=2 or b>=2):#사이드나 음료가 두개이상 입력이 되면
        my_set["code"]=2007
    elif (my_set["code"]!=2006 and a+b>=1): 
        my_set["code"]=2005
        for i in temp:
            if i//100 ==2:
                my_set["set"][0]=i
            elif i//100 ==3:
                my_set["set"][1]=i

    else:
        my_set["code"]=1002

    return my_set
    #print(my_set)


# API NO.5 
def confirm(sentence):
    confirm_code={"code":{}}
    for v in tagger.morphs(sentence):
        if(v=='네' or v=='맞'or v=='넹' or v=='넵'or v=='확인'): #긍정표현
            confirm_code["code"]=2008
        if(v=='아니'or v=='달라요' or v=='다릅니다' or v=='엥'or v=='아닌데요'or v=='아님'): # 부정표현
            confirm_code["code"]="추후 수정기능 구현 후 구현 예정"    
   
    if type(confirm_code["code"]) is dict: #분석 실패
        confirm_code["code"]=1002  
    #print(confirm_code)
    return confirm_code

agger.pos(sentence))

#def main():
    #sentence = input("sentence > ")
    #print(tagger.pos(sentence))
    #confilct_list = [106, 107, 108]
    #print(add_menu(sentence))
    #print(conflict_menu_select(sentence, confilct_list))
    # select_option(sentence)
    #print(set_check(sentence))
    #print(confirm(sentence))

#main()
