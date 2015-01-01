# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para Shurweb
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os,sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "gnula"
__category__ = "F"
__type__ = "generic"
__title__ = "Gnula"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[gnula.py] getmainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Portada"       , action="peliculas"    , url="http://gnula.biz/"))
    itemlist.append( Item(channel=__channel__, title="País"       , action="paises"    , url="http://gnula.biz/"))
    itemlist.append( Item(channel=__channel__, title="Años"      , action="anyos"     , url="http://gnula.biz/"))
    itemlist.append( Item(channel=__channel__, title="Generos"   , action="generos"   , url="http://gnula.biz/"))
    #itemlist.append( Item(channel=__channel__, title="Buscar"    , action="search"))
    return itemlist

def generos(item):
    logger.info("[gnula.py] generos")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<option value="">Filtrar película por género</option>(.*?)/select')
    patron = '<option value="([^"]+)">([^<]+)</option>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    for url,genero in matches:
        scrapedtitle =  scrapertools.htmlclean(genero)
        scrapedplot = ""
        scrapedurl = "http://gnula.biz/"+url
        scrapedthumbnail = ""
        if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action='peliculas', title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle) )
    
    return itemlist

def anyos(item):
    logger.info("[gnula.py] anyos")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<option value="">Filtrar película por año</option>(.*?)/select')
    patron = '<option value="([^"]+)">([^<]+)</option>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #if DEBUG: scrapertools.printMatches(matches)
    for url,letra in matches:
        scrapedtitle =  letra
        scrapedplot = ""
        scrapedurl = "http://gnula.biz/"+url
        scrapedthumbnail = ""
        if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action='peliculas', title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle) )
    
    return itemlist


def paises(item):
    logger.info("[gnula.py] paises")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<option value="">Filtrar película por país</option>(.*?)</select')
    patron = '<option value="([^"]+)">([^<]+)</option>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    for url,pais in matches:
        scrapedtitle =  pais
        scrapedplot = ""
        scrapedurl = "http://gnula.biz/"+url
        scrapedthumbnail = ""
        if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action='peliculas', title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle) )
    
    return itemlist

def peliculas(item,paginacion=True):
    logger.info("[gnula.py] peliculas")
    url = item.url

    '''
    <li class="item"><!--item_grid-->
    <div class="item-grid-imagen"><!--item_imagen-->
    <a href="mi-verano-con-amanda-3.html" class="sprite icono-play"></a>
    <a href="mi-verano-con-amanda-3.html"><figure><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ2AUXjOy4fAiTDACqnmrGDFcsrhfrzVH7jYdXs7SQ0INssg4Te-Q" alt="Mi verano con Amanda 3"></figure></a>
    </div>
    </li><!--fin_item_grid-->
    '''
    # Descarga la página
    data = scrapertools.cachePage(url)
    patron  = '<li class="item"><!--item_grid[^<]+'
    patron += '<div class="item-grid-imagen"><!--item_imagen[^<]+'
    patron += '<a href="[^"]+" class="sprite icono-play"></a[^<]+'
    patron += '<a href="([^"]+)"><figure><img src="([^"]+)" alt="([^"]+)">'

    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for url,thumbnail,title in matches:
        scrapedtitle=title
        fulltitle = scrapedtitle
        scrapedplot = ""
        scrapedurl = "http://gnula.biz/"+url
        scrapedthumbnail = thumbnail
        if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action='findvideos', title=scrapedtitle , fulltitle=fulltitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , viewmode="movie", extra=scrapedtitle) )

    patron = "<span \"\">[^<]+</span><a href='([^']+)'>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    for match in matches:
        itemlist.append( Item(channel=__channel__, action='peliculas', title=">> Página siguiente" , url=urlparse.urljoin(item.url,match)) )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    peliculas_items = peliculas(mainlist_items[0])
    bien = False
    for pelicula_item in peliculas_items:
        mirrors = servertools.find_video_items( item=pelicula_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien