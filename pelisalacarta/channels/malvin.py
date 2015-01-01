# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para malvin
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "malvin"
__category__ = "F"
__type__ = "generic"
__title__ = "Malvin.tv"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.channels.malvin mainlist")
    itemlist=[]

    itemlist.append( Item(channel=__channel__ , action="peliculas"  , title="Novedades"          , url="http://www.malvin.tv/"))
    itemlist.append( Item(channel=__channel__ , action="categorias" , title="Listado por género" , url="http://www.malvin.tv/"))
    itemlist.append( Item(channel=__channel__ , action="letras"     , title="Listado alfabético" , url="http://www.malvin.tv/"))

    return itemlist

def peliculas(item):
    logger.info("pelisalacarta.channels.malvin peliculas")
    itemlist = []

    # Extrae las entradas (carpetas)
    data = scrapertools.cachePage(item.url)
    patron = 'class="filmgal">(.*?)<strong>Duraci[^<]+</strong>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    logger.info("hay %d matches" % len(matches))

    for match in matches:
        '''
        <a href="http://www.malvin.tv/ver-pelicula/dredd.html">
        <img width="145" height="199" border="0" src="http://img.pelidb.info/9591-145x199.jpg" alt="Ver pelicula Dredd"/>
        </a>
        </div>
        <div class="pelInfoToolTip" id="divtool-9591">
        <div class="divTituloTool">
        <span class="titulotool">
        <strong>Dredd</strong>
        </span>
        <strong>(2012)</strong>
        </div>
        <div>
        <strong>Género: </strong>Accion / Ciencia-Ficcion
        </div>
        <div class="sinopsis">
        <strong>Sinopsis:</strong> En un futuro cercano, Norteamérica se ha convertido en un páramo asolado por la radiactividad. Una única y gran megalópolis se extiende a lo largo de la costa este: Mega City 1. Esta inmensa y violenta urbe cuenta con una población de más de 400 millones de personas, cada una de las cuales es un [&hellip;]
        </div>
        <div>
        <strong>Duración: </strong> 95 min
        </div>
        </div>
        '''
        scrapedurl = scrapertools.find_single_match(match,'href="([^"]+)"')
        scrapedthumbnail = scrapertools.find_single_match(match,'src="([^"]+)"')
        scrapedtitle = scrapertools.find_single_match(match,'<span class="titulotool"[^<]+<strong>([^<]+)</strong>')
        scrapedplot = scrapertools.find_single_match(match,'<div class="sinopsis"[^<]+<strong[^<]+</strong>([^<]+)</div>')

        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=item.channel , action="findvideos"   , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, fanart=scrapedthumbnail, plot=scrapedplot , viewmode="movie_with_plot"))

    # Extrae la pagina siguiente
    #<a class="nextpostslink" href="http://www.malvin.tv/page/2">
    next_page = scrapertools.find_single_match(data,'<a class="nextpostslink" href="([^"]+)">')
    if next_page!="":
        itemlist.append( Item(channel=__channel__, action="peliculas" , title=">> Página siguiente" , url=next_page, folder=True))

    return itemlist

def categorias(item):
    logger.info("pelisalacarta.channels.malvin categorias")
                
    itemlist = []
    data = scrapertools.cachePage(item.url)
    data = scrapertools.find_single_match(data,'<div id="genero">(.*?)<div class="corte"></div>')

    # Extrae las entradas (carpetas)
    patron = '<a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl,scrapedtitle in matches:
        url = urlparse.urljoin(item.url,scrapedurl)
        title = scrapedtitle
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        
        itemlist.append( Item(channel=item.channel , action="peliculas"   , title=title , url=url , thumbnail=thumbnail, plot=plot ))
    
    return itemlist

def letras(item):
    logger.info("pelisalacarta.channels.malvin letras")

    itemlist = []
    data = scrapertools.cachePage(item.url)
    data = scrapertools.find_single_match(data,'<div id="abecedario">(.*?)<div class="corte"></div>')

    # Extrae las entradas (carpetas)
    patron = '<a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for scrapedurl,scrapedtitle in matches:
        url = urlparse.urljoin(item.url,scrapedurl)
        title = scrapedtitle
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        
        itemlist.append( Item(channel=item.channel , action="peliculas"   , title=title , url=url , thumbnail=thumbnail, plot=plot ))
    
    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    novedades_items = peliculas(mainlist_items[0])
    bien = False
    for novedades_item in novedades_items:
        mirrors = servertools.find_video_items( item=novedades_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien