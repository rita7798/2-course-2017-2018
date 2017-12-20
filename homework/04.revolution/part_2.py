import json
import os
import re
from part_1 import main


REGWORD = re.compile("{(\w*)")
REGPART = re.compile("{\w*=(\w*)")
REGCASE = re.compile("\W(\w{2,4}.\w{2})\W")

VOWELS = ["а", "о", "э", "и", "у", "ы", "е", "ё", "ю", "я"]
CONSONANTS = ["б", "в", "г", "д", "ж", "з", "к", "л", "м", "н", "п", "р", "с", "т", "ф", "х", "ц", "ч", "ш", "щ"]


def stage_1(req):
    try:
        file = open('data.json')
    except:
        print('словаря не существует' "\n" "подгружаю...")
        main()
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    print(req)
    if req in data:
        print("есть в словаре")
        r = data[req]
    elif req == "." or req == "-" or req == "":
        r = None
    else:
        r = stage_2(req, data)
    return r


def stage_2(req, data):
    res1 = ""
    with open("a.txt", "w", encoding="utf-8") as f:
        f.write(req)
    os.system("/Users/margaritaberseneva/hello_flask/mystem -ig a.txt res.txt")
    print("mystem.")
    with open("res.txt", "r", encoding="utf-8") as f:
        result = f.read()
    if REGWORD.search(result):
        res1 = REGWORD.search(result).group(1)
    if res1 in data:
        print("есть в словаре, но другая форма")
        a = stage_3(result, req) #подумать здесь!
    else:
        print("нет в словаре")
        a = stage_4(result, req)
    return a


def stage_3(result, req):
    res_1 = ""
    if REGPART.search(result):
        if  "S" == REGPART.search(result).group(1):
            try:
                case = REGCASE.search(result).group(1)
                if  case == "дат,ед":
                    res_1 = req[:-1] + "ѣ"
                elif  case == "пр,ед":
                    res_1 = req[:-1] + "ѣ"
                elif req[-1] in CONSONANTS:
                    res_1 = req + "ъ"
                else:
                    res_1 = req
            except:
                res_1 = req
        elif "A" == REGPART.search(result).group(1):
            if req.endswith("ие"):
                res_1 = req.replace("ие", "iя")
            elif req.endswith("ые"):
                res_1 = req.replace("ые", "ыя")
            elif req.endswith("иеся"):
                res_1 = req.replace("иеся", "iяся")
            else:
                res_1 = req
        else:
            res_1 = req
    return res_1


def stage_4(result, req):
    res_2 = ""
    if REGPART.search(result):
        if  "S" == REGPART.search(result).group(1):
            try:
                case = REGCASE.search(result).group(1)
                if  case == "дат,ед":
                    res_2 = res_2[:-1] + "ѣ"
                elif  case == "пр,ед":
                    res_2 = res_2[:-1] + "ѣ"
                else:
                    res_2 = req
            except:
                res_2 = req
        elif "A" == REGPART.search(result).group(1):
            if req.endswith("ие"):
                res_2 = req.replace("ие", "iя")
            elif req.endswith("ые"):
                res_2 = req.replace("ые", "ыя")
            elif req.endswith("иеся"):
                res_2 = req.replace("иеся", "iяся")
            else:
                res_2 = req
        else:
            res_2 = req
    else:
        res_2 = req
    for j in range (len(res_2)):
        if res_2[j] == "и":
            try:
                if res_2[j+1] in VOWELS:
                    res_2 = res_2[:j]+"i"+res_2[j+1:]
            except:
                continue
    if res_2[-1] in CONSONANTS:
        res_2 = res_2 + "ъ"
    if res_2.startswith("бес"):
        res_2 = res_2.replace("бес", "без")
    elif res_2.startswith("черес"):
        res_2 = res_2.replace("черес", "через")
    elif res_2.startswith("чрез"):
        res_2 = res_2.replace("чрез", "чрес")
    return res_2


if __name__ == "__main__":
        main()
