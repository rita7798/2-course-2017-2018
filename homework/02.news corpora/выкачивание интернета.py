import time
import html
import urllib.request
import re
import os
import csv


PAGEURL = 'http://gazeta-bam.ru/inova_block_mediaset/7191/card/?page='

REGAUTHOR = re.compile("Автор:.*?<span>(\w.*?)\W?</span>", re.DOTALL)
REGNAME = re.compile("<meta name=\"title\" content=\"(.*?)\"/>", re.DOTALL)
REGCATEGORY = re.compile("<li class=\"uil-mo-popup-card__header__inline-list__categoryes__list__item\">.*?\">(.*?)</a></li>", re.DOTALL)
REGDAY = re.compile("<div class=\"uil-mo-popup-card__header__created\">\s*?(\d{2})\..*\s*?</div>", re.DOTALL)
REGMONTH = re.compile("<div class=\"uil-mo-popup-card__header__created\">\s*?\d{2}\.(\d{2})\..*\s*?</div>", re.DOTALL)
REGYEAR = re.compile("<div class=\"uil-mo-popup-card__header__created\">\s*?\d{2}\.\d{2}\.(\d{4}).*\s*?</div>", re.DOTALL)

REGTAG = re.compile('<.*?>', flags=re.U | re.DOTALL)
REGSCRIPT = re.compile('<script>.*?</script>', flags=re.U | re.DOTALL)
REGSCRIPT1 = re.compile('<style>.*?</style>', flags=re.U | re.DOTALL) 
REGSCRIPT2 = re.compile('<script type.*?>.*?</script>', flags=re.U | re.DOTALL)
REGSCRIPT3 = re.compile('<style type.*?>.*?</style>', flags=re.U | re.DOTALL) 
REGCOMMENT = re.compile('<!--.*?-->', flags=re.U | re.DOTALL) 


def download_page():
        for k in range (1,763): # переход по страницам с новостями (12 штук на каждой странице) выкачала до 633, всего -- 763 (3.10.17)
                textpage = ""
                number = str(k + 1)
                page = urllib.request.urlopen(PAGEURL + number)
                print("{} страница обрабатывается".format(k))
                time.sleep(2)
                textpage = page.read().decode('utf-8')
                download_news(textpage)
                print("_______________________")


def download_news(textpage):
        news_set = set()
        news = re.findall('<div class="uil-mo-stat-icons__item uil-mo-stat-icons__item_icon_eye with-text"><a href="(.*?)" title', textpage, flags=re.U | re.DOTALL) # находим все ссылки на 12 страниц с новостями
        for i in range(len(news)):
                news_set.add(news[i])
        print(len(news_set), " ссылок на новости найдено")
        for j in news_set:
                url = j
                download_newspage(url)


def download_newspage(url):
        time.sleep(2)
        fullurl = "http://gazeta-bam.ru/{}".format(url)
        print("{} новость обрабатывается.".format(fullurl))
        try:
                page = urllib.request.urlopen(fullurl)
        except:
                print("Error at the {}".format(page))
        textnews = page.read().decode('utf-8')
        information(textnews, fullurl)


def information(textnews, fullurl):
        if REGAUTHOR.search(textnews):
                author = REGAUTHOR.search(textnews).group(1)
        else:
                author = ""
        name = REGNAME.search(textnews).group(1)
        category = REGCATEGORY.search(textnews).group(1)
        day = REGDAY.search(textnews).group(1)
        month = REGMONTH.search(textnews).group(1)
        year = REGYEAR.search(textnews).group(1)
        data = "{}.{}.{}".format(day, month, year)
        metadata(author, name, data, category, fullurl, year, month) # запись метадаты
        clean_t = cleaning(textnews)
        onewordname = name.replace(" ", "_")
        onewordname = re.sub("[.,!?()\"-\/]", "", onewordname )
        making_plain(clean_t, author, onewordname, month, year, data, category, fullurl, name) # запись специального plain текста
        tagged_xml(month, year, onewordname, name) # запись tagged xml текста
        tagged_plain(month, year, onewordname, name) # запись tagged plain текста
        making_plain1(clean_t, author, onewordname, month, year, data, category, fullurl, name) # запись plain текста
        print("page done.")

        
