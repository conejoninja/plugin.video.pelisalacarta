# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para somosmovies
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "somosmovies"
__category__ = "F,S,D,A"
__type__ = "generic"
__title__ = "Somosmovies"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[somosmovies.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Películas"    , action="menupeliculas"))
    itemlist.append( Item(channel=__channel__, title="Series"       , action="peliculas", url="http://www.somosmovies.com/search/label/Series?updated-max=&max-results=18"))
    
    return itemlist

def menupeliculas(item):
    logger.info("[somosmovies.py] menupeliculas")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Novedades"    , action="peliculas", url="http://www.somosmovies.com"))
    itemlist.append( Item(channel=__channel__, title="Género"       , action="generos", url="http://www.somosmovies.com/"))
    itemlist.append( Item(channel=__channel__, title="Año"          , action="anyos", url="http://www.somosmovies.com/"))
    itemlist.append( Item(channel=__channel__, title="País"         , action="paises", url="http://www.somosmovies.com/"))
    
    return itemlist

def peliculas(item):
    logger.info("[somosmovies.py] peliculas")
    itemlist=[]

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    logger.info("data="+data)

    # Extrae las entradas
    '''
    <article CLASS='post crp'>
    <header><h3 CLASS='post-title entry-title item_name'>
    <a href='http://www.somosmovies.com/2013/11/elysium-2013_24.html' title='Elysium (2013)'>Elysium (2013)</a>
    </h3>
    </header>
    <section CLASS='post-body entry-content clearfix'>
    <a href='http://www.somosmovies.com/2013/11/elysium-2013_24.html' title='Elysium (2013)'><center>
    <img border="0" src="http://1.bp.blogspot.com/-J15zDm0KXVA/UoOmwu563kI/AAAAAAAALqw/zBww3WoCyEw/s1600/Poster.Elysium.2013.jpg" style="display: block; height: 400px; width: 312px;">
    </center>
    </a>
    <div CLASS='es-LAT'></div>
    <div CLASS='pie-post'>
    <div style='float:left'>
    <div class='fb-like' data-href='http://www.somosmovies.com/2013/11/elysium-2013_24.html' data-layout='button_count' data-send='false' data-show-faces='false' data-width='120'></div>
    </div>
    </div>
    <div STYLE='clear: both;'></div>
    </section>
    </article>
    '''
    patron = "<article(.*?)</article>"
    matches = re.compile(patron,re.DOTALL).findall(data)

    for match in matches:
        logger.info("match="+match)
        scrapedtitle = scrapertools.get_match(match,"<a href='[^']+' title='([^']+)'")
        scrapedurl = urlparse.urljoin(item.url, scrapertools.get_match(match,"<a href='([^']+)' title='[^']+'") )
        scrapedplot = ""
        try:
            scrapedthumbnail = urlparse.urljoin(item.url, scrapertools.get_match(match,'<img border="0" src="([^"]+)"') )
        except:
            scrapedthumbnail = ""
        try:
            idioma = scrapertools.get_match(match,"</center[^<]+</a[^<]+<div CLASS='([^']+)'></div>")
            scrapedtitle = scrapedtitle + " ("+idioma.upper()+")"
        except:
            pass
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade a XBMC
        itemlist.append( Item(channel=__channel__, action="enlaces", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # Extrae el paginador
    #<a CLASS='blog-pager-older-link' href='http://www.somosmovies.com/search?updated-max=2012-08-22T23:10:00-05:00&amp;max-results=16' id='Blog1_blog-pager-older-link' title='Siguiente Película'>Siguiente &#187;</a>
    patronvideos  = "<a CLASS='blog-pager-older-link' href='([^']+)' id='Blog1_blog-pager-older-link' title='Siguiente"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        #http://www.somosmovies.com/search/label/Peliculas?updated-max=2010-12-20T08%3A27%3A00-06%3A00&max-results=12
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        scrapedurl = scrapedurl.replace("%3A",":")
        itemlist.append( Item(channel=__channel__, action="peliculas", title=">> Página siguiente" , url=scrapedurl , folder=True) )

    return itemlist

def anyos(item):
    logger.info("[animeflv.py] anyos")

    itemlist = []

    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<h2>Año</h2>(.*?)</ul')
    patron = "<a href='([^']+)'>([^<]+)</a>"
    matches = re.compile(patron,re.DOTALL).findall(data)    

    for scrapedurl,scrapedtitle in matches:
        title = scrapertools.entityunescape(scrapedtitle)
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="peliculas" , title=title , url=url, thumbnail=thumbnail, plot=plot))
    return itemlist

def generos(item):
    logger.info("[animeflv.py] generos")

    itemlist = []

    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<h2>Género</h2>(.*?)</ul')
    patron = "<a href='([^']+)'>([^<]+)</a>"
    matches = re.compile(patron,re.DOTALL).findall(data)    

    for scrapedurl,scrapedtitle in matches:
        title = scrapertools.entityunescape(scrapedtitle)
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="peliculas" , title=title , url=url, thumbnail=thumbnail, plot=plot))
    return itemlist

