# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para tubehentai
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys

from core import scrapertools
from core import config
from core import logger
from core.item import Item
from servers import servertools

__channel__ = "tubehentai"
__category__ = "A"
__type__ = "generic"
__title__ = "tubehentai"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[tubehentai.py] mainlist")
    return novedades(Item(channel=__channel__, title="Novedades" , action="novedades" , url="http://tubehentai.com/" ))

def novedades(item):
    logger.info("[tubehentai.py] getnovedades")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #<a href="http://tubehentai.com/videos/slave_market_¨c_ep1-595.html"><img class="img" width="145" src="http://tubehentai.com/media/thumbs/5/9/5/./f/595/595.flv-3.jpg" alt="Slave_Market_&Acirc;&uml;C_Ep1" id="4f4fbf26f36
    patron = '<a href="(http://tubehentai.com/videos/[^"]+)"><img.*?src="(http://tubehentai.com/media/thumbs/[^"]+)" alt="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        # Titulo
        scrapedtitle = match[2]
        scrapedurl = match[0]
        scrapedthumbnail = match[1].replace(" ", "%20")
        scrapedplot = scrapertools.htmlclean(match[2].strip())
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action="play", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=False) )

    # ------------------------------------------------------
    # Extrae el paginador
    # ------------------------------------------------------
    #<a href="page2.html" class="next">Next »</a>
    patronvideos  = '<a href=\'(page[^\.]+\.html)\'[^>]*?>Next[^<]*?<\/a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,"/" + matches[0])
        logger.info("[tubehentai.py] " + scrapedurl)
        itemlist.append( Item(channel=__channel__, action="novedades", title=">> Página siguiente" , url=scrapedurl) )

    return itemlist

def play(item):
    logger.info("[tubehentai.py] detail")
    itemlist=[]
    
    #s1.addParam("flashvars","overlay=http://tubehentai.com/media/thumbs/5/2/3/9/c/5239cf74632cbTHLaBlueGirlep3%20%20Segment2000855.000001355.000.mp4
    #http://tubehentai.com/media/thumbs/5/2/3/9/c/5239cf74632cbTHLaBlueGirlep3%20%20Segment2000855.000001355.000.mp4
    #http://tubehentai.com/media/videos/5/2/3/9/c/5239cf74632cbTHLaBlueGirlep3%20%20Segment2000855.000001355.000.mp4?start=0
    data = scrapertools.cachePage(item.url)
    url = scrapertools.get_match(data,'s1.addParam\("flashvars","overlay=(.*?\.mp4)')
    url = url.replace("/thumbs","/videos")
    #url = url+"?start=0"
    logger.info("url="+url)
    server="Directo"
    itemlist.append( Item(channel=__channel__, title="" , url=url , server=server, folder=False) )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True

    # mainlist
    videos_items = mainlist(Item())
    
    for video_item in videos_items:
        mirrors = play(video_item)
        if len(mirrors)>0:
            return True

    print "No hay ningún vídeo en la sección de novedades"
    return False