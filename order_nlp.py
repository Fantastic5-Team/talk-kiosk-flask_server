from konlpy.tag import Mecab
import json

with open("intent.json", "r") as f:
    data = json.load(f)

order = data["order"]
search = data["search"]

tagger = Mecab()
sentence = input("sentence > ")
# print(tagger.morphs(sentence))

for i in tagger.morphs(sentence):
    if i in search:
        print(sentence, ": 메뉴 검색")
    if i in order:
        print(sentence, ": 메뉴 주문")
