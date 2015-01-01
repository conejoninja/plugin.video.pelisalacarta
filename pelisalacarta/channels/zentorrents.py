# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para zentorrents
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "zentorrents"
__category__ = "F"
__type__ = "generic"
__title__ = "Zentorrents"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.zentorrents mainlist")
    
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Películas"      , action="peliculas", url="http://zentorrents.palasaka.net/peliculas/" ,thumbnail="http://www.navymwr.org/assets/movies/images/img-popcorn.png", fanart="http://s18.postimg.org/u9wyvm809/zen_peliculas.jpg"))
    itemlist.append( Item(channel=__channel__, title="Peliculas 1080" , action="peliculas", url="http://zentorrents.palasaka.net/tags/1080p" ,thumbnail="http://www.sony.net/Fun/design/history/product/2000/img/img_2006_full-hd_01.jpg", fanart="http://s9.postimg.org/i5qhadsjj/zen_1080.jpg"))
    itemlist.append( Item(channel=__channel__, title="Peliculas 720"  , action="peliculas", url="http://zentorrents.palasaka.net/tags/720p", thumbnail="http://2.bp.blogspot.com/-xEVhZY1_4vc/UEkfrP1OwWI/AAAAAAAAA7Q/2EeW2O9A4Rc/s1600/HD720.jpg", fanart="http://s15.postimg.org/5kqx9ln7v/zen_720.jpg"))
    itemlist.append( Item(channel=__channel__, title="Series"         , action="peliculas", url="http://zentorrents.palasaka.net/series",  thumbnail="http://data2.whicdn.com/images/10110324/original.jpg", fanart="http://s10.postimg.org/t0xz1t661/zen_series.jpg"))
    itemlist.append( Item(channel=__channel__, title="Buscar..."      , action="search"   , url="http://zentorrents.palasaka.net/buscar", thumbnail="http://newmedia-art.pl/product_picture/full_size/bed9a8589ad98470258899475cf56cca.jpg", fanart="http://s23.postimg.org/jdutugvrf/zen_buscar.jpg"))
    
    
    return itemlist

def search(item,texto):
    logger.info("pelisalacarta.palasaka search")
    itemlist = []
    
    try:
        texto = texto.replace(" ","+")
        item.url = item.url+"?searchword=%s&ordering=&searchphrase=all&limit=20"
        item.url = item.url % texto
        itemlist.extend(buscador(item))
        
        return itemlist
    
    except:
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def buscador(item):
    logger.info("pelisalacarta.zentorrents buscador")
    itemlist = []
    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    #data = scrapertools.get_match(data,'</form>(<table class="contentpaneopen">.*?</table>)')
    if "highlight" in data:
        searchword = scrapertools.get_match(data,'<span class="highlight">([^<]+)</span>')
        data = re.sub(r'<span class="highlight">[^<]+</span>',searchword,data)
    #<fieldset><div class="resultimage"><a title="Carmina Y Amén" href="/peliculas/15188-carmina-y-amen"><img alt="Carmina Y Amén" class="thumbnailresult" src="http://zentorrents.palasaka.net/images/articles/15/15188t.jpg"/></a></div><div class="resulttitle"><a class="contentpagetitle" href="/peliculas/15188-carmina-y-amen">Carmina Y Amén</a><br /><span class="small">(Descargas/Películas)</span></div><div class="resultinfo">Carmina y Aménarranca con la muerte súbita del marido de la protagonista, que convence a su hija (María León) de no dar parte de la defunción hasta pasados dos días para poder cobrar la paga doble que...</div></fieldset>
    
    patron = '<fieldset><div class="resultimage">'       # Empezamos el patrón por aquí para que no se cuele nada raro
    patron+= '<a title="([^"]+)" '                       # scrapedtitulo
    patron+= 'href="([^"]+)".*?'                         # scrapedurl
    patron+= 'src="([^"]+)".*?'                          # scrapedthumbnail
    patron+= '<span class="small">\(([^\)]+)\)</span>'   # scrapedcreatedate
    patron+= '</div>'                                    #
    patron+= '<div class="resultinfo">([^<]+)</div>'     # scrapedplot
    
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedtitulo, scrapedurl, scrapedthumbnail, scrapedcreatedate, scrapedplot in matches:
        scrapedtitulo = scrapedtitulo + " (Torrent: " + scrapedcreatedate + ")"
        scrapedurl = "http://zentorrents.palasaka.net" + scrapedurl
        
        itemlist.append( Item(channel=__channel__, title=scrapedtitulo, url=scrapedurl, action="findvideos", thumbnail=scrapedthumbnail, fulltitle=scrapedtitulo, plot=scrapedplot, folder=True) )

    return itemlist




