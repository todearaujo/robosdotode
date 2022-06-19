from urllib.request import urlopen, Request
from lxml import html
import lxml.html.clean
import os
import tweepy
import pandas as pd
import os
from GoogleNews import GoogleNews as gn
from cachetools import cached, TTLCache

cache = TTLCache(maxsize=100, ttl=60)

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

@cached(cache)
def gettweets(list, n):
  consumer_key = os.environ["CONSUMER_KEY_TW"]
  consumer_secret = os.environ["CONSUMER_SECRET_TW"]
  access_token = os.environ["ACCESS_TOKEN_TW"]
  access_token_secret = os.environ["ACCESS_TOKEN_SECRET_TW"]

  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)

  api = tweepy.API(auth)

  timeline = api.list_timeline(list_id = list, count = n, include_rts = False)

  ids = {'ID':[], 'Eng':[]}

  for tweet in timeline:
      ids["ID"].append(tweet.id)
      ids["Eng"].append(tweet.retweet_count + tweet.favorite_count)

  df = pd.DataFrame(ids).sort_values(by=['Eng'], ascending=False).head(30).reset_index()
  tweets = df["ID"].tolist()
  return tweets

@cached(cache)
def gnews(termos, periodo):
  getg = gn(lang='pt',encode='utf-8',period=periodo)
  getg.get_news(termos)
  manchetes = getg.results(sort=True)
  return manchetes

@cached(cache)
def gbusca(termos, periodo):
  getg = gn(lang='pt',encode='utf-8',period=periodo)
  getg.search(termos)
  manchetes = getg.results(sort=True)
  return manchetes