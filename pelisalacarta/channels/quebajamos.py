# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para quebajamos.li
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core import jsontools
from core.item import Item
from servers import servertools

DEBUG = config.get_setting("debug")

__category__ = "A"
__type__ = "generic"
__title__ = "Quebajamos"
__channel__ = "quebajamos"
__language__ = "ES"
__creationdate__ = "20140615"

DEFAULT_HEADERS = []
DEFAULT_HEADERS.append( ["User-Agent","Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; es-ES; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12"] )

def isGeneric():
    return True

def login():

    url = "http://webtv.quebajamos.com/process.php"
    post = "sublogin=1&user="+config.get_setting("quebajamosuser")+"&pass="+config.get_setting("quebajamospassword")
    data = scrapertools.cache_page(url,post=post)

def mainlist(item):
    logger.info("pelisalacarta.channels.quebajamos mainlist")

    itemlist = []

    if config.get_setting("quebajamosaccount")!="true":
        itemlist.append( Item( channel=__channel__ , title="Habilita tu cuenta en la configuración..." , action="openconfig" , url="" , folder=False ) )
    else:
        login()
        itemlist.append( Item(channel=__channel__, action="peliculas"   , title="Lo último"       , url="http://webtv.quebajamos.com/" ))
        itemlist.append( Item(channel=__channel__, action="peliculas"   , title="Estrenos"        , url="http://webtv.quebajamos.com/estrenos" ))
        itemlist.append( Item(channel=__channel__, action="peliculas"   , title="Películas"       , url="http://webtv.quebajamos.com/peliculas" ))
        itemlist.append( Item(channel=__channel__, action="peliculas"   , title="Películas HD"    , url="http://webtv.quebajamos.com/hd" ))
        itemlist.append( Item(channel=__channel__, action="peliculas"   , title="Películas 3D"    , url="http://webtv.quebajamos.com/3d" ))
        itemlist.append( Item(channel=__channel__, action="series"   , title="Series"          , url="http://webtv.quebajamos.com/series" ))
        itemlist.append( Item(channel=__channel__, action="series"   , title="Series HD"       , url="http://webtv.quebajamos.com/serieshd" ))
        itemlist.append( Item(channel=__channel__, action="series"   , title="Documentales"    , url="http://webtv.quebajamos.com/programastv" ))
        itemlist.append( Item(channel=__channel__, action="series"   , title="Zona deportes"   , url="http://webtv.quebajamos.com/zonadeportiva" ))
        itemlist.append( Item(channel=__channel__, action="series"   , title="XXX"             , url="http://webtv.quebajamos.com/xxx" ))
        itemlist.append( Item(channel=__channel__, action="search"    , title="Buscar..."       , url="http://webtv.quebajamos.com/search?buscar=" ))
       
    return itemlist

def openconfig(item):
    if "xbmc" in config.get_platform() or "boxee" in config.get_platform():
        config.open_settings( )
    return []

