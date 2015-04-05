# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para peliculasmx
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "peliculasmx"
__category__ = "F"
__type__ = "generic"
__title__ = "peliculasmx"
__language__ = "ES"
__creationdate__ = "20130528"

DEBUG = config.get_setting("debug")
    
def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.channels.peliculasmx mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Últimas añadidas", action="peliculas" , url="http://www.peliculasmx.net/" , extra="http://www.peliculasmx.net/"))
    itemlist.append( Item(channel=__channel__, title="Últimas por género" , action="generos" , url="http://www.peliculasmx.net/"))
    itemlist.append( Item(channel=__channel__, title="Últimas por letra" , action="letras" , url="http://www.peliculasmx.net/"))
    itemlist.append( Item(channel=__channel__, title="Buscar..." , action="search" , url="http://www.peliculasmx.net/"))
    return itemlist

def generos(item):
    logger.info("pelisalacarta.channels.peliculasmx generos")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
               
    patron = '>.*?<li><a title="(.*?)" href="(.*?)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if (DEBUG): scrapertools.printMatches(matches)
                                          
    for match in matches:
        scrapedurl = urlparse.urljoin("",match[1])
        scrapedurl = scrapedurl.replace(".html","/page/0.html")
        extra = scrapedurl.replace ("/page/0.html","/page/")
        scrapedtitle = match[0]
        #scrapedtitle = scrapedtitle.replace("","")
        scrapedthumbnail = ""
        scrapedplot = ""
        logger.info(scrapedtitle)
                
        if scrapedtitle=="Eroticas +18":        
            if config.get_setting("enableadultmode") == "true":
                itemlist.append( Item(channel=__channel__, action="peliculas", title="Eroticas +18" , url="http://www.myhotamateurvideos.com" , thumbnail=scrapedthumbnail , plot=scrapedplot , extra="" , folder=True) )
        else:
            if scrapedtitle <> "" and len(scrapedtitle) < 20 and scrapedtitle <> "Iniciar Sesion":
                 itemlist.append( Item(channel=__channel__, action="peliculas", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=extra, folder=True) )

    itemlist = sorted(itemlist, key=lambda Item: Item.title)    
    return itemlist
    
    
def letras(item):
    logger.info("pelisalacarta.channels.peliculasmx letras")

    extra = item.url
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="0-9", url="http://www.peliculasmx.net/letra/09.html", extra="http://www.peliculasmx.net/letra/09.html"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="A"  , url="http://www.peliculasmx.net/letra/a.html", extra="http://www.peliculasmx.net/letra/a.html"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="B"  , url="http://www.peliculasmx.net/letra/b.html", extra="http://www.peliculasmx.net/letra/b.html"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="C"  , url="http://www.peliculasmx.net/letra/c.html", extra="http://www.peliculasmx.net/letra/c.html"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="D"  , url="http://www.peliculasmx.net/letra/d.html", extra="http://www.peliculasmx.net/letra/d.html"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="E"  , url="http://www.peliculasmx.net/letra/e.html", extra="http://www.peliculasmx.net/letra/e.html"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="F"  , url="http://www.peliculasmx.net/letra/f.html", extra="http://www.peliculasmx.net/letra/f.html"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="G"  , url="http://www.peliculasmx.net/letra/g.html", extra="http://www.peliculasmx.net/letra/g.html"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="H"  , url="http://www.peliculasmx.net/letra/h.html", extra="http://www.peliculasmx.net/letra/h.html"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="I"  , url="http://www.peliculasmx.net/letra/i.html", extra="http://www.peliculasmx.net/letra/i.html"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="J"  , url="http://www.peliculasmx.net/letra/j.html", extra="http://www.peliculasmx.net/letra/j.html"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="K"  , url="http://www.peliculasmx.net/letra/k.html", extra="http://www.peliculasmx.net/letra/k.html"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="L"  , url="http://www.peliculasmx.net/letra/l.html", extra="http://www.peliculasmx.net/letra/l.html"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="M"  , url="http://www.peliculasmx.net/letra/m.html", extra="http://www.peliculasmx.net/letra/m.html"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="N"  , url="http://www.peliculasmx.net/letra/n.html", extra="http://www.peliculasmx.net/letra/n.html"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="O"  , url="http://www.peliculasmx.net/letra/o.html", extra="http://www.peliculasmx.net/letra/o.html"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="P"  , url="http://www.peliculasmx.net/letra/p.html", extra="http://www.peliculasmx.net/letra/p.html"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Q"  , url="http://www.peliculasmx.net/letra/q.html", extra="http://www.peliculasmx.net/letra/q.html"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="R"  , url="http://www.peliculasmx.net/letra/r.html", extra="http://www.peliculasmx.net/letra/r.html"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="S"  , url="http://www.peliculasmx.net/letra/s.html", extra="http://www.peliculasmx.net/letra/s.html"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="T"  , url="http://www.peliculasmx.net/letra/t.html", extra="http://www.peliculasmx.net/letra/t.html"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="U"  , url="http://www.peliculasmx.net/letra/u.html", extra="http://www.peliculasmx.net/letra/u.html"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="V"  , url="http://www.peliculasmx.net/letra/v.html", extra="http://www.peliculasmx.net/letra/v.html"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="W"  , url="http://www.peliculasmx.net/letra/w.html", extra="http://www.peliculasmx.net/letra/w.html"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="X"  , url="http://www.peliculasmx.net/letra/x.html", extra="http://www.peliculasmx.net/letra/x.html"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Y"  , url="http://www.peliculasmx.net/letra/y.html", extra="http://www.peliculasmx.net/letra/y.html"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Z"  , url="http://www.peliculasmx.net/letra/z.html", extra="http://www.peliculasmx.net/letra/z.html"))

    return itemlist


