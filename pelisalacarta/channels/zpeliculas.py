# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para seriespepito
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "zpeliculas"
__category__ = "F"
__type__ = "generic"
__title__ = "ZPeliculas"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[zpeliculas.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="destacadas"        , title="Destacadas", url="http://www.zpeliculas.com", thumbnail="http://www.zpeliculas.com/templates/mytopV2/images/footer-logo.png", fanart="http://www.zpeliculas.com/templates/mytopV2/images/background.png"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="Últimas peliculas", url="http://www.zpeliculas.com/", thumbnail="http://www.zpeliculas.com/templates/mytopV2/images/footer-logo.png", fanart="http://www.zpeliculas.com/templates/mytopV2/images/background.png"))
    itemlist.append( Item(channel=__channel__, action="sugeridas"        , title="Películas sugeridas", url="http://www.zpeliculas.com", thumbnail="http://www.zpeliculas.com/templates/mytopV2/images/footer-logo.png", fanart="http://www.zpeliculas.com/templates/mytopV2/images/background.png"))
    itemlist.append( Item(channel=__channel__, action="generos"        , title="Por género", url="http://www.zpeliculas.com", thumbnail="http://www.zpeliculas.com/templates/mytopV2/images/footer-logo.png", fanart="http://www.zpeliculas.com/templates/mytopV2/images/background.png"))
    itemlist.append( Item(channel=__channel__, action="alfabetico"   , title="Listado alfabético", thumbnail="http://www.zpeliculas.com/templates/mytopV2/images/footer-logo.png", fanart="http://www.zpeliculas.com/templates/mytopV2/images/background.png"))
    itemlist.append( Item(channel=__channel__, action="search"        , title="Buscador", url="http://www.zpeliculas.com", thumbnail="http://www.zpeliculas.com/templates/mytopV2/images/footer-logo.png", fanart="http://www.zpeliculas.com/templates/mytopV2/images/background.png"))
    
    return itemlist

def alfabetico(item):
    logger.info("[zpeliculas.py] alfabetico")
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="A", url="http://www.zpeliculas.com/cat/a"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="B", url="http://www.zpeliculas.com/cat/b"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="C", url="http://www.zpeliculas.com/cat/c"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="D", url="http://www.zpeliculas.com/cat/d"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="E", url="http://www.zpeliculas.com/cat/e"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="F", url="http://www.zpeliculas.com/cat/f"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="G", url="http://www.zpeliculas.com/cat/g"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="H", url="http://www.zpeliculas.com/cat/h"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="I", url="http://www.zpeliculas.com/cat/i"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="J", url="http://www.zpeliculas.com/cat/j"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="K", url="http://www.zpeliculas.com/cat/k"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="L", url="http://www.zpeliculas.com/cat/l"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="M", url="http://www.zpeliculas.com/cat/m"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="N", url="http://www.zpeliculas.com/cat/n"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="O", url="http://www.zpeliculas.com/cat/o"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="P", url="http://www.zpeliculas.com/cat/p"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="Q", url="http://www.zpeliculas.com/cat/q"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="R", url="http://www.zpeliculas.com/cat/r"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="S", url="http://www.zpeliculas.com/cat/s"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="T", url="http://www.zpeliculas.com/cat/t"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="U", url="http://www.zpeliculas.com/cat/u"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="V", url="http://www.zpeliculas.com/cat/v"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="W", url="http://www.zpeliculas.com/cat/w"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="X", url="http://www.zpeliculas.com/cat/x"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="Y", url="http://www.zpeliculas.com/cat/y"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="Z", url="http://www.zpeliculas.com/cat/z"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="0", url="http://www.zpeliculas.com/cat/0"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="1", url="http://www.zpeliculas.com/cat/1"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="2", url="http://www.zpeliculas.com/cat/2"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="3", url="http://www.zpeliculas.com/cat/3"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="4", url="http://www.zpeliculas.com/cat/4"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="5", url="http://www.zpeliculas.com/cat/5"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="6", url="http://www.zpeliculas.com/cat/6"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="7", url="http://www.zpeliculas.com/cat/7"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="8", url="http://www.zpeliculas.com/cat/8"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="9", url="http://www.zpeliculas.com/cat/9"))

    return itemlist
    
	
