import time
import html
import urllib.request
import re
import os
import csv


def download_page():
        pageUrl = 'http://gazeta-bam.ru/inova_block_mediaset/7191/card/?page='
        for k in range (73,74): # переход по страницам с новостями (12 штук на каждой странице)  всего -- 760 
                textpage = ""
                number = str(k + 1)
                page = urllib.request.urlopen(pageUrl + number)
                print(number, " страница обрабатывается.")
                time.sleep(2)
                textpage = page.read().decode('utf-8')
                download_news(textpage)
                print("_______________________")


def download_news(textpage):
        news = re.findall('<div class="uil-mo-stat-icons__item uil-mo-stat-icons__item_icon_eye with-text"><a href="(.*?)" title', textpage, flags=re.U | re.DOTALL) # находим все ссылки на 12 страниц с новостями
        print(len(news), " ссылок на новости найдено")
        for j in range(len(news)):
                url = news[j]
                download_newspage(url)


def download_newspage(url):
        fullurl = "http://gazeta-bam.ru/" + url
        print(fullurl, " новость обрабатывается.")
        page = urllib.request.urlopen(fullurl) # переходим на новость
        textnews = page.read().decode('utf-8')
        regAuthor = re.compile("Автор:.*?<span>(\w.*?)\W?</span>", re.DOTALL)
        regName = re.compile("<meta name=\"title\" content=\"(.*?)\"/>", re.DOTALL)
        regCategory = re.compile("<li class=\"uil-mo-popup-card__header__inline-list__categoryes__list__item\">.*?\">(.*?)</a></li>", re.DOTALL)
        regDay = re.compile("<div class=\"uil-mo-popup-card__header__created\">\s*?(\d{2})\..*\s*?</div>", re.DOTALL)
        regMonth = re.compile("<div class=\"uil-mo-popup-card__header__created\">\s*?\d{2}\.(\d{2})\..*\s*?</div>", re.DOTALL)
        regYear = re.compile("<div class=\"uil-mo-popup-card__header__created\">\s*?\d{2}\.\d{2}\.(\d{4}).*\s*?</div>", re.DOTALL)
        if regAuthor.search(textnews) != None:
                author = regAuthor.search(textnews).group(1)
        else:
                author = "no name"
        name = regName.search(textnews).group(1)
        category = regCategory.search(textnews).group(1)
        day = regDay.search(textnews).group(1)
        month = regMonth.search(textnews).group(1)
        year = regYear.search(textnews).group(1)
        data = day + "." + month + "." + year
        metadata(author, name, data, category, fullurl, year, month) # запись метадаты
        clean_t = cleaning(textnews)
        onewordname = name.replace(" ", "")
        making_plain(clean_t, author, onewordname, month, year, data, category, fullurl, name) # запись специального plain текста
        tagged_xml(month, year, onewordname, name) # запись tagged xml текста
        tagged_plain(month, year, onewordname, name) # запись tagged plain текста
        making_plain1(clean_t, author, onewordname, month, year, data, category, fullurl, name) # запись plain текста
        print("page done.")

        
def metadata(author, name, data, category, fullurl, year, month):
        path = "БАМ"+ os.sep + "plain" + os.sep+ year + os.sep + month
        row = '\n{}\t{}\t\t\t{}\t{}\tпублицистика\t\t\t{}\t\tнейтральный\tн-возраст\tн-уровень\tрайонная\t{}\tБАМ\t\t{}\tгазета\tРоссия\tАмурская область\tru'.format(path, author, name, data, category, fullurl, year)
        with open (os.path.join('БАМ', 'metadata.csv'), 'a', encoding = 'utf-8') as f:
                output = csv.writer(f, delimiter='\t')
                output.writerow(["{}\t{}\t\t\t{}\t{}\tпублицистика\t\t\t{}\t\tнейтральный\tн-возраст\tн-уровень\tрайонная\t{}\tБАМ\t\t{}\tгазета\tРоссия\tАмурская область\tru".format(path, author, name, data, category, fullurl, year)])
        print("метаданные записались.")
        return


def cleaning(textnews):
        regTag = re.compile('<.*?>', flags=re.U | re.DOTALL)
        regScript = re.compile('<script>.*?</script>', flags=re.U | re.DOTALL)
        regScript1 = re.compile('<style>.*?</style>', flags=re.U | re.DOTALL) 
        regScript2 = re.compile('<script type.*?>.*?</script>', flags=re.U | re.DOTALL)
        regScript3 = re.compile('<style type.*?>.*?</style>', flags=re.U | re.DOTALL) 
        regComment = re.compile('<!--.*?-->', flags=re.U | re.DOTALL)                            
        clean_t = regScript.sub("", textnews)
        clean_t = regScript1.sub("", clean_t)
        clean_t = regScript2.sub("", clean_t)
        clean_t = regScript3.sub("", clean_t)
        clean_t = regComment.sub("", clean_t)
        clean_t = regTag.sub("", clean_t)
        return clean_t


