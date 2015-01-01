# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para serieonline.net
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "serieonline"
__category__ = "F,S,D"
__type__ = "generic"
__title__ = "Serieonline"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[serieonline.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Episodios destacados"      , action="destacados"     , url="http://www.serieonline.net/"))
    itemlist.append( Item(channel=__channel__, title="Nuevos episodios"          , action="novedades"      , url="http://www.serieonline.net/"))
    itemlist.append( Item(channel=__channel__, title="Series (con carátula)"     , action="series"         , url="http://www.serieonline.net/series/"))
    itemlist.append( Item(channel=__channel__, title="Series (listado completo)" , action="seriescompleto" , url="http://www.serieonline.net/"))
    itemlist.append( Item(channel=__channel__, title="Buscar"                    , action="search"))
    
    return itemlist

def search(item,texto):
    logger.info("[serieonline.py] search")
    if item.url=="":
        item.url="http://www.serieonline.net/buscar/"
    texto = texto.replace(" ","+")
    post = "tag="+texto
    try:
        data = scrapertools.cache_page(item.url,post=post)
        '''
        <a href="/merlin/" class="link_superpuesto"></a>
        <img src="/imagenes/series/horizontal/merlin.jpg"></img>
        <a href="/merlin/">Merlín</a>
        '''
        patron  = '<a href="([^"]+)"[^<]+</a[^<]+<img src="([^"]+)"[^<]+</img>[^<]+<a href="[^"]+">([^<]+)</a>'    
        matches = re.compile(patron,re.DOTALL).findall(data)
        if DEBUG: scrapertools.printMatches(matches)
    
        itemlist = []
        for url,thumbnail,title in matches:
            title = unicode( title, "iso-8859-1" , errors="replace" ).encode("utf-8")
            scrapedtitle = title.strip()
            scrapedplot = ""
            scrapedurl = urlparse.urljoin(item.url,url)
            scrapedthumbnail = urlparse.urljoin(item.url,thumbnail)
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
    
            # Añade al listado de XBMC
            itemlist.append( Item(channel=__channel__, action="episodios", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , viewmode="movie", folder=True) )
    
        return itemlist

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def destacados(item):
    logger.info("[serieonline.py] destacados")

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas
    patronvideos  = '<a href="([^"]+)" title="([^"]+)"><img src="([^"]+)" alt="([^"]+)" class="captify" /></a>'

    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[1] + " " + match[3]
        scrapedtitle = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")
        scrapedplot = ""
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = urlparse.urljoin(item.url,match[2])
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , viewmode="movie", folder=True) )

    return itemlist

def novedades(item):
    logger.info("[serieonline.py] novedades")

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas
    patronvideos  = '<div class="capitulo"><div class="imagen-text"><a href="([^"]+)"><img src="([^"]+)"[^<]+</a></div><div class="texto-capitulo"><a href="[^"]+">([^<]+)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for url,thumbnail,title in matches:
        title = unicode( title, "iso-8859-1" , errors="replace" ).encode("utf-8")
        scrapedtitle = title
        scrapedplot = ""
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = urlparse.urljoin(item.url,thumbnail)
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , viewmode="movie", folder=True) )

    # Extrae el paginador
    patronvideos  = '<div class="paginacion-num"><a href="([^"]+)">'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedtitle = ">> Página siguiente"
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="novedades", title=scrapedtitle , url=scrapedurl , folder=True) )

    return itemlist

def series(item,paginacion=True):
    logger.info("[serieonline.py] series")

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas
    '''
    <div class="series">
    <div class="mostrar-series-imagen">
    <a href="http://www.serieonline.net/90210/">
    <img src="http://www.serieonline.net/imagenes/90210.jpg" alt="90210" height="155" width="200" />
    </a>
    </div>
    <div class="mostrar-series-texto">
    <a href="http://www.serieonline.net/90210/">90210</a>
    
    </div>
    </div>
    '''

    patronvideos  = '<div class="series">[^<]+'
    patronvideos += '<div class="mostrar-series-imagen">[^<]+'
    patronvideos += '<a href="([^"]+)">[^<]+'
    patronvideos += '<img src="([^"]+)"[^<]+'
    patronvideos += '</a>[^<]+'
    patronvideos += '</div>[^<]+'
    patronvideos += '<div class="mostrar-series-texto">[^<]+'
    patronvideos += '<a href="[^>]+>([^<]+)</a>'

    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = unicode(match[2],"iso-8859-1",errors="replace").encode("utf-8")
        scrapedplot = ""
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = urlparse.urljoin(item.url,match[1])
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action="episodios", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , show=scrapedtitle, viewmode="movie", folder=True) )

    # Extrae el paginador
    patronvideos  = '<div class="paginacion-num">\d+</div><div class="paginacion-num"><a href="([^"]+)">'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedtitle = ">> Página siguiente"
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        newitem = Item(channel=__channel__, action="series", title=scrapedtitle , url=scrapedurl , folder=True)
        if paginacion:
            itemlist.append( newitem )
        else:
            itemlist.extend( series(newitem,paginacion) )

    return itemlist

