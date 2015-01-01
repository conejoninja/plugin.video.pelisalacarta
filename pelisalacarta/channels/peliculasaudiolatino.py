# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para peliculasaudiolatino
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "peliculasaudiolatino"
__category__ = "F"
__type__ = "generic"
__title__ = "Peliculasaudiolatino"
__language__ = "ES"
__creationdate__ = "20111014"

DEBUG = config.get_setting("debug")
    
def isGeneric():
    return True

def mainlist(item):
    logger.info("channels.peliculasaudiolatino mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Recién agregadas", action="peliculas", url="http://www.peliculasaudiolatino.tv/newest-movies/page/0.html"))
    itemlist.append( Item(channel=__channel__, title="Recién actualizadas", action="peliculas", url="http://www.peliculasaudiolatino.tv/updated-movies/page/0.html"))
    itemlist.append( Item(channel=__channel__, title="Las más vistas", action="peliculas", url="http://www.peliculasaudiolatino.tv/most-viewed-movies/page/0.html"))
    itemlist.append( Item(channel=__channel__, title="Mejor puntuación", action="peliculas", url="http://www.peliculasaudiolatino.tv/top-rated-movies/page/0.html"))
    
    itemlist.append( Item(channel=__channel__, title="Listado alfabético" , action="letras", url="http://www.peliculasaudiolatino.tv/browse-movies.html"))
    itemlist.append( Item(channel=__channel__, title="Listado por géneros" , action="generos", url="http://www.peliculasaudiolatino.tv"))
    itemlist.append( Item(channel=__channel__, title="Listado por años" , action="anyos", url="http://www.peliculasaudiolatino.tv"))
    
    itemlist.append( Item(channel=__channel__, title="Buscar..." , action="search") )
    return itemlist

def peliculas(item):
    logger.info("channels.peliculasaudiolatino peliculas")

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas de la pagina seleccionada
    patron = '<td class=.*?<a href="([^"]+)"><img src="([^"]+)" alt="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for match in matches:
        scrapedurl = match[0]
        scrapedtitle = match[2].strip()
        scrapedthumbnail = match[1]
        scrapedplot = ""
        logger.info(scrapedtitle)

        # Añade al listado
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , fulltitle=scrapedtitle, url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , viewmode="movie", folder=True) )
           
    # Extrae la marca de siguiente página
    next_page = scrapertools.find_single_match(data,'<a href="([^"]+)">Siguiente >>')
    if next_page!="":
        itemlist.append( Item(channel=__channel__, action="peliculas", title=">> Página siguiente" , url=urlparse.urljoin(item.url,next_page).replace("/../../","/"), folder=True) )

    return itemlist

def peliculas2(item):
    logger.info("channels.peliculasaudiolatino peliculas2")

    itemlist = []
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    patron = '<td height=90 valign=top width=60>.*?<a href="([^"]+)"><img src="([^"]+)" .*?<b>([^<]+)</b>.*?<td><b>([^<]+)</b></td>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if (DEBUG): scrapertools.printMatches(matches)
    for match in matches:
        scrapedurl = urlparse.urljoin("http://www.peliculasaudiolatino.tv",match[0])
        scrapedtitle = match[2].strip()
        scrapedthumbnail = match[1]
        scrapedplot = match[3]
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , fulltitle=scrapedtitle, url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , viewmode="movie_with_plot", folder=True) )

    # Extrae la marca de siguiente página
    next_page = scrapertools.find_single_match(data,"<a href='([^']+)'>Siguiente >>")
    if next_page!="":
        itemlist.append( Item(channel=__channel__, action="peliculas2", title=">> Página siguiente" , url=urlparse.urljoin(item.url,next_page).replace("/../../","/"), folder=True) )

    return itemlist

