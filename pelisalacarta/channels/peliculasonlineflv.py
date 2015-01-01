# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para peliculasonlineflv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "peliculasonlineflv"
__category__ = "F,D"
__type__ = "generic"
__title__ = "Peliculas Online FLV"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[peliculasonlineflv.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Novedades",  action="peliculas", url="http://www.peliculasonlineflv.net"))
    itemlist.append( Item(channel=__channel__, title="Por orden alfabético", action="letras", url="http://www.peliculasonlineflv.net"))
    itemlist.append( Item(channel=__channel__, title="Por géneros", action="generos", url="http://www.peliculasonlineflv.net"))
    itemlist.append( Item(channel=__channel__, title="Buscar...", action="search"))
    return itemlist

def search(item,texto):
    logger.info("[peliculasonlineflv.py] search")
    if item.url=="":
        item.url="http://www.peliculasonlineflv.net/buscar/?s="
    
    texto = texto.replace(" ","+")
    item.url = item.url + texto

    try:
        return peliculas(item)

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def letras(item):
    logger.info("[peliculasonlineflv.py] letras")
    itemlist=[]

    # Descarga la pagina
    data = scrapertools.cachePage(item.url)

    # Patron de las entradas
    patron  = '<li><a href="(/letra[^"]+)">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    # Añade las entradas encontradas
    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle
        url = urlparse.urljoin(item.url,scrapedurl)
        scrapedplot = ""
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="peliculas", title=title , url=url , thumbnail=thumbnail , plot=plot , folder=True) )

    return itemlist

def generos(item):
    logger.info("[peliculasonlineflv.py] generos")
    itemlist=[]

    # Descarga la pagina
    data = scrapertools.cachePage(item.url)

    # Patron de las entradas
    patron  = '<li><a href="(/genero[^"]+)" title="([^"]+)">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    # Añade las entradas encontradas
    for scrapedurl,scrapedtitle in matches:
        title = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")
        url = urlparse.urljoin(item.url,scrapedurl)
        scrapedplot = ""
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="peliculas", title=title , url=url , thumbnail=thumbnail , plot=plot , folder=True) )

    return itemlist

def peliculas(item):
    logger.info("[peliculasonlineflv.py] peliculas")
    itemlist=[]

    # Descarga la pagina
    data = scrapertools.cachePage(item.url)
    '''
    <div class="pelis">
    <a href="http://www.peliculasonlineflv.net/pelicula/io-e-te-tu-y-yo-2012-subtitulada/" title="Io e te (Tú y yo) (2012) - Subtitulada"><img class="port" src="http://www.peliculasonlineflv.net/img/1495.jpg" alt="Io e te (Tú y yo) (2012) - Subtitulada"></a>
    <div class="pelis-desc">
    <h3>Io e te (Tú y yo) (2012) - Subtitulada</h3>
    <p class="desc-mid">
    La pelicula trata sobre la historia de un adolescente de catorce años que engaña a sus padres con una coartada de una esquiada entre amigos para, en realidad, pasar esos días en un sótano con la intención de ayudar a su hermanastra mayor a superar su adicción a la heroína.
    </p>
    <p class="desc-low">
    <span class="desc-item"><span class="bold">Reparto: </span> Tea Falco, Jacopo Olmo Antinori, Sonia Bergamasco, Veronica Lazar</span>
    <span class="desc-item"><span class="bold">Director: </span> Bernardo Bertolucci</span>
    <span class="desc-item"><span class="bold">G&eacute;nero: </span> Drama, Family</span>
    </p>
    </div>
    '''

    # Patron de las entradas
    patron  = '<div class="pelis"[^<]+'
    patron += '<a href="([^"]+)" title="([^"]+)"><img class="port" src="([^"]+)"[^<]+</a[^<]+'
    patron += '<div class="pelis-desc"[^<]+'
    patron += '<h3[^<]+</h3[^<]+'
    patron += '<p class="desc-mid">([^<]+)</p>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    # Añade las entradas encontradas
    for scrapedurl,scrapedtitle,scrapedthumbnail,scrapedplot in matches:
        title = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")
        url = scrapedurl
        plot = scrapedplot
        thumbnail = scrapedthumbnail
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=title , url=url , thumbnail=thumbnail , plot=plot , folder=True) )

    patron = '<span class="actual">[^<]+</span[^<]+<a href="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        siguiente_url = urlparse.urljoin(item.url,"/"+matches[0])
        itemlist.append( Item(channel=__channel__, action="peliculas", title=">> Página siguiente" , url=siguiente_url , folder=True) )

    return itemlist

