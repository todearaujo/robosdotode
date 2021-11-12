from flask import Flask
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv
import io
import requests

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template(
        "home.html")

@app.route("/sobre")
def sobre():
    arquivo = open("templates/sobre.html")
    return arquivo.read()