def generos(item):
    logger.info("channels.peliculasaudiolatino categorias")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Limita el bloque donde buscar
    data = scrapertools.find_single_match(data,'<span>Generos</span>(.*?)</div>')

    # Extrae las entradas
    patron = '<li><a href="(http://www.peliculasaudiolatino.tv/genre[^"]+)"><span>([^<]+)</span></a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if (DEBUG): scrapertools.printMatches(matches)
                                          
    for match in matches:
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedtitle = match[1].replace("&nbsp;&nbsp;&nbsp;*","").strip()
        scrapedthumbnail = ""
        scrapedplot = ""
        logger.info(scrapedtitle)

        itemlist.append( Item(channel=__channel__, action="peliculas2", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    itemlist = sorted(itemlist, key=lambda Item: Item.title)    
    return itemlist
    
def letras(item):
    logger.info("channels.peliculasaudiolatino letras")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Limita el bloque donde buscar
    data = scrapertools.find_single_match(data,"<h4>Alfabeticamente </h4><br[^<]+<center>(.*?)</center>")

    # Extrae las entradas
    patron = '<a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if (DEBUG): scrapertools.printMatches(matches)
                                          
    for scrapedurl,scrapedtitle in matches:
        url = urlparse.urljoin(item.url,scrapedurl)
        title = scrapedtitle
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="peliculas2", title=title , url=url , thumbnail=thumbnail , plot=plot, folder=True) )

    return itemlist

def anyos(item):
    logger.info("channels.peliculasaudiolatino anyos")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    logger.info("channels.peliculasaudiolatino data="+data)

    # Limita el bloque donde buscar
    '''
    <span>Ultimos A&ntilde;os</span></a>
    <div class="columns two">
    <ul class="one">
    <li><a href="http://www.peliculasaudiolatino.tv/year/2014.html"><span>2014</span></a>
    <li><a href="http://www.peliculasaudiolatino.tv/year/2013.html"><span>2013</span></a>
    <li><a href="http://www.peliculasaudiolatino.tv/year/2012.html"><span>2012</span></a>
    <li><a href="http://www.peliculasaudiolatino.tv/year/2011.html"><span>2011</span></a>
    <li><a href="http://www.peliculasaudiolatino.tv/year/2010.html"><span>2010</span></a>
    </ul>
    <ul class="two">
    <li><a href="http://www.peliculasaudiolatino.tv/year/2009.html"><span>2009</span></a>
    <li><a href="http://www.peliculasaudiolatino.tv/year/2008.html"><span>2008</span></a>
    <li><a href="http://www.peliculasaudiolatino.tv/year/2007.html"><span>2007</span></a>
    <li><a href="http://www.peliculasaudiolatino.tv/year/2006.html"><span>2006</span></a>
    <li><a href="http://www.peliculasaudiolatino.tv/year/2005.html"><span>2005</span></a>
    </ul>
    </div>

    '''
    data = scrapertools.find_single_match(data,"<span>Ultimos A.ntilde.os</span>(.*?)</div>")
    logger.info("channels.peliculasaudiolatino data="+data)

    # Extrae las entradas
    patron = '<li><a href="(http://www.peliculasaudiolatino.tv/year[^"]+)"><span>([^<]+)</span>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if (DEBUG): scrapertools.printMatches(matches)
                                          
    for scrapedurl,scrapedtitle in matches:
        url = urlparse.urljoin(item.url,scrapedurl)
        title = scrapedtitle
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="peliculas2", title=title , url=url , thumbnail=thumbnail , plot=plot, folder=True) )

    return itemlist

def search(item,texto):
    logger.info("channels.peliculasaudiolatino search")
    itemlist = []

    texto = texto.replace(" ","+")
    try:
        # Series
        item.url="http://www.peliculasaudiolatino.tv/result.php?q=%s&type=search&x=0&y=0"
        item.url = item.url % texto
        item.extra = ""
        itemlist.extend(peliculas2(item))
        itemlist = sorted(itemlist, key=lambda Item: Item.title) 
        
        return itemlist
        
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []
    
    '''url = "http://www.peliculasaudiolatino.tv/series-anime"
    data = scrapertools.cachePage(url)

    # Extrae las entradas de todas series
    patronvideos  = '<li>[^<]+'
    patronvideos += '<a.+?href="([\D]+)([\d]+)">[^<]+'
    patronvideos += '.*?/>(.*?)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        scrapedtitle = match[2].strip()

        # Realiza la busqueda
        if scrapedtitle.lower()==texto.lower() or texto.lower() in scrapedtitle.lower():
            logger.info(scrapedtitle)
            scrapedurl = urlparse.urljoin(url,(match[0]+match[1]))
            scrapedthumbnail = urlparse.urljoin("http://www.peliculasaudiolatino.tv/images/series/",(match[1]+".png"))
            scrapedplot = ""

            # Añade al listado
            itemlist.append( Item(channel=__channel__, action="listacapitulos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist'''


