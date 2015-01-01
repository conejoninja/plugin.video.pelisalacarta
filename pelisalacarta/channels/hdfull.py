# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para hdfull
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "hdfull"
__category__ = "F,S,D"
__type__ = "generic"
__title__ = "HDFull"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.channels.hdfull mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="menupeliculas" , title="Películas" , url="http://hdfull.tv/", folder=True))
    itemlist.append( Item(channel=__channel__, action="menuseries"    , title="Series" , url="http://hdfull.tv/", folder=True))
    itemlist.append( Item(channel=__channel__, action="search"        , title="Buscar..."))
    return itemlist

def menupeliculas(item):
    logger.info("pelisalacarta.channels.hdfull menupeliculas")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Últimas películas" , url="http://hdfull.tv/peliculas", folder=True))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Últimas películas de estreno" , url="http://hdfull.tv/peliculas-estreno", folder=True))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Últimas películas actualizadas" , url="http://hdfull.tv/peliculas-actualizadas", folder=True))
    itemlist.append( Item(channel=__channel__, action="generos" , title="Últimas películas por género" , url="http://hdfull.tv/", folder=True))
    return itemlist

def menuseries(item):
    logger.info("pelisalacarta.channels.hdfull menuseries")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="novedades_episodios" , title="Últimos episodios emitidos" , url="http://hdfull.tv/ultimos-episodios", folder=True))
    itemlist.append( Item(channel=__channel__, action="novedades_episodios" , title="Últimos episodios estreno" , url="http://hdfull.tv/episodios-estreno", folder=True))
    itemlist.append( Item(channel=__channel__, action="novedades_episodios" , title="Últimos episodios actualizados" , url="http://hdfull.tv/episodios-actualizados", folder=True))
    itemlist.append( Item(channel=__channel__, action="series"    , title="Últimas series" , url="http://hdfull.tv/series", folder=True))
    itemlist.append( Item(channel=__channel__, action="series"    , title="Series más valoradas" , url="http://hdfull.tv/series/imdb_rating", folder=True))
    itemlist.append( Item(channel=__channel__, action="generos_series" , title="Últimas series por género" , url="http://hdfull.tv/", folder=True))
    return itemlist

def search(item,texto):
    logger.info("pelisalacarta.channels.hdfull search")
    if item.url=="":
        item.url="http://www.divxatope.com/buscar/descargas"
    item.extra = urllib.urlencode({'search':texto})

    try:
        return lista(item)
    # Se captura la excepci?n, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def peliculas(item):
    logger.info("pelisalacarta.channels.hdfull peliculas")
    itemlist = []

    '''
    <div class="item" style="text-align:center">
    <a href="http://hdfull.tv/pelicula/magic-in-the-moonlight" class="spec-border-ie" title="">
    <img class="img-preview spec-border"  src="http://hdfull.tv/templates/hdfull/timthumb.php?src=http://hdfull.tv/thumbs/movie_8378be0c7f5ef678fa082b5f8e04eac4.jpg&amp;w=130&amp;h=190&amp;zc=1" alt="Magia a la luz de la luna" title="Magia a la luz de la luna" style="width:130px;height:190px;background-color: #717171;"/>
    </a>
    </div>

    <div class="rating-pod">
    <div class="left">
    <img src="http://hdfull.tv/templates/hdfull/images/spa.png" style="margin-right: 1px;"/>
    <img src="http://hdfull.tv/templates/hdfull/images/lat.png" style="margin-right: 1px;"/>
    </div>
    '''

    patron  = '<div class="item"[^<]+'
    patron += '<a href="([^"]+)"[^<]+'
    patron += '<img.*?src="([^"]+)" alt="([^"]+)"[^<]+'
    patron += '</a[^<]+'
    patron += '</div[^<]+'
    patron += '<div class="rating-pod"[^<]+'
    patron += '<div class="left"(.*?)</div>'

    data = scrapertools.cachePage(item.url)
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedthumbnail,scrapedtitle,bloqueidiomas in matches:

        thumbnail = scrapertools.find_single_match(scrapedthumbnail,"timthumb.php.src=([^\&]+)&")
        textoidiomas = extrae_idiomas(bloqueidiomas)
        title = scrapedtitle.strip()+" ("+textoidiomas[:-1]+")"
        url = urlparse.urljoin(item.url,scrapedurl)
        plot = ""

        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=title , fulltitle = title, url=url , thumbnail=thumbnail , plot=plot , folder=True, viewmode="movie"))

    next_page_url = scrapertools.find_single_match(data,'<a href="([^"]+)">.raquo;</a> ')
    if next_page_url!="":
        itemlist.append( Item(channel=__channel__, action="peliculas", title=">> Página siguiente" , url=urlparse.urljoin(item.url,next_page_url) , folder=True) )

    return itemlist

