# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para tusnovelas.com
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "tusnovelas"
__category__ = "S"
__type__ = "generic"
__title__ = "Tus novelas"
__language__ = "ES"
__creationdate__ = "20120703"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.channels.tusnovelas mainlist")
    
    itemlist = []

    itemlist.append( Item(channel=__channel__, action="series"              , title="Últimas telenovelas añadidas" , url="http://tusnovelas.com/lista-novelas/"))
    itemlist.append( Item(channel=__channel__, action="series_top"          , title="Telenovelas TOP"              , url="http://tusnovelas.com/"))
    itemlist.append( Item(channel=__channel__, action="series_emision"      , title="Telenovelas en Emisión"       , url="http://tusnovelas.com/"))
    itemlist.append( Item(channel=__channel__, action="letras"              , title="Todas por orden alfabético"   , url="http://tusnovelas.com/"))

    return itemlist

def series_top(item):
    logger.info("pelisalacarta.channels.tusnovelas series_top")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.find_single_match(data,'<ul class="eltop">(.*?)</ul>')
    patron  = '<li[^<]+<a href="([^"]+)"[^>]+>([^<]+)</a>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        url = urlparse.urljoin("http://tusnovelas.com/",scrapedurl)
        thumbnail = ""
        title = scrapedtitle
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="episodios", title=title , url=url , folder=True) )

    return itemlist

def series_emision(item):
    logger.info("pelisalacarta.channels.tusnovelas series_emision")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.find_single_match(data,'<ul class="enemi">(.*?)</ul>')
    patron  = '<li[^<]+<a href="([^"]+)"[^>]+>([^<]+)</a>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        url = urlparse.urljoin("http://tusnovelas.com/",scrapedurl)
        thumbnail = ""
        title = scrapedtitle
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="episodios", title=title , url=url , folder=True) )

    return itemlist

def letras(item):
    logger.info("pelisalacarta.channels.tusnovelas letras")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.find_single_match(data,'<div id="abc">(.*?)</ul>')
    patron  = '<li[^<]+<a href="([^"]+)"[^>]+>([^<]+)</a>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        url = urlparse.urljoin("http://tusnovelas.com/",scrapedurl)
        thumbnail = ""
        title = scrapedtitle
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="series", title=title , url=url , folder=True) )

    return itemlist

def series(item):
    logger.info("pelisalacarta.channels.tusnovelas series")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    '''
    <div class="pelis">
    <a href="novela/lo-que-la-vida-me-robo.html"><img class="port" src="img/photos/portadas_160x240/72.jpg" alt="Lo que la vida me robó"  width="160" height="240px"  /></a>
    <!-- Descripción -->
    <div class="pelis-desc">
    <h3>Lo que la vida me robó</h3>
    <p class="desc-mid">
    La vida le jugo a Monserrat una mala pasada, su madre la obligo a casarse con un hombre a quién ella no ama, todo por salvar a su familia de la miseria ya que este hombre es rico.
    <br /><br />
    Por este matrimonio debe renunciar al amor real, el cual será encarcelado injustamente producto de una trampa por parte de la madre de Monserrat. Pero la vida muchas veces es bastante complicada y ella podría encontrar el amor en donde menos lo espera.                </p>
    <p class="desc-low">
    <span class="desc-item"><span class="bold">Actores y Actrices: </span> Daniela Castro, Angelique Boyer, Sebastián Rulli, Luis Roberto Guzmán, Sergio Sendel, Rogelio Guerra, Eric del Castillo, Gabriela Rivero, Grettell Valdez, Lisset Gutiérrez Salazar, Alberto Estrella, Ana Bertha Espín, Juan Carlos Barreto, Luis Uribe, Osvaldo Benavides, Verónica Jaspeado, Margarita Magaña.</span>
    <span class="desc-item"><span class="bold">Canal: </span> El Canal de las Estrellas</span>
    <span class="desc-item"><span class="bold">País </span> México </span>
    </p>
    </div>
    <!-- Fin Descripción -->
    </div><!--end .pelis-->
    '''
    patron  = '<div class="pelis"[^<]+'
    patron += '<a href="([^"]+)"><img class="port" src="([^"]+)"[^<]+</a[^<]+'
    patron += '<!-- Des[^<]+'
    patron += '<div class="pelis-desc"[^<]+'
    patron += '<h3>([^<]+)</h3>(.*?)</div>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedthumbnail,scrapedtitle,scrapedplot in matches:
        url = urlparse.urljoin("http://tusnovelas.com/",scrapedurl)
        thumbnail = urlparse.urljoin("http://tusnovelas.com/",scrapedthumbnail)
        title = scrapedtitle
        plot = scrapertools.htmlclean(scrapedplot)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="episodios", title=title , url=url , thumbnail=thumbnail ,fanart=thumbnail , plot=plot , viewmode="movie_with_plot" , folder=True) )
    
    next_page_url = scrapertools.find_single_match(data,'<a href="([^"]+)">Siguiente</a>')
    if next_page_url!="":
        itemlist.append( Item(channel=__channel__, action="series", title=">> Página siguiente" , url=next_page_url , folder=True) )

    return itemlist

def episodios(item):
    logger.info("pelisalacarta.channels.tusnovelas episodios")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    patron  = '<li><a href="(capitulo/[^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for url,scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        scrapedurl = urlparse.urljoin("http://tusnovelas.com/",url)

        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
    
    return itemlist

def findvideos(item):
    logger.info("pelisalacarta.channels.tusnovelas findvideos")
    data = scrapertools.cache_page(item.url)
    itemlist=[]

    patron = '<embed type="application/x-shockwave-flash" src="http://www.todoanimes.com/reproductor/player.swf".*?file=([^\&]+)&'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for match in matches:
        itemlist.append( Item(channel=__channel__, action="play", server="directo", title=item.title , url=match , thumbnail=item.thumbnail , plot=item.plot , folder=False) )

    #<embed width="680" height="450" flashvars="file=mp4:p/459791/sp/45979100/serveFlavor/flavorId/0_0pacv7kr/forceproxy/true&amp;image=&amp;skin=&amp;abouttext=&amp;dock=false&amp;streamer=rtmp://rtmpakmi.kaltura.com/ondemand/&amp;
    patron = '<embed width="[^"]+" height="[^"]+" flashvars="file=([^\&]+)&.*?streamer=(rtmp[^\&]+)&'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for final,principio in matches:
        itemlist.append( Item(channel=__channel__, action="play", server="directo", title=item.title , url=principio+final , thumbnail=item.thumbnail , plot=item.plot , folder=False) )


    from servers import servertools
    itemlist.extend(servertools.find_video_items(data=data))
    for videoitem in itemlist:
        videoitem.channel=__channel__
        videoitem.action="play"
        videoitem.folder=False
        videoitem.title = "["+videoitem.server+"]"

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():

    # mainlist
    mainlist_items = mainlist(Item())
    novedades_items = novedades_episodios(mainlist_items[1])
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    bien = False
    for singleitem in novedades_items:
        mirrors = findvideos( item=singleitem )
        if len(mirrors)>0:
            bien = True
            break

    return bien