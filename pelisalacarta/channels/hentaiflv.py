# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para hentaiflv (por Kira)
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

DEBUG = config.get_setting("debug")

__category__ = "A,X"
__type__ = "generic"
__title__ = "Hentaiflv"
__channel__ = "hentaiflv"
__language__ = "ES"
__creationdate__ = "20140414"

HENTAIFLV_REQUEST_HEADERS = []
HENTAIFLV_REQUEST_HEADERS.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:22.0) Gecko/20100101 Firefox/22.0"])
HENTAIFLV_REQUEST_HEADERS.append(["Accept-Encoding","gzip, deflate"])
HENTAIFLV_REQUEST_HEADERS.append(["Cache-Control","max-age=0"])
HENTAIFLV_REQUEST_HEADERS.append(["Connection","keep-alive"])
HENTAIFLV_REQUEST_HEADERS.append(["Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"])
HENTAIFLV_REQUEST_HEADERS.append(["Accept-Language","es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3"])

def isGeneric():
    return True

def mainlist(item):
    logger.info("[hentaiflv.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="novedades"     , title="Novedades"   , url="http://hentaiflv.net/" ))
    itemlist.append( Item(channel=__channel__, action="generos"    , title="Generos"              , url="" ))
    itemlist.append( Item(channel=__channel__, action="search"        , title="Buscar"              , url="http://hentaiflv.net/buscar/" ))
  
    return itemlist

def generos(item):
    logger.info("[hentaiflv.py] menuseries")
    
    
    itemlist = []
    
    itemlist.append( Item(channel=__channel__, action="series"  , title="Anal"           , url="http://hentaiflv.net/genero/anal.html" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="Bakunyu"             , url="http://hentaiflv.net/genero/bakunyu.html" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="Big Boobs"           , url="http://hentaiflv.net/genero/big-boobs.html" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="BJ/Oral"           , url="http://hentaiflv.net/genero/oral.html" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="Bondage"           , url="http://hentaiflv.net/genero/bondage.html" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="Ecchi"               , url="http://hentaiflv.net/genero/ecchi.html" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="Eroguro"           , url="http://hentaiflv.net/genero/eroguro.html" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="Escolares"           , url="http://hentaiflv.net/genero/escolares.html" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="Ficcion"               , url="http://hentaiflv.net/genero/ficcion.html" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="Furry"           , url="http://hentaiflv.net/genero/furry.html" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="Futanari"           , url="http://hentaiflv.net/genero/futanari.html" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="Gore"             , url="http://hentaiflv.net/genero/gore.html" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="Incest"           , url="http://hentaiflv.net/genero/incest.html" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="Lolicon"           , url="http://hentaiflv.net/genero/lolicon.html" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="Magical"           , url="http://hentaiflv.net/genero/magical.html" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="Ninjas"           , url="http://hentaiflv.net/genero/ninjas.html" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="Nurses/Maids"             , url="http://hentaiflv.net/genero/nurses.html" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="Orgies"           , url="http://hentaiflv.net/genero/orgies.html" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="POV"           , url="http://hentaiflv.net/genero/pov.html" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="Pregnant"             , url="http://hentaiflv.net/genero/pregnant.html" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="Reporteras de TV"             , url="http://hentaiflv.net/genero/reporteras-de-tv..html" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="Romance"           , url="http://hentaiflv.net/genero/romance.html" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="Scat & Urination"           , url="http://hentaiflv.net/genero/urination.html" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="Shoutakon"           , url="http://hentaiflv.net/genero/shoutakon.html" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="Shrine Maidens"           , url="http://hentaiflv.net/genero/shrine-maidens.html" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="Softcore"               , url="http://hentaiflv.net/genero/softcore.html" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="Teachers"           , url="http://hentaiflv.net/genero/teachers.html" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="Trenes/Rail"           , url="http://hentaiflv.net/genero/trenes.html" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="Violacion"           , url="http://hentaiflv.net/genero/violacion.html" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="Yaoi"           , url="http://hentaiflv.net/genero/yaoi.html" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="Yuri"           , url="http://hentaiflv.net/genero/yuri.html" ))

    
    return itemlist




def search(item,texto):
    logger.info("[hentaiflv.py] search")
    if item.url=="":
        item.url="http://hentaiflv.net/buscar/"
    texto = texto.replace(" ","+")
    item.url = item.url+texto+".html"
    try:
        return series(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def novedades(item):
    logger.info("[animeflv.py] novedades")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url , headers = HENTAIFLV_REQUEST_HEADERS)

    # Extrae las entradas (carpetas)  
    '''
    <div class="not">
    <a href="/ver/cyclops-shoujo-saipu-12.html" title="Cyclops Shoujo Saipu 12">
    <img class="imglstsr lazy" src="http://cdn.animeflv.net/img/mini/957.jpg" border="0">
    <span class="tit_ep"><span class="tit">Cyclops Shoujo Saipu 12</span></span>
    </a>
    '''
    patronvideos  = '<div class="not"[^<]+<a href="([^"]+)" title="([^"]+)"[^<]+<img class="[^"]+" src="([^"]+)"[^<]+<span class="tit_ep"><span class="tit">([^<]+)<'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    itemlist = []
    
    for match in matches:
        scrapedtitle = scrapertools.entityunescape(match[3])
        fulltitle = scrapedtitle
        # directory = match[1]
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = urlparse.urljoin(item.url,match[2].replace("mini","portada"))
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, fulltitle=fulltitle, viewmode="movie"))

    return itemlist

