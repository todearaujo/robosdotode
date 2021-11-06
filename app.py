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
    return """
      <h1>Sobre</h1>
      <a href="/">Página inicial</a> - <a href="/covid-pr">COVID-19 PR</a> - <a href="/uol-economia">Destaques da home do UOL Economia</a> - 
      <p>Esse site foi codado por <b>Álvaro Justen</b> durante uma disciplina do MJDA e editado com códigos Python (um pouco-rs) por Thiago Araújo (Tode). É um projeto contínuo até o fim da disciplina.</p>
    """

@app.route("/uol-economia")

def uol():
  linkuol = "https://economia.uol.com.br/" #Link para extração
  respuol = urlopen(linkuol) #Requisição do conteúdo da página
  conteudouol = respuol.read().decode("utf-8") #Definição da variável com o conteúdo
  soupuol = BeautifulSoup(conteudouol, "html.parser") #Chama o análise do BS

  for a in soupuol.find('div', {"class": "highlights"}).select('a[href]'): #Encontrar destaques e links
    print(a.text.strip()) #Imprimir texto
    print(a['href']) #Imprimir link
    print() #Dar espaço
    return
