import time, re, html
import urllib.request


def download_page(pageUrl):
        page = urllib.request.urlopen(pageUrl)
        print(pageUrl)
        time.sleep(2)
        text = page.read().decode('ISO-8859-1')
        return text


def making_text(text):
# поиск ненужных частей
        regTag = re.compile('<.*?>', flags=re.U | re.DOTALL)
        regScript = re.compile('<script>.*?</script>', flags=re.U | re.DOTALL) 
        regScript2 = re.compile('<script type.*?>.*?</script>', flags=re.U | re.DOTALL)
        regScript3 = re.compile('<style type.*?>.*?</style>', flags=re.U | re.DOTALL) 
        regComment = re.compile('<!--.*?-->', flags=re.U | re.DOTALL)        
#клининг                     
        clean_t = regScript.sub("", text)
        clean_t = regScript2.sub("", clean_t)
        clean_t = regScript3.sub("", clean_t)
        clean_t = regComment.sub("", clean_t)
        clean_t = regTag.sub("", clean_t)
#запись в файл
        with open('text.txt', 'a', encoding='utf-8') as f:
                f.write(html.unescape(clean_t))


def other_pages(text):
        reg = re.search('<a rel="next" href="(.*?)" title=', text, flags = re.DOTALL)
        if reg == None:
                next_page = None
                return next_page
        else:
                next_page = 'http://www.forumishqiptar.com/' + reg.group(1)
                return next_page


def main():
        print("Обработанные страницы: ")
        link = ""
        urls = []
        pageUrl = 'http://www.forumishqiptar.com/threads/162259-NDIHME-%21%21%21-Per-kontrate-Arrenged-employment-NOC-00-Kanada'
        while True:
                if pageUrl not in urls:
                        urls.append(pageUrl)
                        text = download_page(pageUrl)
                        making_text(text)
                        next_page = other_pages(text)
                        while next_page != None:
                                text = download_page(next_page)
                                making_text(text)
                                next_page = other_pages(text)
                        else:
                                link = re.search('<!-- next / previous links --(.*?)<a href="(.*?)">', text, re.DOTALL )
                                link = link.group(2)                        
                                pageUrl= 'http://www.forumishqiptar.com/' + link
                else:
                        print('Done')
                        break


main()
