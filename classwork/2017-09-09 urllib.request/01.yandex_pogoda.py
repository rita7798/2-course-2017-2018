import re
import urllib.request


def getting_code():
    request = urllib.request.Request('https://yandex.ru/pogoda/moscow')
    with urllib.request.urlopen(request) as response:
       code = response.read().decode('utf-8')
       print(code)
    return code


#1
def extracting_temp(code):
    regTemp = re.compile('<div class="current-weather__thermometer current-weather__thermometer_type_now">(.*?)</div>')
    temp = regTemp.findall(code)
    for i in range (len(temp)):
        print("Погода сейчас: ", temp[i])
    regCloud = re.compile('<span class="current-weather__comment">(.*?)</span><div class="current-weather__thermometer current-weather__thermometer_type_now">')
    cloud = regCloud.findall(code)
    for i in range (len(cloud)):
        print("Облачность: ", cloud[i])


#2
def extracting_sun(code):
    regRise = re.compile('<span class="current-weather__info-label">Восход: </span>(.*?)<span')
    rise = regRise.findall(code)
    for i in range (len(rise)):
        print("Восход: ", rise[i])
    regSunset = re.compile('<span class="current-weather__info-label current-weather__info-label_type_sunset">Закат: </span>(.*?)</div>')
    sunset = regSunset.findall(code)
    for i in range (len(sunset)):
        print("Закат: ", sunset[i])

#3
def extracting_tomorrow(code):
    regTd = re.compile('<div class="forecast-brief__item-temp-day" title="Максимальная температура днём">(.*?)</div></div><div')
    td = regTd.findall(code)
    regTn = re.compile('title="Минимальная температура ночью">(.*?)</div>')
    tn = regTn.findall(code)
    for i in range (len(td)):
        for l in range (len(tn)):
            print("Завтра днем:", td[i+1], "\n" "Завтра ночью:", tn[l+1])
            return


#additional
def extracting_actuality(code):
    regTime = re.compile('<div class="current-weather__info-row current-weather__info-row_type_time">(.*?)</div>')
    time = regTime.findall(code)
    regDay = re.compile('<span class="forecast-brief__item-day-name">сегодня</span><span class="forecast-brief__item-day">(.*?)</span>')
    day = regDay.findall(code)
    for i in range (len(time)):
        for l in range (len(day)):
            print(time[i], day[l])
    

def main():
    code = getting_code()
    extracting_temp(code)
    extracting_sun(code)
    extracting_tomorrow(code)
    extracting_actuality(code)

main()
