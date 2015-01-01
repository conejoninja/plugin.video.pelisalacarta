# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cineblog01
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
import re, htmlentitydefs

from core import scrapertools
from core import logger
from core import config
from core.item import Item

__channel__ = "cineblog01"
__category__ = "F,S,A"
__type__ = "generic"
__title__ = "Cineblog01 (IT)"
__language__ = "IT"
sito="http://www.cb01.tv"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[cineblog01.py] mainlist")
    itemlist = []
	

    # Main options
    itemlist.append( Item(channel=__channel__, action="peliculas"  , title="Film - Novita'" , url=sito))
    #itemlist.append( Item(channel=__channel__, action="menuvk"     , title="Film - VK senza blochi" , url=sito))
    itemlist.append( Item(channel=__channel__, action="menugeneros", title="Film - Per genere" , url=sito))
    itemlist.append( Item(channel=__channel__, action="menuanyos"  , title="Film - Per anno" , url=sito))
    itemlist.append( Item(channel=__channel__, action="search"     , title="Film - Cerca" ))
    itemlist.append( Item(channel=__channel__, action="listserie"  , title="Serie Tv" , url=sito+"/serietv/" ))
    itemlist.append( Item(channel=__channel__, action="search", title="Serie Tv - Cerca" , extra="serie"))
    itemlist.append( Item(channel=__channel__, action="listserie"  , title="Anime" , url=sito+"/anime/" ))

    return itemlist

def menuvk(item):
    logger.info("[cineblog01.py] menuvk")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    
    # Narrow search by selecting only the combo
    bloque = scrapertools.get_match(data,'<select name="select1"(.*?)</select')
    
    # The categories are the options for the combo  
    patron = '<option value="([^"]+)">([^<]+)</option>'
    matches = re.compile(patron,re.DOTALL).findall(bloque)
    scrapertools.printMatches(matches)

    for url,titulo in matches:
        scrapedtitle = titulo
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="peliculas" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

def menugeneros(item):
    logger.info("[cineblog01.py] menuvk")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    logger.info(data)

    # Narrow search by selecting only the combo
    bloque = scrapertools.get_match(data,'<select name="select2"(.*?)</select')
    
    # The categories are the options for the combo  
    patron = '<option value="([^"]+)">([^<]+)</option>'
    matches = re.compile(patron,re.DOTALL).findall(bloque)
    scrapertools.printMatches(matches)

    for url,titulo in matches:
        scrapedtitle = titulo
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="peliculas" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

def menuanyos(item):
    logger.info("[cineblog01.py] menuvk")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    logger.info(data)
    
    # Narrow search by selecting only the combo
    bloque = scrapertools.get_match(data,'<select name="select3"(.*?)</select')
    
    # The categories are the options for the combo  
    patron = '<option value="([^"]+)">([^<]+)</option>'
    matches = re.compile(patron,re.DOTALL).findall(bloque)
    scrapertools.printMatches(matches)

    for url,titulo in matches:
        scrapedtitle = titulo
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="peliculas" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

