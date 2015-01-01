# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cine-adicto.com by Bandavi
# Actualización Carles Carmona 15/08/2011
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys

from core import scrapertools
from core import config
from core import logger
from core.item import Item
from pelisalacarta import buscador
from servers import servertools

__channel__ = "teledocumentales"
__category__ = "D"
__type__ = "generic"
__title__ = "Teledocumentales"
__language__ = "ES"
__creationdate__ = "20111019"


DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[teledocumentales.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="ultimo"        , title="Últimos Documentales"    , url="http://www.teledocumentales.com/"))
    itemlist.append( Item(channel=__channel__, action="ListaCat"      , title="Listado por Genero"      , url="http://www.teledocumentales.com/"))
    
    return itemlist

def ultimo(item):
    logger.info("[telecodocumentales.py] Ultimos")
    itemlist = []
                  
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas    
    patron = '<div class="imagen"(.*?)<div style="clear.both">'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for match in matches:
        scrapedtitle = scrapertools.get_match(match,'<img src="[^"]+" alt="([^"]+)"')
        scrapedtitle = scrapertools.htmlclean(scrapedtitle)
        scrapedurl = scrapertools.get_match(match,'<a href="([^"]+)"')
        scrapedthumbnail = scrapertools.get_match(match,'<img src="([^"]+)" alt="[^"]+"')
        scrapedplot = scrapertools.get_match(match,'<div class="excerpt">([^<]+)</div>')
        itemlist.append( Item(channel=item.channel , action="findvideos"  , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot , fanart=scrapedthumbnail, viewmode="movie_with_plot" ))

    # Extrae la marca de siguiente pagina
    try:
        next_page = scrapertools.get_match(data,'<a class="next" href="([^"]+)">')
        itemlist.append( Item(channel=item.channel , action="ultimo" , title=">> Página siguiente" , url=urlparse.urljoin(item.url,next_page)))
    except:
        pass

    return itemlist

def ListaCat(item):
    logger.info("[telecodocumentales.py] Ultimos")

    url = item.url
                  
    data = scrapertools.cachePage(url)

    # Extrae las entradas (carpetas)
    
    #<div class="slidethumb">
    #<a href="http://www.cine-adicto.com/transformers-dark-of-the-moon.html"><img src="http://www.cine-adicto.com/wp-content/uploads/2011/09/Transformers-Dark-of-the-moon-wallpaper.jpg" width="638" alt="Transformers: Dark of the Moon 2011" /></a>
    #</div>

    patron = '<div id="menu_horizontal">(.*?)<div class="cuerpo">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    logger.info("hay %d matches" % len(matches))
    

    itemlist = []
    for match in matches:
        data2 = match
        patron  = '<li class="cat-item cat-item-.*?<a href="(.*?)".*?>(.*?)</a>.*?</li>'
        matches2 = re.compile(patron,re.DOTALL).findall(data2)
        logger.info("hay %d matches2" % len(matches2))

        for match2 in matches2:
            scrapedtitle = match2[1].replace("&#8211;","-").replace("&amp;","&").strip()
            scrapedurl = match2[0]
            scrapedthumbnail = match2[0].replace(" ","%20")
            scrapedplot = ""
            
            itemlist.append( Item(channel=item.channel , action="ultimo"  , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot , fanart=scrapedthumbnail ))

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    # mainlist
    mainlist_items = mainlist(Item())
    
    # Da por bueno el canal si alguno de los vídeos de "Ultimos videos" devuelve mirrors
    ultimos_items = ultimo(mainlist_items[0])
    
    bien = False
    for ultimo_item in ultimos_items:
        play_items = detail(ultimo_item)
        if len(play_items)>0:
            return True
    
    return False