def seriescompleto(item):
    logger.info("[serieonline.py] seriescompleto")

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas
    data = scrapertools.get_match(data , '<div id="lista-series-menu">(.*?)\s+<div class="clear"></div>')

    patronvideos  = '<a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for url,title in matches:
        title = unicode( title, "iso-8859-1" , errors="replace" ).encode("utf-8")
        scrapedtitle = title
        scrapedplot = ""
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action="episodios", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , show=scrapedtitle, folder=True) )

    return itemlist

def episodios(item):
    logger.info("[serieonline.py] episodios")

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas
    patronvideos  = '<li>[^<]+'
    patronvideos += '<a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    itemlist = []
    for url,title in matches:
        title = unicode( title, "iso-8859-1" , errors="replace" ).encode("utf-8")
        scrapedtitle = title
        scrapedplot = ""
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , show=item.show, plot=scrapedplot , folder=True) )

    return itemlist

def findvideos(item):
    logger.info("[serieonline.py] findvideos")
    itemlist = []
    
    '''
    <div class="enlace_contenedor">
    <div class="enlace_contenedor_enlace">
    <a href="http://www.serieonmirror.com/section/64846/a102bca9daa4b450c692bf8c610408fa/" target="_blank" title="Descargar de rapidgator">Descargar</a>
    </div>
    <div class="enlace_contenedor_servidor_ server rapidgator"></div>
    <div class="enlace_contenedor_idioma_ES" title="Español"><div></div></div>
    <div class="enlace_contenedor_idioma_" title=""><div></div></div>
    <div class="enlace_contenedor_info"><p><b></b></p></div>
    <div class="enlace_contenedor_up"><p><b>Emel</b></p></div>	<div class="enlace_contenedor_info_contenedor">
    <p></p>
    </div>
    <div class="clear"></div>
    </div>
    '''

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    patron = '<div class="enlace_contenedor">(.*?)<div class="clear">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for match in matches:
        logger.info("match="+match)
        
        patron2  = '<a href="([^"]+)[^<]+</a>[^<]+</div>[^<]+'
        patron2 += '<div class="enlace_contenedor_servidor_ server ([^"]+)"></div>[^<]+'
        patron2 += '<div class="enlace_contenedor_idioma[^"]+" title="([^"]+)"><div></div></div>[^<]+'
        patron2 += '<div class="enlace_contenedor_idioma[^"]+" title="([^"]*)"><div></div></div>[^<]+'
	patron2 += '<div class="enlace_contenedor_info"><p><b>(.*?)</b></p></div>'
        matches2 = re.compile(patron2,re.DOTALL).findall(match)
        for url,server,audio,subtitulos,info in matches2:
	    patronhd="720p"
	    matcheshd=re.compile(patronhd,re.DOTALL).findall(info)
	    if (len(matcheshd)>0):
		title="[HD] Ver en "+server+" (audio "+audio+", subtitulos "+subtitulos+")"
	    else:
		title="Ver en "+server+" (audio "+audio+", subtitulos "+subtitulos+")"
	    print "#"+info+"#"
            if subtitulos=="":
                subtitulos="no"
            itemlist.append( Item(channel=__channel__, action="play", title=title , url=url , thumbnail=item.thumbnail , show=item.show, plot=item.plot , folder=False) )

    return itemlist

def play(item):
    logger.info("[serieonline.py] play")
    itemlist = []
    print("play"+item.server)
    data = scrapertools.cachePage(item.url)
    
    from servers import servertools
    itemlist = servertools.find_video_items(data=data)
    for videoitem in itemlist:
        videoitem.channel = item.channel
        videoitem.folder=False
        videoitem.action="play"
    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    novedades_items = novedades(mainlist_items[1])
    bien = False
    for novedades_item in novedades_items:
        mirrors = findvideos( item=novedades_item )

        for mirror in mirrors:
            mediaurl = play( mirror )
            if len(mediaurl)>0:
                return True

    return False