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

__channel__ = "sintonizzate"
__category__ = "F"
__type__ = "generic"
__title__ = "Sintonizzate.me"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[sintonizzate.py] mainlist")

    itemlist = []
	
    itemlist.append( Item(channel=__channel__, action="agregadas"        , title="Últimas agregadas", url="http://sintonizzate.me/",fanart="http://sintonizzate.me/Temas/default/img/bg.png"))
    itemlist.append( Item(channel=__channel__, action="listalfabetico"   , title="Listado alfabético",fanart="http://sintonizzate.me/Temas/default/img/bg.png"))
    itemlist.append( Item(channel=__channel__, action="generos"    , title="Por géneros",    url="http://www.peliculaspepito.com/",fanart="http://sintonizzate.me/Temas/default/img/bg.png"))
    itemlist.append( Item(channel=__channel__, action="search"        , title="Buscador", url="http://sintonizzate.me/",fanart="http://sintonizzate.me/Temas/default/img/bg.png"))
    
    return itemlist

def search(item,texto):
    busqueda=texto.replace(" ","+")
    data = scrapertools.cachePage("http://sintonizzate.me/buscar/?q=" + busqueda)
    # Descarga la página
    data = scrapertools.get_match(data,'(<ul class="peliculas clf cntclsx4 f_left_li"> .*?</ul>)')
    
    '''
    <div class="peli_img_img"> 
    <a href="http://sintonizzate.me/pelicula/641/mortal-kombat-1995.html" title="Mortal Kombat (1995)"><img src="http://sintonizzate.me/files/uploads/641.jpg" alt="Mortal Kombat (1995)" /></a> 
    </div> 
    '''
    patron = '<div class="peli_img_img">.*?href="(.*?)".*?src="(.*?)".*?alt="(.*?)"'
    patron += '.*?Sinopsis.*?<p>(.*?)</p>.*?<strong>Genero</strong>:(.*?), (.*?)</div>.*?<strong>Idioma</strong>: (.*?)</div>.*?<strong>Calidad</strong>: (.*?)</div>'
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []
    for scrapedurl,scrapedthumbnail,scrapedtitle, sipnosis, categoria, scrapedyear, idioma, calidad in matches:
        logger.info("title="+scrapedtitle)
        title = scrapertools.htmlclean(scrapedtitle).strip()
        title = title.replace("\r","").replace("\n","")
        title = title.replace(" Online","")
        title = unicode( title, "iso-8859-1" , errors="replace" ).encode("utf-8")
        title = re.compile("\s+",re.DOTALL).sub(" ",title)
        title = title + " [" + idioma +"][" + calidad + "]"
        logger.info("title="+title)
        year = scrapedyear
        url = scrapedurl
        thumbnail = scrapedthumbnail
        plot = sipnosis
        plot = unicode( plot, "iso-8859-1" , errors="replace" ).encode("utf-8")
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        if "Programa TV" not in categoria:
            if "Serie TV" not in categoria:
                itemlist.append( Item(channel=__channel__, action="findvideos" , language=idioma,  title=title, category=categoria, url=url, thumbnail=thumbnail, plot=plot, show=title, viewmode="movie", fanart=thumbnail))

    return itemlist


def agregadas(item):
    logger.info("[sintonizzate.py] agregadas")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,' <ul class="Aportes (.*?)</ul>')
    
    '''
    <div class="peli_img_img"> 
    <a href="http://sintonizzate.me/pelicula/641/mortal-kombat-1995.html" title="Mortal Kombat (1995)"><img src="http://sintonizzate.me/files/uploads/641.jpg" alt="Mortal Kombat (1995)" /></a> 
    </div> 
    '''
    patron = '<div class="peli_img_img">.*?href="(.*?)".*?src="(.*?)".*?alt="(.*?)"'
    patron += '.*?Sinopsis.*?<p>(.*?)</p>.*?<strong>Genero</strong>:(.*?), (.*?)</div>.*?<strong>Idioma</strong>: (.*?)</div>.*?<strong>Calidad</strong>: (.*?)</div>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []
    for scrapedurl,scrapedthumbnail,scrapedtitle, sipnosis, categoria, scrapedyear, idioma, calidad in matches:
        logger.info("title="+scrapedtitle)
        title = scrapertools.htmlclean(scrapedtitle).strip()
        title = title.replace("\r","").replace("\n","")
        title = title.replace(" Online","")
        title = unicode( title, "iso-8859-1" , errors="replace" ).encode("utf-8")
        title = re.compile("\s+",re.DOTALL).sub(" ",title)
        title = title + " [" + idioma +"][" + calidad + "]"
        logger.info("title="+title)
        year = scrapedyear
        url = scrapedurl
        thumbnail = scrapedthumbnail
        plot = sipnosis
        plot = unicode( plot, "iso-8859-1" , errors="replace" ).encode("utf-8")
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        if "Programa TV" not in categoria:
            if "Serie TV" not in categoria:
                itemlist.append( Item(channel=__channel__, action="findvideos" , language=idioma,  title=title, category=categoria, url=url, thumbnail=thumbnail, plot=plot, show=title, viewmode="movie", fanart=thumbnail))
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'<!--<nav>-->(.*?)<!--</nav>-->')
    patron = 'href="(.*?)" >(.*?)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for siguientes, buena in matches:
        siguiente = "http://www.sintonizzate.me/" + siguientes
        if "Siguiente" in buena:
            itemlist.append( Item(channel=__channel__, action="agregadas" , title="Siguiente >>" , url=siguiente, thumbnail="", plot=plot, show=title, viewmode="movie", fanart="http://pelisalacarta.mimediacenter.info/fanart/seriespepito.jpg"))
    
    return itemlist

