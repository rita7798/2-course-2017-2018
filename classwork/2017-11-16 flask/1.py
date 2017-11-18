import csv
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def info():
    d={}
    language = request.args['name']
    language = language.capitalize()
    with open("languages.tsv", encoding = "utf-8") as f:
        for line in f.readlines():
            line = line[:-1].split("\t")
            d[line[0]] = line[1:]
    if '1' in request.args:
        a1 = d[language][0]
    else:
        a1 = ""
    if '2' in request.args:
        a2 = d[language][1]
    else:
        a2 = ""
    if '3' in request.args:
        a3 = d[language][2]
    else:
        a3 = ""
    if '97' in request.args:
        a97 = d[language][3]
    else:
        a97 = ""
    if 'num' in request.args:
        anum = d[language][4]
    else:
        anum = ""
    return "Коды для языка " + language + " : " + a1 + " " + a2 + " " + a3 + " " + a97 + " " + anum


if __name__ == '__main__':
    app.run(debug=True)
