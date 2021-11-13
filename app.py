from flask import Flask
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv

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
def home():
    return render_template("home.html")
