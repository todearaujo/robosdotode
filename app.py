import pandas as pd
from flask import Flask, render_template, redirect, url_for, make_response, send_from_directory
from flask_talisman import Talisman
from urllib.request import urlopen, Request
from lxml import html
import lxml.html.clean
from cachetools import cached, TTLCache

cache = TTLCache(maxsize=128, ttl=900)

@cached(cache)
def scrape_a_to_dict(page,xpathexp):
  resp = Request(page, headers={'User-Agent': 'Mozilla/5.0'})
  conteudo = urlopen(resp).read().decode("utf-8")
  ohtml = html.fromstring(conteudo)
  
  tagxpath = ohtml.xpath(xpathexp)

  dict = {"Destaque":[], "Link":[]}
  for a in tagxpath:
    dict["Destaque"].append(lxml.html.fromstring(a.xpath("text()")[0]).text_content().strip())
    dict["Link"].append(a.xpath("@href")[0])
  return dict

@cached(cache)
def scrape_h_to_dict(page,xpathexph2,xpathexpa):
  resp = Request(page, headers={'User-Agent': 'Mozilla/5.0'})
  conteudo = urlopen(resp).read().decode("utf-8")
  ohtml = html.fromstring(conteudo)
  
  tagxpathh2 = ohtml.xpath(xpathexph2)
  tagxpatha = ohtml.xpath(xpathexpa)
  
  dict = {"Destaque":[], "Link":[]}
  for h2 in tagxpathh2:
    dict["Destaque"].append(lxml.html.fromstring(h2.xpath("text()")[0]).text_content().strip())
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

@app.route("/offline")
def offline():
    return render_template("offline.html")

@app.route("/economia.webmanifest")
def economiamanifest():
    return render_template("economia.webmanifest")

@app.route('/sw.js')
def sw():
    response=make_response(send_from_directory(path='templates',directory='templates',filename='sw.js'))
    response.headers['Content-Type'] = 'application/javascript'
    return response

@app.route('/push/ossw.js')
def ossw():
    response=make_response(send_from_directory(path='templates',directory='templates',filename='ossw.js'))
    response.headers['Content-Type'] = 'application/javascript'
    return response

@app.route('/push/ossuw.js')
def ossuw():
    response=make_response(send_from_directory(path='templates',directory='templates',filename='ossuw.js'))
    response.headers['Content-Type'] = 'application/javascript'
    return response

@app.route("/economia")
def economia():
    return redirect(url_for('economiadestaques'))

