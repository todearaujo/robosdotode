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