def making_plain(clean_t, author, onewordname, month, year, data, category, fullurl, name):
        path = "БАМ"+ os.sep + "plain" + os.sep+ year + os.sep + month
        folder = os.path.join(path, onewordname + ".txt")
        if not os.path.exists(path):
                os.makedirs(path)
        with open(folder, 'w', encoding = 'utf-8') as f:
                f.write(html.unescape(clean_t))
        print("неразмеченный специальный текст записан.")
        return


def making_plain1(clean_t, author, onewordname, month, year, data, category, fullurl, name):
        path_dead = "/Users/margaritaberseneva/Desktop/БАМ"+ os.sep + "plain" + os.sep+ year + os.sep + month + os.sep + onewordname + ".txt"
        os.remove(path_dead)
        print("неразмеченный специальный текст удален.")
        plain = "@au " + author + "\n@ti " + name + "\n@da " + data + "\n@topic " + category + "\n@url " + fullurl + "\n" + clean_t
        path = "БАМ"+ os.sep + "plain" + os.sep+ year + os.sep + month
        folder = os.path.join(path, name + ".txt")
        if not os.path.exists(path):
                os.makedirs(path)
        with open(folder, 'w', encoding = 'utf-8') as f:
                f.write(html.unescape(plain))
        print("неразмеченный текст записан.")
        return


def tagged_xml(month, year, onewordname, name):
        path_i = "/Users/margaritaberseneva/Desktop/БАМ/plain/" + year + os.sep + month + os.sep 
        path_o = "/Users/margaritaberseneva/Desktop/БАМ/mystem-xml/" + year + os.sep + month + os.sep
        if not os.path.exists(path_o):
                os.makedirs(path_o)
        os.system("/Users/margaritaberseneva/Downloads/mystem -idn --format xml " + path_i + onewordname + '.txt' + " " + path_o + onewordname + '.xml')
        print("размеченный xml текст готов.")


def tagged_plain(month, year, onewordname, name):
        path_i = "/Users/margaritaberseneva/Desktop/БАМ/plain/" + year + os.sep + month + os.sep
        path_o = "/Users/margaritaberseneva/Desktop/БАМ/mystem-plain/" + year + os.sep + month + os.sep
        if not os.path.exists(path_o):
                os.makedirs(path_o)
        os.system("/Users/margaritaberseneva/Downloads/mystem -idn " + path_i + onewordname + '.txt' + " " + path_o + onewordname + '.txt')
        print("размеченный plain текст готов.")


def main():
        os.mkdir("БАМ")
##        template = 'path' + '\t' + 'author' + '\t' + 'sex' + '\t' + 'birthday' + '\t' + 'header' + '\t' + 'created' + '\t' + 'sphere' + '\t' + 'genre_fi' + '\t' + 'type' + '\t' + 'topic' + '\t' + 'chronotop' + '\t' + 'style' + '\t' + 'audience_age' + '\t' + 'audience_level' + '\t' + 'audience_size' + '\t' + 'source' + '\t' + 'publication' + '\t' + 'publ_year' + '\t' + 'medium' + '\t' + 'country' + '\t' + 'region' + '\t' + 'language'
##        with open (os.path.join('БАМ', 'metadata.csv'), 'w', encoding = 'utf-8') as f:
##                f.write(template)
##
##        with open (os.path.join('БАМ', 'metadata.csv'), 'w', encoding = 'utf-8') as f:
##                output = csv.writer(f, delimiter='\t')
##                header = ['path' + '\t' + 'author' + '\t' + 'sex' + '\t' + 'birthday' + '\t' + 'header' + '\t' + 'created' + '\t' + 'sphere' + '\t' + 'genre_fi' + '\t' + 'type' + '\t' + 'topic' + '\t' + 'chronotop' + '\t' + 'style' + '\t' + 'audience_age' + '\t' + 'audience_level' + '\t' + 'audience_size' + '\t' + 'source' + '\t' + 'publication' + '\t' + 'publ_year' + '\t' + 'medium' + '\t' + 'country' + '\t' + 'region' + '\t' + 'language' ]
##                output.writerow(header)
        download_page()


main()
