from flask import Flask
from bs4 import BeautifulSoup
from urllib.request import urlopen

app = Flask(__name__)

@app.route("/")
def hello_world():
    return """
      <h1>Projeto</h1>
      <a href="/covid-pr">COVID-19 PR</a> - <a href="/sobre">Sobre esse site</a>
      <p>
        Olá, professores e colegas de Master, tudo bem?! Este é o projeto do Tode na disciplina do Turicas do segundo tri.
      </p>
    """

@app.route("/sobre")
def sobre():
    return """
      <h1>Sobre</h1>
      <a href="/">Página inicial</a> - <a href="/covid-pr">COVID-19 PR</a>
      <p>Esse site foi codado por <b>Álvaro Justen</b> durante uma disciplina do MJDA e editado com códigos Python (um pouco-rs) por Thiago Araújo (Tode). É um projeto contínuo até o fim da disciplina.</p>
    """

@app.route("/uol-economia")

def covid_pr():
    casos, obitos = dados_covid_pr()
    return f"""
      <h1>COVID-19: Dados sobre o Paraná</h1>
      <a href="/">Página inicial</a> - <a href="/sobre">Sobre esse site</a>
      <p>
        <b>Casos</b>: {casos}
      </p>
      <p>
        <b>Óbitos</b>: {obitos}
      </p>
    """
