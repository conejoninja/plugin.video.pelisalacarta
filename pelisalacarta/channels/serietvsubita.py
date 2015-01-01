# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para serietvsubita
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "serietvsubita"
__category__ = "F,S,D"
__type__ = "generic"
__title__ = "serietvsubita"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.channels.serietvsubita mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="episodios" , title="Novità" , url="http://serietvsubita.net/", folder=True))
    itemlist.append( Item(channel=__channel__, action="series"    , title="Serie" , url="http://serietvsubita.net/", folder=True))
    itemlist.append( Item(channel=__channel__, action="search"    , title="Search...", folder=True))
    return itemlist

def search(item,texto):
    logger.info("pelisalacarta.channels.serietvsubita search")
    item.url="http://serietvsubita.net/?s="+texto+"&op.x=0&op.y=0"

    try:
        return novedades_episodios(item)
    # Se captura la excepci?n, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def series(item):
    logger.info("pelisalacarta.channels.serietvsubita series")
    itemlist = []

    data = scrapertools.cachePage(item.url)
    logger.info("data="+data)

    data = scrapertools.find_single_match(data,'<li id="widget_categories" class="widget png_scale"><h2 class="blocktitle"><span>Serie</span>(.*?)</ul>')
    logger.info("data="+data)

    patron  = '<li class="cat-item[^<]+<a href="([^"]+)[^>]+>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:

        thumbnail = ""
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        plot = ""

        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="episodios", title=title , fulltitle = title, url=url , thumbnail=thumbnail , plot=plot , folder=True, show=title))

    return itemlist

def episodios(item):
    logger.info("pelisalacarta.channels.serietvsubita episodios")
    itemlist = []

    data = scrapertools.cachePage(item.url)
    logger.info("data="+data)

    '''
    <div class="post-36266 post type-post status-publish format-standard hentry category-selfie tag-download tag-putlocker tag-selfie tag-streaming tag-sub-ita">
    <div class="post-meta">
    <a href="http://serietvsubita.net/2014/12/selfie-s01e12-sub-ita-1x12/" title="Selfie S01E12 Sub ITA (1&#215;12)" class="ms"></a>
    '''

    patron  = '<div class="post-[^<]+'
    patron += '<div class="post-meta"[^<]+'
    patron += '<a href="([^"]+)" title="([^"]+)"'

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:

        thumbnail = ""
        title = scrapertools.htmlclean(scrapedtitle).strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        plot = ""

        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=title , fulltitle = title, url=url , thumbnail=thumbnail , plot=plot , show=item.show, folder=True))

    return itemlist
