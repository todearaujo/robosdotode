from flask import Flask
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv
import io
import requests

def dados_covid_pr():
    url = "https://www.saude.pr.gov.br/sites/default/arquivos_restritos/files/documento/2021-11/INFORME_EPIDEMIOLOGICO_05_11_2021_OBITOS_CASOS_Municipio.csv"
    resposta = requests.get(url)
    conteudo = resposta.content.decode(resposta.apparent_encoding)
  
    casos = 0
    obitos = 0
    leitor = csv.DictReader(io.StringIO(conteudo), delimiter=";")
    for registro in leitor:
        casos += int(registro["Casos"])
        obitos += int(registro["Obitos"])

    return casos, obitos

app = Flask(__name__)

@app.route("/")
def hello_world():
    return """
      <h1>Projeto</h1>
      <a href="/uol-economia">Destaques da home do UOL Economia</a> - <a href="/sobre">Sobre esse site</a>
      <p>
        Olá, professores e colegas de Master, tudo bem?! Este é o projeto do Tode na disciplina do Turicas do segundo tri.
      </p>
    """

@app.route("/sobre")
def sobre():
    arquivo = open("templates/home.html")
    return arquivo.read()
