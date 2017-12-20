import html
import json
import re
import urllib.request

PAGE = "http://www.dorev.ru/ru-index.html"
URL = "http://www.dorev.ru/"

REGPAGE = re.compile("bgcolor=\"#CCCCCC\"><a href=\"(.{18})", flags=re.U | re.DOTALL)

REG1 = re.compile("<td class=\"uu\">(\w{2,15})</td><td></td><td class=\"uu\">(\w{2,15})</td><td align=\"center\">", flags=re.U | re.DOTALL)
REG2 = re.compile("<td class=\"uu\">(\w{2,15})</td><td></td><td class=\"uu\">(\w{1,9})<span.*\"u1\">(\w{1}).*</span>(\w{1,7})</td>", flags=re.U | re.DOTALL)
REG3 = re.compile("<td class=\"uu\">(\w{2,15})</td><td></td><td class=\"uu\">(\w{1,9})<span.*\"u1\">(\w{1}).*</span>(\w{1,9})(</td>| \(|, )", flags=re.U | re.DOTALL)

# это рабочий кусок кода (функция ниже), когда я начинала делать, все было ок,
# но за день до дедлайна сайт стал блочить, поэтому пользуюсь уже скачанным словарем,
# но функционал в программе оставляю

def download_main_page(PAGE):
        page = urllib.request.urlopen(PAGE)
        text = page.read().decode('windows-1251')
        if REGPAGE.findall(text):
                res = REGPAGE.findall(text)
        else:
                print("Не удалось скачать словарь.")
                res = ""
        return res       


def download_page(pageUrl):
        page = urllib.request.urlopen(pageUrl)
        text = page.read().decode('windows-1251').replace("color", "\n")
        text = text.split("\n")
        return text


def getting_text(text, d, dictionary):
        for i in range(len(text)):
                if REG1.search(text[i]):
                        res = REG1.search(text[i]).group(1)
                        res2 = REG1.search(text[i]).group(2)
                        d = {res : res2}
                        dictionary.update(d)
                elif REG2.search(text[i]):
                        res = REG2.search(text[i]).group(1)
                        res2 = REG2.search(text[i]).group(2)+REG2.search(text[i]).group(3)+REG2.search(text[i]).group(4)
                        d = {res : res2}
                        dictionary.update(d)
                elif REG3.search(text[i]):
                        res = REG3.search(text[i]).group(1)
                        res2 = REG3.search(text[i]).group(2)+REG3.search(text[i]).group(3)+REG3.search(text[i]).group(4)
                        d = {res : res2}
                        dictionary.update(d)
                else:
                        continue
        return dictionary

                
def main():
        d = dict()
        dictionary= dict()
        res = download_main_page(PAGE)
        for i in res:
                pageUrl = URL + i
                text = download_page(pageUrl) 
                getting_text(text, d, dictionary)
        j = json.dumps(dictionary, ensure_ascii=False, indent = 4)
        with open("data.json", 'w', encoding="utf-8") as f:       
                f.write(j)
                                      

if __name__ == "__main__":
        main()
