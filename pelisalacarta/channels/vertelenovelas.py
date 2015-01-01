# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para vertelenovelas
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "vertelenovelas"
__category__ = "S"
__type__ = "generic"
__title__ = "Ver Telenovelas"
__language__ = "ES"
__creationdate__ = "20121015"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[vertelenovelas.py] mainlist")
    
    itemlist = []

    itemlist.append( Item(channel=__channel__, action="novedades_episodios" , title="Últimos capítulos agregados"    , url="http://vertelenovelas.net/"))
    itemlist.append( Item(channel=__channel__, action="emision"             , title="Lista de telenovelas en emisión", url="http://vertelenovelas.net/"))
    itemlist.append( Item(channel=__channel__, action="todas"               , title="Lista completa"                 , url="http://vertelenovelas.net/"))
    itemlist.append( Item(channel=__channel__, action="letras"              , title="Lista alfabética"               , url="http://vertelenovelas.net/"))

    return itemlist

def novedades_episodios(item):
    logger.info("[vertelenovelas.py] novedades_episodios")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    patron  = '<div class="premiere"[^<]+'
    patron += '<div class="new"></div[^<]+'
    patron += '<a href="([^"]+)"[^<]+'
    patron += '<img class="cart feel" src="([^"]+)" alt="([^"]+)"[^<]+'
    patron += '<span class="tit_ep tit">([^<]+)</span>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedthumbnail,serie,scrapedtitle in matches:
        title = serie+" "+scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = scrapedthumbnail
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=title , url=url , thumbnail=thumbnail, viewmode="movie", folder=True) )

    return itemlist

def letras(item):
    logger.info("[vertelenovelas.py] letras")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'<div id="abc">(.*?)</ul>')

    #<li class="abc"><a href="letra/a/" title="Telenovelas que comienzan con la Letra A">A</a></li>
    patron  = '<li[^<]+<a href="(letra[^"]+)[^>]+>([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"]")
        itemlist.append( Item(channel=__channel__, action="series", title=title , url=url , folder=True) )
    
    return itemlist

def episodios(item):
    logger.info("[vertelenovelas.py] episodios")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    try:
        data = scrapertools.get_match(data,'<div id="scroollllable"(.*?)</ul>')
        patron  = '<li><a href="([^"]+)"><i class="fx icon-play"></i>([^<]+)</a>'
    except:
        patron  = '<li><a href="([^"]+)">([^<]+)</a>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        title = scrapertools.htmlclean(scrapedtitle)
        plot = ""
        thumbnail = ""
        url = urlparse.urljoin(item.url,scrapedurl)

        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=title , url=url , thumbnail=thumbnail , plot=plot , folder=True) )
    
    return itemlist

def findvideos(item):
    logger.info("[vertelenovelas.py] findvideos")
    data = scrapertools.cache_page(item.url)
    itemlist=[]

    #<embed type="application/x-shockwave-flash" src="http://vertelenovelas.net/player.swf" width="680" height="430" id="mpl" name="mpl" quality="high" allowscriptaccess="always" allowfullscreen="true" wmode="transparent" flashvars="&file=http://content1.catalog.video.msn.com/e2/ds/4eeea8b3-6228-492b-a2be-e8b920cf4d4e.flv&backcolor=fd4bc5&frontcolor=fc9dde&lightcolor=ffffff&controlbar=over&volume=100&autostart=false&image=">
    #<embed type="application/x-shockwave-flash" src="http://vertelenovelas.net/player.swf" width="680" height="430" id="mpl" name="mpl" quality="high" allowscriptaccess="always" allowfullscreen="true" wmode="transparent" flashvars="&file=http://content1.catalog.video.msn.com/e2/ds/4eeea8b3-6228-492b-a2be-e8b920cf4d4e.flv&backcolor=fd4bc5&frontcolor=fc9dde&lightcolor=ffffff&controlbar=over&volume=100&autostart=false&image="></embed></d
    patron = '<embed type="application/x-shockwave-flash" src="http://vertelenovelas.net/player.swf".*?file=([^\&]+)&'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for match in matches:
        itemlist.append( Item(channel=__channel__, action="play", server="directo", title=item.title , url=match , thumbnail=item.thumbnail , plot=item.plot , folder=False) )

    #<embed width="680" height="450" flashvars="file=mp4:p/459791/sp/45979100/serveFlavor/flavorId/0_0pacv7kr/forceproxy/true&amp;image=&amp;skin=&amp;abouttext=&amp;dock=false&amp;streamer=rtmp://rtmpakmi.kaltura.com/ondemand/&amp;
    patron = '<embed width="[^"]+" height="[^"]+" flashvars="file=([^\&]+)&.*?streamer=(rtmp[^\&]+)&'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for final,principio in matches:
        itemlist.append( Item(channel=__channel__, action="play", server="directo", title=item.title , url=principio+final , thumbnail=item.thumbnail , plot=item.plot , folder=False) )

    #file=mp4:/c/g1MjYyYjpCnH8dRolOZ2G7u1KsleMuDS/DOcJ-FxaFrRg4gtDIwOjkzOjBrO8N_l0&streamer=rtmp://cp96275.edgefcs.net/ondemand&
    patron = 'file=([^\&]+)&streamer=(rtmp[^\&]+)&'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for final,principio in matches:
        itemlist.append( Item(channel=__channel__, action="play", server="directo", title=item.title , url=principio+"/"+final , thumbnail=item.thumbnail , plot=item.plot , folder=False) )


    from servers import servertools
    itemlist.extend(servertools.find_video_items(data=data))
    for videoitem in itemlist:
        videoitem.channel=__channel__
        videoitem.action="play"
        videoitem.folder=False
        videoitem.title = "["+videoitem.server+"]"

    return itemlist

def todas(item):
    logger.info("[vertelenovelas.py] todas")
    itemlist=[]

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'<ul class="ntop">(.*?)</ul>')
    patron  = '<li[^<]+<a href="([^"]+)[^>]+>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"]")
        itemlist.append( Item(channel=__channel__, action="episodios", title=title , url=url , folder=True) )
    
    return itemlist

def emision(item):
    logger.info("[vertelenovelas.py] emision")
    itemlist=[]

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    data = scrapertools.get_match(data,'<ul class="nemi">(.*?)</ul>')
    patron  = '<li[^<]+<a href="([^"]+)[^>]+>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"]")
        itemlist.append( Item(channel=__channel__, action="episodios", title=title , url=url , folder=True) )
    
    return itemlist

def series(item):
    logger.info("[vertelenovelas.py] series")
    itemlist=[]

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    patron  = '<div class="novels"[^<]+'
    patron += '<div[^<]+</div[^<]+'
    patron += '<a href="([^"]+)"><img class="[^"]+" src="([^"]+)"[^<]+'
    patron += '<span class="tit_no tit ellipsis">([^<]+)</span'
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"]")
        itemlist.append( Item(channel=__channel__, action="episodios", title=title , url=url , thumbnail=thumbnail, folder=True) )
    
    return itemlist
