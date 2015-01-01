# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para robinfilm
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "robinfilm"
__category__ = "F"
__type__ = "generic"
__title__ = "Robinfilm (IT)"
__language__ = "IT"
__creationdate__ = "20110516"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[robinfilm.py] mainlist")
    item.url = "http://robinfilm-new.blogspot.com.es/"
    return novedades(item)

def novedades(item):
    logger.info("[robinfilm.py] novedades")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    '''
    <div class='post-outer'>
    <li class='box' id='post'>
    <div class='postim' id='post'>
    <div class='btitle'>
    <h2>
    <a href='http://robinfilm-new.blogspot.com.es/2012/03/magnifica-presenza.html'>Magnifica Presenza</a>
    </h2>
    </div>
    <span class='inwriter'>RobinFilm 2</span>
    <a href='http://robinfilm-new.blogspot.com.es/2012/03/magnifica-presenza.html'>
    <script type='text/javascript'>
    //<![CDATA[
    function bp_thumbnail_resize(image_url,post_title)
    {
    var image_size=150;
    var show_default_thumbnail=true;
    var default_thumbnail="http://2.bp.blogspot.com/-HwP_JBU2mro/Tzw3VVlf6JI/AAAAAAAAAMM/zb6zvyD8b1M/s000/default.png";
    if(show_default_thumbnail == true && image_url == "") image_url= default_thumbnail;
    image_tag='<img src="'+image_url.replace('/s72-c/','/s'+image_size+'-c/')+'" class="bookcover" alt="'+post_title+'"/>';
    if(image_url!="") return image_tag; else return "";
    }
    //]]>
    </script>
    <script type='text/javascript'>
    document.write(bp_thumbnail_resize("http://3.bp.blogspot.com/-yXd3CBvCPzQ/T2-FSlJrqCI/AAAAAAAAABE/pzqPTyY51kA/s72-c/Magnifica+presenza+streaming.jpg","Magnifica Presenza"));
    </script>
    </a>
    </div>
    </li>
    </div>
    '''
    patronvideos  = "<div class='post-outer'>[^<]+"
    patronvideos += "<li class='box' id='post'>[^<]+"
    patronvideos += "<div class='postim' id='post'>[^<]+"
    patronvideos += "<div class='btitle'>[^<]+"
    patronvideos += "<h2>[^<]+"
    patronvideos += "<a href='([^']+)'>([^<]+)</a>.*?"
    patronvideos += 'bp_thumbnail_resize\("([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for scrapedurl,scrapedtitle,scrapedthumbnail in matches:
        scrapedplot = ""
        scrapedthumbnail = scrapedthumbnail.replace("s72-c","s320-c")
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    #<a class='blog-pager-older-link' href='http://robinfilm-new.blogspot.com.es/search?updated-max=2012-03-15T10:44:00-07:00&amp;max-results=12' id='Blog1_blog-pager-older-link' title='Messages plus anciens'>Messages plus anciens</a>
    #<a class='blog-pager-older-link' href='http://www.robinfilm.com/search?updated-max=2011-10-13T18%3A12%3A00%2B02%3A00&max-results=21' id='Blog1_blog-pager-older-link' title='Post più vecchi'>Post più vecchi</a>
    patron = "<a class='blog-pager-older-link' href='([^']+)'"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = ">> Página siguiente"
        scrapedplot = ""
        scrapedurl = urlparse.urljoin(item.url,match)
        scrapedthumbnail = match[2]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="novedades", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    # mainlist
    peliculas_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    bien = False
    for pelicula_item in peliculas_items:
        mirrors = servertools.find_video_items( item=pelicula_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien