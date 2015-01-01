# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "seriesblanco"
__category__ = "F"
__type__ = "generic"
__title__ = "Series Blanco"
__language__ = "ES"

host = "http://seriesblanco.com/"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.seriesblanco mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Series", action="series", url=host))
    itemlist.append( Item(channel=__channel__, title="Buscar...", action="search", url=host))

    return itemlist

def search(item,texto):
    logger.info("[pelisalacarta.seriesblanco search texto="+texto)

    itemlist = []

    item.url = "http://seriesblanco.com/search.php?q1=%s" % (texto)
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|<Br>|<BR>|<br>|<br/>|<br />|-\s","",data)
    data = re.sub(r"<!--.*?-->","",data)

    patron = "<div style='float:left;width: 33%;text-align:center;'><a href='([^']+)' title='Capitulos de: ([^']+)'>"

    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        itemlist.append( Item(channel=__channel__, title =scrapedtitle , url=urlparse.urljoin(host,scrapedurl), action="episodios", show=scrapedtitle) )

    try:
        return itemlist
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def series(item):
    logger.info("pelisalacarta.seriesblanco series")

    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|<Br>|<BR>|<br>|<br/>|<br />|-\s","",data)
    data = re.sub(r"<!--.*?-->","",data)

    patron = "<li><a href='([^']+)' title='([^']+)'>[^<]+</a></li>"

    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        itemlist.append( Item(channel=__channel__, title =scrapedtitle , url=urlparse.urljoin(host,scrapedurl), action="episodios", show=scrapedtitle) )

    return itemlist

def episodios(item):
    logger.info("pelisalacarta.seriesblanco episodios")

    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|<Br>|<BR>|<br>|<br/>|<br />|-\s","",data)
    data = re.sub(r"<!--.*?-->","",data)
    data = re.sub(r"a> <img src=/banderas/","a><idioma/",data)
    data = re.sub(r" <img src=/banderas/","|",data)
    data = re.sub(r"\.png border='0' height='13' width='20' /><","/idioma><",data)
    data = re.sub(r"\.png border='0' height='13' width='20' />","",data)

    patron = "<a href='([^']+)'>([^<]+)</a><idioma/([^/]+)/idioma>"

    matches = re.compile(patron,re.DOTALL).findall(data)

    idiomas = {'es':'Español','la':'latino','vos':'VOS','vo':'VO'}

    for scrapedurl, scrapedtitle, scrapedidioma in matches:
        idioma = ""
        for i in scrapedidioma.split("|"):
            idioma+= " [" + idiomas[i] + "]"
        title = item.title + " - " + scrapedtitle + idioma
        itemlist.append( Item(channel=__channel__, title =title , url=scrapedurl, action="findvideos", show=item.show) )

    ## Opción "Añadir esta serie a la biblioteca de XBMC"
    if (config.get_platform().startswith("xbmc") or config.get_platform().startswith("boxee")) and len(itemlist)>0:
        itemlist.append( Item(channel=__channel__, title="Añadir esta serie a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="episodios", show=item.show) )

    return itemlist

def findvideos(item):
    logger.info("pelisalacarta.seriesblanco findvideos")

    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|<Br>|<BR>|<br>|<br/>|<br />|-\s","",data)
    data = re.sub(r"<!--.*?-->","",data)
    data = re.sub(r"<td class='tam12'></td></tr>","<td class='tam12'>SD</td></tr>",data)

    patron = "<td class='tam12'><img src='/banderas/([^\.]+)\.[^']+'[^>]+></td>"
    patron+= "<td class='tam12'>([^<]+)</td>"
    patron+= "<td class='tam12'><img src='/servidores/([^\.]+)\.[^']+'[^>]+></td>"
    patron+= "<td><a class='[^']+' href='([^']+)'[^>]+>"
    patron+= "([^>]+)</a></td>"
    patron+= "<td class='tam12'>[^<]+</td><td class='tam12'>([^<]+)</td></tr>"
    matches = re.compile(patron,re.DOTALL).findall(data)

    idiomas = {'es':'Español','la':'latino','vos':'VOS','vo':'VO'}

    for scrapedidioma, scrapedfecha, scrapedservidor, scrapedurl, scrapedmodo, scrapedcalidad in matches:
        title = scrapedmodo + " [" + scrapedservidor + "] [" + idiomas[scrapedidioma] + "] [" + scrapedcalidad + "] (" + scrapedfecha + ")"
        itemlist.append( Item(channel=__channel__, title =title , url=scrapedurl, action="play", show=item.show) )

    return itemlist

def play(item):
    logger.info("pelisalacarta.channels.seriesblanco play url="+item.url)

    itemlist = servertools.find_video_items(data=item.url)

    for videoitem in itemlist:
        videoitem.title = item.title
        videoitem.channel = __channel__

    return itemlist    
