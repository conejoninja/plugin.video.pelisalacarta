# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "bricocine"
__category__ = "F"
__type__ = "generic"
__title__ = "bricocine"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.bricocine mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Pelis-MicroHD"      , action="peliculas", url="http://www.bricocine.com/c/hd-microhd/", thumbnail="http://bancofotos.net/photos/20141014141328265114709.jpg", fanart="http://bancofotos.net/photos/20141014141330155135952.jpg"))
    itemlist.append( Item(channel=__channel__, title="Pelis Bluray-Rip" , action="peliculas", url="http://www.bricocine.com/c/bluray-rip/",  thumbnail="http://bancofotos.net/photos/20141014141328602166199.jpg", fanart="http://bancofotos.net/photos/20141014141330252951873.jpg"))
    itemlist.append( Item(channel=__channel__, title="Pelis DvdRip" , action="peliculas", url="http://www.bricocine.com/c/dvdrip/", thumbnail="http://bancofotos.net/photos/20141014141330844118036.jpg", fanart="http://bancofotos.net/photos/20141014141330679189128.jpg"))
    itemlist.append( Item(channel=__channel__, title="Pelis 3D" , action="peliculas", url="http://www.bricocine.com/c/3d/", thumbnail="http://www.eias3d.com/wp-content/uploads/2011/07/3d2_5.png", fanart="http://bancofotos.net/photos/20141015141335228330727.jpg"))
    itemlist.append( Item(channel=__channel__, title="Series"         , action="peliculas", url="http://www.bricocine.com/c/series", thumbnail="http://img0.mxstatic.com/wallpapers/bc795faa71ba7c490fcf3961f3b803bf_large.jpeg", fanart="http://bancofotos.net/photos/20141015141340620193665.jpg"))
    itemlist.append( Item(channel=__channel__, title="Buscar"         , action="search", url="", thumbnail="http://fc04.deviantart.net/fs70/i/2012/285/3/2/poltergeist___tv_wallpaper_by_elclon-d5hmmlp.png", fanart="http://bancofotos.net/photos/20141015141335277420974.jpg"))
    

    return itemlist


def search(item,texto):
    logger.info("pelisalacarta.bricocine search")
    texto = texto.replace(" ","+")
    item.url = "http://www.bricocine.com/index.php/?s=%s" % (texto)
    try:
        return peliculas(item)
    # Se captura la excepciÛn, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []
    



def peliculas(item):
    logger.info("pelisalacarta.bricocine peliculas")
    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    '''
   <div class="post-10888 post type-post status-publish format-standard hentry category-the-leftovers tag-ciencia-ficcion tag-drama tag-fantasia tag-misterio"><div class="entry"> <a href="http://www.bricocine.com/10888/leftovers-temporada-1/"> <img src="http://www.bricocine.com/wp-content/plugins/wp_movies/files/thumb_185_the_leftovers_.jpg" alt="The Leftovers " /> </a></div><div class="entry-meta"><div class="clearfix"><div itemprop="aggregateRating" itemscope itemtype="http://schema.org/AggregateRating" class="rating"  title="Puntos IMDB: 7.4"><div class="rating-stars imdb-rating"><div class="stars" style="width:74%"></div></div><div itemprop="ratingValue" class="rating-number"> 7.4</div></div><div itemprop="aggregateRating" itemscope itemtype="http://schema.org/AggregateRating" class="rating"  title="Puntos Bricocine: 6.2"><div class="rating-stars brico-rating"><div class="stars" style="width:62%"></div></div><div itemprop="ratingValue" class="rating-number"> 6.2</div></div> <span class="vcard author none"> Publicado por <a class="fn" href="" rel="author" target="_blank"></a> </span> <span class="date updated none">2014-10-07T23:36:17+00:00</span></div></div><h2 class="title2 entry-title"> <a href="http://www.bricocine.com/10888/leftovers-temporada-1/"> The Leftovers  &#8211; Temporada 1 </a></h2></div> </article> <article class="hentry item-entry"><div class="post-10088 post type-post status-publish format-standard hentry category-the-last-ship tag-accion tag-ciencia-ficcion tag-drama tag-the tag-thriller"><div class="entry"> <a href="http://www.bricocine.com/10088/last-ship-temporada-1/"> <img src="http://www.bricocine.com/wp-content/plugins/wp_movies/files/thumb_185_the_last_ship_.jpg" alt="The Last Ship " /> </a></div><div class="entry-meta"><div class="clearfix"><div itemprop="aggregateRating" itemscope itemtype="http://schema.org/AggregateRating" class="rating"  title="Puntos IMDB: 7.4"><div class="rating-stars imdb-rating"><div class="stars" style="width:74%"></div></div><div itemprop="ratingValue" class="rating-number"> 7.4</div></div><div itemprop="aggregateRating" itemscope itemtype="http://schema.org/AggregateRating" class="rating"  title="Puntos Bricocine: 7.0"><div class="rating-stars brico-rating"><div class="stars" style="width:70%"></div></div><div itemprop="ratingValue" class="rating-number"> 7.0</div></div> <span class="vcard author none"> Publicado por <a class="fn" href="" rel="author" target="_blank"></a> </span> <span class="date updated none">2014-10-07T23:32:25+00:00</span></div></div><h2 class="title2 entry-title"> <a href="http://www.bricocine.com/10088/last-ship-temporada-1/"> The Last Ship &#8211; Temporada 1 </a></h2></div> </article> <article class="hentry item-entry">

    '''

    patron = '<div class="entry"> '
    patron += '<a href="([^"]+)"> '
    patron += '<img src="([^"]+)".*?'
    patron += 'alt="([^"]+)".*?'
    patron += 'class="rating-number">([^<]+)</div></div>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl, scrapedthumbnail, scrapedtitle, scrapedcreatedate in matches:
        scrapedtitle = scrapedtitle + "(Puntuación:" + scrapedcreatedate + ")"
       
        itemlist.append( Item(channel=__channel__, title=scrapedtitle, url=scrapedurl, action="findvideos", thumbnail=scrapedthumbnail, folder=True) )
    
    ## Paginación
    #<span class='current'>1</span><a href='http://www.bricocine.com/c/hd-microhd/page/2/'
    
    # Si falla no muestra ">> Página siguiente"
    try:
        next_page = scrapertools.get_match(data,"<span class='current'>\d+</span><a href='([^']+)'")
        itemlist.append( Item(channel=__channel__, title=">> Página siguiente", url=next_page, action="peliculas", folder=True) )
    except: pass
    
    return itemlist

def findvideos(item):
    logger.info("pelisalacarta.bricocine findvideos")
    
    itemlist = []
    data = scrapertools.cache_page(item.url)
    
    #id_torrent = scrapertools.get_match(item.url,"(\d+)-")
    patron = '<span class="title">([^"]+)</span>.*?'
    patron += 'id="([^"]+)" href="([^"]+)"'
    
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    import base64
    for title_torrent, scrapedtitle, url_torrent in matches:
        title_torrent = "["+title_torrent.replace("file","torrent")+"]"
        url_torrent = base64.decodestring(url_torrent.split('&u=')[1][::-1])
        itemlist.append( Item(channel=__channel__, title = title_torrent , action="play", url=url_torrent, server="torrent", folder=False) )
    
    return itemlist