def extrae_idiomas(bloqueidiomas):
    logger.info("idiomas="+bloqueidiomas)
    patronidiomas = '([a-z0-9]+).png"'
    idiomas = re.compile(patronidiomas,re.DOTALL).findall(bloqueidiomas)
    textoidiomas = ""
    for idioma in idiomas:
        textoidiomas = textoidiomas + idioma + "/"

    return textoidiomas


def series(item):
    logger.info("pelisalacarta.channels.hdfull series")
    itemlist = []

    '''
    <div class="item" style="text-align:center">
    <a href="http://hdfull.tv/serie/alarm-for-cobra-11" class="spec-border-ie" title="">
    <img class="img-preview spec-border show-thumbnail"  src="http://hdfull.tv/templates/hdfull/timthumb.php?src=http://hdfull.tv/thumbs/show_ed4ff7f4db4c0e6e575bdf7e18c2ede0.jpg&amp;w=130&amp;h=190&amp;zc=1" alt=" " />
    </a>
    </div>

    <div class="rating-pod">
    <div class="left">
    </div>


    <div class="right">
    <div class="rating">7<b class="dec">7</b></div>
    <img src="http://hdfull.tv/templates/hdfull/images/star.png" style="float:right;border:0px;margin-right: 5px;" />
    </div>
    </div>

    <h5 class="left">
    <div class="title-overflow"></div>
    <a class="link" href="http://hdfull.tv/serie/alarm-for-cobra-11" title="Alerta Cobra">
    Alerta Cobra
    </a>
    '''

    patron  = '<div class="item"[^<]+'
    patron += '<a href="([^"]+)"[^<]+'
    patron += '<img.*?src="([^"]+)".*?'
    patron += '<h5 class="left"[^<]+'
    patron += '<div class="title-overflow"></div[^<]+'
    patron += '<a[^>]+>([^<]+)</a'

    data = scrapertools.cachePage(item.url)
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:

        thumbnail = scrapertools.find_single_match(scrapedthumbnail,"timthumb.php.src=([^\&]+)&")
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        plot = ""

        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="episodios", title=title , fulltitle = title, url=url , thumbnail=thumbnail , plot=plot , folder=True, show=title, viewmode="movie"))

    next_page_url = scrapertools.find_single_match(data,'<a href="([^"]+)">.raquo;</a> ')
    if next_page_url!="":
        itemlist.append( Item(channel=__channel__, action="series", title=">> Página siguiente" , url=urlparse.urljoin(item.url,next_page_url) , folder=True) )

    return itemlist

