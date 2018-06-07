# coding: utf-8

# Веб-сервис: На основе сценария сериала (13 reasons why) и марковской модели (например, как тут https://habrahabr.ru/post/88514/)
# программа генерирует предложения в ответ на реплику пользователя

import re
from random import uniform
from collections import defaultdict
# import json
import os.path
from flask import Flask
from flask import request, render_template


app = Flask(__name__)

@app.route('/')
def start():
    return render_template('q.html')


alphabet = re.compile(u'[a-zA-Z0-9-]+|[.,:;?!]+')
data = []


def gen_lines(corpus):
    with open ('13reasons.txt', 'r', encoding='utf8') as f:
        for line in f.readlines():
            data.append(line.lower())
    return data
            
        
def gen_tokens(data):
    for line in data:
        for token in alphabet.findall(line):
            yield token

            
def gen_trigrams(tokens, word_last):
    t0, t1 = word_last, '$'
    for t2 in tokens:
        yield t0, t1, t2
        if t2 in '.!?':
            yield t1, t2, '$'
            yield t2, '$','$'
            t0, t1 = '$', '$'
        else:
            t0, t1 = t1, t2

            
def train(corpus, word_last):
    data = gen_lines(corpus)
    tokens = gen_tokens(data)
    trigrams = gen_trigrams(tokens, word_last)

    bi, tri = defaultdict(lambda: 0.0), defaultdict(lambda: 0.0)

    for t0, t1, t2 in trigrams:
        bi[t0, t1] += 1
        tri[t0, t1, t2] += 1
        
    model = {}
    for (t0, t1, t2), freq in tri.items():
        if (t0, t1) in model:
            model[t0, t1].append((t2, freq/bi[t0, t1]))
        else:
            model[t0, t1] = [(t2, freq/bi[t0, t1])]
    return model


def generate_sentence(model):
    phrase = ''
    t0, t1 = '$', '$'
    while 1:
        t0, t1 = t1, unirand(model[t0, t1])
        if t1 == '$':
            break
        if t1 in ('.!?,;:') or t0 == '$':
            phrase += t1
        else:
            phrase += ' ' + t1
    return phrase.capitalize()


def unirand(seq):
    sum_, freq_ = 0, 0
    for item, freq in seq:
        sum_ += freq
    rnd = uniform(0, sum_)
    for token, freq in seq:
        freq_ += freq
        if rnd < freq_:
            return token


@app.route('/answer')
def answer(word=None, res=None):
    s = str(request.args["word"])
    sent = s.split()
    word_last = sent[len(sent)-1]
    word = "— " + str(request.args["word"]).capitalize()
    model = train('13reasons.txt', word_last)
    res = generate_sentence(model)
    if "- " not in res:
        res = "— " + res
    else:
        res = res.replace("- ", "— ")
    return render_template('a.html', word=word, res=res)


if __name__ == '__main__':
    app.run(debug=True)
