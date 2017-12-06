from flask import Flask
from flask import request, render_template
import json

app = Flask(__name__)

@app.route('/')
def questions(arr1=None, arr3=None, arr4=None):
    arr1 = ["name", "age"]
    arr3 = ["среднее", "высшее", "неоконченное высшее", "другое"]
    arr4 = [i for i in range(1,4)]
    return render_template('form_questions.html', arr1=arr1, arr3=arr3, arr4=arr4)


@app.route('/thanks')
def writing():
    answer = ""
    if 'name' in request.args:
        name = request.args["name"]
    else:
        name = ""
    if 'age' in request.args:
        age = request.args["age"]
    else:
        age = ""
    if 'degree' in request.args:
        degree = request.args["degree"]
    else:
        degree = ""
    if '1' in request.args:
        a1 = request.args["1"]
    else:
        a1 = ""
    if '2' in request.args:
        a2 = request.args["2"]
    else:
        a2 = ""
    if '3' in request.args:
        a3 = request.args["3"]
    else:
        a3 = ""
    answer = name + "\t" + age + "\t" + degree + "\t" + a1 + "\t" + a2  + "\t" + a3 + "\n"
    with open("answers.tsv", 'a', encoding="utf-8") as f:
        f.write(answer)
    return render_template('form_thanks.html')


@app.route('/main')
def main_page():
    return render_template('form_main.html')


@app.route('/json')
def j_making(arr=None):
    arr= []
    with open("answers.tsv", 'r', encoding="utf-8") as f:
        for line in f.readlines():
            line = line[:-1].split("\t")
            dictionary = {"name": line[0], "age": line[1], "degree": line[2],  "1": line[3], "2": line[4], "3": line[5]}
            arr.append(dictionary)
    j = json.dumps(arr, ensure_ascii=False, indent = 4)
    with open("data.json", 'w', encoding="utf-8") as f:       
        f.write(j)
    return render_template('form_json.html', arr=arr)


@app.route('/search')
def search(arr1=None):
    arr1 = ["среднее", "высшее", "неоконченное высшее", "другое"]
    return render_template('form_search.html', arr1=arr1)


@app.route('/results')
def results(degree = None, arr2=[]):
    degree = ""
    arr2 = []
    with open("data.json", 'r', encoding="utf-8") as f:       
        data = json.load(f)
    degree = str(request.args["degree"])
    for i in range(len(data)):
        if degree == data[i]["degree"]:
            a = data[i]["1"] +"\t"+ data[i]["2"] +"\t"+ data[i]["3"] +";"
            arr2.append(a)
        else:
             continue
    return render_template('form_results.html', degree=degree, arr2=arr2)


@app.route('/stats')
def statictics(total=None, d=None):
    a = 0
    b = 0
    c = 0
    total = 0
    d = dict()
    with open("data.json", 'r', encoding="utf-8") as f:       
        data = json.load(f)
        total = len(data)
    for i in range(len(data)):
        if "Москве" == data[i]["1"]:
            a += 1
        else:
             continue
    answer1 = str(round(a/total*100, 1))
    for i in range(len(data)):
        if "Лондон" == data[i]["2"]:
            b += 1
        else:
             continue
    answer2 = str(round(b/total*100, 1))
    for i in range(len(data)):
        if "Торонто" == data[i]["3"]:
            c += 1
        else:
             continue
    answer3 = str(round(c/total*100, 1))
    d = {"первый":answer1 , "второй":answer2 , "третий":answer3}
    return render_template('form_stats.html', total=total, d=d)
    

if __name__ == '__main__':
    app.run(debug=True)
