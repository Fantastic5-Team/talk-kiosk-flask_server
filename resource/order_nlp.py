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
        # client에게 전달할 최종 객체
        result_dict = {"order_list": [], "code": ""}

        # 아니와 같은 부정어를 말하면 주문완료 code 2001 반환
        if sentence == "아니" or sentence == "아니요" or sentence == "아니오" or sentence == "다음":
            result_dict["code"] = 2001
        # 메뉴 보여줘 : 모든 메뉴 코드 및 code 1001 반환
        elif sentence == "메뉴 보여줘":
            menu_list = list(map(int, list(menu_dict.keys())))
            result_dict = {"order_list": [
                {"menu": menu_list, "option": [], "set": [], "qty": 0}], "code": 1001}
            return result_dict
        # 빈 문장 : code 1002로 에러처리
        elif sentence == "":
            result_dict["code"] = 1002
        # 주문 받기 시작
        else:
            temp_string = ""

            for word in tagger.pos(sentence):
                if word[1] == "NNG":
                    temp_string = temp_string + word[0]
                    print(temp_string)
                    temp_string, result_dict = one_menu_insert(
                        temp_string, result_dict)

                    if temp_string == "라지세트" or temp_string == "세트라지":
                        if int(result_dict["order_list"][-1]["menu"][0]) < 200:
                            result_dict["order_list"][-1]["set"] = [202, 302]
                            temp_string = ""
                    elif "세트" in temp_string and len(temp_string) != 2:
                        if int(result_dict["order_list"][-1]["menu"][0]) < 200:
                            result_dict["order_list"][-1]["set"] = [201, 301]
                            temp_string = temp_string.replace("세트", "")

                    elif temp_string == "라지":
                        if int(result_dict["order_list"][-1]["menu"][0]) > 200:
                            menu_temp_array = []

                            for menu in result_dict["order_list"][-1]["menu"]:
                                if "라지" in menu_dict[str(menu)]:
                                    menu_temp_array.append(menu)
                            result_dict["order_list"][-1]["menu"] = menu_temp_array
                            temp_string = temp_string.replace("라지", "")

                    for value in menu_dict.values():
                        if value in temp_string:
                            print(value)
                            temp_string, result_dict = one_menu_insert(
                                value, result_dict)

                elif word[1] == "NR":
                    count = int(
                        utils.find_key_value_list(num_dict, word[0]))
                    result_dict["order_list"][-1]["qty"] = count
                elif word[1] == "SN":
                    count = int(word[0])
                elif utils.exist_key_value_list(num_dict, word[0]):
                    count = int(utils.find_key_value_list(num_dict, word[0]))
                elif word[0] == "개":
                    result_dict["order_list"][-1]["qty"] = count

            if temp_string == "세트":
                if int(result_dict["order_list"][-1]["menu"][0]) < 200:
                    result_dict["order_list"][-1]["set"] = [201, 301]
            else:
                temp_string, result_dict = one_menu_insert(
                    temp_string, result_dict)

            if result_dict["order_list"] != []:
                result_dict["code"] = 1001
            else:
                result_dict["code"] = 1002

        return result_dict
    except:  # 에러 처리 code 1002
        return {"order_list": [], "code": 1002}

#temp_string이 포함된 메뉴 이름들이 있는 경우 result_dict에 단품으로 추가
def one_menu_insert(temp_string, result_dict):
    menu_id = utils.find_key(menu_dict, temp_string)
    if menu_id != None:
        conflict_menu_list = utils.find_menu(menu_dict, temp_string)
        result_dict["order_list"].append(
            {"menu": conflict_menu_list, "option": [], "set": [], "qty": 1})
        temp_string = ""
    return temp_string, result_dict


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
            elif word[1] == "NR":
                menu_id = conflict_list[int(
                    utils.find_key_value_list(num_dict, word[0])) - 1]

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
                    opt_select["option"].append(
                        int(utils.find_key(opt_dict, v)))
                    opt_select["code"] = 2003
        if "code" not in opt_select:
            opt_select["code"] = 1002
        print(opt_select)
        return opt_select
    except:
        return {"option": [], "code": 1002}


# API NO.4 세트 메뉴 선택

