# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para trailers de ecartelera
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

DEBUG = config.get_setting("debug")

__channel__ = "ecarteleratrailers"
__category__ = "F"
__type__ = "generic"
__title__ = "Trailers ecartelera"
__language__ = "ES,EN"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[ecarteleratrailers.py] mainlist")
    itemlist=[]

    if item.url=="":
        item.url="http://www.ecartelera.com/videos/"
    
    # ------------------------------------------------------
    # Descarga la página
    # ------------------------------------------------------
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # ------------------------------------------------------
    # Extrae las películas
    # ------------------------------------------------------
    patron  = '<div class="cuadronoticia">.*?<img src="([^"]+)".*?'
    patron += '<div class="cnottxtv">.*?<h3><a href="([^"]+)">([^<]+)</a></h3>.*?'
    patron += '<img class="bandera" src="http\:\/\/www\.ecartelera\.com\/images\/([^"]+)"[^<]+'
    patron += '<br/>([^<]+)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[2] #unicode( , "iso-8859-1" , errors="replace" ).encode("utf-8")

        if match[3]=="fl_1.gif":
            scrapedtitle += " (Castellano)"
        elif match[3]=="fl_2.gif":
            scrapedtitle += " (Inglés)"
        
        scrapedurl = match[1]
        scrapedthumbnail = match[0]
        scrapedplot = match[4]

        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, server="directo", viewmode="movie_with_plot", folder=False))

    # ------------------------------------------------------
    # Extrae la página siguiente
    # ------------------------------------------------------
    patron = '<a href="([^"]+)">Siguiente</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG:
        scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = "Pagina siguiente"
        scrapedurl = match
        scrapedthumbnail = ""
        scrapeddescription = ""

        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action="mainlist" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, server="directo", folder=True))

    return itemlist

# Reproducir un vídeo
def play(item):
    logger.info("[ecarteleratrailers.py] play")
    itemlist=[]
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    logger.info(data)

    # Extrae las películas
    patron  = "file\: '([^']+)'"
    matches = re.compile(patron,re.DOTALL).findall(data)

    if len(matches)>0:
        url = urlparse.urljoin(item.url,matches[0])
        logger.info("[ecarteleratrailers.py] url="+url)
        itemlist.append( Item(channel=__channel__, action="play" , title=item.title , url=url, thumbnail=item.thumbnail, plot=item.plot, server="directo", folder=False))

    return itemlist


# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    
    # mainlist
    mainlist_items = mainlist(Item())
    if len(mainlist_items)==0:
        print "ecartelera: Lista de canales vacía"
        return False
    
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    video_items = play(mainlist_items[0])
    if len(mainlist_items)==0:
        print "ecartelera: No devuelve videos"
        return False

    return True