# Al llamarse "search" la función, el launcher pide un texto a buscar y lo añade como parámetro
def search(item,texto):
    logger.info("[cineblog01.py] "+item.url+" search "+texto)

    try:

        if item.extra=="serie":
            item.url = "http://www.cb01.tv/serietv/?s="+texto
            return listserie(item)
        else:
            item.url = "http://www.cb01.tv/?s="+texto
            return peliculas(item)

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def listcat(item):
    logger.info("[cineblog01.py] mainlist")
    itemlist = []
    if item.url =="":
        item.url = sito
        
    # Descarga la página
    data = scrapertools.cache_page(item.url)
    logger.info(data)

    # Extrae las entradas (carpetas)
    patronvideos  = '<div id="covershot".*?<a.*?<img src="(.*?)".*?'
    patronvideos += '<div id="post-title"><a href="(.*?)".*?'
    patronvideos += '<h3>(.*?)</h3>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        # Titulo
        scrapedtitle = scrapertools.unescape(match[2])
        scrapedurl = urlparse.urljoin(item.url,match[1])
        scrapedthumbnail = urlparse.urljoin(item.url,match[0])
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    # Remove the next page mark
    patronvideos = '<a href="(http://www.cb01.tv/category/[0-9a-zA-Z]+/page/[0-9]+/)">Avanti >'
    patronvideos += '/page/[0-9]+/)">Avanti >'
    matches = re.compile (patronvideos, re.DOTALL).findall (data)
    scrapertools.printMatches (matches)

    if len(matches)>0:
        scrapedtitle = "(Next Page ->)"
        scrapedurl = matches[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="listcat" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

def peliculas(item):
    logger.info("[cineblog01.py] mainlist")
    itemlist = []

    if item.url =="":
        item.url = sito

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    logger.info(data)

    # Extrae las entradas (carpetas)
    patronvideos  = '<div id="covershot".*?<a.*?<img src="(.*?)".*?'
    patronvideos += '<div id="post-title"><a href="(.*?)".*?'
    patronvideos += '<h3>(.*?)</h3>(.*?)</p>'
    #patronvideos += '<div id="description"><p>(.?*)</div>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = scrapertools.unescape(match[2])
        scrapedurl = urlparse.urljoin(item.url,match[1])
        scrapedthumbnail = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = scrapedthumbnail.replace(" ", "%20");
        scrapedplot = scrapertools.unescape(match[3])
        scrapedplot = scrapertools.htmlclean(scrapedplot).strip()
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, viewmode="movie_with_plot", fanart=scrapedthumbnail))

    # Next page mark
    try:
        bloque = scrapertools.get_match(data,"<div id='wp_page_numbers'>(.*?)</div>")
        # <a href="http://cineblog01.com/page/2/">Avanti
        # <a href="http://www.cineblog01.com/category/streaming/vk/animazione-vk/page/2/">Avanti > </a></li>
        patronvideos = '<a href="([^"]+)">Avanti'
        matches = re.compile (patronvideos, re.DOTALL).findall (data)
        scrapertools.printMatches (matches)
    
        if len(matches)>0:
            scrapedtitle = ">> Avanti"
            scrapedurl = matches[0]
            scrapedthumbnail = ""
            scrapedplot = ""
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
    
            itemlist.append( Item(channel=__channel__, action="peliculas" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))
    except:
        pass

    return itemlist

def listserie(item):
    logger.info("[cineblog01.py] mainlist")
    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    logger.info(data)

    # Extrae las entradas (carpetas)
    patronvideos  = '<div id="covershot"><a[^<]+<p[^<]+<img.*?src="([^"]+)".*?'
    patronvideos += '<div id="post-title"><a href="([^"]+)"><h3>([^<]+)</h3></a></div>[^<]+'
    patronvideos += '<div id="description"><p>(.*?)</p>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = scrapertools.unescape(match[2])
        scrapedurl = urlparse.urljoin(item.url,match[1])
        scrapedthumbnail = urlparse.urljoin(item.url,match[0])
        scrapedplot = scrapertools.unescape(match[3])
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action="findvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    # Put the next page mark
    try:
        next_page = scrapertools.get_match(data,"<link rel='next' href='([^']+)'")
        itemlist.append( Item(channel=__channel__, action="listserie" , title=">> Next page" , url=next_page, thumbnail=scrapedthumbnail, plot=scrapedplot))
    except:
        pass

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True
    
    # mainlist
    mainlist_items = mainlist(Item())
    
    # Comprueba que todas las opciones por categorias tengan algo (excepto los buscadores)
    for mainlist_item in mainlist_items:
        if mainlist_item.action.startswith("menu"):
            exec "itemlist = "+mainlist_item.action+"(mainlist_item)"
            
            # Lee la primera categoría sólo
            exec "itemlist2 ="+itemlist[0].action+"(itemlist[0])"
            if len(itemlist2)==0:
                return false

    # Comprueba si alguno de los vídeos de "Novedades" devuelve mirrors
    for mainlist_item in mainlist_items:
        if mainlist_item.action=="peliculas" or mainlist_item.action=="listserie":
            exec "itemlist = "+mainlist_item.action+"(mainlist_item)"
    
            bien = False
            for episodio_item in itemlist:
                from servers import servertools
                mirrors = servertools.find_video_items(item=episodio_item)
                if len(mirrors)>0:
                    bien = True
                    break

    return bien
