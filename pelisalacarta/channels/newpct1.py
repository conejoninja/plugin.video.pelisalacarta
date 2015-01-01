# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para newpct1
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
__title__ = "newpct1"
__channel__ = "newpct1"
__language__ = "ES"
__creationdate__ = "20141102"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[newpct1.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="submenu", title="Películas", url="http://www.newpct1.com/", extra="peliculas") )
    itemlist.append( Item(channel=__channel__, action="submenu", title="Series", url="http://www.newpct1.com/", extra="series") )
    itemlist.append( Item(channel=__channel__, action="search", title="Buscar") )

    return itemlist

def search(item,texto):
    logger.info("[newpct1.py] search")

    item.url = "http://www.newpct1.com/index.php?page=buscar&q=%s&ordenar=Nombre&inon=Ascendente" % texto

    return busqueda(item)

def busqueda(item):
    logger.info("[newpct1.py] busqueda")
    itemlist=[]

    data = re.sub(r'\n|\r|\t|\s{2}|<!--.*?-->|<i class="icon[^>]+"></i>',"",scrapertools.cache_page(item.url))
    data = unicode( data, "iso-8859-1" , errors="replace" ).encode("utf-8")

    patron = '<ul class="buscar-list">(.*?)</ul>'
    fichas = scrapertools.get_match(data,patron)

    #<li><a href="http://www.newpct1.com/descargar/x-men-primera-generacion/40669/" title="Descargar DVDScreener X-Men Primera Generacion "><img src="http://www.newpct1.com/pictures/f/minis/40669_x-men-primera-generacion--.jpg" alt="Descargar DVDScreener X-Men Primera Generacion "></a> <div class="info"><a href="http://www.newpct1.com/descargar/x-men-primera-generacion/40669/" title="Descargar DVDScreener X-Men Primera Generacion "><h2 style="padding:0;">X-Men Primera Generacion [DVD Screener][Spanish][2011]</h2> </a><span class="votadas">6.50</span><span>08-07-2011</span><span>1.9 GB</span><span class="color"> <a href="http://www.newpct1.com/descargar/x-men-primera-generacion/40669/" title="Descargar DVDScreener X-Men Primera Generacion "> Descargar</a> </div> </li>

    patron  = '<img src="([^"]+)".*?'
    patron += '<a href="([^"]+)".*?'
    patron += '<h2[^>]*>([^<]+)</h2> </a>'
    patron += '<span class="votadas">([^<]+)</span>'
    patron += '<span>([^<]+)</span>'
    patron += '<span>([^<]+)</span>'

    matches = re.compile(patron,re.DOTALL).findall(fichas)

    for scrapedthumbnail,scrapedurl,scrapedtitle,votos,fecha,peso in matches:
        url = scrapedurl
        title = scrapedtitle+"["+votos+"]["+fecha+"]["+peso+"]"
        thumbnail = scrapedthumbnail
        itemlist.append( Item(channel=__channel__, action="findvideos", title=title, url=url, thumbnail=thumbnail) )

    if "pagination" in data:
        patron = '<ul class="pagination">(.*?)</ul>'
        paginacion = scrapertools.get_match(data,patron)

        if "Next" in paginacion:
            url_next_page  = scrapertools.get_match(paginacion,'<a href="([^"]+)">Next</a>')
            itemlist.append( Item(channel=__channel__, action="busqueda" , title=">> Página siguiente" , url=url_next_page))

    return itemlist

def submenu(item):
    logger.info("[newpct1.py] submenu")
    itemlist=[]

    data = re.sub(r"\n|\r|\t|\s{2}|(<!--.*?-->)","",scrapertools.cache_page(item.url))
    data = unicode( data, "iso-8859-1" , errors="replace" ).encode("utf-8")

    patron = '<li><a href="http://www.newpct1.com/'+item.extra+'/">.*?<ul>(.*?)</ul>'
    data = scrapertools.get_match(data,patron)

    patron = '<a href="([^"]+)".*?>([^>]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        url = scrapedurl

        itemlist.append( Item(channel=__channel__, action="listado" ,title=title, url=url, extra="pelilist") )
        itemlist.append( Item(channel=__channel__, action="alfabeto" ,title=title+" [A-Z]", url=url, extra="pelilist") )
    
    return itemlist

def alfabeto(item):
    logger.info("[newpct1.py] alfabeto")
    itemlist = []

    data = re.sub(r"\n|\r|\t|\s{2}|(<!--.*?-->)","",scrapertools.cache_page(item.url))
    data = unicode( data, "iso-8859-1" , errors="replace" ).encode("utf-8")

    patron = '<ul class="alfabeto">(.*?)</ul>'
    data = scrapertools.get_match(data,patron)

    patron = '<a href="([^"]+)"[^>]+>([^>]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.upper()
        url = scrapedurl

        itemlist.append( Item(channel=__channel__, action="completo" ,title=title, url=url, extra=item.extra) )

    return itemlist

