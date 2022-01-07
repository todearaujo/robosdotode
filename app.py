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

  conteudos = []
  links = []
  dic = {}
  for a in tagxpath:
    conteudos.append(lxml.html.fromstring(a.xpath("text()")[0]).text_content().strip())
    links.append(a.xpath("@href")[0])
    dic = dict(zip(conteudos, links))
  return dic

@cached(cache)
def scrape_h_to_dict(page,xpathexph2,xpathexpa):
  resp = Request(page, headers={'User-Agent': 'Mozilla/5.0'})
  conteudo = urlopen(resp).read().decode("utf-8")
  ohtml = html.fromstring(conteudo)
  
  tagxpathh2 = ohtml.xpath(xpathexph2)
  tagxpatha = ohtml.xpath(xpathexpa)
  
  conteudos = []
  links = []
  dic = {}
  for h2 in tagxpathh2:
    conteudos.append(lxml.html.fromstring(h2.xpath("text()")[0]).text_content().strip())
  for a in tagxpatha:
    links.append(a.xpath("@href")[0])
  dic = dict(zip(conteudos, links))
  return dic

app = Flask(__name__)

@app.route("/")
def home():
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
    response.headers['Cache-Control'] = 'no-cache'
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
    
    valor = scrape_a_to_dict('https://valor.globo.com/','//div[@class="container-topo-3-colunas grid-x"]//div[@class="highlight__title theme-title-element "]//a')

    folha1 = scrape_h_to_dict('https://www1.folha.uol.com.br/mercado/','//div[contains(@class, "c-main-headline")]//a[contains(@class, "c-main-headline")]//h2','//div[contains(@class, "c-main-headline")]//a[contains(@class, "c-main-headline")]')
    folha2 = scrape_h_to_dict('https://www1.folha.uol.com.br/mercado/','//div[contains(@class, "c-headline")]//div[contains(@class, "c-headline__wrapper")]//div[contains(@class, "c-headline__content")]//a//h2[contains(@class, "c-headline__title")]','//div[contains(@class, "c-headline")]//div[contains(@class, "c-headline__wrapper")]//div[contains(@class, "c-headline__content")]//a[contains(@class, "c-headline__url")]')
    
    folha = {**folha1,**folha2}
    
    infomoney = scrape_a_to_dict('https://www.infomoney.com.br/','//div[@class="row mt-5 default_Big"]//div//div//div//span//a')
    
    investnews = scrape_h_to_dict('https://investnews.com.br/','//div[@class="mvp-feat1-left-wrap relative"]//h2','//div[@class="mvp-feat1-left-wrap relative"]//a')
    
    moneytimes1 = scrape_a_to_dict('https://www.moneytimes.com.br/','//div[@class="home-highlight"]//h2/a')
    moneytimes2 = scrape_a_to_dict('https://www.moneytimes.com.br/','//div[@class="secondary"]//a')
    moneytimes3 = scrape_a_to_dict('https://www.moneytimes.com.br/','//div[@class="home-list"]/div/h3/a')

    moneytimes = {**moneytimes1, **moneytimes2, **moneytimes3}
    
    exame1 = scrape_h_to_dict('https://minha.exame.com/','//div[contains(@class, "Section__HighlightSection")]//a//h3','//div[contains(@class, "Section__HighlightSection")]//a')
    exame2 = scrape_h_to_dict('https://exame.com/','//div[@class="hide_thumb widget-home-box-item-info"]//a//h2','//div[@class="hide_thumb widget-home-box-item-info"]//a[@class="widget-home-box-list-item-title"]')
    exame3 = scrape_a_to_dict('https://exame.com/','//div[@class="highlight-infos"]//span[@class="full-widget-title"]//a')
    exame4 = scrape_a_to_dict('https://exame.com/','//div[@class="highlight-infos"]//li[@class="highlight-bullet"]//a')

    exame = {**exame1, **exame2, **exame3, **exame4}

    oglobo = scrape_a_to_dict('https://oglobo.globo.com/economia/','//section[@class="block five-teasers"]//div/div/div/article/div/h1/a') 

    oespecialista = scrape_a_to_dict('https://oespecialista.com.br/','//div[@id="front-page-top"]//h3//a')

    uol = scrape_h_to_dict('https://uol.com.br/economia/','//section[contains(@class, "highlights-with-photo")]//h2','//section[contains(@class, "highlights-with-photo")]//a')

    inteligenciaf1 = scrape_a_to_dict('https://inteligenciafinanceira.com.br/','//div[contains(@class, "main-feed__feature")]//h2[contains(@class, "main-feed__title")]//a')
    inteligenciaf2 = scrape_a_to_dict('https://inteligenciafinanceira.com.br/','//a[contains(@class, "list_needtoknow__link")]')

    inteligenciaf = {**inteligenciaf1,**inteligenciaf2}

    sites = dict(infomoney = infomoney, folha = folha,  investnews = investnews,
                moneytimes = moneytimes,  exame = exame,  oglobo = oglobo, 
                valor = valor, oespecialista = oespecialista, uol = uol, inteligenciaf = inteligenciaf)

    return render_template("economia-destaques.html", **sites)

@app.route("/economia/maislidas")
def economiamaislidas():

  investnews = scrape_h_to_dict('https://investnews.com.br/','//div[@class="mvp-feat1-mid-wrap left relative"]//p','//div[@class="mvp-feat1-mid-wrap left relative"]//a')
  
  moneytimes = scrape_a_to_dict('https://www.moneytimes.com.br/ultimas-noticias/','//div[@class="widget widget-maislidas widget-mt-mais-lidas"]//a')
  
  exame = scrape_h_to_dict('https://exame.com/','//div[@class="widget-popular-posts-info"]//h3','//div[@class="widget-popular-posts-info"]//a')
  
  valor = scrape_a_to_dict('https://valor.globo.com/','//div[@data-component-type="card-mais-lidas"]//a')
  
  oespecialista = scrape_a_to_dict('https://oespecialista.com.br/','//div[@id="popular-posts"]//li//a')
  
  sites = dict(investnews = investnews, moneytimes = moneytimes, exame = exame, valor = valor, oespecialista = oespecialista)
  
  return render_template("economia-maislidas.html", **sites)

@app.route("/economia/webstories")
def economiawebstories():

  investnews = scrape_h_to_dict('https://investnews.com.br/web-stories/','//li[contains(@class, "mvp-blog-story")]//h2','//li[contains(@class, "mvp-blog-story")]//a')
  
  infomoney = scrape_a_to_dict('https://www.infomoney.com.br/web-stories/','//span[contains(@class, "hl-title")]//a')
  
  sites = dict(investnews = investnews, infomoney = infomoney)
  
  return render_template("economia-webstories.html", **sites)

Talisman(app, content_security_policy=None)