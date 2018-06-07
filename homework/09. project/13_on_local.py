# coding: utf-8

# Веб-сервис: На основе сценария сериала (13 reasons why) и марковской модели (например, как тут https://habrahabr.ru/post/88514/)
# программа генерирует предложения в ответ на реплику пользователя

import re
from random import uniform
from collections import defaultdict
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

            
def gen_trigrams(tokens):
    t0, t1 = '$', '$'
    for t2 in tokens:
        yield t0, t1, t2
        if t2 in '.!?':
            yield t1, t2, '$'
            yield t2, '$','$'
            t0, t1 = '$', '$'
        else:
            t0, t1 = t1, t2

            
def train(corpus):
    data = gen_lines(corpus)
    tokens = gen_tokens(data)
    trigrams = gen_trigrams(tokens)
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


def generate_sentence(model, word_last):
    phrase = ''
    t0, t1 = '$', word_last
    phrase += t1
    while 1:
        try:
            t0, t1 = t1, unirand(model[t0, t1])
        except:
            return '.'
        if t1 == '$':
            break
        if t1 in ('.!?,;:\'') or t0 == '$':
            phrase += t1
        elif t0 in ('\''):
            phrase += t1
        else:
            phrase += ' ' + t1
    phrase_ = get_names(phrase)
    return phrase_


def get_names(phrase):
    names = ['Clay', 'Jensen', 'Hannah', 'Baker', 'Tony', 'Padilla', 'Jessica', 'Davis', 'Justin', 'Foley',
             'Bryce', 'Walker', 'Alex', 'Standall', 'Zach', 'Dempsey', 'Tyler', 'Down', 'Lainie', 'Jensen',
             'Kevin', 'Porter', 'Olivia', 'Baker', 'Andy', 'Baker', 'Matt', 'Jensen', 'Courtney', 'Crimsen',
             'Marcus', 'Cole', 'Sheri', 'Holland', 'Ryan', 'Shaver', 'Skye', 'Miller', 'Montgomery', 'Jeff',
             'Atkins', 'Gary', 'Bolan', 'Pam', 'Bradley', 'Caleb', 'Mackenzie', 'Jackie', 'Brad', 'Kat',
             'Bill', 'Greg', 'Davis', 'Karen', 'Dempsey', 'Todd', 'Crimsen', 'Dennis', 'Vasquez', 'Barry',
             'Walker', 'Nora', 'Walker', 'Carolyn', 'Standall', 'Chlöe', 'Rice', 'Sonya', 'Struhl', 'Scott',
             'Reed', 'Nina', 'Jones', 'Rick', 'Wlodimierz']
    for _word in phrase.split():
        word = _word.strip('.!?,;:\'').capitalize()
        if word in names:
            phrase = phrase.replace(_word, word)
    return phrase


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
    sent = s.strip('.!?,;:\'\"\/\\').split()
    word_last = sent[len(sent)-1].lower()
    s = "— " + s
    model = train('13reasons.txt')
    res = generate_sentence(model, word_last)
    for word in res.split():
        if word.isupper() == False:
            res = res.replace(word, word.capitalize())
        break
    if "- " not in res:
        res = "— " + res
    else:
        res = res.replace("- ", "— ")
    return render_template('a.html', word=s, res=res)


if __name__ == '__main__':
    app.run(debug=True)
