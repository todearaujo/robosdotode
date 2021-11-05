from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Olá, <b>Tode</b>!</p>"

@app.route("/sobre")
def sobre():
    return "<h1>Sobre</h1> <p>Esse site foi criado por <b>Álvaro Justen</b>.</p>"