def paises(item):
    logger.info("[animeflv.py] paises")

    itemlist = []

    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<h2>País</h2>(.*?)</ul')
    patron = "<a href='([^']+)'>([^<]+)</a>"
    matches = re.compile(patron,re.DOTALL).findall(data)    

    for scrapedurl,scrapedtitle in matches:
        title = scrapertools.entityunescape(scrapedtitle)
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="peliculas" , title=title , url=url, thumbnail=thumbnail, plot=plot))
    return itemlist

def enlaces(item):
    logger.info("[somosmovies.py] enlaces")
    itemlist = []
    
    data = scrapertools.cachePage(item.url)
    
    '''
    <fieldset id="enlaces">
    <legend>Enlaces</legend><br />
    <div class="clearfix uno">
    <div class="dos"><b> Episodio 1</b>: <small>30 Days Without an Accident</small></div><div class="tres"><a href="http://bit.ly/1aIiGdq" target="_blank">MEGA</a> <b class="sep">|</b> <a href="http://bit.ly/GY8PWg" target="_blank">1Fichier</a> <b class="sep">|</b> <a href="http://bit.ly/15CGs8G" target="_blank">4Shared</a> <b class="sep">|</b> <a href="http://bit.ly/17RTYZl" target="_blank">180upload</a> <b class="sep">|</b> <a href="http://goo.gl/ognvK7" target="_blank">TurboBit</a></div>
    </div>
    <div class="clearfix uno">
    <div class="dos"><b> Episodio 2</b>: Infected</div><div class="tres"><a href="http://bit.ly/1fyubIg" target="_blank">MEGA</a> <b class="sep">|</b> <a href="http://bit.ly/1a9voBA" target="_blank">1Fichier</a> <b class="sep">|</b> <a href="http://bit.ly/19pmMpo" target="_blank">4Shared</a> <b class="sep">|</b> <a href="http://bit.ly/1aYd0be" target="_blank">180upload</a> <b class="sep">|</b> <a href="http://goo.gl/rI9OL7" target="_blank">TurboBit</a></div>
    </div>
    <div class="clearfix uno">
    <div class="dos"><b> Episodio 3</b>: Isolation</div><div class="tres"><a href="http://bit.ly/1fyucfd" target="_blank">MEGA</a> <b class="sep">|</b> <a href="http://bit.ly/17UzXLX" target="_blank">1Fichier</a> <b class="sep">|</b> <a href="http://bit.ly/17tmo9Y" target="_blank">4Shared</a> <b class="sep">|</b> <a href="http://bit.ly/1eqtMEL" target="_blank">180upload</a> <b class="sep">|</b> <a href="http://goo.gl/2f3Jj5" target="_blank">TurboBit</a></div>
    </div>
    <div class="clearfix uno">
    <div class="dos"><b> Episodio 4</b>: Indifference</div><div class="tres"><a href="http://bit.ly/1aPKmwf" target="_blank">MEGA</a> <b class="sep">|</b> <a href="http://bit.ly/185vLcB" target="_blank">1Fichier</a> <b class="sep">|</b> <a href="http://bit.ly/1iJ5mGm" target="_blank">4Shared</a> <b class="sep">|</b> <a href="http://bit.ly/1hadtPR" target="_blank">180upload</a> <b class="sep">|</b> <a href="http://goo.gl/lYoQoo" target="_blank">TurboBit</a></div>
    </div>
    <div class="clearfix uno">
    <div class="dos"><b> Episodio 5</b>: Internment</div><div class="tres"><a href="http://bit.ly/1aYcERL" target="_blank">MEGA</a> <b class="sep">|</b> <a href="http://bit.ly/HSRa1F" target="_blank">1Fichier</a> <b class="sep">|</b> <a href="http://bit.ly/1dilJZe" target="_blank">4Shared</a> <b class="sep">|</b> <a href="http://bit.ly/1iG6sWi" target="_blank">180upload</a> <b class="sep">|</b> <a href="http://goo.gl/0tHIKr" target="_blank">TurboBit</a></div>
    </div>
    <div class="clearfix uno">
    <div class="dos"><b> Episodio 6</b>: Live Bait</div><div class="tres"><a href="http://bit.ly/17Z1EUf" target="_blank">MEGA</a> <b class="sep">|</b> <a href="http://bit.ly/1ddc0Ym" target="_blank">1Fichier</a> <b class="sep">|</b> <a href="http://bit.ly/I0GBKK" target="_blank">4Shared</a> <b class="sep">|</b> <a href="http://bit.ly/1jx50TF" target="_blank">180upload</a> <b class="sep">|</b> <a href="http://goo.gl/mgXyof" target="_blank">TurboBit</a></div>
    </div>
    <div class="clearfix uno">
    <div class="dos"><b> Episodio 7</b>: Dead Weight</div><div class="tres"><a href="http://bit.ly/17UwbIi" target="_blank">MEGA</a> <b class="sep">|</b> <a href="http://bit.ly/17NZj1D" target="_blank">1Fichier</a> <b class="sep">|</b> <a href="http://bit.ly/1aTE4vw" target="_blank">4Shared</a> <b class="sep">|</b> <a href="http://bit.ly/IhQa8C" target="_blank">180upload</a> <b class="sep">|</b> <a href="http://goo.gl/ZiSH47" target="_blank">TurboBit</a> <b style="font-style:italic;color:red;">Nuevo!</b></div>
    </div>
    <div class="clearfix uno">
    <div class="dos"><b> Episodio 8</b>: Too Far Gone</div><div class="tres"><i style="font-style:italic">Disponible el 02 de Diciembre.</i></div>
    </div>
    </fieldset>
    '''
    '''
    <fieldset id="enlaces">
    <h5 class='h5'>Season 1</h5>
    <div class="clearfix uno">
    <div class="dos"><b> Capítulo 1</b>: Yesterday's Jam</div><div class="tres"><a href="http://bit.ly/14OorEU" target="_blank">1Fichier</a> <b class="sep">|</b> <a href="http://bit.ly/Z2uWNc" target="_blank">PutLocker</a> <b class="sep">|</b> <a href="http://bit.ly/11nIqHi" target="_blank">SockShare</a> <b class="sep">|</b> <a href="http://bit.ly/XYo0jN" target="_blank">FreakShare</a></div>
    <div class="dos"><b> Capítulo 2</b>: Calamity Jen</div><div class="tres"><a href="http://bit.ly/XecqUq" target="_blank">1Fichier</a> <b class="sep">|</b> <a href="http://bit.ly/10algD1" target="_blank">PutLocker</a> <b class="sep">|</b> <a href="http://bit.ly/YTsGe4" target="_blank">SockShare</a> <b class="sep">|</b> <a href="http://bit.ly/16xaKYZ" target="_blank">FreakShare</a></div>
    <div class="dos"><b> Capítulo 3</b>: Fifty-Fifty</div><div class="tres"><a href="http://bit.ly/12i5mq8" target="_blank">1Fichier</a> <b class="sep">|</b> <a href="http://bit.ly/10aljyA" target="_blank">PutLocker</a> <b class="sep">|</b> <a href="http://bit.ly/12gnyo1" target="_blank">SockShare</a> <b class="sep">|</b> <a href="http://bit.ly/10xM8LC" target="_blank">FreakShare</a></div>
    <div class="dos"><b> Capítulo 4</b>: The Red Door</div><div class="tres"><a href="http://bit.ly/10al5Yg" target="_blank">1Fichier</a> <b class="sep">|</b> <a href="http://bit.ly/10wyHMz" target="_blank">PutLocker</a> <b class="sep">|</b> <a href="http://bit.ly/10rHP5P" target="_blank">SockShare</a> <b class="sep">|</b> <a href="http://bit.ly/10xM9PW" target="_blank">FreakShare</a></div>
    <div class="dos"><b> Capítulo 5</b>: The Haunting of Bill Crouse</div><div class="tres"><a href="http://bit.ly/10wyAjT" target="_blank">1Fichier</a> <b class="sep">|</b> <a href="http://bit.ly/XecCmO" target="_blank">PutLocker</a> <b class="sep">|</b> <a href="http://bit.ly/XYoPt0" target="_blank">SockShare</a> <b class="sep">|</b> <a href="http://bit.ly/14OpPXW" target="_blank">FreakShare</a></div>
    <div class="dos"><b> Capítulo 6</b>: Aunt Irma Visits</div><div class="tres"><a href="http://bit.ly/17dCeEj" target="_blank">1Fichier</a> <b class="sep">|</b> <a href="http://bit.ly/12i5JRM" target="_blank">PutLocker</a> <b class="sep">|</b> <a href="http://bit.ly/10amVIA" target="_blank">SockShare</a> <b class="sep">|</b> <a href="http://bit.ly/17dDdUU" target="_blank">FreakShare</a></div>
    </div>
    <h5 class='h5'>Season 2</h5>
    <div class="clearfix uno">
    <div class="dos"><b> Capítulo 1</b>: The Work Outing</div><div class="tres"><a href="http://bit.ly/XOrCcl" target="_blank">1Fichier</a> <b class="sep">|</b> <a href="http://bit.ly/10wDjCe" target="_blank">PutLocker</a> <b class="sep">|</b> <a href="http://bit.ly/12ibnDi" target="_blank">SockShare</a> <b class="sep">|</b> <a href="http://bit.ly/17dEXgU" target="_blank">FreakShare</a></div>
    <div class="dos"><b> Capítulo 2</b>: Return of the Golden Child</div><div class="tres"><a href="http://bit.ly/16p6Tvh" target="_blank">1Fichier</a> <b class="sep">|</b> <a href="http://bit.ly/13SeTJq" target="_blank">PutLocker</a> <b class="sep">|</b> <a href="http://bit.ly/10zwtuf" target="_blank">SockShare</a> <b class="sep">|</b> <a href="http://bit.ly/XqnsZ7" target="_blank">FreakShare</a></div>
    '''
    '''
    <fieldset id="enlaces">
    <legend>Enlaces</legend><br />
    <div class="clearfix uno">
    <div class="dos">
    <b>AVI</b> <small>480p</small></div>
    <div class="tres">
    <a href="http://bit.ly/1dQbvlS" target="_blank">1Fichier</a> <b class="sep">|</b> <a href="http://bit.ly/Nd96Hh" target="_blank">MEGA</a> <b class="sep">|</b> <a href="http://bit.ly/1d3a534" target="_blank">4Shared</a> <b class="sep">|</b> <a href="http://goo.gl/TOipXB" target="_blank">TurboBit</a> <b class="sep">|</b> <a href="http://bit.ly/1oUWtPP" target="_blank">FreakShare</a>
    </div>
    </div>
    <div class="clearfix uno">
    <div class="dos">
    <b>MP4</b> <small>1080p</small></div>
    <div class="tres">
    <a href="http://bit.ly/1c40BEG" target="_blank">1Fichier</a> <b class="sep">|</b> <a href="http://bit.ly/OcZDki" target="_blank">MEGA</a> <b class="sep">|</b> <a href="http://bit.ly/1gjElZY" target="_blank">4Shared</a> <b class="sep">|</b> <a href="http://goo.gl/fc43B2" target="_blank">TurboBit</a> <b class="sep">|</b> <a href="http://bit.ly/1e9GxAq" target="_blank">FreakShare</a>
    </div>
    </div>
    </fieldset>
    '''
    # Se queda con la caja de enlaces
    data = scrapertools.get_match(data,'<fieldset id="enlaces"[^<]+<legend>Enlaces</legend>(.*?)</fieldset>')
    patron = '<div class="dos"[^<]+<b>([^<]+)</b>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for title in matches:
        itemlist.append( Item(channel=__channel__, action="findvideos" , title="Enlaces "+title.strip() , url=item.url, extra=title, thumbnail=item.thumbnail, plot=item.plot, folder=True))

    return itemlist