def episodios(item):
    logger.info("pelisalacarta.channels.hdfull episodios")
    itemlist = []

    temporadas_items = temporadas(item)

    for temporada_item in temporadas_items:
        episodios_temporada_items = episodios_temporada(temporada_item)

        for episodio in episodios_temporada_items:
            itemlist.append(episodio)

    if (config.get_platform().startswith("xbmc") or config.get_platform().startswith("boxee")) and len(itemlist)>0:
        itemlist.append( Item(channel=item.channel, title="Añadir esta serie a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="episodios", show=item.show))
        itemlist.append( Item(channel=item.channel, title="Descargar todos los episodios de la serie", url=item.url, action="download_all_episodes", extra="episodios", show=item.show))

    return itemlist

def temporadas(item):
    logger.info("pelisalacarta.channels.hdfull temporadas")
    itemlist = []

    '''
    <div class="flickr item left home-thumb-item">
    <a href='http://hdfull.tv/serie/stargate-sg-1/temporada-5' rel="bookmark">
    <img class="tooltip" original-title="Temporada 5" alt="Temporada 5" src="http://hdfull.tv/templates/hdfull/timthumb.php?src=http://hdfull.tv/thumbs/season_527af04264f6516e9a324dd1d3ded7f8.jpg&amp;w=130&amp;h=190&amp;zc=1" />
    <h5>Temporada 5</h5>
    </a>
    </div>
    '''

    patron  = '<div class="flickr[^<]+'
    patron += "<a href='([^']+)'[^<]+"
    patron += '<img class="tooltip" original-title="([^"]+)" alt="[^"]+" src="([^"]+)"'

    data = scrapertools.cachePage(item.url)
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle,scrapedthumbnail in matches:

        thumbnail = scrapertools.find_single_match(scrapedthumbnail,"timthumb.php.src=([^\&]+)&")
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        plot = ""

        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="episodios_temporada", title=title , fulltitle = title, url=url , thumbnail=thumbnail , plot=plot , show=item.show, folder=True))

    return itemlist

def episodios_temporada(item):
    logger.info("pelisalacarta.channels.hdfull episodios_temporada")
    itemlist = []

    '''
    <div class="item">
    <a href="http://hdfull.tv/serie/forever-2014/temporada-1/episodio-11" class="spec-border-ie" title="">
    <img class="img-preview spec-border show-thumbnail-wide"  src="http://hdfull.tv/templates/hdfull/timthumb.php?src=http://hdfull.tv/thumbs/ethumb_tt3487382_1_11.jpg&amp;w=220&amp;h=124&amp;zc=1" alt="Temp 1. Ep 11" title="Temp 1. Ep 11" />
    </a>
    </div>
    <div class="rating-pod">
    <div class="left">
    <img src="http://hdfull.tv/templates/hdfull/images/eng.png" style="margin-right: 1px;"/>
    <img src="http://hdfull.tv/templates/hdfull/images/engsub.png" style="margin-right: 1px;"/>
    <img src="http://hdfull.tv/templates/hdfull/images/spa.png" style="margin-right: 1px;"/>
    <img src="http://hdfull.tv/templates/hdfull/images/sub.png" style="margin-right: 1px;"/>
    </div>
    <div class="right">
    <div class="rating">1<b class="sep">x</b>11</div>
    </div>
    </div>
    <h5 class="left">
    <div class="title-overflow"></div>
    <a class="link" href="http://hdfull.tv/serie/forever-2014/temporada-1/episodio-11" title="Skinny Dipper">Skinny Dipper</a>
    '''

    patron  = '<div class="item"[^<]+'
    patron += '<a href="([^"]+)"[^<]+'
    patron += '<img class="[^"]+"\s+src="([^"]+)"[^<]+'
    patron += '</a[^<]+'
    patron += '</div[^<]+'
    patron += '<div class="rating-pod"[^<]+'
    patron += '<div class="left"(.*?)</div[^<]+'
    patron += '<div class="right"[^<]+'
    patron += '<div class="rating">(.*?)</div[^<]+'
    patron += '</div[^<]+'
    patron += '</div[^<]+'
    patron += '<h5 class="left"[^<]+'
    patron += '<div class="title-overflow"></div[^<]+'
    patron += '<a[^>]+>([^<]+)</a>'

    data = scrapertools.cachePage(item.url)
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedthumbnail,bloqueidiomas,episodenumber,episodetitle in matches:

        thumbnail = scrapertools.find_single_match(scrapedthumbnail,"timthumb.php.src=([^\&]+)&")
        title = scrapertools.htmlclean(episodenumber).strip()+" "+episodetitle.strip()
        textoidiomas = extrae_idiomas(bloqueidiomas)
        title = title.strip()+" ("+textoidiomas[:-1]+")"
        url = urlparse.urljoin(item.url,scrapedurl)
        plot = ""

        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=title , fulltitle = title, url=url , thumbnail=thumbnail , plot=plot , show=item.show, folder=True))

    return itemlist