def set_check(sentence, set):
    try:
        cek = 0
        my_set = {"set": set, "code": 2005}
        side_count = 0
        drink_count = 0
        for v in tagger.morphs(sentence):
            if(v == '아니' or v == '다음'):
                my_set["code"] = 2006
                return my_set

        if sentence == "":
            my_set["code"] = 1002
        else:
            temp_string = ""
            temp_side_string = ""
            tmep_drink_string = ""

            for word in tagger.pos(sentence):
                if word[1] == "NNG":
                    temp_string = temp_string + word[0]
                    if temp_string == "라지":
                        if temp_side_string == "감자튀김":
                            temp_string = temp_side_string+temp_string
                            side_count = side_count-1
                        if tmep_drink_string == "사이다":
                            temp_string = tmep_drink_string+temp_string
                        if tmep_drink_string == "콜라":
                            temp_string = tmep_drink_string+temp_string
                        if tmep_drink_string == "제로콜라":
                            temp_string = tmep_drink_string+temp_string

                    side_id = utils.find_key(menu_dict, temp_string)
                    if side_id != None:
                        if int(side_id) < 200:
                            continue
                        elif int(side_id) < 300:
                            cek = 1
                            my_set["set"][0] = int(side_id)
                            side_count = side_count+1
                            if temp_string == "감자튀김":
                                temp_side_string = temp_string

                            temp_string = ""

                        else:
                            cek = 1
                            my_set["set"][1] = int(side_id)
                            drink_count = drink_count+1

                            if temp_string == "사이다":
                                tmep_drink_string = temp_string

                            if temp_string == "사이다라지":
                                tmep_drink_string = ""
                                drink_count = drink_count-1
                            if temp_string == "콜라":
                                tmep_drink_string = temp_string

                            if temp_string == "콜라라지":
                                tmep_drink_string = ""
                                drink_count = drink_count-1
                            if temp_string == "제로콜라":
                                tmep_drink_string = temp_string

                            if temp_string == "제로콜라라지":
                                tmep_drink_string = ""
                                drink_count = drink_count-1

                            temp_string = ""

        if (drink_count > 1 or side_count > 1):
            my_set["code"] = 2007

        if cek != 1:
            my_set["code"] = 1002

        return my_set
    except:
        return {"set": set, "code": 1002}


# API NO.5
def confirm(sentence):
    try:
        confirm_code = {"code": {}}
        for v in tagger.morphs(sentence):
            if(v == '네' or v == '맞' or v == '넹' or v == '넵' or v == '확인'):  # 긍정표현
                confirm_code["code"] = 2008
            if(v == '아니' or v == '달라요' or v == '다릅니다' or v == '엥' or v == '아닌데요' or v == '아님'):  # 부정표현
                confirm_code["code"] = 1001

        if type(confirm_code["code"]) is dict:  # 분석 실패
            confirm_code["code"] = 1002
        # print(confirm_code)
        return confirm_code
    except:
        return {"code": 1002}


# API NO.6       # 매장에서 먹고 가나요??
def takeout(sentence):
    try:
        takeout_code = {"code": {}}
        for v in tagger.morphs(sentence):
            if(v == '네' or v == '맞' or v == '매장' or v == '넵' or v == '안'):  # 매장 식사 안(안에서 먹고갈게요)
                takeout_code["code"] = 1001
                takeout_code["isTakeout"] = False  # 매장 식사
                return takeout_code
            if(v == '아니' or v == '아닌데요' or v == '아님' or v == '밖' or v == '집' or v == '괜찮' or v == '테이크' or v == '아웃'):  # 부정표현
                takeout_code["code"] = 1001
                takeout_code["isTakeout"] = True  # takeout
                return takeout_code

        if type(takeout_code["code"]) is dict:  # 분석 실패
            takeout_code["code"] = 1002
            return takeout_code
    except:
        return {"code": 1002}


def main():
    sentence = input("sentence > ")
    print(tagger.pos(sentence))
    # confilct_list = [106, 107, 108]
    print(add_menu(sentence))
    #print(conflict_menu_select(sentence, confilct_list))
    # select_option(sentence)
    #print(set_check(sentence, [201, 301]))
    # print(confirm(sentence))
    # print(takeout(sentence))

    ####밑에 메뉴판 표시용 conflict####
    # conflict_list = [101,102,103,104,105,106,107,108,109,110,111,112,113,201,202,203,204,205,301,302,303,304,305,306,307]#모든 메뉴충돌
    # conflict_list = [201,202,203,204,205,301,302,303,304,305,306,307]#사이드 메뉴만 충돌
main()
