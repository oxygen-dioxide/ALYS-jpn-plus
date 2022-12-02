from typing import Dict, Set, List, Union

orig:Dict[str,str]={"あ":"a",
    "い":"i",
    "う":"u",
    "え":"e",
    "お":"o",
    "か":"ka",
    "き":"ki",
    "く":"ku",
    "け":"ke",
    "こ":"ko",
    "さ":"sa",
    "すぃ":"si",
    "す":"su",
    "せ":"se",
    "そ":"so",
    "た":"ta",
    "てぃ":"ti",
    "とぅ":"tu",
    "て":"te",
    "と":"to",
    "な":"na",
    "に":"ni",
    "ぬ":"nu",
    "ね":"ne",
    "の":"no",
    "は":"ha",
    "ひ":"hi",
    "ふ":"hu",
    "へ":"he",
    "ほ":"ho",
    "ま":"ma",
    "み":"mi",
    "む":"mu",
    "め":"me",
    "も":"mo",
    "や":"ya",
    "ゆ":"yu",
    "よ":"yo",
    "ら":"ra",
    "り":"ri",
    "る":"ru",
    "れ":"re",
    "ろ":"ro",
    "わ":"wa",
    "うぉ":"wo",
    "を":"o",
    "が":"ga",
    "ぎ":"gi",
    "ぐ":"gu",
    "げ":"ge",
    "ご":"go",
    "ざ":"za",
    "ずぃ":"zi",
    "ず":"zu",
    "ぜ":"ze",
    "ぞ":"zo",
    "だ":"da",
    "でぃ":"di",
    "どぅ":"du",
    "で":"de",
    "ど":"do",
    "ば":"ba",
    "び":"bi",
    "ぶ":"bu",
    "べ":"be",
    "ぼ":"bo",
    "ぱ":"pa",
    "ぴ":"pi",
    "ぷ":"pu",
    "ぺ":"pe",
    "ぽ":"po",
    "きゃ":"kya",
    "きゅ":"kyu",
    "きょ":"kyo",
    "しゃ":"sha",
    "し":"shi",
    "しゅ":"shu",
    "しょ":"sho",
    "ちゃ":"cha",
    "ち":"chi",
    "ちゅ":"chu",
    "ちょ":"cho",
    "つぁ":"tsa",
    "つぃ":"tsi",
    "つ":"tsu",
    "つぇ":"tse",
    "つぉ":"tso",
    "にゃ":"nya",
    "にゅ":"nyu",
    "にょ":"nyo",
    "ひゃ":"hya",
    "ひゅ":"hyu",
    "ひょ":"hyo",
    "ふぁ":"fa",
    "ふぃ":"fi",
    "ふぇ":"fe",
    "ふぉ":"fo",
    "みゃ":"mya",
    "みゅ":"myu",
    "みょ":"myo",
    "りゃ":"rya",
    "りゅ":"ryu",
    "りょ":"ryo",
    "ぎゃ":"gya",
    "ぎゅ":"gyu",
    "ぎょ":"gyo",
    "じゃ":"ja",
    "じ":"ji",
    "じゅ":"ju",
    "じょ":"jo",
    "びゃ":"bya",
    "びゅ":"byu",
    "びょ":"byo",
    "ぴゃ":"pya",
    "ぴゅ":"pyu",
    "ぴょ":"pyo",
    "ん":"N",
    }


import json
import yaml

#symbols部分：
symbols_set:Dict[str,str]=dict()# symbol=>type
for (kana,romaji) in orig.items():
    if(len(romaji)>1):
        symbols_set[romaji[:-1]]="fricative"
    symbols_set[romaji[-1]]="vowel"
    symbols_set[romaji]="vowel"
symbols:List[Dict[str,str]]=[{"symbol":i,"type":j} for (i,j) in symbols_set.items()]

#orig：日文假名转罗马音
#entries：包含日文假名和罗马音的完整字典
exp=orig.copy()
for i in list(exp.values()):
    if(not(i in exp)):
        exp[i]=i

entries_set:Dict[str,List[str]]={}
for (kana,romaji) in orig.items():
    entries_set[kana]=[romaji]
    entries_set[romaji]=[romaji]
entries:List[Dict[str,Union[str,List[str]]]]=[{"grapheme":i,"phonemes":j} for (i,j) in entries_set.items()]
yaml.dump(
    {"symbols":symbols,"entries":entries},
    open("arpasing.yaml","w",encoding="utf8"),
    allow_unicode=True)

#生成替换表
"""
otoconvert={
    "Calias":{value:key for (key,value) in orig.items()},
    "Valias":{i:i[-1] for i in list(orig.values())},
    "Cs":list(set(i[:-1] for i in list(orig.values()))),
    "Vs":list(set(i[-1] for i in list(orig.values()))),
}
with open("otoconvert.json","w",encoding="utf8") as otoconvertfile:
    json.dump(otoconvert,otoconvertfile,ensure_ascii=False,indent=4)     """