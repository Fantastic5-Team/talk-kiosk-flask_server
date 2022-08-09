from konlpy.tag import Mecab
import json
import utils

# json 파일 불러오기
with open("resource/intent.json", "r") as f:
    data = json.load(f)
f.close()

order = data["order"]
search = data["search"]

with open("resource/menu-table.json", "r") as f:
    data = json.load(f)
f.close

menu_dict = data

# 형태소 분석 및 의도파악
tagger = Mecab()
sentence = input("sentence > ")
print(tagger.morphs(sentence))
print(tagger.nouns(sentence))

for i in tagger.morphs(sentence):
    if i in search:
        print(sentence, ": 메뉴 검색")
    if i in order:
        print(sentence, ": 메뉴 주문")

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

# 주문 딕셔너리 생성
my_order = {}