def listado(item):
    logger.info("[newpct1.py] listado")
    itemlist = []

    data = re.sub(r"\n|\r|\t|\s{2}|(<!--.*?-->)","",scrapertools.cache_page(item.url))
    data = unicode( data, "iso-8859-1" , errors="replace" ).encode("utf-8")

    patron = '<ul class="'+item.extra+'">(.*?)</ul>'
    fichas = scrapertools.get_match(data,patron)

    #<li><a href="http://www.newpct1.com/pelicula/x-men-dias-del-futuro-pasado/ts-screener/" title="Descargar XMen Dias Del Futuro gratis"><img src="http://www.newpct1.com/pictures/f/58066_x-men-dias-del-futuro--blurayrip-ac3-5.1.jpg" width="130" height="180" alt="Descargar XMen Dias Del Futuro gratis"><h2>XMen Dias Del Futuro </h2><span>BluRayRip AC3 5.1</span></a></li>

    patron  = '<a href="([^"]+)"[^>]+>'
    patron += '<img src="([^"]+)"[^>]+>'
    patron += '<h2[^>]*>([^<]+)</h2>'
    patron += '<span>([^<]*)</span>'

    matches = re.compile(patron,re.DOTALL).findall(fichas)

    for scrapedurl,scrapedthumbnail,scrapedtitle,calidad in matches:
        url = scrapedurl
        title = scrapedtitle+calidad
        thumbnail = scrapedthumbnail
        action = "findvideos"
        if "1.com/series" in url: action = "episodios"
        itemlist.append( Item(channel=__channel__, action=action, title=title, url=url, thumbnail=thumbnail) )

    if "pagination" in data:
        patron = '<ul class="pagination">(.*?)</ul>'
        paginacion = scrapertools.get_match(data,patron)

        if "Next" in paginacion:
            url_next_page  = scrapertools.get_match(paginacion,'<a href="([^"]+)">Next</a>')
            itemlist.append( Item(channel=__channel__, action="listado" , title=">> Página siguiente" , url=url_next_page, extra=item.extra))

    return itemlist

def episodios(item):
    logger.info("[newpct1.py] episodios")
    itemlist=[]

    data = re.sub(r'\n|\r|\t|\s{2}|<!--.*?-->|<i class="icon[^>]+"></i>',"",scrapertools.cache_page(item.url))
    data = unicode( data, "iso-8859-1" , errors="replace" ).encode("utf-8")

    patron = '<ul class="buscar-list">(.*?)</ul>'
    fichas = scrapertools.get_match(data,patron)

    #<li><a href="http://www.newpct1.com/serie/forever/capitulo-101/" title="Serie Forever 1x01"><img src="http://www.newpct1.com/pictures/c/minis/1880_forever.jpg" alt="Serie Forever 1x01"></a> <div class="info"> <a href="http://www.newpct1.com/serie/forever/capitulo-101/" title="Serie Forever 1x01"><h2 style="padding:0;">Serie <strong style="color:red;background:none;">Forever - Temporada 1 </strong> - Temporada<span style="color:red;background:none;">[ 1 ]</span>Capitulo<span style="color:red;background:none;">[ 01 ]</span><span style="color:red;background:none;padding:0px;">Espa�ol Castellano</span> Calidad <span style="color:red;background:none;">[ HDTV ]</span></h2></a> <span>27-10-2014</span> <span>450 MB</span> <span class="color"><ahref="http://www.newpct1.com/serie/forever/capitulo-101/" title="Serie Forever 1x01"> Descargar</a> </div></li>

    patron  = '<a href="([^"]+)" title="([^"]+)">'
    patron += '<img src="([^"]+)".*?'
    patron += '<span style=".*?0px;">([^<]+)</span>[^<]+'
    patron += '<span style=".*?none;">([^<]+)</span>.*?'
    patron += '<span>([^<]+)</span> '
    patron += '<span>([^<]+)</span>'

    matches = re.compile(patron,re.DOTALL).findall(fichas)

    for scrapedurl,scrapedtitle,scrapedthumbnail,idioma,calidad,fecha,peso in matches:
        url = scrapedurl
        title = scrapedtitle+" "+idioma+" "+calidad+"[ "+fecha+" ][ "+peso+" ]"
        thumbnail = scrapedthumbnail
        itemlist.append( Item(channel=__channel__, action="findvideos", title=title, url=url, thumbnail=thumbnail) )

    if "pagination" in data:
        patron = '<ul class="pagination">(.*?)</ul>'
        paginacion = scrapertools.get_match(data,patron)

        if "Next" in paginacion:
            url_next_page  = scrapertools.get_match(paginacion,'<a href="([^"]+)">Next</a>')
            itemlist.append( Item(channel=__channel__, action="episodios" , title=">> Página siguiente" , url=url_next_page))

    return itemlist

