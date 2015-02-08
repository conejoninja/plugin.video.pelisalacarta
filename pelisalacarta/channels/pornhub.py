# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para pornhub
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "pornhub"
__category__ = "F"
__type__ = "generic"
__title__ = "PornHub"
__language__ = "ES"
__fanart__="http://i.imgur.com/PwFvoss.jpg"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[pornhub.py] mainlist")
    itemlist = []
    
    item.url ="http://es.pornhub.com"
    
    # Descarga la página
    data = get_main_page(item.url + "/categories?o=al")
    data = scrapertools.find_single_match(data,'<div id="categoriesStraightImages">(.*?)</ul>')
    
    '''
    <li class="cat_pic" data-category="28">
                    <div class="category-wrapper">
                        <a href="/video?c=28"><img src="http://i0.cdn2b.image.pornhub.phncdn.com/m=eXs28zjadqg/static/images/categories/28.jpg" alt="Maduras" /></a>
                        <h5>
                            <a href="/video?c=28"><strong>Maduras</strong>
                            <span>(<var>3950</var>)</span></a>
                        </h5>
                    </div>
                </li>
    '''
    
    # Extrae las categorias
    patron  = '<li class="cat_pic" data-category="\d+">.*?'
    patron += '<a href="([^"]+)">'
    patron += '<img src="([^"]+)" '
    patron += 'alt="([^"]+)"'
        
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        title = scrapedtitle
        url = urlparse.urljoin(item.url,scrapedurl + "&o=cm")
        thumbnail = scrapedthumbnail
        #thumbnail =""
       
        #try:
        itemlist.append( Item(channel=__channel__, action="peliculas", title=title, url=url , fanart=__fanart__ , thumbnail=thumbnail, folder=True) )
        #except:
            #logger.info("pelisalacarta.channels.pornhub except")
            
        itemlist.sort(key=lambda x: x.title)
    return itemlist

def peliculas(item):
    logger.info("[pornhub.py] peliculas")
    itemlist = []
       
    # Descarga la página
    data = get_main_page(item.url)
    data = scrapertools.find_single_match(data,'<ul class="nf-videos videos row-4-thumbs">(.*?)<div class="pre-footer">')
    
    '''
    <li class="videoblock" id="37717631" _vkey="2064578485" >
    <div class="wrap">
        <div class="phimage">
                            <a href="/view_video.php?viewkey=2064578485" title="Glamorous Brunette Gets Fucked Hard On Armchair 2" class="img" data-related-url="/video/ajax_related_video?vkey=2064578485">
                                    <div class="marker-overlays">
                <var class="duration">16:29</var>
                                    <span class="hd-thumbnail">HD</span>
                                            </div>
            <img src="http://cdn1b.static.pornhub.phncdn.com/www-static/images/blank.gif" alt="Glamorous Brunette Gets Fucked Hard On Armchair 2" data-smallthumb="http://i1.cdn2b.image.pornhub.phncdn.com/m=eGcE8daaaa/videos/201501/19/37717631/original/12.jpg" data-mediumthumb="http://i1.cdn2b.image.pornhub.phncdn.com/m=eWdT8daaaa/videos/201501/19/37717631/original/12.jpg" class="thumb" width="150" class="rotating" id="238153595837717631" onmouseover="startThumbChange(37717631, '238153595837717631', 16, 'http://i1.cdn2b.image.pornhub.phncdn.com/m=eWdT8daaaa/videos/201501/19/37717631/original/{index}.jpg');" onmouseout="endThumbChange('238153595837717631');" title="Glamorous Brunette Gets Fucked Hard On Armchair 2" />
                            </a>
                                </div>
                    <div class="add-to-playlist-icon display-none">
                <button type="button" data-title="Agregar a una lista de reproducción" class="tooltipTrig open-playlist-link playlist-trigger" onclick="return false;" data-rel="2064578485" >+</button>
            </div>
                            <div class="thumbnail-info-wrapper clearfix">
                <span class="title">
                                            <a href="/view_video.php?viewkey=2064578485" title="Glamorous Brunette Gets Fucked Hard On Armchair 2">Glamorous Brunette Gets Fucked Hard On Armchair 2</a>
                                    </span>
                <span class="views"><var>35</var> vistas</span>
                <div class="rating-container up">
                    <div class="main-sprite icon"></div>
                    <div class="value">100%</div>
                </div>
                                <var class="added">5 hours ago</var>
            </div>
                    </div>
    </li>
    '''
        
    # Extrae las peliculas
    patron = '<div class="phimage">.*?'
    patron += '<a href="/view_video.php\?viewkey=([^"]+)" title="([^"]+).*?'
    patron += '<var class="duration">([^<]+)</var>(.*?)</div>.*?'
    patron += 'data-smallthumb="([^"]+)"'
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    for viewkey,scrapedtitle,duration,scrapedhd,thumbnail in matches:       
        title=scrapedtitle.replace('&amp;','&')+" ("+duration+")"
        scrapedhd = scrapertools.find_single_match(scrapedhd,'<span class="hd-thumbnail">(.*?)</span>')
        if (scrapedhd == 'HD') : title += ' [HD]'
        url= 'http://es.pornhub.com/embed/' + viewkey
                
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="play", title=title , url=url ,fanart=__fanart__, thumbnail=thumbnail) )
        
    # Paginador
    patron = '<li class="page_next"><a href="([^"]+)"'
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    if len(matches)>0:
        url=urlparse.urljoin("http://es.pornhub.com",matches[0].replace('&amp;','&'))
        itemlist.append( Item(channel=__channel__, action="peliculas", title=">> Página siguiente" ,fanart=__fanart__, url=url)) 
    return itemlist


def play(item):
    logger.info("[pornhub.py] play")
    itemlist=[]
    
    #item.url='http://es.pornhub.com/embed/' + viewkey
    
    # Descarga la página
    data = get_main_page(item.url)
    data = scrapertools.find_single_match(data,'html5Config([^}]+)},')
    url = scrapertools.get_match(data,"src\s+:\s+'([^']+)',")
    
    #url= "http://cdn2b.embed.pornhub.phncdn.com/videos/201501/19/37717631/480P_600K_37717631.mp4?rs=200&ri=2500&ip=188.79.24.200&s=1421873759&e=1421880959&h=6cd0058bc8e5abac9ccfdaa50c6bdf19"
    #logger.info("url="+url)
    server="Directo"
    itemlist.append( Item(channel=__channel__, title="" , url=url , server=server, folder=False) )

    return itemlist
    

def get_main_page(url):
    logger.info("[pornhub.py] get_main_page")

    headers=[]
    headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:20.0) Gecko/20100101 Firefox/20.0"])
    headers.append(["Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"])
    headers.append(["Accept-Language","es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3"])
    headers.append(["Accept-Encoding","gzip, deflate"])

    # Descarga la página
    data = scrapertools.cachePage(url,headers=headers)
    #logger.info("pelisalacarta.channels.pornhub data="+data)

    return data
