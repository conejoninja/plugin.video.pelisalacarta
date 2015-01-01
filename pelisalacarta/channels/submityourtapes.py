# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import cookielib
import urlparse,urllib2,urllib,re
import os
import sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools
import urllib

__channel__ = "submityourtapes"
__category__ = "F"
__type__ = "generic"
__title__ = "submityourtapes"
__language__ = "ES"
__adult__ = "true"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[submityourtapes.py] mainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="videos"    , title="Útimos videos" , url="http://www.submityourtapes.com/"))
    itemlist.append( Item(channel=__channel__, action="videos"    , title="Más vistos" , url="http://www.submityourtapes.com/most-viewed/1.html"))
    itemlist.append( Item(channel=__channel__, action="videos"    , title="Más votados" , url="http://www.submityourtapes.com/top-rated/1.html"))
    itemlist.append( Item(channel=__channel__, action="search"    , title="Buscar", url="http://www.submityourtapes.com/index.php?mode=search&q=%s&submit=Search"))
    
    return itemlist

# REALMENTE PASA LA DIRECCION DE BUSQUEDA

def search(item,texto):
    logger.info("[submityourtapes.py] search")
    tecleado = texto.replace( " ", "+" )
    item.url = item.url % tecleado
    return videos(item)

# SECCION ENCARGADA DE BUSCAR

def videos(item):
    logger.info("[submityourtapes.py] videos")

    itemlist = [] 
    '''
    <div class='content_item'>
    <a href="/videos/264559/hard-doggy-creampie.html"><img src="http://static2.cdn.submityourtapes.com/thumbs/240x180/b/7/5/126302/264559/0.jpg" alt="Blonde Wife Gets Facial" title="HARD Doggy Creampie" name="im264559" border="1" id='im264559' width="240" height="180" onmouseover="if (typeof(startm)=='function') {startm(this);}" onmouseout="if (typeof(endm)=='function') {endm(this,4);}" /></a><br />
    '''
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    patron  = "<div class='content_item'[^<]+"
    patron += '<a href="([^"]+)"><img src="([^"]+)" alt="[^"]+" title="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        title = scrapedtitle
        url =  urlparse.urljoin( item.url , scrapedurl )
        thumbnail = urlparse.urljoin( item.url , scrapedthumbnail )
        plot = ""
        # Depuracion
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")            
        itemlist.append( Item(channel=__channel__, action="play" , title=title , url=url, thumbnail=thumbnail, plot=plot, folder=False))

    # Paginador
    try:
        next_url = scrapertools.get_match(data,'<span class=\'current\'>\d+</span> <a href="([^"]+)">')
        next_url = urlparse.urljoin(item.url,next_url)
        itemlist.append( Item(channel=__channel__, action="videos" , title=">> Página siguiente" , url=next_url) )
    except:
        pass

    return itemlist

# SECCION ENCARGADA DE VOLCAR EL LISTADO DE CATEGORIAS CON EL LINK CORRESPONDIENTE A CADA PAGINA
    
def listcategorias(item):
    logger.info("[submityourtapes.py] listcategorias")
    itemlist = []
    return itemlist
    

# OBTIENE LOS ENLACES SEGUN LOS PATRONES DEL VIDEO Y LOS UNE CON EL SERVIDOR
def play(item):
    logger.info("[submityourtapes.py] play")
    # <div id="movies" style="width: 100%; ">
    data = scrapertools.downloadpage(item.url)
    
    itemlist = []
    matches = re.compile('so.addVariable\("file", "([^"]+)"\);', re.DOTALL).findall(data)
    if len(matches)>0:
        parsed_url = urllib.unquote_plus(matches[0])
        print parsed_url
        paginador = Item(channel=__channel__, action="play" , title=item.title, fulltitle=item.fulltitle , url=parsed_url, thumbnail=item.thumbnail, plot=item.plot, show=item.title, server="directo", folder=False)
    else:
        paginador = None
    
    if paginador is not None:
        itemlist.append( paginador )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    # mainlist
    mainlist_items = mainlist(Item())
    
    # Da por bueno el canal si alguno de los vídeos de "Ultimos videos" devuelve mirrors
    videos_items = videos(mainlist_items[0])
    
    bien = False
    for video_item in videos_items:
        play_items = play(video_item)
        if len(play_items)>0:
            return True
    
    return False