from flask import Flask
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv
import io
import requests

app = Flask(__name__)

def dados_covid_pr():
    hoje = datetime.datetime.now().date()
    ontem = hoje - datetime.timedelta(days=1)
    for data in (hoje, ontem):
        url = f"https://www.saude.pr.gov.br/sites/default/arquivos_restritos/files/documento/{data.year}-{data.month:02d}/INFORME_EPIDEMIOLOGICO_{data.day:02d}_{data.month:02d}_{data.year}_OBITOS_CASOS_Municipio.csv"
        resposta = requests.get(url)
        if resposta.ok:
            conteudo = resposta.content.decode(resposta.apparent_encoding)
            break
  
    casos = 0
    obitos = 0
    leitor = csv.DictReader(io.StringIO(conteudo), delimiter=";")
    for registro in leitor:
        casos += int(registro["Casos"])
        obitos += int(registro["Obitos"])

    return data, casos, obitos

@app.route("/")
def hello_world():
    return render_template(
        "home.html")

@app.route("/sobre")
def sobre():
    arquivo = open("templates/sobre.html")
    return arquivo.read()

@app.route("/covid-19")
def covid():
    ultima_data, casos, obitos = dados_covid_pr()
    return datareturn render_template(
        "covid-19.html",
        data=ultima_data,
        casos=casos_pr,
        obitos=obitos_pr
    )
