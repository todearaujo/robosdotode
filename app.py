import csv
import datetime
import io
import os
import requests
from flask import Flask, render_template
from flask import request

def scrapeatodict(page,xpathexp):
  resp = Request(page, headers={'User-Agent': 'Mozilla/5.0'})
  conteudo = urlopen(resp).read().decode("utf-8")
  ohtml = html.fromstring(conteudo)
  
  tagxpath = ohtml.xpath(xpathexp)
  
  dict = {"Título":[], "Link":[]}
  for a in tagxpath:
    dict["Título"].append(a.xpath("text()")[0])
    dict["Link"].append(a.xpath("@href")[0])
  return dict

def scrapeh2todict(page,xpathexph2,xpathexpa):
  resp = Request(page, headers={'User-Agent': 'Mozilla/5.0'})
  conteudo = urlopen(resp).read().decode("utf-8")
  ohtml = html.fromstring(conteudo)
  
  tagxpathh2 = ohtml.xpath(xpathexph2)
  tagxpatha = ohtml.xpath(xpathexpa)
  
  dict = {"Título":[], "Link":[]}
  for h2 in tagxpathh2:
    dict["Título"].append(h2.xpath("text()")[0])
  for a in tagxpatha:
    dict["Link"].append(a.xpath("@href")[0])
  return dict

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("home.html")

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/ronda")
def ronda():
    investnews = pd.DataFrame(scrapeh2todict(
        'https://investnews.com.br/',
        '//div[@class="mvp-feat1-left-wrap relative"]//h2',
        '//div[@class="mvp-feat1-left-wrap relative"]//a'))
    inhtml = investnews.to_html(render_links=True,index=False)
    
    return render_template(
        "ronda.html",
        inhtml = inhtml,
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
