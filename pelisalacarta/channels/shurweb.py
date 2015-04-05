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
    logger.info("[shurweb.py] getmainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Peliculas"    , action="menupeliculas"    , fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg"))
    itemlist.append( Item(channel=__channel__, title="Series"       , action="menuseries"       , url="http://www.tushurweb.com/shurseries/"              , fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg"))
    itemlist.append( Item(channel=__channel__, title="Documentales" , action="menudocumentales" , url="http://www.tushurweb.com/peliculas/documentales/"  , fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg"))
    itemlist.append( Item(channel=__channel__, title="Animación"    , action="menuanimacion"    , url="http://www.tushurweb.com/peliculas/animacion/"     , fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg"))    
    itemlist.append( Item(channel=__channel__, title="Buscar"       , action="search") )
    return itemlist

def menupeliculas(item):
    logger.info("[shurweb.py] menupeliculas")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Películas - A-Z"      , action="menuaz"               , url="http://www.tushurweb.com/peliculas/" , fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg"))
    itemlist.append( Item(channel=__channel__, title="Novedades"            , action="novedades_peliculas"  , url="http://www.tushurweb.com/"           , fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg"))
    itemlist.append( Item(channel=__channel__, title="Decadas"              , action="menupelisanos"        , url="http://www.tushurweb.com/peliculas/" , fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg"))
    return itemlist

def menuseries(item):
    logger.info("[shurweb.py] menuseries")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Series A-Z" , action="menuaz"           , url="http://www.tushurweb.com/series/"  , fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg") )
    itemlist.append( Item(channel=__channel__, title="Novedades"  , action="novedades_series" , url="http://www.tushurweb.com/"         , fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg"))
    return itemlist

def menudocumentales(item):
    logger.info("[shurweb.py] menudocumentales")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Documentales - A-Z" , action="menuaz"                 , url="http://www.tushurweb.com/documentales/"  , fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg") )
    itemlist.append( Item(channel=__channel__, title="Novedades"          , action="novedades_documentales" , url="http://www.tushurweb.com/"               , fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg"))
    itemlist.append( Item(channel=__channel__, title="Temas"              , action="menudocumentalestemas"  , url="http://www.tushurweb.com/documentales"   , fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg"))
    return itemlist

def menuanimacion(item):
    logger.info("[shurweb.py] menuanimacion")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Animacion - A-Z"    , action="menuaz"        , url="http://www.tushurweb.com/animacion/"     , fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg") )
    return itemlist

def menuaz(item):
    logger.info("[shurweb.py] menuaz")
    data = scrapertools.cachePage(item.url)
    data = scrapertools.unescape(data)
    data = scrapertools.get_match(data,'<ul class="pagination pagination-lg">(.*?)</div>')
    patron  = '<li><a href="(.*?)" rel="nofollow">(.*?)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for url, letra in matches:
      if ("peliculas" in item.url or "documentales" in item.url): 
        itemlist.append( Item(channel=__channel__, title=letra, action="peliculas", url=url, fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg"))
      else:
        itemlist.append( Item(channel=__channel__, title=letra, action="series"   , url=url, fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg"))      
    return itemlist

def menudocumentalestemas(item):
    logger.info("[shurweb.py] Documentales Temas")
    data = scrapertools.cachePage(item.url)
    data = scrapertools.unescape(data)
    data = scrapertools.get_match(data,'<span class=\'hidden-minibar\'>Documentales(.*?)<a href="http://www.tushurweb.com/animacion/"')
    patron  = '<a href=\'(.*?)\'>.{50}<i class=\'fa fa-picture-o\'></i>.{50}<span class=\'hidden-minibar\'>(.*?)</span>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for url, nombre in matches:
      if (nombre <> "Todos"):
        itemlist.append( Item(channel=__channel__, title=nombre, action="peliculas", url=url, fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg"))
    return itemlist

def menupelisanos(item):
    logger.info("[shurweb.py] Pelis decadas")
    data = scrapertools.cachePage(item.url)
    data = scrapertools.unescape(data)
    data = scrapertools.get_match(data,'<span class=\'hidden-minibar\'>Películas(.*?)<li class=\'submenu\'>')
    patron  = "<a href='(.*?)'[ ]*>.{50}<i class='fa fa-video-camera'></i>.{50}<span class='hidden-minibar'>(.*?)</span>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for url, nombre in matches:
      if (nombre <> "Todas" and nombre <> "Animación"  ):
        itemlist.append( Item(channel=__channel__, title=nombre , action="peliculas" , url=url, fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg"))
    return itemlist

def findvideos(item):
    logger.info("[shurweb.py] BuscarEnlaces")
    data = scrapertools.cachePage(item.url)
    data = scrapertools.unescape(data)
    from servers import longurl
    data=longurl.get_long_urls(data)   
    itemlist = []
    from servers import servertools
    itemlist.extend(servertools.find_video_items(data=data))
    for videoitem in itemlist:
            videoitem.channel=__channel__
            videoitem.action="play"
            videoitem.folder=False
            videoitem.thumbnail= item.thumbnail
            videoitem.title = "["+videoitem.server + "] - " + item.title
    return itemlist

def novedades_peliculas(item):
    logger.info("[shurweb.py] novedades_peliculas")
    data = scrapertools.cachePage(item.url)
    data = scrapertools.unescape(data)
    data = scrapertools.get_match(data,'<div class="tab-pane fade" id="pelis">(.*?)<div class="tab-pane fade" id="docus"')
    return peliculas(item,data=data)

def novedades_series(item):
    logger.info("[shurweb.py] novedades_series")
    data = scrapertools.cachePage(item.url)
    data = scrapertools.unescape(data)
    data = scrapertools.get_match(data,'<div class="tab-pane fade in active" id="series">(.*?)<div class="tab-pane fade" id="pelis">')
    patron = '<a class="video_thumb" href="([^"]+)" rel="bookmark" title="([^"]+)">.*?<img.*?src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    
    itemlist = []
    for url,title,thumbnail in matches:
        if DEBUG: logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action='findvideos', title=title, url=url, thumbnail=thumbnail, fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg") )
    return itemlist
    
def novedades_documentales(item):
    logger.info("[shurweb.py] novedades_documentales")
    data = scrapertools.cachePage(item.url)
    data = scrapertools.unescape(data)
    data = scrapertools.get_match(data,'<div class="tab-pane fade" id="docus">(.*?)<div class="panel panel-primary">')
    return peliculas(item,data=data)

# Al llamarse "search" la función, el launcher pide un texto a buscar y lo añade como parámetro
def search(item,texto,categoria=""):
    logger.info("[shurweb.py] "+item.url+" search "+texto)
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
    logger.info("[shurweb.py] peliculas")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.unescape(data)
    patronvideos = '<a class="video_thumb" href="([^"]+)" rel="bookmark" title="([^"]+)"[^<]+<img width="\d+" height="\d+" src="([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        
        if url.startswith("http://www.tushurweb.com/pelicula/"):
            itemlist.append( Item(channel=__channel__, action='findvideos', title=scrapedtitle, url=scrapedurl, thumbnail=scrapedthumbnail, fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg") )
        else:
            itemlist.append( Item(channel=__channel__, action='episodios' , title=scrapedtitle, url=scrapedurl, thumbnail=scrapedthumbnail, fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg") )

    return itemlist

def series(item,data=""):
    logger.info("[shurweb.py] series")
    itemlist = []

    # Descarga la página
    if data=="": data = scrapertools.cache_page(item.url)
    data = scrapertools.unescape(data)
    patronvideos = '<a class="video_thumb" href="([^"]+)" rel="bookmark" title="([^"]+)"[^<]+<img src="([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action='episodios', title=scrapedtitle, url=scrapedurl, thumbnail=scrapedthumbnail, fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg") )

    next_page_url = scrapertools.find_single_match(data,'<li><a class="next page-numbers" href="([^"]+)">')
    if next_page_url!="":
        itemlist.append( Item(channel=__channel__, action='series', title="Página siguiente >" , url=next_page_url, fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg") )

    return itemlist

def episodios(item):
    logger.info("[shurweb.py] episodios")
    data = scrapertools.cachePage(item.url)
    data = scrapertools.unescape(data)
    patron  = '<a class="video_title" href="([^"]+)"><button type="button" class="btn btn-danger"><i class="fa fa-eye"></i></button>     ([^"]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for url, title in matches:
        thumbnail = item.thumbnail
        if DEBUG: logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action='findvideos', title=title , url=url , thumbnail=thumbnail, fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg", viewmode="movie_with_plot") )

    if config.get_platform().startswith("xbmc") or config.get_platform().startswith("boxee"):
        itemlist.append( Item(channel=item.channel, title="Añadir esta serie a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="episodios", show=item.show,fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg") )
        itemlist.append( Item(channel=item.channel, title="Descargar todos los episodios de la serie", url=item.url, action="download_all_episodes", extra="episodios", show=item.show,fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg"))

    return itemlist

def peliculas(item,data=""):
    logger.info("[shurweb.py] peliculas")
    itemlist = []
    logger.info(item.url)

    # Descarga la página
    if data=="": data = scrapertools.cache_page(item.url)
    data = scrapertools.unescape(data)
    patronvideos = '<a class="video_thumb" href="([^"]+)" rel="bookmark" title="([^"]+)"[^<]+<img width="\d+" height="\d+" src="([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append(Item(channel=__channel__, action='findvideos', title=scrapedtitle, url=scrapedurl, thumbnail=scrapedthumbnail, fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg") )
    next_page_url = scrapertools.find_single_match(data,'<a class="nextpostslink" rel="next" href="([^"]+)">»</a>')
    if next_page_url!="":
        itemlist.append( Item(channel=__channel__, action='peliculas', title="Página siguiente >", url=next_page_url,fanart="http://pelisalacarta.mimediacenter.info/fanart/shurweb.jpg") )

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
