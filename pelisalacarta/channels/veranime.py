# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para http://www.veranime.net/
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

__channel__ = "veranime"
__category__ = "A"
__type__ = "generic"
__title__ = "Ver-anime"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[veranime.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Ultimos capítulos", action="ultimos"     , url="http://www.vanime.net/", extra="enem"))
    itemlist.append( Item(channel=__channel__, title="Nuevos animes"    , action="series"      , url="http://www.vanime.net/", extra="estr"))
    itemlist.append( Item(channel=__channel__, title="Top semanal"      , action="series"      , url="http://www.vanime.net/", extra="decs"))
    itemlist.append( Item(channel=__channel__, title="+ Vistos"         , action="series"      , url="http://www.vanime.net/", extra="msvd"))
    itemlist.append( Item(channel=__channel__, title="+ Valorados"      , action="series"      , url="http://www.vanime.net/", extra="msan"))
    itemlist.append( Item(channel=__channel__, title="Buscar"           , action="search"))

    return itemlist

def ultimos(item):
    logger.info("[veranime.py] novedades")
    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,"<!--<"+item.extra+">-->(.*?)<!--</"+item.extra+">-->")

    # Extrae las entradas
    #<a href="http://www.vanime.net/anime/kami-nomi-zo-shiru-sekai.html" title="Kami Nomi zo Shiru Sekai"><img class="poab" src="http://www.vimagen.net/va/kami-nomi-zo-shiru-sekai.gif" alt="Kami Nomi zo Shiru Sekai" /></a>
    patron = '<a href="([^"]+)" title="([^"]+)"><img class="[^"]+" src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for url,title,thumbnail in matches:
        scrapedurl = url
        scrapedtitle = title
        scrapedthumbnail = thumbnail
        scrapedplot = ""

        # Añade al listado
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def series(item):
    logger.info("[veranime.py] series")
    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,"<!--<"+item.extra+">-->(.*?)<!--</"+item.extra+">-->")

    # Extrae las entradas
    #<a href="http://www.vanime.net/anime/kami-nomi-zo-shiru-sekai.html" title="Kami Nomi zo Shiru Sekai"><img class="poab" src="http://www.vimagen.net/va/kami-nomi-zo-shiru-sekai.gif" alt="Kami Nomi zo Shiru Sekai" /></a>
    patron = '<a href="([^"]+)" title="([^"]+)"><img class="[^"]+" src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for url,title,thumbnail in matches:
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedtitle = title
        scrapedthumbnail = thumbnail
        scrapedplot = ""

        # Añade al listado
        itemlist.append( Item(channel=__channel__, action="episodios", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , show=scrapedtitle, folder=True) )

    return itemlist

