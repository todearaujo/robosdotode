from flask import Flask, render_template, redirect, make_response, send_from_directory
from flask_talisman import Talisman
from todescrapers import *

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/chamada/")
def chamada():
    return render_template("chamada.html")

@app.route("/sobre/")
def sobre():
    return render_template("sobre.html")

@app.route("/offline/")
def offline():
    return render_template("offline.html")

@app.route('/<manifest>')
def buildmanifest(manifest):
    return render_template(manifest)

@app.route('/<arquivo>.js')
def js(arquivo):
    response=make_response(send_from_directory(path='templates',directory='templates',filename=arquivo + '.js'))
    response.headers['Content-Type'] = 'application/javascript'
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Charset'] = 'utf-8'
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

@app.route("/economia/<secao>/")
def economia(secao):
    return render_template("/economia/" + secao)

@app.route("/economia/")
def economiahome():
    return redirect('/economia/destaques/')

@app.route("/economia/destaques/")
def economiadestaques():
    
    valor = scrape_a_to_dict('https://valor.globo.com/','//div[contains(@class, "container-topo")]//div[contains(@class, "highlight")]//div[@class="highlight__content"]//h2//a')

    valorinveste = scrape_a_to_dict('https://valorinveste.globo.com/','//div[@class="container-topo-3-colunas grid-x"]//div[@class="highlight__title theme-title-element "]//a')

    infomoney = scrape_a_to_dict('https://www.infomoney.com.br/','//div[@class="row mt-5 default_Big"]//div//div//div//span//a')
    
    investnews = scrape_h_to_dict('https://investnews.com.br/','//div[@class="mvp-feat1-left-wrap relative"]//h2','//div[@class="mvp-feat1-left-wrap relative"]//a')
    
    moneytimes1 = scrape_a_to_dict('https://www.moneytimes.com.br/','//div[@class="home-highlight"]//h2/a')
    moneytimes2 = scrape_a_to_dict('https://www.moneytimes.com.br/','//div[@class="secondary"]//a')
    moneytimes3 = scrape_a_to_dict('https://www.moneytimes.com.br/','//div[@class="home-list"]/div/h3/a')

    moneytimes = {**moneytimes1, **moneytimes2, **moneytimes3}

    inteligenciaf1 = scrape_a_to_dict('https://inteligenciafinanceira.com.br/','//span[contains(@class, "home-new__featured-article")]//a')
    inteligenciaf2 = scrape_a_to_dict('https://inteligenciafinanceira.com.br/','//span[contains(@class, "home-new__articles__article-card")]//a')

    inteligenciaf = {**inteligenciaf1,**inteligenciaf2}

    sites = dict(infomoney = infomoney, investnews = investnews, moneytimes = moneytimes,  valor = valor, valorinveste = valorinveste, inteligenciaf = inteligenciaf)

    return render_template("economia-destaques.html", **sites)

@app.route("/economia/maislidas/")
def economiamaislidas():

  investnews = scrape_h_to_dict('https://investnews.com.br/','//div[@class="mvp-feat1-mid-wrap left relative"]//p','//div[@class="mvp-feat1-mid-wrap left relative"]//a')
  
  moneytimes = scrape_a_to_dict('https://www.moneytimes.com.br/ultimas-noticias/','//div[@class="widget widget-maislidas widget-mt-mais-lidas"]//a')
  
  valor = scrape_a_to_dict('https://valor.globo.com/','//div[@data-component-type="card-mais-lidas"]//a')

  valorinveste = scrape_a_to_dict('https://valorinveste.globo.com/','//div[@data-component-type="card-mais-lidas"]//a')

  inteligenciaf = scrape_a_to_dict('https://inteligenciafinanceira.com.br/saiba/','//div[contains(@class, "most-viewed")]//li[contains(@class, "list_mostviewed")]//div//div//a')
 
  sites = dict(investnews = investnews, moneytimes = moneytimes, valor = valor, valorinveste = valorinveste, inteligenciaf = inteligenciaf)
  
  return render_template("economia-maislidas.html", **sites)

@app.route("/economia/webstories/")
def economiawebstories():

  investnews = scrape_h_to_dict('https://investnews.com.br/web-stories/','//li[contains(@class, "mvp-blog-story")]//h2','//li[contains(@class, "mvp-blog-story")]//a')
  
  infomoney = scrape_a_to_dict('https://www.infomoney.com.br/web-stories/','//span[contains(@class, "hl-title")]//a')

  inteligenciaf = scrape_a_to_dict('https://inteligenciafinanceira.com.br/web-stories/','//div[contains(@class, "main-feed__title-area")]//span[contains(@class, "main-feed")]//a')

  suno = scrape_h_to_dict('https://www.suno.com.br/web-stories/','//div[contains(@class, "webStories")]//h2','//div[contains(@class, "webStories")]//a')
 
  sites = dict(investnews = investnews, infomoney = infomoney, inteligenciaf = inteligenciaf, suno = suno)
  
  return render_template("economia-webstories.html", **sites)

@app.route("/fusoes/<secao>/")
def fusoes(secao):
    if secao == "busca":
        valor = scrape_h_to_dict('https://valor.globo.com/busca/?q=fus%C3%A3o+aquisi%C3%A7%C3%A3o','//div[contains(@class, "widget--info__title")]','//div[contains(@class, "widget--info__text-container")]//a')
        neofeed = scrape_a_to_dict('https://neofeed.com.br/?s=fus%C3%A3o+aquisi%C3%A7%C3%A3o','//div[contains(@class, "td_module_10")]//h3[contains(@class, "entry-title td-module-title")]//a')
        moneytimes = scrape_a_to_dict('https://www.moneytimes.com.br/?s=fus%C3%B5es+aquisi%C3%A7%C3%B5es','//h2[contains(@class, "news-item__title")]//a')
        estadao = scrape_h_to_dict('https://busca.estadao.com.br/?q=fus%C3%A3o+aquisi%C3%A7%C3%A3o','//div[contains(@class, "lista")]//h3','//div[contains(@class, "lista")]//a[contains(@class, "link-title")]')
        sites = dict(valor = valor, neofeed = neofeed, moneytimes = moneytimes, estadao = estadao)
        return render_template("fusoes-busca.html", **sites) 
    elif secao == "gnews":
        conteudo = gnews("fusões e aquisições", "7d")
        return render_template("fusoes-gnews.html", conteudo = conteudo)   
    elif secao == "gbusca":
        conteudo = gbusca("fusões e aquisições", "7d")
        return render_template("fusoes-gbusca.html", conteudo = conteudo)

Talisman(app, content_security_policy=None)