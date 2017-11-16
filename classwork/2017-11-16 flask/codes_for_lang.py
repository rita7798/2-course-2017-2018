from flask import Flask
from flask import request
import csv

app = Flask(__name__)

@app.route('/')
def info():
    language = request.args['name']
    language = language.capitalize()
    lang = {}
    with open("languages.tsv") as f:
        reader = csv.reader (f, delimiter="\t")
        for row in reader:
            for i in row[:1]:
                a = ', '.join(row[1:])
                lang[i] = a
                if language in lang: 
                    return "Коды для языка " + language + " : " + str(lang[language])
            

if __name__ == '__main__':
    app.run(debug=True)