def generos(item):
    logger.info("[zpeliculas.py] generos")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="Acción", url="http://www.zpeliculas.com/peliculas/p-accion/"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="Animación", url="http://www.zpeliculas.com/peliculas/p-animacion/"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="Aventura", url="http://www.zpeliculas.com/peliculas/p-aventura/"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="Biografía", url="http://www.zpeliculas.com/peliculas/p-biografia/"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="Bélico", url="http://www.zpeliculas.com/peliculas/p-belico/"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="Ciencia Ficción", url="http://www.zpeliculas.com/peliculas/p-cienciaficcion/"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="Comedia", url="http://www.zpeliculas.com/peliculas/p-comedia/"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="Crimen", url="http://www.zpeliculas.com/peliculas/p-crimen/"))  
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="Drama", url="http://www.zpeliculas.com/peliculas/p-drama/"))	
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="Fantasía", url="http://www.zpeliculas.com/peliculas/p-fantasia/"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="Histórico", url="http://www.zpeliculas.com/peliculas/p-historico/"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="Intriga", url="http://www.zpeliculas.com/peliculas/p-intriga/"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="Musical", url="http://www.zpeliculas.com/peliculas/p-musical/"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="Romántica", url="http://www.zpeliculas.com/peliculas/p-romantica/"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="Terror", url="http://www.zpeliculas.com/peliculas/p-terror/"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="Thriller", url="http://www.zpeliculas.com/peliculas/p-thriller/"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="Western", url="http://www.zpeliculas.com/peliculas/p-western/"))
    itemlist.append( Item(channel=__channel__, action="porgeneros"        , title="Otros", url="http://www.zpeliculas.com/peliculas/p-otros/"))
    return itemlist


def search(item,texto):

    post = urllib.urlencode({"story": texto, "do": "search", "subaction": "search", "x": "0", "y": "0"})
    data = scrapertools.cache_page("http://www.zpeliculas.com",post=post)

    patron  = '<div class="leftpane">(.*?)<div class="clear"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []

    for match in matches:
        scrapedtitle = scrapertools.find_single_match(match,'<div class="shortname">([^<]+)</div>')
        scrapedurl = scrapertools.find_single_match(match,'<a href="([^"]+)"')
        scrapedthumbnail = scrapertools.find_single_match(match,'<img src="([^"]+)"')
        scrapedyear = scrapertools.find_single_match(match,'<div class="year"[^>]+>([^<]+)</div>')
        scrapedidioma = scrapertools.find_single_match(match,'title="Idioma">([^<]+)</div>')
        scrapedcalidad = scrapertools.find_single_match(match,'<div class="shortname"[^<]+</div[^<]+<div[^>]+>([^<]+)</div>')

        title = scrapedtitle + ' ('+scrapedyear+') ['+scrapedidioma+'] ['+scrapedcalidad+']'
        url = scrapedurl
        thumbnail = scrapedthumbnail
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , url=url, thumbnail=thumbnail, plot=plot, show=title, viewmode="movie", fanart=thumbnail))

    return itemlist