def novedades_episodios(item):
    logger.info("pelisalacarta.channels.hdfull novedades_episodios")
    itemlist = []

    '''
    <div class="item" style="text-align:center">
    <a href="http://hdfull.tv/pelicula/magic-in-the-moonlight" class="spec-border-ie" title="">
    <img class="img-preview spec-border"  src="http://hdfull.tv/templates/hdfull/timthumb.php?src=http://hdfull.tv/thumbs/movie_8378be0c7f5ef678fa082b5f8e04eac4.jpg&amp;w=130&amp;h=190&amp;zc=1" alt="Magia a la luz de la luna" title="Magia a la luz de la luna" style="width:130px;height:190px;background-color: #717171;"/>
    </a>
    </div>

    <div class="rating-pod">
    <div class="left">
    <img src="http://hdfull.tv/templates/hdfull/images/spa.png" style="margin-right: 1px;"/>
    <img src="http://hdfull.tv/templates/hdfull/images/lat.png" style="margin-right: 1px;"/>
    </div>
    '''
    '''
    <div class="item" style="text-align:center">
    <a href="http://hdfull.tv/serie/the-legend-of-korra/temporada-4/episodio-11" class="spec-border-ie" title="">
    <img class="img-preview spec-border show-thumbnail-wide"  src="http://hdfull.tv/templates/hdfull/timthumb.php?src=http://hdfull.tv/thumbs/ethumb_tt1695360_4_11.jpg&amp;w=220&amp;h=124&amp;zc=1" alt="" title="" />
    </a>
    </div>

    <div class="rating-pod">
    <div class="left">
    <img src="http://hdfull.tv/templates/hdfull/images/eng.png" style="margin-right: 1px;" class="flag-lang-eng"/>
    <img src="http://hdfull.tv/templates/hdfull/images/sub.png" style="margin-right: 1px;" class="flag-lang-espsub"/>
    </div>

    <div class="right">
    <div class="rating">4<b class="sep">x</b>11</div>
    </div>
    </div>

    <h5 class="left">
    <div class="title-overflow"></div>
    <a class="link" href="http://hdfull.tv/serie/the-legend-of-korra/temporada-4/episodio-11" title="The Legend of Korra">
    The Legend of Korra
    </a>
    </h5>
    <p class="left">Kuvira's Gambit</p>
    <div id="seen22893"></div>                      
    <div class="clear"></div>
    '''

    patron  = '<div class="item"[^<]+'
    patron += '<a href="([^"]+)"[^<]+'
    patron += '<img.*?src="([^"]+)"[^<]+'
    patron += '</a[^<]+'
    patron += '</div[^<]+'
    patron += '<div class="rating-pod"[^<]+'
    patron += '<div class="left"(.*?)</div[^<]+'
    patron += '<div class="right"[^<]+'
    patron += '<div class="rating">(.*?)</div[^<]+'
    patron += '</div[^<]+'
    patron += '</div[^<]+'
    patron += '<h5 class="left"[^<]+'
    patron += '<div class="title-overflow"></div[^<]+'
    patron += '<a[^>]+>([^<]+)</a[^<]+'
    patron += '</h5[^<]+'
    patron += '<p class="left">([^<]+)</p>'

    data = scrapertools.cachePage(item.url)
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedthumbnail,bloqueidiomas,episode_number,serie_title,episode_title in matches:

        thumbnail = scrapertools.find_single_match(scrapedthumbnail,"timthumb.php.src=([^\&]+)&")
        logger.info("idiomas="+bloqueidiomas)
        patronidiomas = '([a-z0-9]+).png"'
        idiomas = re.compile(patronidiomas,re.DOTALL).findall(bloqueidiomas)
        textoidiomas = ""
        for idioma in idiomas:
            textoidiomas = textoidiomas + idioma + "/"

        title = serie_title.strip()+" "+scrapertools.htmlclean(episode_number.strip())+" "+episode_title.strip()+" ("+textoidiomas[:-1]+")"
        url = urlparse.urljoin(item.url,scrapedurl)
        plot = ""

        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=title , fulltitle = title, url=url , thumbnail=thumbnail , plot=plot , folder=True))

    next_page_url = scrapertools.find_single_match(data,'<a href="([^"]+)">.raquo;</a> ')
    if next_page_url!="":
        itemlist.append( Item(channel=__channel__, action="findvideos", title=">> Página siguiente" , url=urlparse.urljoin(item.url,next_page_url) , folder=True) )

    return itemlist