def peliculas(item):
    logger.info("pelisalacarta.zentorrents peliculas")
    itemlist = []
    
    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    
    #<div class="blogitemfdb "><a title="Frank [MicroHD]" href="/peliculas/15776-frank-microhd"><img alt="Frank [MicroHD]" class="thumbnailarticle" src="http://zentorrents.palasaka.net/images/articles/15/15776t.jpg"/></a><div class="info"><div class="title"><a title="Fran[MicroHD]" href="/peliculas/15776-frank-microhd" class="contentpagetitleblog">Frank [MicroHD]</a></div>    <div class="createdate">30/09/2014</div><div class="text">MicroHD 1080 px AC3 2.0-Castellano. Frank es una original comedia sobre un joven aspirante a músico que se siente perdido al unirse a un grupo pop vanguardista liderado por el misterioso y enigmático Frank: un genio de la música que se esconde bajo una enorme cabeza postiza.</div>        </div><div class="clr"></div></div>
    
    patron =  '<div class="blogitemfdb[^>]+>'
    patron += '<a title="([^"]+)" '
    patron += 'href="([^"]+)".*?'
    patron += 'src="([^"]+)".*?'
    patron += '<div class="createdate">([^<]+)</div>'
    patron+= '<div class="text">([^<]+)</div>'
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    for scrapedtitulo, scrapedurl, scrapedthumbnail, scrapedcreatedate, scrapedplot in matches:
        scrapedtitulo = scrapedtitulo + "(Torrent:" + scrapedcreatedate + ")"
        scrapedurl = "http://zentorrents.palasaka.net" + scrapedurl
        
        itemlist.append( Item(channel=__channel__, title=scrapedtitulo, url=scrapedurl, action="findvideos", thumbnail=scrapedthumbnail, fulltitle=scrapedtitulo, plot=scrapedplot, folder=True) )
    
    # Extrae el paginador
    patronvideos  = '<a href="([^"]+)" title="Siguiente">Siguiente</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="peliculas", title="siguiente>>" , url=scrapedurl , folder=True) )
    
    return itemlist

def findvideos(item):
    logger.info("pelisalacarta.zentorrents findvideos")
    
    itemlist = []
    
    # Descarga la página
    data = scrapertools.cache_page(item.url)
    #}" href="http://zentorrents.palasaka.net/index.php?option=com_profiles&view=download&id=15849&f=aHR0cDovL3plbnRvcnJlbnRzLnBhbGFzYWthLm5ldC9tZWRpYS90b3JyZW50cy8xNTg0OS50b3JyZW50&tmpl=component"
    patron = '}" href="([^"]+)"'
    url = scrapertools.get_match(data, patron)
    
    # Descarga la página
    data = scrapertools.cache_page(url)
    #window.location = 'http://zentorrents.palasaka.net/media/torrents/15849.torrent'
    patron = "window.location = '([^']+)'"
    url_torrent = scrapertools.get_match(data, patron)
    
    itemlist.append( Item(channel=__channel__, title = "[torrent]", action="play", url=url_torrent, server="torrent", folder=False) )
    
    
    return itemlist