def peliculas(item):
    logger.info("pelisalacarta.channels.peliculasmx peliculas")
    extra = item.extra
    itemlist = []
    
      
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    
    patron = '<h2 class="titpeli.*?<a href="([^"]+)" title="([^"]+)".*?peli_img_img">.*?<img src="([^"]+)".*?<strong>Idioma</strong>:.*?/>([^"]+)</div>.*?<strong>Calidad</strong>: ([^"]+)</div>'
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    if (DEBUG): scrapertools.printMatches(matches)
    for match in matches:
        scrapedurl = match[0] #urlparse.urljoin("",match[0])
        scrapedtitle = match[1] + ' ['+ match[4] +']'
        scrapedtitle = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")
        scrapedthumbnail = match[2]
        #scrapedplot = match[0]
        #itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , fulltitle=scrapedtitle, url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle, fulltitle=scrapedtitle, url=scrapedurl , thumbnail=scrapedthumbnail , folder=True) )

    #if extra<>"":
        # Extrae la marca de siguiente página
    #patron = 'page=(.*?)"><span><b>'
    patron  = '<span><b>(.*?)</b></span>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #if DEBUG: scrapertools.printMatches(matches)
    for match in matches:
    #if len(matches)>0:
     nu = int(match[0]) + 1
     scrapedurl = extra + "?page=" + str(nu)
     scrapedtitle = "!Pagina Siguiente ->"
     scrapedthumbnail = ""
     scrapedplot = ""
     itemlist.append( Item(channel=__channel__, action="peliculas", title=scrapedtitle , fulltitle=scrapedtitle, url=scrapedurl , thumbnail=scrapedthumbnail , extra=extra , folder=True) )
    
    
    return itemlist

def findvideos(item):
    logger.info("pelisalacarta.channels.peliculasmx videos")
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    title = item.title
    scrapedthumbnail = item.thumbnail
    itemlist = []
    patron = '<li><a href="#ms.*?">([^"]+)</a></li>.*?<iframe src="(.*?)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #itemlist.append( Item(channel=__channel__, action="play", title=title , fulltitle=item.fulltitle, url=item.url , thumbnail=scrapedthumbnail , folder=False) )

    if (DEBUG): scrapertools.printMatches(matches)
    for match in matches:
        url = match[1]
        title = "SERVIDOR: " + match[0]
        itemlist.append( Item(channel=__channel__, action="play", title=title , fulltitle=item.fulltitle, url=url , thumbnail=scrapedthumbnail , folder=False) )

    return itemlist

