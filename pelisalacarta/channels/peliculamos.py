# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para peliculamos
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

DEBUG = config.get_setting("debug")

__category__ = "A"
__type__ = "generic"
__title__ = "Peliculamos"
__channel__ = "peliculamos"
__language__ = "ES"
__creationdate__ = "20121105"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[peliculamos.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Anime e cartoni"      , action="anime"))
    itemlist.append( Item(channel=__channel__, title="Film"                 , action="film"))
    itemlist.append( Item(channel=__channel__, title="Telefilm / Serie TV"  , action="serie"))

    return itemlist

def anime(item):
    logger.info("[peliculamos.py] anime")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Elenco"         , action="todas", url="http://peliculamos.net/elenco-anime-e-cartoni/", extra='Elenco Anime e Cartoni'))
    itemlist.append( Item(channel=__channel__, title="Ultimi inseriti", action="ultimas", url="http://peliculamos.net/elenco-anime-e-cartoni/ultimi-anime-e-cartoon-inseriti/"))

    return itemlist

def serie(item):
    logger.info("[peliculamos.py] serie")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Elenco"         , action="todas", url="http://peliculamos.net/telefilm-serie-tv/", extra='Elenco Telefilm/Serie TV'))
    itemlist.append( Item(channel=__channel__, title="Ultime puntate" , action="ultimos_episodios", url="http://peliculamos.net/telefilm-serie-tv/ultime-puntate-inserite/"))
    itemlist.append( Item(channel=__channel__, title="Ultime serie"   , action="ultimas_series", url="http://peliculamos.net/telefilm-serie-tv/ultime-serie-inserite/"))

    return itemlist

def film(item):
    logger.info("[peliculamos.py] film")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Elenco"         , action="todas", url="http://peliculamos.net/film-elenco/", extra='Elenco Film'))
    itemlist.append( Item(channel=__channel__, title="Ultimi 100 film inseriti", action="todas", url="http://peliculamos.net/ultimi-100-film-inseriti/", extra='Ultimi 100 Film Inseriti'))

    data = scrapertools.cache_page("http://peliculamos.net/")
    data = scrapertools.get_match(data,'<a href="http://peliculamos.net/film-elenco/">Elenco Film</a><ul(.*?)</ul')
    patron = '<li class="[^"]+"><a href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)    

    for url,title in matches:
        itemlist.append( Item(channel=__channel__, action="todas" , title=title , url=url, extra="Animazione"))        

    return itemlist

def todas(item):
    logger.info("[peliculamos.py] todas")
    itemlist=[]

    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<h1 class="entry-title">'+item.extra+'</h1>(.*?)</ul>')
    #<li><strong><a href="http://peliculamos.net/futurama-streaming-putlocker-nowvideo/">Futurama</a></strong></li>
    #<li><a href="http://peliculamos.net/full-metal-alchimist-brotherhood-streaming-putlocker-nowvideo/"><strong>Full Metal Alchimist</strong></a></li>
    patron = '<li>(.*?)</li>'
    matches = re.compile(patron,re.DOTALL).findall(data)    

    for match in matches:
        title = scrapertools.get_match(match,'<a[^>]+>(.*?)</a>')
        title = scrapertools.htmlclean(title)
        url = scrapertools.get_match(match,'<a.*?href="([^"]+)"')
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , url=url, thumbnail=thumbnail, plot=plot))        

    return itemlist

def ultimas(item):
    logger.info("[peliculamos.py] ultimas")
    itemlist=[]

    data = scrapertools.cache_page(item.url)
    #<li class="associated-post"><a href="http://peliculamos.net/i-griffin-streaming-ita-putlocker-vk-nowvideo/" title="I Griffin Streaming Ita Putlocker VK Nowvideo">I Griffin Streaming Ita Putlocker VK Nowvideo</a></li>
    patron = '<li class="associated-post"><a href="([^"]+)"[^>]+>([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)    

    for url,title in matches:
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , url=url, thumbnail=thumbnail, plot=plot))        

    return itemlist

def ultimos_episodios(item):
    logger.info("[peliculamos.py] ultimos_episodios")
    itemlist=[]

    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    #<p style="text-align: center;"><a href="http://peliculamos.net/the-vampire-diaries-stagione-4-streaming-sub-ita-vk/"><strong>The Vampire Diaries 4&#215;18 Sub ITA</strong></a></p>
    #<p style="text-align: center;"><a href="http://peliculamos.net/criminal-minds-streaming-putlocker-nowvideo-download/"><strong>Criminal Minds 8&#215;07 ITA</strong></a></p>

    patron = '<p style="text-align\: center\;"><a href="([^"]+)">(.*?)</a></p>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for url,title in matches:
        thumbnail = ""
        plot = ""
        title = scrapertools.entityunescape(title)
        title = scrapertools.htmlclean(title)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , url=url, thumbnail=thumbnail, plot=plot))        

    return itemlist

def ultimas_series(item):
    logger.info("[peliculamos.py] ultimas_series")
    itemlist=[]

    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    #<div class="associated-post"><h3 class="post-title"><a href="http://peliculamos.net/the-new-normal-streaming-ita-vk/" title="The New Normal streaming ita Vk">The New Normal streaming ita Vk</a></h3><div class="post-excerpt"><div class="fblike" style="height:25px; height:25px; overflow:hidden;"><iframe src="http://www.facebook.com/plugins/like.php?href=http%3A%2F%2Fpeliculamos.net%2Fthe-new-normal-streaming-ita-vk%2F&amp;layout=standard&amp;show_faces=false&amp;width=450&amp;action=like&amp;font=arial&amp;colorscheme=light" scrolling="no" frameborder="0" allow Transparency="true" style="border:none; overflow:hidden; width:450px;"></iframe></div><p>David e Bryan sono una coppia di Beverly Hills, che hanno tutto dalla vita; una relazione stabile, delle brillanti carriere e una bella casa, l&#8217;unica che manca nella loro vita è un figlio. Ma le cose cambiano quando incontrano Goldie, una giovane madre single dal passato burrascoso, trasferitasi a Los Angeles con la figlia di [...]</p></div></div><div class="associated-post"><h3 class="post-title"><a href="http:

    patron  = '<div class="associated-post"><h3 class="post-title"><a href="([^"]+)" title="[^"]+">([^"]+)</a></h3><div class="post-excerpt">'
    patron += '<div[^<]+<iframe[^<]+</iframe></div><p>([^<]+)<'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for url,title,plot in matches:
        thumbnail = ""
        title = scrapertools.entityunescape(title)
        title = scrapertools.htmlclean(title)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , url=url, thumbnail=thumbnail, plot=plot))        

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True
    
    from servers import servertools
    mainlist_items = mainlist(Item())
    
    # El menú es películas, series, anime
    for mainlist_item in mainlist_items:
        exec "submenu_itemlist = "+mainlist_item.action+"(mainlist_item)"

        # El submenu es todas, ultimas, etc.
        for submenu_item in submenu_itemlist:
            exec "video_itemlist = "+submenu_item.action+"(submenu_item)"

            for video_item in video_itemlist:
                mirrors = servertools.find_video_items(item=video_item)
                if len(mirrors)>0:
                    return True

    return False
