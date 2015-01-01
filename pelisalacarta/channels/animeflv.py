# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para animeflv (por MarioXD)
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

__category__ = "A"
__type__ = "generic"
__title__ = "Animeflv"
__channel__ = "animeflv"
__language__ = "ES"
__creationdate__ = "20111014"

ANIMEFLV_REQUEST_HEADERS = []
ANIMEFLV_REQUEST_HEADERS.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:22.0) Gecko/20100101 Firefox/22.0"])
ANIMEFLV_REQUEST_HEADERS.append(["Accept-Encoding","gzip, deflate"])
ANIMEFLV_REQUEST_HEADERS.append(["Cache-Control","max-age=0"])
ANIMEFLV_REQUEST_HEADERS.append(["Connection","keep-alive"])
ANIMEFLV_REQUEST_HEADERS.append(["Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"])
ANIMEFLV_REQUEST_HEADERS.append(["Accept-Language","es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3"])

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.channels.animeflv mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="novedades"     , title="Últimos episodios"   , url="http://animeflv.net/" ))
    itemlist.append( Item(channel=__channel__, action="menuseries"    , title="Series"              , url="http://animeflv.net/animes/?orden=nombre&mostrar=series" ))
    itemlist.append( Item(channel=__channel__, action="menuovas"      , title="OVAS"                , url="http://animeflv.net/animes/?orden=nombre&mostrar=ovas" ))
    itemlist.append( Item(channel=__channel__, action="menupeliculas" , title="Películas"           , url="http://animeflv.net/animes/?orden=nombre&mostrar=peliculas" ))
    itemlist.append( Item(channel=__channel__, action="search"        , title="Buscar"              , url="http://animeflv.net/animes/?buscar=" ))
  
    return itemlist

def menuseries(item):
    logger.info("pelisalacarta.channels.animeflv menuseries")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="letras"  , title="Por orden alfabético" , url="http://animeflv.net/animes/?orden=nombre&mostrar=series" ))
    itemlist.append( Item(channel=__channel__, action="generos" , title="Por géneros"          , url="http://animeflv.net/animes/?orden=nombre&mostrar=series" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="En emisión"           , url="http://animeflv.net/animes/en-emision/?orden=nombre&mostrar=series" ))
  
    return itemlist

def menuovas(item):
    logger.info("pelisalacarta.channels.animeflv menuovas")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="letras"  , title="Por orden alfabético" , url="http://animeflv.net/animes/?orden=nombre&mostrar=ovas" ))
    itemlist.append( Item(channel=__channel__, action="generos" , title="Por géneros"          , url="http://animeflv.net/animes/?orden=nombre&mostrar=ovas" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="En emisión"           , url="http://animeflv.net/animes/en-emision/?orden=nombre&mostrar=ovas" ))
  
    return itemlist

def menupeliculas(item):
    logger.info("pelisalacarta.channels.animeflv menupeliculas")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="letras"  , title="Por orden alfabético" , url="http://animeflv.net/animes/?orden=nombre&mostrar=peliculas" ))
    itemlist.append( Item(channel=__channel__, action="generos" , title="Por géneros"          , url="http://animeflv.net/animes/?orden=nombre&mostrar=peliculas" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="En emisión"           , url="http://animeflv.net/animes/en-emision/?orden=nombre&mostrar=peliculas" ))
  
    return itemlist

def letras(item):
    logger.info("pelisalacarta.channels.animeflv letras")

    itemlist = []
    data = scrapertools.cache_page(item.url, headers = ANIMEFLV_REQUEST_HEADERS)
    data = scrapertools.get_match(data,'<div class="alfabeto_box"(.*?)</div>')
    patron = '<a href="([^"]+)[^>]+>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)    

    for scrapedurl,scrapedtitle in matches:
        title = scrapertools.entityunescape(scrapedtitle)
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="series" , title=title , url=url, thumbnail=thumbnail, plot=plot))
    return itemlist

def generos(item):
    logger.info("pelisalacarta.channels.animeflv generos")

    itemlist = []

    data = scrapertools.cache_page(item.url, headers = ANIMEFLV_REQUEST_HEADERS)
    data = scrapertools.get_match(data,'<div class="generos_box"(.*?)</div>')
    patron = '<a href="([^"]+)[^>]+>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)    

    for scrapedurl,scrapedtitle in matches:
        title = scrapertools.entityunescape(scrapedtitle)
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="series" , title=title , url=url, thumbnail=thumbnail, plot=plot))
    return itemlist