def porgeneros(item):
    logger.info("[zpeliculas.py] porgeneros")

    # Descarga la página
    body = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(body,'<div class="shortmovies">(.*?)<div class="navigation ignore-select" align="center">')
    
    '''
    <div class="leftpane">
    <div class="movieposter" title="Descargar Sólo los amantes sobreviven">
    <a href="http://www.zpeliculas.com/peliculas/p-drama/1634-slo-los-amantes-sobreviven.html"><img src="http://i.imgur.com/NBPgXrp.jpg" width="110" height="150" alt="Sólo los amantes sobreviven" title="Descargar Sólo los amantes sobreviven" /></a>
    <div class="shortname">Sólo los amantes sobreviven</div>
    <div class="BDRip">BDRip</div>
    </div>
    </div>

    <div class="rightpane">
    <div style="display:block;overflow:hidden;">
    <h2 class="title" title="Sólo los amantes sobreviven"><a href="http://www.zpeliculas.com/peliculas/p-drama/1634-slo-los-amantes-sobreviven.html">Sólo los amantes sobreviven</a></h2>

    <div style="height:105px; overflow:hidden;">
    <div class="small">
    <div class="cats" title="Genero"><a href="http://www.zpeliculas.com/peliculas/p-drama/">Drama</a>, <a href="http://www.zpeliculas.com/peliculas/p-fantasia/">Fantasia</a>, <a href="http://www.zpeliculas.com/peliculas/p-romantica/">Romantica</a></div>
    <div class="year" title="A&ntilde;o">2013</div>
    <div class="ESP" title="Idioma">ESP</div>
    <div class="FA" title="Sólo los amantes sobreviven FA Official Website"><a href="http://www.filmaffinity.com/es/film851633.html" target="_blank" title="Sólo los amantes sobreviven en filmaffinity">Sólo los amantes sobreviven en FA</a></div>
    </div>
    </div>
    <div class="clear" style="height:2px;"></div>
    <div style="float:right">
    '''
    patron  = '<div class="leftpane">(.*?)<div style="float\:right">'
    #<a href="(.*?)"><img src="(.*?)".*?alt="(.*?)".*?<div class="shortname">.*?</div>.*?<div.*?>(.*?)</div>.*?<div class="rightpane">.*?<div class="year" title="A&ntilde;o">(.*?)<.*?"Idioma">(.*?)</div>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []
    
    for match in matches:
        scrapedurl = scrapertools.find_single_match(match,'<a href="([^"]+)"')
        scrapedthumbnail = scrapertools.find_single_match(match,'<img src="([^"]+)"')
        scrapedtitle = scrapertools.find_single_match(match,'<div class="shortname">([^<]+)')
        scrapedcalidad = scrapertools.find_single_match(match,'<div class="shortname">[^<]+</div[^<]+<div class="[^"]+">([^<]+)')
        scrapedyear = scrapertools.find_single_match(match,'<div class="year[^>]+>([^<]+)')
        scrapedidioma = scrapertools.find_single_match(match,'<div class="year[^>]+>[^<]+</div[^<]+<div class[^>]+>([^<]+)')
        
        title = scrapedtitle
        logger.info("title="+scrapedtitle)
        title = title + ' ('+scrapedyear+') ['+scrapedidioma+'] ['+scrapedcalidad+']'
        url = scrapedurl
        thumbnail = scrapedthumbnail
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        
        itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , url=url, thumbnail=thumbnail, plot=plot, show=title, viewmode="movie", fanart=thumbnail))

    next_page = scrapertools.find_single_match(body,'<a href="([^"]+)">Siguiente')
    if next_page!="":
        itemlist.append( Item(channel=__channel__, action="porgeneros" , title="Página siguiente >>" , url=next_page, thumbnail="", plot="", show="", viewmode="movie", fanart=thumbnail))
    
    return itemlist


def destacadas(item):
    logger.info("[zpeliculas.py] destacadas")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'<div id="sliderwrapper">(.*?)<div class="genreblock">')
    '''
    <div class="imageview view-first">
    <a href="/templates/mytopV2/blockpro/noimage-full.png" onclick="return hs.expand(this)"><img src="http://i.imgur.com/H4d96Wn.jpg" alt="Ocho apellidos vascos"></a>
    <div class="mask">
    <h2><a href="/peliculas/p-comedia/1403-ocho-apellidos-vascos.html" title="Ocho apellidos vascos">Ocho apellidos vascos</a></h2>
    </div>
    '''
    patron  = '<div class="imageview view-first">.*?<a href=.*?>.*?src="(.*?)" alt="(.*?)"></a>.*?<h2><a href="(.*?)".*?</div>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []
    
    for scrapedthumbnail, scrapedtitle, scrapedurl in matches:
        
        logger.info("title="+scrapedtitle)
        title = scrapedtitle
        url = "http://www.zpeliculas.com" + scrapedurl
        thumbnail = scrapedthumbnail
        plot = ""
        plot = unicode( plot, "iso-8859-1" , errors="replace" ).encode("utf-8")
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        
        itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , url=url, thumbnail=thumbnail, plot=plot, show=title, viewmode="movie", fanart=thumbnail))
        
    return itemlist

def sugeridas(item):
    logger.info("[zpeliculas.py] sugeridas")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'<ul class="links">(.*?)</ul>')
    '''
    <li><a href="/peliculas/p-accion/425-instinto-asesino.html" title="Descargar Instinto asesino (The Crew)"><span class="movie-name">Instinto asesino (The Crew)</span><img src="http://i.imgur.com/1xXLz.jpg" width="102" height="138" alt="Instinto asesino (The Crew)" title="Descargar Instinto asesino (The Crew)" /></a></li>
    '''
    patron  = '<li>.*?<a href="(.*?)".*?"movie-name">(.*?)</span><img src="(.*?)"'

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []
    
    for scrapedurl, scrapedtitle, scrapedthumbnail  in matches:
        
        logger.info("title="+scrapedtitle)
        title = scrapedtitle
        url = "http://www.zpeliculas.com" + scrapedurl
        thumbnail = scrapedthumbnail
        plot = ""
        plot = unicode( plot, "iso-8859-1" , errors="replace" ).encode("utf-8")
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        
        itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , url=url, thumbnail=thumbnail, plot=plot, show=title, viewmode="movie", fanart=thumbnail))
        
    return itemlist