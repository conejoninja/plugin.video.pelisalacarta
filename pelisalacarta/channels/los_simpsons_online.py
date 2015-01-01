# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para lossimpsonsonline.com.ar por Ignite
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "los_simpsons_online"
__category__ = "S"
__type__ = "generic"
__title__ = "Los Simpsons Online"
__language__ = "ES"

DEBUG = config.get_setting("debug")
    
def isGeneric():
    return True

def mainlist(item):
    logger.info("[simpsonsonline.py] mainlist")
    
    url = "http://www.lossimpsonsonline.com.ar/"
    data = scrapertools.cachePage(url)
    patron  = '<li><a href="([^"]+)" title="([^"]+)">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []

    for match in matches:
         scrapedtitle = match[1]
         scrapedurl = match[0]
         scrapedthumbnail = ""
         scrapedplot = ""
         itemlist.append( Item(channel=__channel__, action="episodios", title=scrapedtitle, url=scrapedurl))

    return itemlist
    
def episodios(item):
    logger.info("[simpsonsonline.py] episodios")

    url = item.url
    url = "http://www.lossimpsonsonline.com.ar"+url
    data = scrapertools.cachePage(url)
    patron = '<div class="item"><a href="([^"]+)" class="thumbnail"><img src="([^"]+)" alt="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    for match in matches:
         scrapedtitle = match[2]
         scrapedurl = "http://www.lossimpsonsonline.com.ar"+match[0]
         scrapedthumbnail = "http://www.lossimpsonsonline.com.ar"+match[1]
         scrapedplot = ""
         itemlist.append( Item(channel=__channel__, action="findvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools

    # Lee todas las temporadas buscando un episodio visible
    temporadas_items = mainlist(Item())
    
    # Empezando por las últimas que es más fácil
    temporadas_items.reverse()
    
    for temporada_item in temporadas_items:
    
        # Da por bueno el canal si alguno de los vídeos devuelve mirrors
        episodios_items = episodios(temporada_item)
        bien = False
        for episodio_item in episodios_items:
            mirrors = servertools.find_video_items( item=episodio_item )
            if len(mirrors)>0:
                return True

    return False