def findvideos(item):
    logger.info("channels.peliculasaudiolatino videos")
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    title = item.title
    scrapedthumbnail = item.thumbnail
    itemlist = []
    patron = "tr>.*?window.open[\D]'([^']+)'.*?Servidor: ([^<]+)<.*?Audio: ([^<]+)<.*?Calidad: ([^<]+)<.*?Formato: ([^<]+)</font>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if (DEBUG): scrapertools.printMatches(matches)
    for match in matches:
        url = match[0]
        title = "Ver en "+match[1]+" ["+match[2]+"]["+match[3]+"]"
        itemlist.append( Item(channel=__channel__, action="play", title=title , fulltitle=item.fulltitle, url=url , thumbnail=scrapedthumbnail , folder=False) )

    return itemlist

def play(item):
    logger.info("channels.peliculasaudiolatino play")
    itemlist=[]

    data2 = scrapertools.cache_page(item.url)
    logger.info("data2="+data2)
    data2 = data2.replace("http://www.peliculasaudiolatino.tv/show/vidbux.php?url=","http://www.vidbux.com/")
    data2 = data2.replace("http://www.peliculasaudiolatino.tv/show/vidxden.php?url=","http://www.vidxden.com/")

    data2 = data2.replace("http://www.peliculasaudiolatino.tv/v/pl/play.php?url=","http://www.putlocker.com/embed/")
    data2 = data2.replace("http://www.peliculasaudiolatino.tv/v/mv/play.php?url=","http://www.modovideo.com/frame.php?v=")
    data2 = data2.replace("http://www.peliculasaudiolatino.tv/v/ss/play.php?url=","http://www.sockshare.com/embed/")
    data2 = data2.replace("http://www.peliculasaudiolatino.tv/v/vb/play.php?url=","http://vidbull.com/")
    data2 = data2.replace("http://www.peliculasaudiolatino.tv/v/vk/play.php?url=","http://vk.com/video_ext.php?oid=")
    data2 = data2.replace("http://www.peliculasaudiolatino.tv/v/ttv/play.php?url=","http://www.tumi.tv/")

    data2 = data2.replace("http://www.peliculasaudiolatino.tv/show/sockshare.php?url=","http://www.sockshare.com/embed/")
    data2 = data2.replace("http://www.peliculasaudiolatino.tv/show/moevide.php?url=","http://moevideo.net/?page=video&uid=")
    data2 = data2.replace("http://www.peliculasaudiolatino.tv/show/novamov.php?url=","http://www.novamov.com/video/")
    data2 = data2.replace("http://www.peliculasaudiolatino.tv/show/movshare.php?url=","http://www.movshare.net/video/")
    data2 = data2.replace("http://www.peliculasaudiolatino.tv/show/divxstage.php?url=","http://www.divxstage.net/video/")
    data2 = data2.replace("http://www.peliculasaudiolatino.tv/show/tumi.php?url=","http://www.tumi.tv/")
    data2 = data2.replace("http://www.peliculasaudiolatino.tv/show/playerto.php?url=","http://played.to/")
    data2 = data2.replace("http://www.peliculasaudiolatino.tv/show/videoweed.php?url=","http://www.videoweed.es/file/")
    data2 = data2.replace("http://www.peliculasaudiolatino.tv/show/netu.php?url=","http://netu.tv/watch_video.php?v=")
    data2 = data2.replace("http://www.peliculasaudiolatino.tv/show/powvideo.php?url=","http://powvideo.net/")
    data2 = data2.replace("http://www.peliculasaudiolatino.tv/show/streamin.php?url=","http://streamin.to/")
    data2 = data2.replace("%26","&")
    logger.info("data2="+data2)

    listavideos = servertools.findvideos(data2)
    for video in listavideos:
        invalid = video[1]
        invalid = invalid[0:8]
        if invalid!= "FN3WE43K" and invalid!="9CC3F8&e":
            scrapedtitle = item.title+video[0]
            videourl = video[1]
            server = video[2]
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+videourl+"]")

            # Añade al listado de XBMC
            itemlist.append( Item(channel=__channel__, action="play", title=scrapedtitle , fulltitle=item.fulltitle, url=videourl , server=server , folder=False) )
    
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
        mirrors = findvideos( item=novedades_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien