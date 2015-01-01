# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para buscar en tu.tv
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

__channel__ = "tutvsite"
__category__ = "G"
__type__ = "generic"
__title__ = "tu.tv"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[tutvsite.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="search"     , title="Buscar"                           , url="http://www.tu.tv/buscar/?str=%s"))

    return itemlist

# Al llamarse "search" la función, el launcher pide un texto a buscar y lo añade como parámetro
def search(item,texto):
    logger.info("[tutvsite.py] search")

    try:
        # La URL puede venir vacía, por ejemplo desde el buscador global
        if item.url=="":
            item.url="http://www.tu.tv/buscar/?str=%s"
    
        # Reemplaza el texto en la cadena de búsqueda
        item.url = item.url % texto

        # Devuelve los resultados
        return list(item)
    
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def list(item):
    logger.info("[tutvsite.py] list")
    itemlist=[]

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas (carpetas)
    '''
    <div class="fila clearfix">
    <div class="datos">
    De: <a href="/usuario/avatarenlinea"><img src="http://uimg.tu.tv/imagenes/minis/usuarios/DEFECTO.gif" width="16" height="16" align="absmiddle"/></a> 		<a href="/usuario/avatarenlinea">avatarenlinea</a><br />
    Categoría: <a href="/categorias/arte-y-animaciones/">Arte y animaciones</a><br />    
    Añadido: 7/5/2007<br />
    <strong>385 votos</strong><br />
    Reproducciones: 238.215 
    </div>
    <div class="limagen">
    <div class="paralistacontent">
    <a href="/videos/avatar-1x19-el-asedio-del-norte-i" ><img src="http://vimg.tu.tv/imagenes/videos/a/v/avatar-1x19-el-asedio-del-norte-i_imagen1.jpg" alt="Avatar - 1x19 - El Asedio del norte I "  width="122" height="92" align="left" class="vid" /></a>
    '''
    patronvideos  = '<div class="fila clearfix">.*?<div class="paralistacontent">(.*?)</div>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    data = ""
    for match in matches:
        data = data + match

    patronvideos  = '<a href="([^"]+)" ><img src="([^"]+)" alt="([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        scrapedtitle = match[2]
        scrapedtitle = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = urlparse.urljoin(item.url,match[1])
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist
