import re
import urllib.request


def getting_code():
    request = urllib.request.Request('http://gazeta-bam.ru')
    with urllib.request.urlopen(request) as response:
       code = response.read().decode('utf-8')
    return code


def extracting_headers(code):
    regTitles = re.compile('<h2 class=\"uil-.*?/\">(.*?)</a></h2>')
    titles = regTitles.findall(code)
    return titles


def making_list(titles):
    for i in range (len(titles)):
        with open('list.txt', 'w', encoding='utf-8') as f:
            for i in range (len(titles)):
                l= str(i+1)
                heading = l + ". " + titles[i] + "\n"
                f.write(heading)


def main():
    code = getting_code()
    titles = extracting_headers(code)
    making_list(titles)
    print("Done")


main()