def findvideos(item):
    logger.info("[peliculasonlineflv.py] findvideos")
    itemlist=[]

    # Descarga la p?gina
    data = scrapertools.cachePage(item.url)

    from servers import servertools
    itemlist.extend(servertools.find_video_items(data=data))
    for videoitem in itemlist:
        videoitem.channel=__channel__
        videoitem.action="play"
        videoitem.folder=False
        videoitem.title = "Ver en "+videoitem.server
        videoitem.fulltitle = item.fulltitle

    # Ahora busca patrones manuales
    try:
        vk_code = scrapertools.get_match(data,"vklat\=([a-zA-Z0-9]+)")
        vk_url = scrapertools.get_header_from_response("http://goo.gl/"+vk_code,header_to_get="location")
        itemlist.append( Item( channel=__channel__ , action="play" , title="Ver en VK (Latino)" , server="vk" , url=vk_url , folder=False ) )
    except:
        logger.info("No encontrado enlace VK")

    try:
        putlocker_code = scrapertools.get_match(data,"plat\=([A-Z0-9]+)")
        putlocker_url = "http://www.putlocker.com/embed/"+putlocker_code
        itemlist.append( Item( channel=__channel__ , action="play" , title="Ver en Putlocker (Latino)" , server="putlocker" , url=putlocker_url , folder=False ) )
    except:
        logger.info("No encontrado enlace PUTLOCKER")

    try:
        vk_code = scrapertools.get_match(data,"vksub\=([a-zA-Z0-9]+)")
        vk_url = scrapertools.get_header_from_response("http://goo.gl/"+vk_code,header_to_get="location")
        itemlist.append( Item( channel=__channel__ , action="play" , title="Ver en VK (Subtitulado)" , server="vk" , url=vk_url , folder=False ) )
    except:
        logger.info("No encontrado enlace VK")

    try:
        putlocker_code = scrapertools.get_match(data,"plsub\=([A-Z0-9]+)")
        putlocker_url = "http://www.putlocker.com/embed/"+putlocker_code
        itemlist.append( Item( channel=__channel__ , action="play" , title="Ver en Putlocker (Subtitulado)" , server="putlocker" , url=putlocker_url , folder=False ) )
    except:
        logger.info("No encontrado enlace PUTLOCKER")

    try:
        vk_code = scrapertools.get_match(data,"vk\=([a-zA-Z0-9]+)")
        vk_url = scrapertools.get_header_from_response("http://goo.gl/"+vk_code,header_to_get="location")
        itemlist.append( Item( channel=__channel__ , action="play" , title="Ver en VK" , server="vk" , url=vk_url , folder=False ) )
    except:
        logger.info("No encontrado enlace VK")

    try:
        putlocker_code = scrapertools.get_match(data,"put\=([A-Z0-9]+)")
        putlocker_url = "http://www.putlocker.com/embed/"+putlocker_code
        itemlist.append( Item( channel=__channel__ , action="play" , title="Ver en Putlocker" , server="putlocker" , url=putlocker_url , folder=False ) )
    except:
        logger.info("No encontrado enlace PUTLOCKER")

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    mainlist_items = mainlist(Item())
    peliculas_items = peliculas(mainlist_items[0])

    for pelicula_item in peliculas_items:
        mirrors = findvideos( item=pelicula_item )
        if len(mirrors)>0:
            return True

    return False