def findvideos(item):
    logger.info("[newpct1.py] findvideos")
    itemlist=[]

    ## Cualquiera de las tres opciones son válidas
    #item.url = item.url.replace("1.com/","1.com/ver-online/")
    #item.url = item.url.replace("1.com/","1.com/descarga-directa/")
    item.url = item.url.replace("1.com/","1.com/descarga-torrent/")

    # Descarga la página
    data = re.sub(r"\n|\r|\t|\s{2}|(<!--.*?-->)","",scrapertools.cache_page(item.url))
    data = unicode( data, "iso-8859-1" , errors="replace" ).encode("utf-8")

    title = scrapertools.find_single_match(data,"<h1><strong>([^<]+)</strong>[^<]+</h1>")
    title+= scrapertools.find_single_match(data,"<h1><strong>[^<]+</strong>([^<]+)</h1>")
    caratula = scrapertools.find_single_match(data,'<div class="entry-left">.*?src="([^"]+)"')

    #<a href="http://tumejorjuego.com/download/index.php?link=descargar-torrent/058310_yo-frankenstein-blurayrip-ac3-51.html" title="Descargar torrent de Yo Frankenstein " class="btn-torrent" target="_blank">Descarga tu Archivo torrent!</a>

    patron = '<a href="([^"]+)" title="[^"]+" class="btn-torrent" target="_blank">'

    # escraped torrent
    url = scrapertools.find_single_match(data,patron)
    if url!="":
        itemlist.append( Item(channel=__channel__, action="play", server="torrent", title=title+" [torrent]", fulltitle=title, url=url , thumbnail=caratula, plot=item.plot, folder=False) )

    # escraped ver vídeos, descargar vídeos un link, múltiples liks
    data = data.replace("'",'"')
    data = data.replace('javascript:;" onClick="popup("http://www.newpct1.com/pct1/library/include/ajax/get_modallinks.php?links=',"")
    data = data.replace("http://tumejorserie.com/descargar/url_encript.php?link=","")
    data = data.replace("$!","#!")

    patron_descargar = '<div id="tab2"[^>]+>.*?</ul>'
    patron_ver = '<div id="tab3"[^>]+>.*?</ul>'

    match_ver = scrapertools.find_single_match(data,patron_ver)
    match_descargar = scrapertools.find_single_match(data,patron_descargar)

    patron = '<div class="box1"><img src="([^"]+)".*?' # logo
    patron+= '<div class="box2">([^<]+)</div>'         # servidor
    patron+= '<div class="box3">([^<]+)</div>'         # idioma
    patron+= '<div class="box4">([^<]+)</div>'         # calidad
    patron+= '<div class="box5"><a href="([^"]+)".*?'  # enlace
    patron+= '<div class="box6">([^<]+)</div>'         # titulo

    enlaces_ver = re.compile(patron,re.DOTALL).findall(match_ver)
    enlaces_descargar = re.compile(patron,re.DOTALL).findall(match_descargar)

    for logo, servidor, idioma, calidad, enlace, titulo in enlaces_ver:
        servidor = servidor.replace("played","playedto")
        titulo = titulo+" ["+servidor+"]"
        itemlist.append( Item(channel=__channel__, action="play", server=servidor, title=titulo , fulltitle = item.title, url=enlace , thumbnail=logo , plot=item.plot , folder=False) )

    for logo, servidor, idioma, calidad, enlace, titulo in enlaces_descargar:
        servidor = servidor.replace("uploaded","uploadedto")
        partes = enlace.split(" ")
        p = 1
        for enlace in partes:
            parte_titulo = titulo+" (%s/%s)" % (p,len(partes)) + " ["+servidor+"]"
            p+= 1
            itemlist.append( Item(channel=__channel__, action="play", server=servidor, title=parte_titulo , fulltitle = item.title, url=enlace , thumbnail=logo , plot=item.plot , folder=False) )

    return itemlist

def completo(item):
    logger.info("[newpct1.py] completo")
    itemlist = []

    # Guarda el valor por si son etquitas para que lo vea 'listadofichas'
    item_extra = item.extra

    # Lee las entradas
    items_programas = listado(item)

    salir = False
    while not salir:

        # Saca la URL de la siguiente página
        ultimo_item = items_programas[ len(items_programas)-1 ]

        # Páginas intermedias
        if ultimo_item.action=="listado":
            # Quita el elemento de "Página siguiente" 
            ultimo_item = items_programas.pop()

            # Añade las entradas de la página a la lista completa
            itemlist.extend( items_programas )
    
            # Carga la sigiuente página
            ultimo_item.extra = item_extra
            items_programas = listado(ultimo_item)

        # Última página
        else:
            # Añade a la lista completa y sale
            itemlist.extend( items_programas )
            salir = True

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True
    
    # mainlist
    mainlist_items = mainlist(Item())
    submenu_items = submenu(mainlist_items[0])
    listado_items = listado(submenu_items[0])
    for listado_item in listado_items:
        play_items = findvideos(listado_item)
        
        if len(play_items)>0:
            return True

    return False