def generos(item):
    logger.info("pelisalacarta.channels.hdfull generos")
    itemlist = []

    data = scrapertools.cachePage(item.url)
    data = scrapertools.find_single_match(data,'<li class="dropdown"><a href="http://hdfull.tv/peliculas"(.*?)</ul>')

    patron  = '<li><a href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="peliculas", title=title , url=url , folder=True) )

    return itemlist

def generos_series(item):
    logger.info("pelisalacarta.channels.hdfull generos_series")
    itemlist = []

    data = scrapertools.cachePage(item.url)
    data = scrapertools.find_single_match(data,'<li class="dropdown"><a href="http://hdfull.tv/series"(.*?)</ul>')

    patron  = '<li><a href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="series", title=title , url=url , folder=True) )

    return itemlist

def findvideos(item):
    logger.info("pelisalacarta.channels.hdfull findvideos")
    itemlist=[]

    # Descarga la pagina
    item.url = item.url.replace("divxatope.com/descargar/","divxatope.com/ver-online/")

    '''
    <div class="embed-selector" style="background-image: url('http://hdfull.tv/templates/hdfull/images/lat.png')" onclick="changeEmbed(29124,countdown);">

    <h5 class="left">
    <span>
    <b class="key"> Idioma: </b> Audio Latino
    </span>
    <span>
    <b class="key">Servidor:</b><b class="provider" style="background-image: url(http://www.google.com/s2/favicons?domain=powvideo.net)">Powvideo</b>
    </span>
    <span>
    <b class="key">Calidad: </b> HD720
    </span>
    </h5>

    <ul class="filter action-buttons">
    <li class="current right" style="float:right">
    <a href="javascript:void(0);" onclick="reportMovie(29124)" class="danger" title="Reportar"><i class="icon-warning-sign icon-white"></i>&nbsp;</a>
    &nbsp;<a href="http://powvideo.net/q87l85llcifz" target="_blank"><i class="icon-share-alt icon-white"></i> Enlace externo</a>
    </li>
    </ul>
    </div>
    '''
    # Descarga la pagina
    data = scrapertools.cachePage(item.url)

    patron  = '<div class="embed-selector"[^<]+'
    patron += '<h5 class="left"[^<]+'
    patron += '<span[^<]+<b class="key">\s*Idioma.\s*</b>([^<]+)</span[^<]+'
    patron += '<span[^<]+<b class="key">\s*Servidor.\s*</b><b[^>]+>([^<]+)</b[^<]+</span[^<]+'
    patron += '<span[^<]+<b class="key">\s*Calidad.\s*</b>([^<]+)</span[^<]+</h5[^<]+'
    patron += '<ul class="filter action-buttons">(.*?)</ul>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for idioma,servername,calidad,bloqueurl in matches:
        title = "Mirror en "+servername.strip()+" ("+calidad.strip()+")"+" ("+idioma.strip()+")"
        title = scrapertools.htmlclean(title)
        url = bloqueurl
        thumbnail = item.thumbnail
        plot = item.title+"\n\n"+scrapertools.find_single_match(data,'<meta property="og:description" content="([^"]+)"')
        plot = scrapertools.htmlclean(plot)
        fanart = scrapertools.find_single_match(data,'<div style="background-image.url. ([^\s]+)')
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append(Item(channel=__channel__, action="play", title=title , fulltitle = title, url=url , thumbnail=thumbnail , plot=plot , fanart=fanart, folder=True, viewmode="movie_with_plot"))

    return itemlist

def play(item):
    logger.info("pelisalacarta.channels.hdfull play")

    itemlist = servertools.find_video_items(data=item.url)

    for videoitem in itemlist:
        videoitem.title = "Enlace encontrado en "+videoitem.server+" ("+scrapertools.get_filename_from_url(videoitem.url)+")"
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist    