def play(item):
    logger.info("pelisalacarta.channels.peliculasmx play")
    itemlist=[]


    from servers import servertools
    itemlist = servertools.find_video_items(data=item.url)
    for videoitem in itemlist:
        videoitem.channel=__channel__
        videoitem.action="play"
        videoitem.folder=False

    return itemlist	
    #data2 = scrapertools.cache_page(item.url)
    #data2 = data2.replace("http://www.peliculasaudiolatino.com/show/mv.php?url=","http://www.megavideo.com/?v=")
    #data2 = data2.replace("http://www.peliculasaudiolatino.com/show/videobb.php?url=","http://www.videobb.com/watch_video.php?v=")
    #data2 = data2.replace("http://www.peliculasaudiolatino.com/show/vidbux.php?url=","http://www.vidbux.com/")
    #data2 = data2.replace("http://www.peliculasaudiolatino.com/show/vidxden.php?url=","http://www.vidxden.com/")
    #data2 = data2.replace("http://www.peliculasaudiolatino.com/show/videozer.php?url=","http://www.videozer.com/video/")
    #data2 = data2.replace("http://www.peliculasaudiolatino.com/v/pl/play.php?url=","http://www.putlocker.com/embed/")
    #data2 = data2.replace("http://www.peliculasaudiolatino.com/v/mv/play.php?url=","http://www.modovideo.com/frame.php?v=")
    #data2 = data2.replace("http://www.peliculasaudiolatino.com/v/ss/play.php?url=","http://www.sockshare.com/embed/")
    #data2 = data2.replace("http://www.peliculasaudiolatino.com/v/vb/play.php?url=","http://vidbull.com/")
    #data2 = data2.replace("http://www.peliculasaudiolatino.com/show/sockshare.php?url=","http://www.sockshare.com/embed/")
    #data2 = data2.replace("http://www.peliculasaudiolatino.com/show/moevide.php?url=","http://moevideo.net/?page=video&uid=")
    #data2 = data2.replace("http://www.peliculasaudiolatino.com/show/novamov.php?url=","http://www.novamov.com/video/")
    #data2 = data2.replace("http://www.peliculasaudiolatino.com/show/movshare.php?url=","http://www.movshare.net/video/")
    #data2 = data2.replace("http://www.peliculasaudiolatino.com/show/divxstage.php?url=","http://www.divxstage.net/video/")
    #listavideos = servertools.findvideos(data2)
    
	#for video in listavideos:
    #    invalid = video[1]
    #    invalid = invalid[0:8]
    #    if invalid!= "FN3WE43K" and invalid!="9CC3F8&e":
    #        scrapedtitle = item.title+video[0]
    #        videourl = item.url
    #        server = video[2]
    #        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+videourl+"]")
    #logger.info("url=" + item.url)
	
            # Añade al listado de XBMC
            #itemlist.append( Item(channel=__channel__, action="play", title=scrapedtitle , fulltitle=item.fulltitle, url=videourl , server=server , folder=False) )
#    itemlist.append( Item(channel=__channel__, action="play" , title=item.title , url=item.url, thumbnail="", plot="", server=item.url))
	
    
 #   return itemlist

def search(item,texto):
    logger.info("pelisalacarta.channels.peliculasmx search")
    itemlist = []

    texto = texto.replace(" ","+")
    try:
        # Series
        item.url="http://www.peliculasmx.net/buscar/?q=%s"
        item.url = item.url % texto
        item.extra = ""
        itemlist.extend(peliculas(item))
        itemlist = sorted(itemlist, key=lambda Item: Item.title) 
        
        return itemlist
        
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []
    
    '''url = "http://www.peliculasaudiolatino.com/series-anime"
    data = scrapertools.cachePage(url)

    # Extrae las entradas de todas series
    patronvideos  = '<li>[^<]+'
    patronvideos += '<a.+?href="([\D]+)([\d]+)">[^<]+'
    patronvideos += '.*?/>(.*?)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        scrapedtitle = match[2].strip()

        # Realiza la busqueda
        if scrapedtitle.lower()==texto.lower() or texto.lower() in scrapedtitle.lower():
            logger.info(scrapedtitle)
            scrapedurl = urlparse.urljoin(url,(match[0]+match[1]))
            scrapedthumbnail = urlparse.urljoin("http://www.peliculasaudiolatino.com/images/series/",(match[1]+".png"))
            scrapedplot = ""

            # Añade al listado
            itemlist.append( Item(channel=__channel__, action="listacapitulos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist'''


# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    
    mainlist_items = mainlist(Item())
    novedades_items = peliculas(mainlist_items[0])

    for novedades_item in novedades_items:
        mirrors = findvideos( item=novedades_item )
        if len(mirrors)>0:
            return True

    return False