@app.route("/economia/destaques")
def economiadestaques():
    
    #Valor Econômico
    valor = pd.DataFrame(scrape_a_to_dict('https://valor.globo.com/','//div[@class="container-topo-3-colunas grid-x"]//div[@class="highlight__title theme-title-element "]//a'))
    vehtml = valor.to_html(render_links=True,index=False,escape=True,table_id="valor")
    
    #InfoMoney
    infomoney = pd.DataFrame(scrape_a_to_dict('https://www.infomoney.com.br/','//div[@class="row mt-5 default_Big"]//div//div//div//span//a'))
    imhtml = infomoney.to_html(render_links=True,index=False,escape=True,table_id="infomoney")
    
    #InvestNews
    investnews = pd.DataFrame(scrape_h_to_dict('https://investnews.com.br/','//div[@class="mvp-feat1-left-wrap relative"]//h2','//div[@class="mvp-feat1-left-wrap relative"]//a'))
    inhtml = investnews.to_html(render_links=True,index=False,escape=True,table_id="investnews")
    
    #MoneyTimes
    moneytimesh21 = pd.DataFrame(scrape_a_to_dict('https://www.moneytimes.com.br/','//div[@class="home-highlight"]//h2/a'))
    moneytimesh22 = pd.DataFrame(scrape_a_to_dict('https://www.moneytimes.com.br/','//div[@class="secondary"]//a'))
    moneytimesh3 = pd.DataFrame(scrape_a_to_dict('https://www.moneytimes.com.br/','//div[@class="home-list"]/div/h3/a'))
    moneytimes1 = moneytimesh21.append(moneytimesh22)
    moneytimes = moneytimes1.append(moneytimesh3)
    mthtml = moneytimes.to_html(render_links=True,index=False,escape=True,table_id="moneytimes")
    
    #Exame
    examea1 = pd.DataFrame(scrape_h_to_dict('https://minha.exame.com/',
                                            '//div[contains(@class, "Section__HighlightSection")]//a//h3','//div[contains(@class, "Section__HighlightSection")]//a'))
    examea2 = pd.DataFrame(scrape_h_to_dict('https://exame.com/',
                                            '//div[@class="hide_thumb widget-home-box-item-info"]//a//h2',
                                            '//div[@class="hide_thumb widget-home-box-item-info"]//a[@class="widget-home-box-list-item-title"]'))
    examea3 = pd.DataFrame(scrape_a_to_dict('https://exame.com/',
                                            '//div[@class="highlight-infos"]//span[@class="full-widget-title"]//a'))
    examea4 = pd.DataFrame(scrape_a_to_dict('https://exame.com/',
                                            '//div[@class="highlight-infos"]//li[@class="highlight-bullet"]//a'))

    exame3 = examea1.append(examea2)
    exame4 = exame3.append(examea3)
    exame = exame4.append(examea4)
    ehtml = exame.to_html(render_links=True,index=False,escape=True,table_id="exame")

    #O Globo
    oglobo = pd.DataFrame(scrape_a_to_dict('https://oglobo.globo.com/economia/','//section[@class="block five-teasers"]//div/div/div/article/div/h1/a'))
    oghtml = oglobo.to_html(render_links=True,index=False,escape=True,table_id="oglobo")

    #O Especialista
    oespecialista = pd.DataFrame(scrape_a_to_dict('https://oespecialista.com.br/','//div[@id="front-page-top"]//h3//a'))
    oehtml = oespecialista.to_html(render_links=True,index=False,escape=True,table_id="oespecialista")

    sites = dict(imhtml = imhtml, inhtml = inhtml, mthtml = mthtml, ehtml = ehtml, oghtml = oghtml, vehtml = vehtml, oehtml = oehtml)

    return render_template("economia-destaques.html", **sites)

@app.route("/economia/maislidas")
def economiamaislidas():

  investnews = pd.DataFrame(scrape_h_to_dict('https://investnews.com.br/','//div[@class="mvp-feat1-mid-wrap left relative"]//p','//div[@class="mvp-feat1-mid-wrap left relative"]//a'))
  inhtml = investnews.to_html(render_links=True,index=False,escape=True,table_id="investnews")

  moneytimes = pd.DataFrame(scrape_a_to_dict('https://www.moneytimes.com.br/ultimas-noticias/','//div[@class="widget widget-maislidas widget-mt-mais-lidas"]//a'))
  mthtml = moneytimes.to_html(render_links=True,index=False,escape=True,table_id="moneytimes")

  exame = pd.DataFrame(scrape_h_to_dict('https://exame.com/','//div[@class="widget-popular-posts-info"]//h3','//div[@class="widget-popular-posts-info"]//a'))
  ehtml = exame.to_html(render_links=True,index=False,escape=True,table_id="exame")

  valor = pd.DataFrame(scrape_a_to_dict('https://valor.globo.com/','//div[@data-component-type="card-mais-lidas"]//a'))
  vehtml = valor.to_html(render_links=True,index=False,escape=True,table_id="valor")

  oespecialista = pd.DataFrame(scrape_a_to_dict('https://oespecialista.com.br/','//div[@id="popular-posts"]//li//a'))
  oehtml = oespecialista.to_html(render_links=True,index=False,escape=True,table_id="oespecialista")

  sites = dict(inhtml = inhtml, mthtml = mthtml, ehtml = ehtml, vehtml = vehtml, oehtml = oehtml)
  
  return render_template("economia-maislidas.html", **sites)

@app.route("/economia/maislidas2")
def economiamaislidas2():

  investnews = scrape_h_to_dict('https://investnews.com.br/','//div[@class="mvp-feat1-mid-wrap left relative"]//p','//div[@class="mvp-feat1-mid-wrap left relative"]//a')
  destaques = investnews["Destaque"]
  links = investnews["Link"]
  indict = dict(zip(destaques, links))

  sites = dict(indict = indict)
  
  return render_template("economia-maislidas2.html", **sites, len = len(indict))

Talisman(app, content_security_policy=None)