def series(item):
    logger.info("[hentaiflv.py] series")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers = HENTAIFLV_REQUEST_HEADERS)

    # Extrae las entradas 
    '''
    <article class="thumbnails entry-content">
          <a href="http://hentaiflv.net/hentai/aki-sora.html" class="tooltip" title="Aki Sora">
                          <img width="194" height="300" src="http://hentaisd.com/images/portadas/Protada_5395_big.jpg" class="attachment-medium wp-post-image" alt="Aki Sora" />                    </a>
        <div style="clear: both;"></div>
      </article>
    '''

    patron  = '<article class="thumbnails entry-content"[^<]+'
    patron += '<a href="([^"]+)"[^<]+<img width="[^"]+" height="[^"]+" src="([^"]+)" class="attachment-medium wp-post-image" alt="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)<=0:
        patron  = '<div class="aboxy_lista"[^<]+'
        patron += '<a href="([^"]+)"[^<]+<img class="[^"]+" src="[^"]+" data-original="([^"]+)"[^<]+</a[^<]+'
        patron += '<span[^<]+</span[^<]+'
        patron += '<a[^>]+>([^<]+)</a.*?'
        patron += '<div class="sinopsis">'
        matches = re.compile(patron,re.DOTALL).findall(data)
    
    itemlist = []
    
    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        title = scrapedtitle
        fulltitle = title
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        plot = ""
        show = title
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="episodios", title=title , url=url , thumbnail=thumbnail , plot=plot , show=show, fulltitle=fulltitle, fanart=thumbnail, viewmode="movies_with_plot", folder=True) )

    patron = '<a href="([^"]+)">\&raquo\;</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for match in matches:
        if len(matches) > 0:
            scrapedurl = urlparse.urljoin(item.url,match)
            scrapedtitle = ">> Pagina Siguiente"
            scrapedthumbnail = ""
            scrapedplot = ""

            itemlist.append( Item(channel=__channel__, action="series", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def episodios(item):
    logger.info("[hentaiflv.py] episodios")
    itemlist = []
    
    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers = HENTAIFLV_REQUEST_HEADERS)

    '''
    <div class="tit">Listado de episodios <span class="fecha_pr">Fecha Pr&oacute;ximo: 2013-06-11</span></div>
    <ul class="anime_episodios" id="listado_epis"><li><a href="/ver/aiura-9.html">Aiura 9</a></li><li><a href="/ver/aiura-8.html">Aiura 8</a></li><li><a href="/ver/aiura-7.html">Aiura 7</a></li><li><a href="/ver/aiura-6.html">Aiura 6</a></li><li><a href="/ver/aiura-5.html">Aiura 5</a></li><li><a href="/ver/aiura-4.html">Aiura 4</a></li><li><a href="/ver/aiura-3.html">Aiura 3</a></li><li><a href="/ver/aiura-2.html">Aiura 2</a></li><li><a href="/ver/aiura-1.html">Aiura 1</a></li></ul>
    '''
    
    patron = '<div class="reproductor">.*?ul class="tabs">(.*?)</ul>'    
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches) > 0:
        patron = '<li rel="tooltip"><a href="([^"]+)">([^<]+)</a></li>'
        matches = re.compile(patron,re.DOTALL).findall(matches[0])
    else:
        patron = '<div class="tit">Listado de episodios.*?</div>(.*?)</ul>'    
        matches = re.compile(patron,re.DOTALL).findall(data)
        if len(matches)>0:
            patron = '<li><a href="([^"]+)">([^<]+)</a>'
            matches = re.compile(patron,re.DOTALL).findall(matches[0])
    

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle
        try:
            episodio = scrapertools.get_match(scrapedtitle,item.show+"\s+(\d+)")
            if len(episodio)==1:
                title = "1x0"+episodio
            else:
                title = "1x"+episodio
        except:
            pass
        
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = item.thumbnail
        plot = item.plot
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=title , url=url , thumbnail=thumbnail , plot=plot , show=item.show, fulltitle=item.show+" "+title, fanart=thumbnail, viewmode="movies_with_plot", folder=True) )

    if config.get_platform().startswith("xbmc") or config.get_platform().startswith("boxee"):
        itemlist.append( Item(channel=__channel__, title="Añadir esta serie a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="episodios", show=item.show) )
        itemlist.append( Item(channel=item.channel, title="Descargar todos los episodios de la serie", url=item.url, action="download_all_episodes", extra="episodios", show=item.show) )

    return itemlist

def findvideos(item):
    logger.info("[animeflv.py] findvideos")

    data = scrapertools.cache_page(item.url, headers = HENTAIFLV_REQUEST_HEADERS)
    
    patron = "var videos \= (.*?)$"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)<=0:   
        patron = "<div class=\"tab_container\">(.*?)<fieldset"
        matches = re.compile(patron,re.DOTALL).findall(data)
        if len(matches)<=0:   
            return []
    
        
        
    data = matches[0]
    logger.info("data="+data)

    itemlist=[]
    
    data = data.replace("\\\\","")
    data = data.replace("\\/","/")
    logger.info("data="+data)

    from servers import servertools
    itemlist.extend(servertools.find_video_items(data=data))
    for videoitem in itemlist:
        videoitem.channel=__channel__
        videoitem.action="play"
        videoitem.folder=False
        videoitem.title = "["+videoitem.server+"]"

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True

    # mainlist
    mainlist_items = mainlist(Item())
    
    # Comprueba que todas las opciones tengan algo (excepto el buscador)
    for mainlist_item in mainlist_items:
        if mainlist_item.action!="search":
            exec "itemlist = "+mainlist_item.action+"(mainlist_item)"
            if len(itemlist)==0:
                return false

    # Comprueba si alguno de los vídeos de "Novedades" devuelve mirrors
    episodios_items = novedades(mainlist_items[0])

    bien = False
    for episodio_item in episodios_items:
        mirrors = findvideos(episodio_item)
        if len(mirrors)>0:
            bien = True
            break

    return bien