def search(item,texto):
    logger.info("pelisalacarta.channels.quebajamos search")

    if item.url=="":
        item.url="http://webtv.quebajamos.com/search?buscar="

    texto = texto.replace(" ","+")

    # Mete el referer en item.extra
    item.url = item.url+texto
    try:
        itemlist = peliculas(item)
        if len(itemlist)==0:
            itemlist = series(item)
        return itemlist
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def peliculas(item):
    logger.info("pelisalacarta.channels.quebajamos peliculas")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)

    # Extrae las entradas (carpetas)  
    '''
    <div id="caja_portada" onmouseover="{overlib('<div id=cucu><div class=head>Her (2013) 1080p ONLINE  <font color=white>|</font>  <font color=green> HD 5.1 </font> </div> <div class=sinopsis>La película nos sitúa en un futuro no  muy lejano donde vive Theodore (Joaquin Phoenix), un hombre solitario que trabaja como escritor y que está pasando por las últimas etapas de un traumático divorcio. La vida de Theodore no es demasiado emocionante, cuando no está trabajando se pasa las horas jugando a videojuegos y, de vez en cuando, sale con sus amigos. Pero todo va a cambiar cuando el escritor decide adquirir un nuevo sistema operativo para su teléfono y su ordenador, y este sistema tiene como nombre  Samantha  (voz de Scarlett Johansson).</div> <div class=info><b>REPARTO:</b> Joaquin Phoenix, Scarlett Johansson, Rooney Mara, Amy Adams, Olivia Wilde, Chris Pratt, Portia Doubleday, Sam Jaeger, Katherine Boecher, Kelly Sarah, Spike Jonze, Bill Hader, Kristen Wiig, Brian Cox <br /><b>GENERO:</b> Comedia, Drama, Ciencia ficción, Romance <br /><b>DURACION:</b> 126 min.</div></div>', WIDTH, 150, DELAY, 100);}" onmouseout="return nd();">
    <div class='hd_icon'></div>
    <div class="wrap_img">
    <a href="/stream/7734">
    <img src="http://image.tmdb.org/t/p/w185/zu5oyq47nMyz6JNA2SJJT1eOeyR.jpg" />
    </a>
    </div>

    <div class="info">
    <p class="titulo">Her (2013) 1080p ...</p>
    <p class="info">Categoria: <span>PeliculasHD</span></p>
    <p class="info">Calidad: <span> <font style="color:#0e3714">HD 5.1</font></span></p>
    <p class="info">Visto <span>30 veces</span></p>
    </div>

    </div>
    '''
    patron  = '<div id="caja_portada" onmouseover=".overlib.\''
    patron += '<div id=cucu><div class=head>(.*?)</div> <div class=sinopsis>(.*?)</div>.*?'
    patron += '<div class="wrap_img"[^<]+'
    patron += '<a href="([^"]+)"[^<]+'
    patron += '<img src="([^"]+)"'

    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for scrapedtitle,scrapedplot,scrapedurl,scrapedthumbnail in matches:
        title = scrapertools.htmlclean(unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")).strip()
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        plot = scrapertools.htmlclean(unicode( scrapedplot, "iso-8859-1" , errors="replace" ).encode("utf-8")).strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        itemlist.append( Item(channel=__channel__, action="play" , title=title , url=url, extra=item.url, thumbnail=thumbnail, plot=plot, viewmode="movie_with_plot"))

        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

    next_page = scrapertools.find_single_match(data,'class="current"[^<]+</a[^<]+<a class="paginate" title="[^"]+" href="([^"]+)"')
    if next_page!="":
        itemlist.append( Item(channel=__channel__, action="peliculas" , title=">> Página siguiente" , url=urlparse.urljoin(item.url,next_page), folder=True))

    return itemlist

def series(item):
    logger.info("pelisalacarta.channels.quebajamos series")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)

    # Extrae las entradas (carpetas)  
    '''
    <div id="caja_portada" onmouseover="{overlib('<div id=cucu><div class=head>Her (2013) 1080p ONLINE  <font color=white>|</font>  <font color=green> HD 5.1 </font> </div> <div class=sinopsis>La película nos sitúa en un futuro no  muy lejano donde vive Theodore (Joaquin Phoenix), un hombre solitario que trabaja como escritor y que está pasando por las últimas etapas de un traumático divorcio. La vida de Theodore no es demasiado emocionante, cuando no está trabajando se pasa las horas jugando a videojuegos y, de vez en cuando, sale con sus amigos. Pero todo va a cambiar cuando el escritor decide adquirir un nuevo sistema operativo para su teléfono y su ordenador, y este sistema tiene como nombre  Samantha  (voz de Scarlett Johansson).</div> <div class=info><b>REPARTO:</b> Joaquin Phoenix, Scarlett Johansson, Rooney Mara, Amy Adams, Olivia Wilde, Chris Pratt, Portia Doubleday, Sam Jaeger, Katherine Boecher, Kelly Sarah, Spike Jonze, Bill Hader, Kristen Wiig, Brian Cox <br /><b>GENERO:</b> Comedia, Drama, Ciencia ficción, Romance <br /><b>DURACION:</b> 126 min.</div></div>', WIDTH, 150, DELAY, 100);}" onmouseout="return nd();">
    <div class='hd_icon'></div>
    <div class="wrap_img">
    <a href="/stream/7734">
    <img src="http://image.tmdb.org/t/p/w185/zu5oyq47nMyz6JNA2SJJT1eOeyR.jpg" />
    </a>
    </div>

    <div class="info">
    <p class="titulo">Her (2013) 1080p ...</p>
    <p class="info">Categoria: <span>PeliculasHD</span></p>
    <p class="info">Calidad: <span> <font style="color:#0e3714">HD 5.1</font></span></p>
    <p class="info">Visto <span>30 veces</span></p>
    </div>

    </div>
    '''
    patron  = '<div class="wrap_img"[^<]+'
    patron += '<a href="([^"]+)"[^<]+'
    patron += '<img src="([^"]+)"[^<]+'
    patron += '</a[^<]+'
    patron += '</div[^<]+'
    patron += '<div class="info"[^<]+'
    patron += '<p class="titulo">([^<]+)</p>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        title = scrapertools.htmlclean(unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")).strip()
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        plot = ""
        url = urlparse.urljoin(item.url,scrapedurl)
        itemlist.append( Item(channel=__channel__, action="episodios" , title=title , url=url, thumbnail=thumbnail, plot=plot, viewmode="movie"))

        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

    next_page = scrapertools.find_single_match(data,'class="current"[^<]+</a[^<]+<a class="paginate" href="([^"]+)"')
    if next_page!="":
        itemlist.append( Item(channel=__channel__, action="series" , title=">> Página siguiente" , url=urlparse.urljoin(item.url,next_page), folder=True))

    return itemlist

def episodios(item):
    logger.info("pelisalacarta.channels.quebajamos episodios")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    #logger.info("data="+data)
    patron  = '<a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for scrapedurl,scrapedtitle in matches:
        title = scrapertools.htmlclean(unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8"))
        thumbnail = ""
        plot = ""
        url = urlparse.urljoin(item.url,scrapedurl)
        itemlist.append( Item(channel=__channel__, action="play" , title=title , url=url, extra=item.url, thumbnail=thumbnail, plot=plot, fulltitle=title))

        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

    if len(itemlist)==0:
        return play(item)

    return itemlist

def play(item):
    logger.info("pelisalacarta.channels.quebajamos play url="+item.url)
    itemlist = []

    # Hace la llamada
    headers = DEFAULT_HEADERS[:]
    headers.append(["Referer",item.extra])
    data = scrapertools.cache_page(item.url,headers=headers)
    logger.info("data="+data)

    url = scrapertools.find_single_match(data,'file\: "([^"]+)"')
    logger.info("url="+url)

    itemlist.append( Item(channel=__channel__, action="play" , title="Ver el vídeo", url=url, server="directo", folder=True))

    return itemlist    
