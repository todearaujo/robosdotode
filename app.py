from flask import Flask, render_template, redirect, make_response, send_from_directory
from flask_talisman import Talisman
from urllib.request import urlopen, Request
from lxml import html
import lxml.html.clean
from cachetools import cached, TTLCache
import tweepy
import pandas as pd
import os
from todescrapers import *

cache = TTLCache(maxsize=128, ttl=900)

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

@app.route("/fusoes.webmanifest")
def fusoesmanifest():
    return render_template("fusoes.webmanifest")

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

@app.route('/static/base.css')
def basecss():
    response=make_response(send_from_directory(path='static',directory='static',filename='base.css'))
    response.headers['Content-Type'] = 'text/css'
    return response

@app.route('/static/sites.css')
def sitescss():
    response=make_response(send_from_directory(path='static',directory='static',filename='sites.css'))
    response.headers['Content-Type'] = 'text/css'
    return response

@app.route("/economia")
def economia():
    return redirect('/economia/destaques')

@app.route("/economia/")
def economiabarra():
    return redirect('/economia/destaques')

@app.route("/economia/tweets")
def tweets():
    return redirect('/economia/tweets/fintwit')

@app.route("/economia/tweets/")
def tweetsbarra():
    return redirect('/economia/tweets/fintwit')

@app.route("/economia/destaques")
def economiadestaques():
    
    valor = scrape_a_to_dict('https://valor.globo.com/','//div[@class="container-topo-centralizado grid-x"]//div[@class="highlight__content"]//div[@class="highlight__title theme-title-element "]//a')

    valorinveste = scrape_a_to_dict('https://valorinveste.globo.com/','//div[@class="container-topo-3-colunas grid-x"]//div[@class="highlight__title theme-title-element "]//a')

    infomoney = scrape_a_to_dict('https://www.infomoney.com.br/','//div[@class="row mt-5 default_Big"]//div//div//div//span//a')
    
    investnews = scrape_h_to_dict('https://investnews.com.br/','//div[@class="mvp-feat1-left-wrap relative"]//h2','//div[@class="mvp-feat1-left-wrap relative"]//a')
    
    moneytimes1 = scrape_a_to_dict('https://www.moneytimes.com.br/','//div[@class="home-highlight"]//h2/a')
    moneytimes2 = scrape_a_to_dict('https://www.moneytimes.com.br/','//div[@class="secondary"]//a')
    moneytimes3 = scrape_a_to_dict('https://www.moneytimes.com.br/','//div[@class="home-list"]/div/h3/a')

    moneytimes = {**moneytimes1, **moneytimes2, **moneytimes3}
    
    exame = scrape_h_to_dict('https://exame.com/','//div[contains(@class, "Section__HighlightSection")]//a//h2','//div[contains(@class, "Section__HighlightSection")]//a')
    
    oglobo = scrape_a_to_dict('https://oglobo.globo.com/economia/','//section[@class="block five-teasers"]//div/div/div/article/div/h1/a') 

    oespecialista = scrape_a_to_dict('https://oespecialista.com.br/','//div[@id="front-page-top"]//h3//a')

    uol = scrape_h_to_dict('https://uol.com.br/economia/','//section[contains(@class, "highlights-with-photo")]//h2','//section[contains(@class, "highlights-with-photo")]//a')

    inteligenciaf1 = scrape_a_to_dict('https://inteligenciafinanceira.com.br/','//div[contains(@class, "main-feed__feature")]//h2[contains(@class, "main-feed__title")]//a')
    inteligenciaf2 = scrape_a_to_dict('https://inteligenciafinanceira.com.br/','//a[contains(@class, "list_needtoknow__link")]')

    inteligenciaf = {**inteligenciaf1,**inteligenciaf2}

    sites = dict(infomoney = infomoney, investnews = investnews, moneytimes = moneytimes,  exame = exame,  oglobo = oglobo, 
                valor = valor, valorinveste = valorinveste, oespecialista = oespecialista, uol = uol, inteligenciaf = inteligenciaf)

    return render_template("economia-destaques.html", **sites)

