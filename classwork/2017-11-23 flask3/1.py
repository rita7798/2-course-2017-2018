from flask import Flask
from flask import request, render_template

app = Flask(__name__)

@app.route('/')
def questions(arr1=None, arr2=None, arr3=None):
    arr1 = ["name", "age"]
    arr2 = ["Мужской", "Женский"]
    arr3 = ["зво́нит", "звони́т"]
    return render_template('form.html', arr1=arr1, arr2=arr2, arr3=arr3)

@app.route('/answer')
def info():
    if 'sex' in request.args:
        a1 = str(request.args["sex"])
    else:
        a1 = ""
    if 'age' in request.args:
        a2 = str(request.args["age"])
    else:
        a2 = ""
    if 'choice' in request.args:
        a3 = str(request.args["choice"])
    else:
        a3 = ""
    text = a1 +"\t"+ a2 +"\t"+ a3
    with open("text.txt", 'r', encoding="utf-8") as f:
        lines = f.readlines()
        if lines == []:
            new_string = str(text)
        else:
            for line in lines:
                new_string = str(line + text)
        h = str(hash(new_string))
    with open("text.txt", 'w', encoding="utf-8") as f:
        f.write(h)
    return str("Записано в документ")


if __name__ == '__main__':
    app.run(debug=True)
