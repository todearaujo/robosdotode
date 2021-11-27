import csv
import datetime
import io
import os
import requests
from flask import Flask, render_template
from flask import request

def dados_covid_pr():
    hoje = datetime.datetime.now().date()
    ontem = hoje - datetime.timedelta(days=1)
    conteudo = None
    for data in (hoje, ontem):
        url1 = f"https://www.saude.pr.gov.br/sites/default/arquivos_restritos/files/documento/{data.year}-{data.month:02d}/INFORME_EPIDEMIOLOGICO_{data.day:02d}_{data.month:02d}_{data.year}_OBITOS_CASOS_Municipio.csv"
        url2 = url1.lower()
        for url in (url1, url2):
            resposta = requests.get(url)
            if resposta.ok:
                conteudo = resposta.content.decode(resposta.apparent_encoding)
                break
        if conteudo:
            break
    if not conteudo:
        return None, None, None
    casos = 0
    obitos = 0
    leitor = csv.DictReader(io.StringIO(conteudo), delimiter=";")
    for registro in leitor:
        casos += int(registro["Casos"])
        obitos += int(registro["Obitos"])

    return data, casos, obitos

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("home.html")

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/covid-pr")
def covid_pr():
    data_ultimo_boletim, casos_pr, obitos_pr = dados_covid_pr()
    return render_template(
        "covid-pr.html", 
        data=data_ultimo_boletim, 
        casos=casos_pr, 
        obitos=obitos_pr
    )
                                                    
@app.route("/telegram", methods=["POST"])
def telegram():
    
    #Token
    token = os.environ["TELEGRAM_TOKEN"]

    #Processa a mensagem
    update = request.json
    chat_id = update["message"]["chat"]["id"]
    text = update["message"]["text"].lower()
    
    if text in ["oi", "ola", "olá", "olar"]:
        answer = "Oi! Como vai?"
    elif text in ["bom dia", "boa tarde", "boa noite"]:
        answer = text
    elif "covid" in  text:
        data, casos, obitos = dados_covid_pr()
        answer = f"Os dados que tenho sobre Covid-19 no PR para a {data} são: {casos} casos e {obitos} obitos."
    else:
        answer = "Não entendi"
        
    #Responde    
    message = {"chat_id": chat_id, "text": answer}
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data=message)
    
    #Finaliza
    return "ok"