def metadata(author, name, data, category, fullurl, year, month):
        path = "БАМ{}plain{}{}{}{}".format(os.sep, os.sep, year, os.sep, month)
        row = '\n{}\t{}\t\t\t{}\t{}\tпублицистика\t\t\t{}\t\tнейтральный\tн-возраст\tн-уровень\tрайонная\t{}\tБАМ\t\t{}\tгазета\tРоссия\tАмурская область\tru'.format(path, author, name, data, category, fullurl, year)
        with open (os.path.join('БАМ', 'metadata.csv'), 'a', encoding = 'utf-8') as f:
                output = csv.writer(f, delimiter='\t')
                output.writerow(["{}\t{}\t\t\t{}\t{}\tпублицистика\t\t\t{}\t\tнейтральный\tн-возраст\tн-уровень\tрайонная\t{}\tБАМ\t\t{}\tгазета\tРоссия\tАмурская область\tru".format(path, author, name, data, category, fullurl, year)])
        print("метаданные записались.")
        return


def cleaning(textnews):                          
        clean_t = REGSCRIPT.sub("", textnews)
        clean_t = REGSCRIPT1.sub("", clean_t)
        clean_t = REGSCRIPT2.sub("", clean_t)
        clean_t = REGSCRIPT3.sub("", clean_t)
        clean_t = REGCOMMENT.sub("", clean_t)
        clean_t = REGTAG.sub("", clean_t)
        return clean_t


def making_plain(clean_t, author, onewordname, month, year, data, category, fullurl, name):
        path = "БАМ{}plain{}{}{}{}".format(os.sep, os.sep, year, os.sep, month)
        folder = os.path.join("{}{}{}.txt".format(path, os.sep, onewordname))
        if not os.path.exists(path):
                os.makedirs(path)
        with open(folder, 'w', encoding = 'utf-8') as f:
                f.write(html.unescape(clean_t))
        print("неразмеченный специальный текст записан.")
        return


def making_plain1(clean_t, author, onewordname, month, year, data, category, fullurl, name):
        plain = "@au {}\n@ti {}\n@da {}\n@topic {}\n@url {}\n{}".format(author, name, data, category, fullurl, clean_t)
        path = "БАМ{}plain{}{}{}{}" .format(os.sep,  os.sep, year, os.sep, month)
        folder = os.path.join(path, onewordname + ".txt")
        if not os.path.exists(path):
                os.makedirs(path)
        with open(folder, 'w', encoding = 'utf-8') as f:
                f.write(html.unescape(plain))
        print("неразмеченный текст записан.")
        return


def tagged_xml(month, year, onewordname, name):
        path_i = "/Users/margaritaberseneva/Desktop/БАМ/plain/{}{}{}{}".format(year, os.sep, month, os.sep)
        path_o = "/Users/margaritaberseneva/Desktop/БАМ/mystem-xml/{}{}{}{}".format(year, os.sep, month, os.sep)
        if not os.path.exists(path_o):
                os.makedirs(path_o)
        os.system(("/Users/margaritaberseneva/Downloads/mystem -idn --format xml {}{}.txt {}{}.xml").format(path_i, onewordname, path_o, onewordname))
        print("размеченный xml текст готов.")


def tagged_plain(month, year, onewordname, name):
        path_i = "/Users/margaritaberseneva/Desktop/БАМ/plain/{}{}{}{}".format(year, os.sep, month, os.sep)
        path_o = "/Users/margaritaberseneva/Desktop/БАМ/mystem-plain/{}{}{}{}".format(year, os.sep, month, os.sep)
        if not os.path.exists(path_o):
                os.makedirs(path_o)
        os.system(("/Users/margaritaberseneva/Downloads/mystem -idn {}{}.txt {}{}.txt").format(path_i, onewordname, path_o, onewordname))
        print("размеченный plain текст готов.")


def main():
        if not os.path.exists("/Users/margaritaberseneva/Desktop/БАМ"):
                os.mkdir("БАМ")
        with open (os.path.join('БАМ', 'metadata.csv'), 'a', encoding = 'utf-8') as f:
                output = csv.writer(f, delimiter='\t')
                header = ['path' + '\t' + 'author' + '\t' + 'sex' + '\t' + 'birthday' + '\t' + 'header' + '\t' + 'created' + '\t' + 'sphere' + '\t' + 'genre_fi' + '\t' + 'type' + '\t' + 'topic' + '\t' + 'chronotop' + '\t' + 'style' + '\t' + 'audience_age' + '\t' + 'audience_level' + '\t' + 'audience_size' + '\t' + 'source' + '\t' + 'publication' + '\t' + 'publ_year' + '\t' + 'medium' + '\t' + 'country' + '\t' + 'region' + '\t' + 'language' + '\n']
                output.writerow(header)
        download_page()


if __name__ == "__main__":
        main()