@app.route("/economia/maislidas")
def economiamaislidas():

  investnews = scrape_h_to_dict('https://investnews.com.br/','//div[@class="mvp-feat1-mid-wrap left relative"]//p','//div[@class="mvp-feat1-mid-wrap left relative"]//a')
  
  moneytimes = scrape_a_to_dict('https://www.moneytimes.com.br/ultimas-noticias/','//div[@class="widget widget-maislidas widget-mt-mais-lidas"]//a')
  
  valor = scrape_a_to_dict('https://valor.globo.com/','//div[@data-component-type="card-mais-lidas"]//a')

  valorinveste = scrape_a_to_dict('https://valorinveste.globo.com/','//div[@data-component-type="card-mais-lidas"]//a')
  
  oespecialista = scrape_a_to_dict('https://oespecialista.com.br/','//div[@id="popular-posts"]//li//a')
  
  sites = dict(investnews = investnews, moneytimes = moneytimes, valor = valor, valorinveste = valorinveste, oespecialista = oespecialista)
  
  return render_template("economia-maislidas.html", **sites)

@app.route("/economia/webstories")
def economiawebstories():

  investnews = scrape_h_to_dict('https://investnews.com.br/web-stories/','//li[contains(@class, "mvp-blog-story")]//h2','//li[contains(@class, "mvp-blog-story")]//a')
  
  infomoney = scrape_a_to_dict('https://www.infomoney.com.br/web-stories/','//span[contains(@class, "hl-title")]//a')
  
  sites = dict(investnews = investnews, infomoney = infomoney)
  
  return render_template("economia-webstories.html", **sites)

@app.route("/economia/tweets/top30")
def toptweets():

  consumer_key = os.environ["CONSUMER_KEY_TW"]
  consumer_secret = os.environ["CONSUMER_SECRET_TW"]
  access_token = os.environ["ACCESS_TOKEN_TW"]
  access_token_secret = os.environ["ACCESS_TOKEN_SECRET_TW"]

  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)

  api = tweepy.API(auth)

  tweetssites = api.list_timeline(list_id = '1479520610908876806', count = '50', include_rts = False)

  sitesids = {'ID':[], 'Eng':[]}

  for tweet in tweetssites:
      sitesids["ID"].append(tweet.id)
      sitesids["Eng"].append(tweet.retweet_count + tweet.favorite_count)

  toptweetsdf = pd.DataFrame(sitesids).sort_values(by=['Eng'], ascending=False).head(30).reset_index()
  toptweets = toptweetsdf["ID"].tolist()

  return render_template("economia-tweets-top30.html", toptweets = toptweets)

@app.route("/economia/tweets/fintwit")
def fintwit():

  consumer_key = os.environ["CONSUMER_KEY_TW"]
  consumer_secret = os.environ["CONSUMER_SECRET_TW"]
  access_token = os.environ["ACCESS_TOKEN_TW"]
  access_token_secret = os.environ["ACCESS_TOKEN_SECRET_TW"]

  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)

  api = tweepy.API(auth)

  fintwittweets = api.list_timeline(list_id = '1450084107199844356', count = '150', include_rts = False)

  fintwitids = {'ID':[], 'Eng':[]}

  for tweet in fintwittweets:
      fintwitids["ID"].append(tweet.id)
      fintwitids["Eng"].append(tweet.retweet_count + tweet.favorite_count)

  fintweetsdf = pd.DataFrame(fintwitids).sort_values(by=['Eng'], ascending=False).head(30).reset_index()
  fintweets = fintweetsdf["ID"].tolist()

  return render_template("economia-tweets-fintwit.html", fintweets = fintweets)

@app.route("/fusoes")
def fusoes():
    return redirect('/fusoes/busca')

@app.route("/fusoes/")
def fusoesbarra():
    return redirect('/fusoes/busca')

@app.route("/fusoes/busca")
def fusoesbusca():

  valor = scrape_h_to_dict('https://valor.globo.com/busca/?q=fus%C3%A3o+aquisi%C3%A7%C3%A3o','//div[contains(@class, "widget--info__title")]','//div[contains(@class, "widget--info__text-container")]//a')

  neofeed = scrape_a_to_dict('https://neofeed.com.br/?s=fus%C3%A3o+aquisi%C3%A7%C3%A3o','//div[contains(@class, "td_module_10")]//h3[contains(@class, "entry-title td-module-title")]//a')

  moneytimes = scrape_a_to_dict('https://www.moneytimes.com.br/?s=fus%C3%B5es+aquisi%C3%A7%C3%B5es','//h2[contains(@class, "news-item__title")]//a')

  estadao = scrape_h_to_dict('https://busca.estadao.com.br/?q=fus%C3%A3o+aquisi%C3%A7%C3%A3o','//div[contains(@class, "lista")]//h3','//div[contains(@class, "lista")]//a[contains(@class, "link-title")]')
  
  sites = dict(valor = valor, neofeed = neofeed, moneytimes = moneytimes, estadao = estadao)
  
  return render_template("fusoes-busca.html", **sites)

Talisman(app, content_security_policy=None)