def findvideos(item):
    logger.info("[somosmovies.py] findvideos")
    itemlist = []
    
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'<fieldset id="enlaces"[^<]+<legend>Enlaces</legend>(.*?)</fieldset>')
    logger.info("[somosmovies.py] data="+data)

    '''
    <div class="dos"><b> Capítulo 10</b>: Mhysa <b style="color:red;font-style:italic">Nuevo!</b></div><div class="tres"><a href="http://bit.ly/19Zh0LG" target="_blank">MEGA</a> <b class="sep">|</b> <a href="http://bit.ly/11vxcOd" target="_blank">1Fichier</a> <b class="sep">|</b> <a href="http://bit.ly/14tpgBb" target="_blank">PutLocker</a> <b class="sep">|</b> <a href="http://bit.ly/17DxZUJ" target="_blank">SockShare</a> <b class="sep">|</b> <a href="http://bit.ly/16YykSk" target="_blank">FreakShare</a> <b class="sep">|</b> <a href="http://bit.ly/13vOcFA" target="_blank">Ver Online &#187;</a></div>
    '''
    data = scrapertools.get_match(data,'<div class="dos"[^<]+<b>'+item.extra+'</b>.*?<div(.*?)</div')
    logger.info("[somosmovies.py] data="+data)
    patron = '<a href="([^"]+)"[^>]+>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for url,title in matches:
        itemlist.append( Item(channel=__channel__, action="play" , title=title , url=url, thumbnail=item.thumbnail, plot=item.plot, server="", folder=False))

    return itemlist

