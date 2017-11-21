from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
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