def episodios(item):
    logger.info("[veranime.py] episodios")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    itemlist = []
    
    # Busca la caratula y el argumento
    scrapedthumbnail = scrapertools.get_match(data,'<li class="bg">[^<]+<img src="([^"]+)"')
    #scrapedplot = scrapertools.get_match(data,'<div class="pefctxt txaj flol">(.*?)</ul>[^<]+</div>"')
    #scrapedplot = scrapertools.htmlclean(scrapedplot)
    scrapedplot = ""

    # Busca donde estan todos los capitulos
    '''
    <ul class="lstcap fonb cnli2 overview txts1 poab widt100">
    
    <li class="clfl">
    
    <a class="btnvis bg flor" href="#" id="cap_avatar-la-leyenda-de-korra--12" onclick="capitulos('avatar-la-leyenda-de-korra--12');return false;">No Visto</a>
    <a class="icob flol pore" href="../avatar-la-leyenda-de-korra-12.html" title="Avatar: La leyenda de Korra 12" >Avatar: La leyenda de Korra 12</a>
    </li><li class="clfl">
    
    <a class="btnvis bg flor" href="#" id="cap_avatar-la-leyenda-de-korra--7" onclick="capitulos('avatar-la-leyenda-de-korra--7');return false;">No Visto</a>
    <a class="icob flol pore" href="../avatar-la-leyenda-de-korra-7.html" title="Avatar: La leyenda de Korra 7" >Avatar: La leyenda de Korra 7</a>
    </li><li class="clfl">
    
    <a class="btnvis bg flor" href="#" id="cap_avatar-la-leyenda-de-korra--1" onclick="capitulos('avatar-la-leyenda-de-korra--1');return false;">No Visto</a>
    <a class="icob flol pore" href="../avatar-la-leyenda-de-korra-1.html" title="Avatar: La leyenda de Korra 1" >Avatar: La leyenda de Korra 1</a>
    </li>
    </ul>
    '''
    
    data = scrapertools.get_match(data,'<ul class="lstcap(.*?)</ul>')
    patron = '<a class="icob flol pore" href="([^"]+)" title="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for url,title in matches:
        scrapedtitle = title
        if scrapedtitle.lower().startswith(item.show.lower()):
            scrapedtitle = scrapedtitle[len(item.show):].strip()

            patron = '\d+'
            matches = re.compile(patron,re.DOTALL).findall(scrapedtitle)
            if len(matches)>0:
                if len(scrapedtitle)==1:
                    scrapedtitle = "0"+scrapedtitle
                scrapedtitle = "1x"+scrapedtitle
            else:
                scrapedtitle = title
            
        scrapedurl = urlparse.urljoin(item.url,url)
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , show=item.show, folder=True) )

    if config.get_platform().startswith("xbmc"):
        itemlist.append( Item(channel=item.channel, title="Añadir estos episodios a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="episodios", show=item.show) )

    return itemlist

def findvideos(item):
    logger.info("[veranime.py] findvideos")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    itemlist = []
    patron = '<a href="(/play[^"]+)" target="animecap[^>]+>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for url,title in matches:
        title = title.replace("&nbsp;","")
        url = urlparse.urljoin(item.url,url)
        itemlist.append( Item(channel=__channel__, action="play", title=title , url=url) )

    return itemlist

def play(item):
    logger.info("[divxonline.py] play")
    itemlist=[]
    data = scrapertools.cachePage(item.url)
    logger.info("data="+data)
    itemlist = servertools.find_video_items(data=data)
    i=1
    for videoitem in itemlist:
        videoitem.title = "Mirror %d%s" % (i,videoitem.title)
        videoitem.fulltitle = item.fulltitle
        videoitem.channel=channel=__channel__
        i=i+1

    return itemlist

def search(item,texto):
    logger.info("[veranime.py] search")
    itemlist = []
    
    # Descarga la página con la busqueda
    data = scrapertools.cache_page( "http://www.vanime.net/core/search.php" , post="searchword="+texto )

    # Extrae las entradas de todas series
    '''
    <li class="rslcnt icob">
    <div class="srcimg flol"><a href="/anime/avatar-libro-fuego.html"><img height="53" widht="41" src="http://www.vimagen.net/va/avatarfuego.gif" alt="Avatar Libro Fuego" /></a></div>
    <div class="srctxt flor">
    <h2><a href="/anime/avatar-libro-fuego.html">Avatar Libro Fuego</a></h2>
    <p class="pln1"><strong>Fecha de Publicacion</strong> 2009-01-06</p>
    <p class="pln2"><strong>Anime:</strong> <strong>Anime</strong>: Finalizado</p>    
    </div>
    </li>
    '''
    patron  = '<li class="rslcnt icob">[^<]+'
    patron += '<div class="srcimg flol"><a href="([^"]+)"><img height="\d+" widht="\d+" src="([^"]+)" alt="([^"]+)" /></a></div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for url,thumbnail,title in matches:
        scrapedtitle = title.strip()
        scrapedurl = urlparse.urljoin("http://www.vanime.net",url)
        scrapedthumbnail = thumbnail
        scrapedplot = ""

        # Añade al listado
        itemlist.append( Item(channel=__channel__, action="episodios", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , show = scrapedtitle, folder=True) )

    itemlist = sorted(itemlist, key=lambda Item: Item.title) 
    return itemlist
