from konlpy.tag import Mecab
import json
import utils

tagger = Mecab()

# 주문 딕셔너리 생성
my_order = {"ordered": {"menu": []}}

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


def main():

    sentence = input("sentence > ")

    add_menu(sentence)


# 메뉴 추가 함수
def add_menu(sentence):
    # 메뉴 주문 리스트
    order_menu_list = []

    for k, v in menu_dict.items():
        if v in sentence:
            menu_dictionary = {}  # 메뉴별 딕셔너리
            menu_dictionary["id"] = utils.find_key(menu_dict, v)
            order_menu_list.append(menu_dictionary)

    # ordered 객체 menu 의 value로 추가
    ordered = my_order["ordered"]
    ordered["menu"] = order_menu_list

    print(my_order)


# 해당 단어가 들어간 메뉴들 출력 함수
def conflict_processing(sentence):
    for menu in tagger.nouns(sentence):
        if menu != "버거":
            menu_list = utils.find_menu(menu_dict, menu)
            if len(menu_list) > 1:
                print("다음의 메뉴 중 선택: ", [utils.find_value(
                    menu_dict, k) for k in menu_list.keys()])
            elif len(menu_list) == 1:
                print("다음의 메뉴 추가: ", menu_list)
            else:
                print("error: 메뉴 없음")


main()