def play(item):
    logger.info("[somosmovies.py] play(item.url="+item.url+")")
    itemlist=[]

    if "bit.ly" in item.url:
        logger.info("Acortador bit.ly")
        location = scrapertools.get_header_from_response(item.url,header_to_get="location")
        logger.info("[somosmovies.py] location="+location)
        item.url = location
        return play(item)

    if "goo.gl" in item.url:
        logger.info("Acortador goo.gl")
        location = scrapertools.get_header_from_response(item.url,header_to_get="location")
        item.url = location
        return play(item)

    #adf.ly
    elif "j.gs" in item.url:
        logger.info("Acortador j.gs (adfly)")
        from servers import adfly
        location = adfly.get_long_url(item.url)
        item.url = location
        return play(item)

    else:
        from servers import servertools
        itemlist=servertools.find_video_items(data=item.url)
        for videoitem in itemlist:
            videoitem.channel=__channel__
            videoitem.folder=False

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True

    # mainlist
    mainlist_items = mainlist(Item())
    peliculas_items = listado(mainlist_items[0])
    if len(peliculas_items)==0:
        print "No salen películas"
        return False
    
    for pelicula_item in peliculas_items:
        mirrors = findvideos(pelicula_item)
        if len(mirrors)>0:
            return True

    print "No hay ningún vídeo en la sección de películas"
    return False