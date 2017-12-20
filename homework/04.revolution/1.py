import json
import os
import re
import urllib.request
from flask import Flask
from flask import request, render_template
from operator import itemgetter
from part_2 import stage_1
from part_3 import opening


app = Flask(__name__)

@app.route('/')
def getting_temp(t=None):
    t = ""
    request = urllib.request.Request('https://yandex.ru/pogoda/skopje')
    with urllib.request.urlopen(request) as response:
       code = response.read().decode('utf-8')
    regTemp = re.compile('<div class="temp fact__temp"><span class="temp__value">(.*?)</span>')
    temp = regTemp.findall(code)
    for t in temp:
        return render_template('f.html', t=t)


@app.route('/answer')
def getting_answer(res=None):
    req = str(request.args["word"])
    res = stage_1(req)
    return render_template('form_res.html', res=res)


@app.route('/site') #8 минут...
def making_site(d=None, a=None):
    opening()
    a = []
    d = dict()
    with open("1.txt", "r", encoding="utf-8") as f:
        a = [i for i in f.read().split()]
    for req in a:
        r = stage_1(req)
        if r:
            if r in d:
                d[r] += 1
            else:
                d[r] = 1
    d_sorted = sorted(d.items(), key=itemgetter(1), reverse=True)
    a = d_sorted[:11]
##    with open("d_sort.txt", "w", encoding="utf-8") as f:
##            f.write(str(sorted(d.items(), key=itemgetter(1), reverse=True)))
##    with open("d.txt", "w", encoding="utf-8") as f:
##            f.write(str(d))
    return render_template('form_site.html', d=d, a=a)


@app.route('/test')
def test(d=None):
    d = {"апрель":"апрѣль", "гнездо":"гнѣздо", "деньги":"дѣньги", "индеецъ":"индеѣцъ", "мешокъ":"мѣшокъ",
         "пепелъ":"пѣпелъ", "ремонтъ":"рѣмонтъ", "северъ":"сѣверъ", "тень":"тѣнь", "цепь":"цѣпь"}
    return render_template('form_test.html', d=d)


@app.route('/results')
def results(total=None):
    total=0
    if 'апрель' in request.args:
        if "апрель" != request.args['апрель']:
            total += 1
        else:
            total=total
    else:
        total=total
    if 'гнездо' in request.args:
        if  'гнездо' != request.args['гнездо']:
            total += 1
        else:
            total = total
    else:
        total = total
    if 'деньги' in request.args:
        if  'деньги' == request.args['деньги']:
            total += 1
        else:
            total = total
    else:
        total = total
    if 'индеецъ' in request.args:
        if  'индеецъ' != request.args['индеецъ']:
            total += 1
        else:
            total = total
    else:
        total = total
    if 'мешокъ' in request.args:
        if  'мешокъ' != request.args['мешокъ']:
            total += 1
        else:
            total = total
    else:
        total = total
    if 'пепелъ' in request.args:
        if  'пепелъ' == request.args['пепелъ']:
            total += 1
        else:
            total = total
    else:
        total = total
    if 'ремонтъ' in request.args:
        if  'ремонтъ' == request.args['ремонтъ']:
            total += 1
        else:
            total = total
    else:
        total = total
    if 'северъ' in request.args:
        if  'северъ' != request.args['северъ']:
            total += 1
        else:
            total = total
    else:
        total = total
    if 'тень' in request.args:
        if  'тень' != request.args['тень']:
            total += 1
        else:
            total = total
    else:
        total = total
    if 'цепь' in request.args:
        if  'цепь' != request.args['цепь']:
            total += 1
        else:
            total = total
    else:
        total = total
    return render_template('form_results.html', total=str(total))


@app.route('/clues')
def clues(clues=None):
    with open("clues.txt", "r", encoding="utf-8") as f:
        clues = f.read().split("\n")
    return render_template('form_clues.html', clues=clues)


if __name__ == '__main__':
    app.run(debug=True)
