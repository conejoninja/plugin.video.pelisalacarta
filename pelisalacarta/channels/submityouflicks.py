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

__channel__ = "submityouflicks"
__category__ = "F"
__type__ = "generic"
__title__ = "submityouflicks"
__language__ = "ES"
__adult__ = "true"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[submityourflicks.py] mainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="videos"    , title="Útimos videos" , url="http://www.submityourflicks.com/"))
    itemlist.append( Item(channel=__channel__, action="videos"    , title="Más vistos" , url="http://www.submityourflicks.com/most-viewed/1.html"))
    itemlist.append( Item(channel=__channel__, action="videos"    , title="Más votados" , url="http://www.submityourflicks.com/top-rated/1.html"))
    itemlist.append( Item(channel=__channel__, action="search"    , title="Buscar", url="http://www.submityourflicks.com/index.php?mode=search&q=%s&submit=Search"))
    
    return itemlist

# REALMENTE PASA LA DIRECCION DE BUSQUEDA

def search(item,texto):
    logger.info("[submityourflicks.py] search")
    tecleado = texto.replace( " ", "+" )
    item.url = item.url % tecleado
    return videos(item)

# SECCION ENCARGADA DE BUSCAR

def videos(item):
    logger.info("[submityourflicks.py] videos")
    # <div id="movies" style="width: 100%; ">
    data = scrapertools.downloadpageGzip(item.url)
    itemlist = [] 
    matches = re.compile(r"""<div class='content_item'>.*?</span>.*?<br style='clear: both;' />.*?</div>""",re.DOTALL).findall(data)
    for match in matches:
        datos = re.compile(r"""<div class='content_item'>.*?</div>""", re.S).findall(match)
        for vid in datos:
            aRef = re.compile(r"""<a href="([^"]+)"><img src="([^"]+)" alt="([^"]+)" title="([^"]+)" name="([^"]+)" border="1" id='([^"]+)' width="170" height="130" onmouseover="([^"]+)" onmouseout="([^"]+)" /></a>""", re.S).findall(vid)
            aTime= re.compile(r"""<span class='l5'>([^"]+)Min<br />.*?</span>""", re.S).findall(vid)
            if len(aTime) > 0:
                cTime= aTime[0].replace("\r\n","")
                cTime= cTime.replace(" ","")
            else:
                cTime=""
                
            aPosted = re.compile(r"""<span class='l5'>.*?Posted: ([^"]+)<br /></span>""", re.S).findall(vid)
            if len(aPosted) > 0:
                cPosted = aPosted[0].replace("\r\n","")
                cPosted = cPosted.replace(" ","")
            else:
                cPosted = ""
                
            video = aRef[0]
            try:
                scrapedtitle = unicode( video[2], "utf-8" ).encode("iso-8859-1")
                scrapedtitle = scrapedtitle+"("+cTime+")["+cPosted+"]"
            except:
                scrapedtitle = video[2]
            scrapedurl =  urlparse.urljoin( "http://www.submityourflicks.com/", video[0] )
            scrapedthumbnail = urlparse.urljoin( "http://www.submityourflicks.com/", video[1] )
            scrapedplot = ""
            # Depuracion
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")            
            itemlist.append( Item(channel=__channel__, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle, folder=False))

    #Paginador
    print "paginador"
    matches = re.compile('<a href="([^"]+)">Next</a>', re.DOTALL).findall(data)
    if len(matches)>0:
        scrapedurl =  urlparse.urljoin( "http://www.submityourflicks.com/", matches[0] )
        print scrapedurl
        paginador = Item(channel=__channel__, action="videos" , title="!Página siguiente" , url=scrapedurl, thumbnail="", plot="", extra = "" , show=item.show)
    else:
        paginador = None
    
    if paginador is not None:
        itemlist.append( paginador )

    return itemlist

# SECCION ENCARGADA DE VOLCAR EL LISTADO DE CATEGORIAS CON EL LINK CORRESPONDIENTE A CADA PAGINA
    
def listcategorias(item):
    logger.info("[xhamster.py] listcategorias")
    itemlist = []
    return itemlist
    

# OBTIENE LOS ENLACES SEGUN LOS PATRONES DEL VIDEO Y LOS UNE CON EL SERVIDOR
def play(item):
    logger.info("[xhamster.py] play")
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