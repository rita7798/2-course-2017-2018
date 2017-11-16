from flask import Flask
from flask import request
import csv

app = Flask(__name__)

@app.route('/')
def info():
    language = request.args['name']
    language = language.capitalize()
    return "Коды для языка " + language + " : " + t1(language) + " " + t2(language) + " " + t3(language) + " " + t97(language) + " " + tnum(language)


def t1(language):
    try:
        request.args['1']
        d1 = {}
        with open("languages.tsv") as f:
            reader = csv.reader (f, delimiter="\t")
            for row in reader:
                for i in row[:1]:
                    d1[i] = row[1]
        a1 = str(d1[language])
    except:
        a1 = ""
    return a1


def t2(language):
    try:
        request.args['2']
        d2 = {}
        with open("languages.tsv") as f:
            reader = csv.reader (f, delimiter="\t")
            for row in reader:
                for i in row[:1]:
                    d2[i] = row[2]
        a2 = str(d2[language])
    except:
        a2 = ""
    return a2


def t3(language):
    try:
        request.args['3']
        d3 = {}
        with open("languages.tsv") as f:
            reader = csv.reader (f, delimiter="\t")
            for row in reader:
                for i in row[:1]:
                    d3[i] = row[3]
        a3 = str(d3[language])
    except:
        a3 = ""
    return a3


def t97(language):
    try:
        request.args['97']
        d97 = {}
        with open("languages.tsv") as f:
            reader = csv.reader (f, delimiter="\t")
            for row in reader:
                for i in row[:1]:
                    d97[i] = row[4]
        a97 = str(d97[language])
    except:
        a97 = ""
    return a97


def tnum(language):
    try:
        request.args['num']
        dnum = {}
        with open("languages.tsv") as f:
            reader = csv.reader (f, delimiter="\t")
            for row in reader:
                for i in row[:1]:
                    dnum[i] = row[5]
        anum = str(dnum[language])
    except:
        anum = ""
    return anum


if __name__ == '__main__':
    app.run(debug=True)
