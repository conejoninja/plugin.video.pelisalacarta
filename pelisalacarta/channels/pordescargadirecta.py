# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal Descarregadirecta Carles Carmona
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

CHANNELNAME = "pordescargadirecta"
DEBUG = True

def isGeneric():
    return True


def mainlist(item):
    logger.info("[pordescargadirecta.py] mainlist")
    itemlist=[]

    itemlist.append( Item(channel=CHANNELNAME , action="subforos"   , title="Peliculas Online"      , url="http://pordescargadirecta.com/peliculas-online-f270/"))
    itemlist.append( Item(channel=CHANNELNAME , action="subforos"   , title="Series Online"         , url="http://pordescargadirecta.com/series-online-f227/"))
    itemlist.append( Item(channel=CHANNELNAME , action="posts"   , title="Documentales y Televisión Online"         , url="http://pordescargadirecta.com/documentales-y-television-online-f399/"))
    itemlist.append( Item(channel=CHANNELNAME , action="posts"   , title="Anime"         , url="http://pordescargadirecta.com/anime-online-f400/"))
   
    return itemlist


def subforos(item):
    logger.info("[descarregadirecta.py] Subforos")

    url = item.url
                
    data = scrapertools.cachePage(url)

    # Extrae las entradas (carpetas)
   
    patron = '<h2 class="forumtitle"><a href="(.*?)">(.*?)</a></h2>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    logger.info("hay %d matches" % len(matches))
    

    itemlist = []
    for match in matches:
        
        # Atributos
        scrapedurl = match[0]
        scrapedtitle =match[1]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
            # A�ade al listado de XBMC
        itemlist.append( Item(channel=item.channel , action="posts"   , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot ))
    
    return itemlist

def posts(item):
    logger.info("[pordescargadirecta.py] Posts")

    url = item.url
                
    data = scrapertools.cachePage(url)

    # Extrae las entradas (carpetas)
    

    patron = '<div class=".*? nonsticky">(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    logger.info("hay %d matches" % len(matches))
    #scrapertools.printMatches(matches)
    

    itemlist = []
    for match in matches:
        data2 = match
        #<a class="title" href="(.*?)" id=".*?">(.*?)</a>
        patron  = '<a class="title.*?" href="(.*?)" id=".*?">(.*?)</a>'
        matches2 = re.compile(patron,re.DOTALL).findall(data2)
        logger.info("hay %d matches2" % len(matches2))
        #scrapertools.printMatches(matches2)
        for match2 in matches2:
            scrapedtitle = match2[1]
            scrapedurl = match2[0]
            scrapedthumbnail = ""
            scrapedplot = ""
            
            itemlist.append( Item(channel=item.channel , action="detail"  , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot , fanart=scrapedthumbnail ))
    
    #Extrae la marca de siguiente p�gina
    #<span class='current'>1</span><a href='http://delatv.com/page/2' class='page'>2</a>
    patronvideos  = '<a rel="next" href="(.*?)" title=".*?">' #"</span><a href='(http://www.cine-adicto.com/page/[^']+)'"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    scrapedtitle = "Pagina Siguiente"
    scrapedurl = matches[0]#matches[0]
    scrapedthumbnail = ""
    scrapedplot = ""
    itemlist.append( Item(channel=item.channel , action="posts"  , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot ))

    return itemlist

def detail(item):
    logger.info("[Descarregadirecta.py] detail")

    title = item.title
    thumbnail = item.thumbnail
    plot = item.plot
    scrapedurl = ""
    url = item.url

    itemlist = []

    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    
    # Usa findvideos    
    listavideos = servertools.findvideos(data)
    
    itemlist = []
    
    for video in listavideos:
        server = video[2]
        scrapedtitle = item.title + " [" + server + "]"
        scrapedurl = video[1]
        
        itemlist.append( Item(channel=CHANNELNAME, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=item.thumbnail, plot=item.plot, server=server, folder=False))



    return itemlist
