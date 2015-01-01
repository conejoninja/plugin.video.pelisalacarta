# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para pelis24
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "pelis24"
__category__ = "F,S"
__type__ = "xbmc"
__title__ = "Pelis24"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("channels.pelis24 mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Novedades"              , action="peliculas" , url="http://pelis24.com/index.php"))
    itemlist.append( Item(channel=__channel__, title="Listado por categorías" , action="categorias", url="http://pelis24.com/index.php", extra="CATEGORIAS"))
    itemlist.append( Item(channel=__channel__, title="Listado por calidades"  , action="categorias", url="http://pelis24.com/index.php", extra="CALIDADES"))
    itemlist.append( Item(channel=__channel__, title="Listado por idiomas"    , action="categorias", url="http://pelis24.com/index.php", extra="IDIOMAS"))
    return itemlist

def peliculas(item):
    logger.info("channels.pelis24 peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cachePage(item.url)

    # Limita el bloque donde buscar
    data = scrapertools.find_single_match(data,"<div id='dle-content'>(.*?<div class=\"navigation\">.*?)</div[^<]+</div[^<]+</div>")

    # Extrae los items    
    patron  = '<div class="movie_box">(.*?)<div class="postbottom">'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for bloque in matches:
        scrapedtitle = scrapertools.find_single_match(bloque,"<h3>([^<]+)</h3>")
        scrapedurl = scrapertools.find_single_match(bloque,'<a href="([^"]+)"><img class="homethumb"')
        scrapedthumbnail = scrapertools.find_single_match(bloque,'<img class="homethumb" style="[^"]+" data-cfsrc="([^"]+)"')
        scrapedplot = scrapertools.find_single_match(bloque,'<span class="pop_desc">(.*?)</span>')

        title = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")
        url = scrapedurl
        thumbnail = scrapedthumbnail.strip()
        plot = unicode( scrapedplot, "iso-8859-1" , errors="replace" ).encode("utf-8").strip()

        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=title , url=url , thumbnail=thumbnail , plot=plot , viewmode="movie_with_plot", folder=True) )

    # Extrae el paginador
    next_page = scrapertools.find_single_match(data,"<a href=\"([^\"]+)\"><spam class='last'>")
    if next_page!="":
        itemlist.append( Item(channel=__channel__, action="peliculas", title=">> Pagina siguiente" , url=next_page , folder=True) )

    return itemlist

def categorias(item):
    logger.info("channels.pelis24 categorias")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    logger.info("data="+data)

    # Limita el bloque donde buscar
    data = scrapertools.find_single_match(data,'<b>'+item.extra+'</b>(.*?)</ul>')
    logger.info("data="+data)

    # Extrae las entradas
    patron = '<a href="([^"]+)"><b>([^<]+)</b></a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if (DEBUG): scrapertools.printMatches(matches)
                                          
    for scrapedurl,scrapedtitle in matches:
        url = urlparse.urljoin(item.url,scrapedurl)
        if url=="http://pelis24.com/movies/bluray/":
            url = "http://pelis24.com/pelicula-3d/"

        if url=="http://pelis24.com/movies/dvdrip/":
            url = "http://pelis24.com/peliculas480p/"

        title = scrapedtitle.strip()
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="peliculas", title=title , url=url , thumbnail=thumbnail , plot=plot , folder=True) )

    return itemlist

# Verificacion automatica de canales: Esta funcion debe devolver "True" si esta ok el canal.
def test():
    from servers import servertools
    
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los videos de "Novedades" devuelve mirrors
    novedades_items = peliculas(mainlist_items[0])
    bien = False
    for novedades_item in novedades_items:
        mirrors = servertools.find_video_items( item=novedades_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien
