# coding: utf-8

import json
import os.path
import random
import urllib.request
from flask import Flask
from flask import request, render_template
from pymorphy2 import MorphAnalyzer
from pymystem3 import Mystem
import key 


morph = MorphAnalyzer()

app = Flask(__name__)

@app.route('/')
def start():
    return render_template('q.html')


def mystem(sentence):
    m = Mystem()
    mystem_lemmas = []
    lemmas = m.lemmatize(sentence)
    for lemma in lemmas:
        ana = m.analyze(lemma)
        for analysis in ana:
            if 'analysis' in analysis:
                mystem_lemmas.append(lemma)
    return mystem_lemmas


def morphy(sentence, mystem_lemmas):
    grammems = set()
    sentence_parts = []
    sentence_parced = []
    for word in sentence.split():
        word = word.strip('.,!?*()«»„“\'";:-')
        if word:
            for lemma in mystem_lemmas:
                ana = morph.parse(word)
                for analysis in ana:
                    if analysis.normal_form == lemma:
                        grammems.add(analysis.tag.POS)
                        grammems.add(analysis.tag.animacy)
                        grammems.add(analysis.tag.aspect)
                        grammems.add(analysis.tag.case)
                        grammems.add(analysis.tag.gender)
                        grammems.add(analysis.tag.involvement)
                        grammems.add(analysis.tag.mood)
                        grammems.add(analysis.tag.number)
                        grammems.add(analysis.tag.person)
                        grammems.add(analysis.tag.tense)
                        grammems.add(analysis.tag.transitivity)
                        grammems.add(analysis.tag.voice)
                        grammems.remove(None)
                        sentence_parts.append(analysis.normalized.tag.POS)
                        sentence_parced.append(grammems)
                        break
                    else:
                        continue
                if grammems == set():
                    first = ana[0]
                    grammems.add(first.tag.animacy)
                    grammems.add(first.tag.aspect)
                    grammems.add(first.tag.case)
                    grammems.add(first.tag.gender)
                    grammems.add(first.tag.involvement)
                    grammems.add(first.tag.mood)
                    grammems.add(first.tag.number)
                    grammems.add(first.tag.person)
                    grammems.add(first.tag.tense)
                    grammems.add(first.tag.transitivity)
                    grammems.add(first.tag.voice)
                    grammems.remove(None)
                    sentence_parts.append(first.normalized.tag.POS)
                    sentence_parced.append(grammems)
                mystem_lemmas.pop(0)
                grammems = set()
                break
    return sentence_parts, sentence_parced


def getting_worlds():
    with open ('wall.txt', 'w', encoding='utf-8') as f:
        req = urllib.request.Request('https://api.vk.com/method/wall.get?owner_id=-34215577&count=100&v=5.74&access_token={}'.format(key.access))
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
        data = json.loads(html)
        for j in range(100):
            f.write(data["response"]["items"][j]['text']+'\n')


def listing_words():
    words = {}
    if os.path.exists('wall.txt') == False:
        getting_worlds()
    with open ('wall.txt', 'r', encoding='utf-8') as f:
        text = f.read().lower().split()
    for word in text:
        if word != '—':
            new_word = word.strip('.,!?*()«»„“\'";:-')
            ana = morph.parse(new_word)
            first = ana[0]
            if first.tag.POS:
                words[first.word] = [first.tag.POS]
            else:
                continue
    return words


def choosing_words(sentence_parts, sentence_parced, words):
    candidates = []
    new_sent = []
    for part in sentence_parts:
        for k,v in words.items():
            if part == v[0]:
                candidates.append(k)
            else:
                continue
        for tags in sentence_parced:
            while candidates:
                candidate = random.choice(candidates)
                chance = morph.parse(candidate)[0]
                if chance.inflect(tags):
                    new_sent.append((chance.inflect(tags)).word)
                    candidates = []
                else:
                    continue
            sentence_parced.pop(0)
            break
    s = ' '.join(new_sent)
    return s


@app.route('/answer')
def answer(res=None):
    sentence = str(request.args["word"])
    mystem_lemmas = mystem(sentence)
    sentence_parts, sentence_parced = morphy(sentence, mystem_lemmas)
    words = listing_words()
    s = choosing_words(sentence_parts, sentence_parced, words)
    res = s.capitalize()
    return render_template('a.html', res=res)


if __name__ == '__main__':
    app.run(debug=True)
