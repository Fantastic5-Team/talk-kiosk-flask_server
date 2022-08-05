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

menu = data
# print(utils.find_value(menu, "101"))
# print(utils.find_key(menu, "더블 치즈버거"))

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

# 주문 딕셔너리 생성
my_order = {}
