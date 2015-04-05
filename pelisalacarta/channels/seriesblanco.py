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
idiomas = {'es':'Español','la':'Latino','vos':'VOS','vo':'VO'}

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.seriesblanco mainlist")

    itemlist = []
    itemlist.append( Item( channel=__channel__, title="Series", action="series", url=urlparse.urljoin(host,"lista_series/") ) )
    itemlist.append( Item( channel=__channel__, title="Buscar...", action="search", url=host) )

    return itemlist

def search(item,texto):
    logger.info("[pelisalacarta.seriesblanco search texto="+texto)

    itemlist = []

    item.url = urlparse.urljoin(host,"/search.php?q1=%s" % (texto))
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|<Br>|<BR>|<br>|<br/>|<br />|-\s","",data)
    data = re.sub(r"<!--.*?-->","",data)

    #<div style='float:left;width: 620px;'><div style='float:left;width: 33%;text-align:center;'><a href='/serie/20/against-the-wall.html' '><img class='ict' src='http://4.bp.blogspot.com/-LBERI18Cq-g/UTendDO7iNI/AAAAAAAAPrk/QGqjmfdDreQ/s320/Against_the_Wall_Seriesdanko.jpg' alt='Capitulos de: Against The Wall' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='/serie/20/against-the-wall.html' style='font-size: 11px;'> Against The Wall</a></div><br><br>

    patron = "<div style='text-align:center;line-height:20px;height:20px;'><a href='([^']+)' style='font-size: 11px;'>([^<]+)</a>"

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
    data = re.sub(r"a></td><td> <img src=/banderas/","a><idioma/",data)
    data = re.sub(r" <img src=/banderas/","|",data)
    data = re.sub(r"\.png border='\d+' height='\d+' width='\d+' /><","/idioma><",data)
    data = re.sub(r"\.png border='\d+' height='\d+' width='\d+' />","",data)

    #<a href='/serie/534/temporada-1/capitulo-00/the-big-bang-theory.html'>1x00 - Capitulo 00 </a></td><td> <img src=/banderas/vo.png border='0' height='15' width='25' /> <img src=/banderas/vos.png border='0' height='15' width='25' /></td></tr>

    patron = "<a href='([^']+)'>([^<]+)</a><idioma/([^/]+)/idioma>"

    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedidioma in matches:
        idioma = ""
        for i in scrapedidioma.split("|"):
            idioma+= " [" + idiomas[i] + "]"
        title = item.title + " - " + scrapedtitle + idioma
        itemlist.append( Item(channel=__channel__, title =title , url=urlparse.urljoin(host,scrapedurl), action="findvideos", show=item.show) )

    if len(itemlist) == 0 and "<title>404 Not Found</title>" in data:
        itemlist.append( Item(channel=__channel__, title ="la url '"++"' parece no estar disponible en la web. Iténtalo más tarde." , url=item.url, action="series") )

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
    data = re.sub(r"<center>|</center>","",data)

    #<tr><td class='tam12'><img src='/banderas/es.png' width='30' height='20' /></td><td class='tam12'>2014-10-04</td><td class='tam12'><center><a href='/enlace/534/1/01/1445121/' rel='nofollow' target='_blank' alt=''><img src='/servidores/allmyvideos.jpg' width='80' height='25' /></a></center></td><td class='tam12'><center>Darkgames</center></td><td class='tam12'></td></tr>

    #<tr><td class='tam12'><img src='/banderas/es.png' width='30' height='20' /></td><td class='tam12'>2014-10-04</td><td class='tam12'><a href='/enlace/534/1/01/1444719/' rel='nofollow' target='_blank' alt=''><img src='/servidores/uploaded.jpg' width='80' height='25' /></a></td><td class='tam12'><center>Darkgames</center></td><td class='tam12'>SD</td></tr>

    patron = "<td class='tam12'><img src='/banderas/([^\.]+)\.[^']+'[^>]+></td>"
    patron+= "<td class='tam12'>([^<]+)</td>"
    patron+= "<td class='tam12'><a href='([^']+)'[^>]+>"
    patron+= "<img src='/servidores/([^\.]+)\.[^']+'[^>]+></a></td>"
    patron+= "<td class='tam12'>[^<]+</td>"
    patron+= "<td class='tam12'>([^<]+)</td>"
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedidioma, scrapedfecha, scrapedurl, scrapedservidor, scrapedcalidad in matches:
        title = "Ver en " + scrapedservidor + " [" + idiomas[scrapedidioma] + "] [" + scrapedcalidad + "] (" + scrapedfecha + ")"
        itemlist.append( Item(channel=__channel__, title =title , url=urlparse.urljoin(host,scrapedurl), action="play", show=item.show) )

    return itemlist

def play(item):
    logger.info("pelisalacarta.channels.seriesblanco play url="+item.url)

    data = scrapertools.cache_page(item.url)

    patron = "<input type='button' value='Ver o Descargar' onclick='window.open\(\"([^\"]+)\"\);'/>"
    url = scrapertools.find_single_match(data,patron)

    itemlist = servertools.find_video_items(data=url)

    for videoitem in itemlist:
        videoitem.title = item.title
        videoitem.channel = __channel__

    return itemlist    
