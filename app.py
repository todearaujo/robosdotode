import csv
import datetime
import requests
from urllib.request import urlopen, Request
from lxml import html
import pandas as pd
from flask import Flask, render_template, render_template_string, make_response
from flask import request

def scrapeatodict(page,xpathexp):
  resp = Request(page, headers={'User-Agent': 'Mozilla/5.0'})
  conteudo = urlopen(resp).read().decode("utf-8")
  ohtml = html.fromstring(conteudo)
  
  tagxpath = ohtml.xpath(xpathexp)
  
  dict = {"Destaque":[], "Link":[]}
  for a in tagxpath:
    dict["Destaque"].append(a.xpath("text()")[0])
    dict["Link"].append(a.xpath("@href")[0])
  return dict

def scrapeh2todict(page,xpathexph2,xpathexpa):
  resp = Request(page, headers={'User-Agent': 'Mozilla/5.0'})
  conteudo = urlopen(resp).read().decode("utf-8")
  ohtml = html.fromstring(conteudo)
  
  tagxpathh2 = ohtml.xpath(xpathexph2)
  tagxpatha = ohtml.xpath(xpathexpa)
  
  dict = {"Destaque":[], "Link":[]}
  for h2 in tagxpathh2:
    dict["Destaque"].append(h2.xpath("text()")[0])
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
    
    #Valor Econômico
    valor = pd.DataFrame(scrapeatodict('https://valor.globo.com/',
                                       '//div[@class="container-topo-3-colunas grid-x"]//div[@class="highlight__title theme-title-element "]//a'))
    vehtml = valor.to_html(render_links=True,index=False,escape=True,table_id="valor")
    
    #InfoMoney
    infomoney = pd.DataFrame(scrapeatodict('https://www.infomoney.com.br/',
                                           '//div[@class="row mt-5 default_Big"]//div//div//div//span//a'))
    imhtml = infomoney.to_html(render_links=True,index=False,escape=True,table_id="infomoney")
    
    #InvestNews
    investnews = pd.DataFrame(scrapeh2todict('https://investnews.com.br/',
                                             '//div[@class="mvp-feat1-left-wrap relative"]//h2',
                                             '//div[@class="mvp-feat1-left-wrap relative"]//a'))
    inhtml = investnews.to_html(render_links=True,index=False,escape=True,table_id="investnews")
    
    #MoneyTimes
    moneytimesh21 = pd.DataFrame(scrapeatodict('https://www.moneytimes.com.br/',
                                               '//div[@class="home-highlight"]//h2/a'))
    moneytimesh22 = pd.DataFrame(scrapeatodict('https://www.moneytimes.com.br/',
                                               '//div[@class="secondary"]//a'))
    moneytimesh3 = pd.DataFrame(scrapeatodict('https://www.moneytimes.com.br/',
                                              '//div[@class="home-list"]/div/h3/a'))
    moneytimes1 = moneytimesh21.append(moneytimesh22)
    moneytimes = moneytimes1.append(moneytimesh3)
    mthtml = moneytimes.to_html(render_links=True,index=False,escape=True,table_id="moneytimes")
    
    #UOL
    #uol = pd.DataFrame(scrapeh2todict('https://economia.uol.com.br/',
    #                                  '//div[@class="highlights"]//a//h2','//div[@class="highlights"]//div/a'))
    #uhtml = uol.to_html(render_links=True,index=False,escape=True,table_id="uol")
    
    #Exame
    examea1 = pd.DataFrame(scrapeh2todict('https://minha.exame.com/',
                                          '//div[@class="hide_thumb widget-home-box-item-info"]//a[@class="widget-home-box-list-item-title"]//h2',
                                          '//div[@class="hide_thumb widget-home-box-item-info"]//a[@class="widget-home-box-list-item-title"]'))
    examea2 = pd.DataFrame(scrapeh2todict('https://exame.com/',
                                          '//div[@class="hide_thumb widget-home-box-item-info"]//a//h2',
                                          '//div[@class="hide_thumb widget-home-box-item-info"]//a[@class="widget-home-box-list-item-title"]'))
    examea3 = pd.DataFrame(scrapeatodict('https://exame.com/',
                                         '//div[@class="highlight-infos"]//span[@class="full-widget-title"]//a'))
    examea4 = pd.DataFrame(scrapeatodict('https://exame.com/',
                                         '//div[@class="highlight-infos"]//li[@class="highlight-bullet"]//a'))

    exame3 = examea1.append(examea2)
    exame4 = exame3.append(examea3)
    exame = exame4.append(examea4)
    ehtml = exame.to_html(render_links=True,index=False,escape=True,table_id="exame")

    #O Globo
    oglobo = pd.DataFrame(scrapeatodict('https://oglobo.globo.com/economia/',
                                        '//section[@class="block five-teasers"]//div/div/div/article/div/h1/a'))
    oghtml = oglobo.to_html(render_links=True,index=False,escape=True,table_id="oglobo")

    return render_template(
        "ronda.html",
        imhtml = imhtml,
        inhtml = inhtml,
        mthtml = mthtml,
        uhtml = uhtml,
        ehtml = ehtml,
        oghtml = oghtml,
        vehtml = vehtml,
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