def alfabetico(item):
    logger.info("[sintonizzate.py] agregadas")
    #Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'<ul class="peliculas clf cntclsx4 f_left_li">(.*?)</ul>')
    
    '''
    <div class="peli_img_img"> 
    <a href="http://sintonizzate.me/pelicula/641/mortal-kombat-1995.html" title="Mortal Kombat (1995)"><img src="http://sintonizzate.me/files/uploads/641.jpg" alt="Mortal Kombat (1995)" /></a> 
    </div> 
    '''

    patron = '<div class="peli_img_img">.*?href="(.*?)".*?src="(.*?)".*?alt="(.*?)"'
    patron += '.*?Sinopsis.*?<p>(.*?)</p>.*?<strong>Genero</strong>:(.*?), (.*?)</div>.*?<strong>Idioma</strong>: (.*?)</div>.*?<strong>Calidad</strong>: (.*?)</div>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []

    for scrapedurl,scrapedthumbnail,scrapedtitle, sipnosis, categoria, scrapedyear, idioma, calidad in matches:
        logger.info("title="+scrapedtitle)
        title = scrapertools.htmlclean(scrapedtitle).strip()
        title = title.replace("\r","").replace("\n","")
        title = title.replace(" Online","")
        title = unicode( title, "iso-8859-1" , errors="replace" ).encode("utf-8")
        title = re.compile("\s+",re.DOTALL).sub(" ",title)
        title = title + " [" + idioma +"][" + calidad + "]"
        logger.info("title="+title)
        year = scrapedyear
        url = scrapedurl
        thumbnail = scrapedthumbnail
        plot = sipnosis
        plot = unicode( plot, "iso-8859-1" , errors="replace" ).encode("utf-8")
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        if "Programa TV" not in categoria:
            if "Serie TV" not in categoria:
                itemlist.append( Item(channel=__channel__, action="findvideos" , language=idioma,  title=title, category=categoria, url=url, thumbnail=thumbnail, plot=plot, show=title, viewmode="movie", fanart=thumbnail))
    return itemlist


def generos(item):
    logger.info("[sintonizzate.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="alfabetico" , title="Acción",url="http://sintonizzate.me/categoria/accion/"))
    itemlist.append( Item(channel=__channel__, action="alfabetico" , title="Animación",url="http://sintonizzate.me/categoria/animacion/"))
    itemlist.append( Item(channel=__channel__, action="alfabetico" , title="Anime",url="http://sintonizzate.me/categoria/anime/"))
    itemlist.append( Item(channel=__channel__, action="alfabetico" , title="Aventura",url="http://sintonizzate.me/categoria/aventura/"))
    itemlist.append( Item(channel=__channel__, action="alfabetico" , title="Bélico",url="http://sintonizzate.me/categoria/belico/"))
    itemlist.append( Item(channel=__channel__, action="alfabetico" , title="Biográfico",url="http://sintonizzate.me/categoria/biografico/"))
    itemlist.append( Item(channel=__channel__, action="alfabetico" , title="Ciencia Ficción",url="http://sintonizzate.me/categoria/ciencia-ficcion/"))
    itemlist.append( Item(channel=__channel__, action="alfabetico" , title="Comedia",url="http://sintonizzate.me/categoria/comedia/"))
    itemlist.append( Item(channel=__channel__, action="alfabetico" , title="Documental",url="http://sintonizzate.me/categoria/documental/"))
    itemlist.append( Item(channel=__channel__, action="alfabetico" , title="Drama",url="http://sintonizzate.me/categoria/drama/"))
    itemlist.append( Item(channel=__channel__, action="alfabetico" , title="Fantasía",url="http://sintonizzate.me/categoria/fantasia/"))
    itemlist.append( Item(channel=__channel__, action="alfabetico" , title="Infantil",url="http://sintonizzate.me/categoria/infantil/"))
    itemlist.append( Item(channel=__channel__, action="alfabetico" , title="Musical",url="http://sintonizzate.me/categoria/musical/"))
    itemlist.append( Item(channel=__channel__, action="alfabetico" , title="Romance",url="http://sintonizzate.me/categoria/romance/"))
    itemlist.append( Item(channel=__channel__, action="alfabetico" , title="Suspense",url="http://sintonizzate.me/categoria/suspense/"))
    itemlist.append( Item(channel=__channel__, action="alfabetico" , title="Terror",url="http://sintonizzate.me/categoria/terror/"))
    itemlist.append( Item(channel=__channel__, action="alfabetico" , title="Thriller",url="http://sintonizzate.me/categoria/thriller/"))

    return itemlist

def listalfabetico(item):
    logger.info("[sintonizzate.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="alfabetico" , title="0-9",url="http://sintonizzate.me/letra/09.html"))
    for letra in ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']:
        caracter = letra.lower()
        url = "http://sintonizzate.me/letra/" + caracter +".html"
        itemlist.append( Item(channel=__channel__, action="alfabetico" , title=letra,url=url,fanart="http://sintonizzate.me/Temas/default/img/bg.png"))

    return itemlist



# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test(url):
    try:
        data = scrapertools.cachePage(url)
        data = scrapertools.get_match(data,'<p id="content">(.*?)</p>')
        patron = 'File was deleted'
        matches = re.compile(patron,re.DOTALL).findall(data)
        scrapertools.printMatches(matches)
        ficha = "0"
        if len(matches) > 0:
            ficha = "1"
        return ficha
    except:
        return "0"