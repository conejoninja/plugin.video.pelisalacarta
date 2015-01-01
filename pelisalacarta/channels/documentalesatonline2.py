# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para documentalesatonline2
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys

from core import scrapertools
from core import config
from core import logger
from core.item import Item
from servers import servertools

import xml.dom.minidom

__channel__ = "documentalesatonline2"
__category__ = "D"
__type__ = "generic"
__title__ = "La Guarida de bizzente"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[documentalesatonline2.py] mainlist")
    itemlist=[]

    itemlist.append( Item(channel=__channel__, title="Novedades"  , action="novedades" , url="http://www.bizzentte.com/"))
    itemlist.append( Item(channel=__channel__, title="Categorías" , action="categorias" , url="http://www.bizzentte.com/"))
    itemlist.append( Item(channel=__channel__, title="Buscar"     , action="search"))

    return itemlist

def search(item):
    buscador.listar_busquedas(item)

def searchresults(params,tecleado,category):
    logger.info("[documentalesatonline2.py] search")

    buscador.salvar_busquedas(params,tecleado,category)
    tecleado = tecleado.replace(" ", "+")
    searchUrl = "http://documentalesatonline.loquenosecuenta.com/search/"+tecleado+"?feed=rss2&paged=1"
    novedades(params,searchUrl,category)

def categorias(item):
    logger.info("[documentalesatonline2.py] novedades")
    itemlist=[]

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    #logger.info(data)

    # Extrae las entradas (carpetas)
    #<li class="jcl_category" style="display:none;" >
    #<a href="http://www.bizzentte.com/categoria/categorias-en-general-para-todo/arte-y-cultura/" >Arte y Cultura (80)</a>
    #<a class="jcl_link" href="#jcl" title="Ver Sub-Categor&iacute;as">
    #<span class="jcl_symbol" style="padding-left:5px">(+)</span></a>
    #<ul>
    #<li class="jcl_category" style="display:none;" ><a href="http://www.bizzentte.com/categoria/categorias-en-general-para-todo/arte-y-cultura/fotografia/" >Fotografia (2)</a></li><li class="jcl_category" style="display:none;" ><a href="http://www.bizzentte.com/categoria/categorias-en-general-para-todo/arte-y-cultura/grafiti/" >Grafiti (2)</a></li>
    patronvideos  = '<li class="jcl_category"[^>]+><a href="([^"]+)"[^>]*>([^<]+)</a></li>'
    # '\" url nombre cantidad_entradas
    matches = re.compile(patronvideos).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        #xbmctools.addnewfolder( __channel__ , "novedades" , category , match[1] , match[0] + "feed?paged=1" , "" , "")
        itemlist.append( Item(channel=__channel__, action="novedades", title=match[1] , url=match[0] , folder=True) )

    return itemlist

def novedades(item):
    logger.info("[documentalesatonline2.py] novedades")
    itemlist=[]

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    
    # Entradas
    '''
    <h2 id="post-5250"><a href="http://www.bizzentte.com/2011/08/chips-implantes-de-futuro-2009-documental-c-odisea-rfid-espanol/" rel="bookmark">Chips: Implantes de futuro.2009 (Documental C.Odisea) (RFID) (Español)</a></h2>
    <div class="main">
    <p>En este interesante documental, seguimos a Mark Stepanek mientras delibera si debe o no obtener una identificación por radiofrecuencia (RFID), es decir, implantarse un microchip, semejante al que pueda llevar una mascota, en su propia mano..</p>
    <ul class="readmore">
    <li>&raquo;
    <a href="http://www.bizzentte.com/2011/08/chips-implantes-de-futuro-2009-documental-c-odisea-rfid-espanol/#comments">Comentarios</a>
    <a href="http://www.bizzentte.com/2011/08/chips-implantes-de-futuro-2009-documental-c-odisea-rfid-espanol/#comments" title="Comentarios en Chips: Implantes de futuro.2009 (Documental C.Odisea) (RFID) (Español)">(3)</a>						</li>
    </ul>
    </div>
    '''
    '''
    <div class="entry">
    <div class="latest">
    <h2 id="post-6553"><a href="http://www.bizzentte.com/2013/02/equipo-de-investigacion-lasexta-todos-los-capitulos-de-la-4%c2%aa-temporada-espanol/" rel="bookmark">Equipo de Investigación (laSexta) (Todos los capítulos de la 4ª Temporada) (Español)</a></h2>
    <div class="main">
    <a href="http://www.bizzentte.com/2013/02/equipo-de-investigacion-lasexta-todos-los-capitulos-de-la-4%c2%aa-temporada-espanol/" title="Equipo de Investigación (laSexta) (Todos los capítulos de la 4ª Temporada) (Español)"><img src="http://www.bizzentte.com/wp-content/uploads/2013/01/Equipo-de-investigacion-4x00-Portada.jpg" alt="Equipo de Investigación (laSexta) (Todos los capítulos de la 4ª Temporada) (Español)" class="listimg" /></a>
    <p>Os dejo toda la 4ª temporada en HDTV..</p>
    <ul class="readmore">
    <li>&raquo;
    <a href="http://www.bizzentte.com/2013/02/equipo-de-investigacion-lasexta-todos-los-capitulos-de-la-4%c2%aa-temporada-espanol/#comments">Comentarios</a>
    <a href="http://www.bizzentte.com/2013/02/equipo-de-investigacion-lasexta-todos-los-capitulos-de-la-4%c2%aa-temporada-espanol/#respond" title="Comentarios en Equipo de Investigación (laSexta) (Todos los capítulos de la 4ª Temporada) (Español)">(0)</a>                     </li>
    </ul>
    </div>
    '''
    patron  = '<h2 id="post-[^"]+"><a href="([^"]+)"[^>]+>([^<]+)</a></h2>[^<]+'
    patron += '<div class="main">.*?'
    patron += '<p>([^<]+)</p>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = ""
        scrapedplot = match[2]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # Página siguiente
    patron  = '<a href="([^"]+)" >P..gina siguiente \&raquo\;</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        itemlist.append( Item(channel=__channel__, action="novedades", title="!Página siguiente" , url=urlparse.urljoin(item.url,match) , folder=True) )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    peliculas_items = novedades(mainlist_items[0])
    bien = False
    for pelicula_item in peliculas_items:
        mirrors = servertools.find_video_items( item=pelicula_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien