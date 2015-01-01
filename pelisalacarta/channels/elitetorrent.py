# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para elitetorrent
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "elitetorrent"
__category__ = "F,S,D"
__type__ = "generic"
__title__ = "Elite Torrent"
__language__ = "ES"

DEBUG = config.get_setting("debug")
BASE_URL = 'http://www.elitetorrent.net'

def isGeneric():
    return True

def mainlist(item):
    logger.info("[elitetorrent.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Docus y TV"     , action="peliculas", url="http://www.elitetorrent.net/categoria/6/docus-y-tv/modo:mini"))
    itemlist.append( Item(channel=__channel__, title="Estrenos"       , action="peliculas", url="http://www.elitetorrent.net/categoria/1/estrenos/modo:mini"))
    itemlist.append( Item(channel=__channel__, title="Películas"      , action="peliculas", url="http://www.elitetorrent.net/categoria/2/peliculas/modo:mini"))
    itemlist.append( Item(channel=__channel__, title="Peliculas HDRip", action="peliculas", url="http://www.elitetorrent.net/categoria/13/peliculas-hdrip/modo:mini"))
    itemlist.append( Item(channel=__channel__, title="Peliculas MicroHD", action="peliculas", url="http://www.elitetorrent.net/categoria/17/peliculas-microhd/modo:mini"))
    itemlist.append( Item(channel=__channel__, title="Peliculas VOSE" , action="peliculas", url="http://www.elitetorrent.net/categoria/14/peliculas-vose/modo:mini"))
    itemlist.append( Item(channel=__channel__, title="Series"         , action="peliculas", url="http://www.elitetorrent.net/categoria/4/series/modo:mini"))
    itemlist.append( Item(channel=__channel__, title="Series VOSE"    , action="peliculas", url="http://www.elitetorrent.net/categoria/16/series-vose/modo:mini"))

    return itemlist

def peliculas(item):
    logger.info("[elitetorrent.py] peliculas")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    '''
    <li>
    <a href="/torrent/23471/mandela-microhd-720p"><img src="thumb_fichas/23471.jpg" border="0" title="Mandela (microHD - 720p)" alt="IMG: Mandela (microHD - 720p)"/></a>
    <div class="meta">
    <a class="nombre" href="/torrent/23471/mandela-microhd-720p" title="Mandela (microHD - 720p)">Mandela (microHD - 720p)</a>
    <span class="categoria">Peliculas microHD</span>
    <span class="fecha">Hace 2 sem</span>
    <span class="descrip">Título: Mandela: Del mito al hombre<br />
    '''
    patron =  '<a href="(/torrent/[^"]+)">'
    patron += '<img src="(thumb_fichas/[^"]+)" border="0" title="([^"]+)"[^>]+></a>'
    patron += '.*?<span class="descrip">(.*?)</span>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl, scrapedthumbnail, scrapedtitle, scrapedplot in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(BASE_URL, scrapedurl)
        thumbnail = urlparse.urljoin(BASE_URL, scrapedthumbnail)
        plot = re.sub('<[^<]+?>', '', scrapedplot)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="play", title=title , url=url , thumbnail=thumbnail , plot=plot , folder=False, viewmode="movie_with_plot") )

    # Extrae el paginador
    patronvideos  = '<a href="([^"]+)" class="pagina pag_sig">Siguiente \&raquo\;</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="peliculas", title="Página siguiente >>" , url=scrapedurl , folder=True) )

    return itemlist

def play(item):
    logger.info("[elitetorrent.py] play")
    itemlist = []

    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    #<a href="magnet:?xt=urn:btih:d6wtseg33iisp7jexpl44wfcqh7zzjuh&amp;dn=Abraham+Lincoln+Cazador+de+vampiros+%28HDRip%29+%28EliteTorrent.net%29&amp;tr=http://tracker.torrentbay.to:6969/announce" class="enlace_torrent degradado1">Descargar por magnet link</a> 
    link = scrapertools.get_match(data,'<a href="(magnet[^"]+)" class="enlace_torrent[^>]+>Descargar por magnet link</a>')
    link = urlparse.urljoin(item.url,link)
    logger.info("link="+link)

    itemlist.append( Item(channel=__channel__, action="play", server="torrent", title=item.title , url=link , thumbnail=item.thumbnail , plot=item.plot , folder=False) )

    return itemlist
