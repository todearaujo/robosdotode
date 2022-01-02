from urllib.request import urlopen, Request
from lxml import html
import lxml.html.clean
from cachetools import cached, TTLCache

cache = TTLCache(maxsize=10, ttl=900)

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