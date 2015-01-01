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

__channel__ = "shurweb"
__category__ = "F,S,D,A"
__type__ = "generic"
__title__ = "Shurweb"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.channels.shurweb getmainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Series"                   , action="letras"       , url="http://www.tushurweb.com/series/", fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg"))
    itemlist.append( Item(channel=__channel__, title="Peliculas"                , action="menupeliculas", fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg"))
    itemlist.append( Item(channel=__channel__, title="Animacion"                , action="series"       , url="http://www.tushurweb.com/animacion/", fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg"))
    itemlist.append( Item(channel=__channel__, title="Documentales"             , action="peliculas"    , url="http://www.tushurweb.com/documentales/", fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg"))
    itemlist.append( Item(channel=__channel__, title="Buscar"                   , action="search") )
    return itemlist

def menupeliculas(item):
    logger.info("pelisalacarta.channels.shurweb menupeliculas")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Todas"     , action="peliculas", url="http://www.tushurweb.com/peliculas", fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg"))
    itemlist.append( Item(channel=__channel__, title="10's"      , action="peliculas", url="http://www.tushurweb.com/peliculas/10s/", fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg"))
    itemlist.append( Item(channel=__channel__, title="00's"      , action="peliculas", url="http://www.tushurweb.com/peliculas/00s/", fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg"))
    itemlist.append( Item(channel=__channel__, title="90's"      , action="peliculas", url="http://www.tushurweb.com/peliculas/90s/", fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg"))
    itemlist.append( Item(channel=__channel__, title="80's"      , action="peliculas", url="http://www.tushurweb.com/peliculas/80s/", fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg"))
    itemlist.append( Item(channel=__channel__, title="70's"      , action="peliculas", url="http://www.tushurweb.com/peliculas/70s/", fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg"))
    itemlist.append( Item(channel=__channel__, title="60's"      , action="peliculas", url="http://www.tushurweb.com/peliculas/60s/", fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg"))
    itemlist.append( Item(channel=__channel__, title="Animación" , action="peliculas", url="http://www.tushurweb.com/peliculas/animacion/", fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg") )
    itemlist.append( Item(channel=__channel__, title="Antiguas"  , action="peliculas", url="http://www.tushurweb.com/peliculas/antiguas/", fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg") )
    return itemlist

# Al llamarse "search" la función, el launcher pide un texto a buscar y lo añade como parámetro
def search(item,texto,categoria=""):
    logger.info("pelisalacarta.channels.shurweb "+item.url+" search "+texto)
    itemlist = []

    texto = texto.replace(" ","+")
    try:
        item.url = "http://www.tushurweb.com/?s="+texto
        itemlist.extend(buscador(item))
        return itemlist
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def buscador(item,paginacion=True):
    logger.info("pelisalacarta.channels.shurweb peliculas")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    
    patronvideos = '<a class="video_thumb" href="([^"]+)" rel="bookmark" title="([^"]+)"[^<]+<img width="\d+" height="\d+" src="([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        title = scrapertools.htmlclean(scrapedtitle)
        plot = ""
        url = scrapedurl
        thumbnail = scrapedthumbnail
        if DEBUG: logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        
        if url.startswith("http://www.tushurweb.com/pelicula/"):
            itemlist.append( Item(channel=__channel__, action='findvideos', title=title , fulltitle=title , url=url , thumbnail=thumbnail , plot=plot) )
        else:
            itemlist.append( Item(channel=__channel__, action='episodios', title=title , show=title , url=url , thumbnail=thumbnail , plot=plot) )

    return itemlist

def letras(item):
    logger.info("pelisalacarta.channels.shurweb letras")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.find_single_match(data,'<div id="alphaList" align="center"><ul(.*?)</ul>')
    
    patronvideos = '<li><a href="([^"]+)" rel="nofollow">([^<]+)</a></li>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        title = scrapedtitle
        plot = ""
        url = scrapedurl
        thumbnail = ""
        if DEBUG: logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        
        itemlist.append( Item(channel=__channel__, action='series', title=title , url=url , thumbnail=thumbnail , plot=plot) )

    return itemlist

def series(item):
    logger.info("pelisalacarta.channels.shurweb series")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    patronvideos = '<a class="video_thumb" href="([^"]+)" rel="bookmark" title="([^"]+)"[^<]+<img src="([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        title = scrapertools.htmlclean(scrapedtitle)
        plot = ""
        url = scrapedurl
        thumbnail = scrapedthumbnail
        if DEBUG: logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        
        itemlist.append( Item(channel=__channel__, action='episodios', title=title , show=title , url=url , thumbnail=thumbnail , plot=plot) )

    next_page_url = scrapertools.find_single_match(data,'<li><a class="next page-numbers" href="([^"]+)">')
    if next_page_url!="":
        itemlist.append( Item(channel=__channel__, action='series', title=">> Página siguiente" , url=next_page_url , thumbnail="" , plot=plot) )

    return itemlist

def episodios(item):
    logger.info("pelisalacarta.channels.shurweb episodios")
    itemlist=[]

    data = scrapertools.cachePage(item.url)
    item.plot = scrapertools.find_single_match(data,'<div class="col-sm-10">(.*?)<script')
    item.plot = scrapertools.htmlclean(item.plot)

    patron  = '<div class="video"[^<]+<a class="video_title" href="([^"]+)">(.*?)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        title = scrapertools.htmlclean(scrapedtitle).strip()
        url = scrapedurl
        plot = item.plot
        thumbnail = ""
        if DEBUG: logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action='findvideos', title=title , show=item.show , url=url , thumbnail=thumbnail , plot=plot , extra=scrapedtitle ,fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg", viewmode="movie_with_plot") )

    if config.get_platform().startswith("xbmc") or config.get_platform().startswith("boxee"):
        itemlist.append( Item(channel=item.channel, title="Añadir esta serie a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="episodios", show=item.show) )
        itemlist.append( Item(channel=item.channel, title="Descargar todos los episodios de la serie", url=item.url, action="download_all_episodes", extra="episodios", show=item.show))

    return itemlist

def peliculas(item):
    logger.info("pelisalacarta.channels.shurweb peliculas")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    
    patronvideos = '<a class="video_thumb" href="([^"]+)" rel="bookmark" title="([^"]+)"[^<]+<img width="\d+" height="\d+" src="([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        title = scrapertools.htmlclean(scrapedtitle)
        plot = ""
        url = scrapedurl
        thumbnail = scrapedthumbnail
        if DEBUG: logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")        
        itemlist.append( Item(channel=__channel__, action='findvideos', title=title , fulltitle=title , url=url , thumbnail=thumbnail , plot=plot) )

    next_page_url = scrapertools.find_single_match(data,'<a class="nextpostslink" href="([^"]+)">')
    if next_page_url!="":
        itemlist.append( Item(channel=__channel__, action='peliculas', title=">> Página siguiente" , url=next_page_url , thumbnail="" , plot=plot) )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools

    item = Item(channel=__channel__, title="Peliculas", action="peliculas", url="http://www.tushurweb.com/peliculas/")
    peliculas_items = peliculas(item)
    if len(peliculas_items)==0:
        return False

    item = Item(channel=__channel__, title="Series", action="series", url="http://www.tushurweb.com/series/b/")
    series_items = series(item)
    if len(series_items)==0:
        return False

    for pelicula_item in peliculas_items:
        mirrors = servertools.find_video_items(item=pelicula_item)
        if len(mirrors)>0:
            bien = True
            break

    return False