def search(item,texto):
    logger.info("pelisalacarta.channels.animeflv search")
    if item.url=="":
        item.url="http://animeflv.net/animes/?buscar="
    texto = texto.replace(" ","+")
    item.url = item.url+texto
    try:
        return series(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def novedades(item):
    logger.info("pelisalacarta.channels.animeflv novedades")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url , headers = ANIMEFLV_REQUEST_HEADERS)

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
    logger.info("pelisalacarta.channels.animeflv series")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers = ANIMEFLV_REQUEST_HEADERS)

    # Extrae las entradas 
    '''
    <div class="aboxy_lista">
    <a href="/ova/nurarihyon-no-mago-ova.html" title="Nurarihyon no Mago OVA"><img class="lazy portada" src="/img/blank.gif" data-original="http://cdn.animeflv.net/img/portada/1026.jpg" alt="Nurarihyon no Mago OVA"/></a>
    <span style="float: right; margin-top: 0px;" class="tipo_1"></span>
    <a href="/ova/nurarihyon-no-mago-ova.html" title="Nurarihyon no Mago OVA" class="titulo">Nurarihyon no Mago OVA</a>
    <div class="generos_links"><b>Generos:</b> <a href="/animes/genero/accion/">Acci&oacute;n</a>, <a href="/animes/genero/shonen/">Shonen</a>, <a href="/animes/genero/sobrenatural/">Sobrenatural</a></div>
    <div class="sinopsis">La historia empieza en alrededor de 100 a&ntilde;os despu&eacute;s de la desaparici&oacute;n de Yamabuki Otome, la primera esposa Rihan Nura. Rihan por fin recobr&oacute; la compostura y la vida vuelve a la normalidad. A medida que la cabeza del Clan Nura, est&aacute; ocupado trabajando en la construcci&oacute;n de un mundo armonioso para los seres humanos y youkai. Un d&iacute;a, &eacute;l ve a Setsura molesta por lo que decide animarla tomando el clan para ir a disfrutar de las aguas termales &hellip;</div>
    </div>
    '''

    patron  = '<div class="aboxy_lista"[^<]+'
    patron += '<a href="([^"]+)"[^<]+<img class="[^"]+" src="[^"]+" data-original="([^"]+)"[^<]+</a[^<]+'
    patron += '<span[^<]+</span[^<]+'
    patron += '<a[^>]+>([^<]+)</a.*?'
    patron += '<div class="sinopsis">(.*?)</div'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for scrapedurl,scrapedthumbnail,scrapedtitle,scrapedplot in matches:
        title = scrapedtitle
        fulltitle = title
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        plot = scrapertools.htmlclean(scrapedplot)
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
    logger.info("pelisalacarta.channels.animeflv episodios")
    itemlist = []
    
    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers = ANIMEFLV_REQUEST_HEADERS)

    '''
    <div class="tit">Listado de episodios <span class="fecha_pr">Fecha Pr&oacute;ximo: 2013-06-11</span></div>
    <ul class="anime_episodios" id="listado_epis"><li><a href="/ver/aiura-9.html">Aiura 9</a></li><li><a href="/ver/aiura-8.html">Aiura 8</a></li><li><a href="/ver/aiura-7.html">Aiura 7</a></li><li><a href="/ver/aiura-6.html">Aiura 6</a></li><li><a href="/ver/aiura-5.html">Aiura 5</a></li><li><a href="/ver/aiura-4.html">Aiura 4</a></li><li><a href="/ver/aiura-3.html">Aiura 3</a></li><li><a href="/ver/aiura-2.html">Aiura 2</a></li><li><a href="/ver/aiura-1.html">Aiura 1</a></li></ul>
    '''

    # Saca enlaces a los episodios
    data = scrapertools.get_match(data,'<div class="tit">Listado de episodios.*?</div>(.*?)</ul>')
    patron = '<li><a href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)

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
    logger.info("pelisalacarta.channels.animeflv findvideos")

    data = scrapertools.cache_page(item.url, headers = ANIMEFLV_REQUEST_HEADERS)
    data = scrapertools.get_match(data,"var videos \= (.*?)$")
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
