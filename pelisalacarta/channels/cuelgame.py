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

__channel__ = "cuelgame"
__category__ = "F"
__type__ = "generic"
__title__ = "Cuélgame"
__language__ = "ES"

DEBUG = config.get_setting("debug")


def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.cuelgame mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Cine" , action="finvideos", url="http://cuelgame.net/?category=4" ,thumbnail="http://img5a.flixcart.com/image/poster/q/t/d/vintage-camera-collage-sr148-medium-400x400-imadkbnrnbpggqyz.jpeg", fanart="http://bancofotos.net/photos/20141013141322374126063.jpg"))
    itemlist.append( Item(channel=__channel__, title="Series" , action="finvideos", url="http://cuelgame.net/?category=8" ,thumbnail="http://bancofotos.net/photos/20141013141323462138745.jpg", fanart="http://bancofotos.net/photos/20141013141323334136022.jpg"))
    itemlist.append( Item(channel=__channel__, title="TV" , action="finvideos", url="http://cuelgame.net/?category=67" ,thumbnail="http://naldzgraphics.net/wp-content/uploads/2008/08/353.png", fanart="http://bancofotos.net/photos/20141014141326115192067.jpg"))
    itemlist.append( Item(channel=__channel__, title="Documentales" , action="finvideos", url="http://cuelgame.net/?category=68" ,thumbnail="http://bancofotos.net/photos/20141014141326328313144.jpg", fanart="http://bancofotos.net/photos/20141014141326361136841.jpg"))
    itemlist.append( Item(channel=__channel__, title="Música" , action="finvideos", url="http://cuelgame.net/?category=13" ,thumbnail="http://flikie.s3.amazonaws.com/ImageStorage/12/122b5e1d240544d1bc46f55109292611.jpg", fanart="http://bancofotos.net/photos/20141014141327205127084.jpg"))

    itemlist.append( Item(channel=__channel__, title="Buscar"   , action="search", url="", thumbnail="http://images2.alphacoders.com/846/84682.jpg", fanart="http://bancofotos.net/photos/20141014141326763609735.jpg"))
    
    

    return itemlist

def search(item,texto):
    logger.info("pelisalacarta.cuelgame search")
    texto = texto.replace(" ","+")
    item.url = "http://cuelgame.net/search.php?q=%s" % (texto)
    try:
        return finvideos(item)
    # Se captura la excepciÛn, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []




def finvideos(item):
    logger.info("pelisalacarta.cuelgame finvideos")
    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    # corrige la falta de imagen
    data = re.sub(r"</div><p>","</div><img src='http://ampaenriquealonso.files.wordpress.com/2011/09/logocineenlacalle.png' texto ><p>",data)
    '''
   <h2> <a href="magnet:?xt=urn:btih:4E7192D0885DDB9219699BBFFD72E709006BF9F2&amp;dn=automata+2014+hdrip+xvid+sam+etrg&amp;tr=udp%3A%2F%2Fopen.demonii.com%3A1337%2Fannounce" class="l:12087"onmousedown="return clk(this, 12087)" >Automata (2014) [HDRip] [VO] </a><img src="http://cuelgame.net/img/common/is-magnet.png" class="media-icon" width="18" height="15" alt="magnet" title="magnet" /> <a href="magnet:?xt=urn:btih:4E7192D0885DDB9219699BBFFD72E709006BF9F2&dn=automata+2014+hdrip+xvid+sam+etrg&tr=udp%3A%2F%2Fopen.demonii.com%3A1337%2Fannounce" title="Direct link" rel="nofollow, noindex"><img src="http://cuelgame.net/img/common/link-02.png" class="media-icon" width="18" height="15" alt="Enlace directo" title="Enlace directo" /></a> </h2> <div class="news-submitted"><a href="/user/Dios" class="tooltip u:1179"><img src="http://cuelgame.net/cache/00/04/1179-1328100564-25.jpg" width="25" height="25" alt=""/></a><strong>magnet:?xt=urn:btih:4E7192D0885DDB9219699BBFFD72E709006BF...</strong><br /> por<a href="/user/Dios/history">Dios</a> hace7 horaspublicado hace5 horas 58 minutos</div><img src='http://cuelgame.net/cache/00/2f/thumb-12087.jpg' width='70' height='70' alt='' class='thumbnail'/><p> En un futuro no lejano, en el que el planeta Tierra sufre una creciente desertización, Jacq Vaucan (Antonio Banderas), un agente de seguros de una compañía de robótica, investiga un caso en apariencia rutinario cuando descubre algo que podría tener consecuencias decisivas para el futuro de la humanidad. Banderas produce y protagoniza este thriller futurista, que especula sobre lo que ocurriría si la inteligencia artificial superase a la humana.|<i> Más info. en comentarios.</i></p>

    '''
    #id_torrent = scrapertools.get_match(item.url,"(\d+)-")
    patron = '<h2> '
    patron += '<a href="([^"]+)".*?'
    patron += 'class="l:\d+".*? >([^<]+)</a>.*?'
    patron += '<img src=\'([^\']+)\'.*?'
    patron += '<p>([^<]+)<.*?>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl, scrapedtitle, scrapedthumbnail, scrapedplot in matches:
        
        # No deja pasar items de la mula
        if not scrapedurl.startswith("ed2k:"):
            scrapedtitle.strip()
            scrapedplot = re.sub(r"\|<i> Más info. en comentarios.</i>","",scrapedplot)
            scrapedplot = re.sub(r"<.*?>","",scrapedplot).strip()


        
    
        itemlist.append( Item(channel=__channel__, title=scrapedtitle, url=scrapedurl, action="play", server="torrent", thumbnail=scrapedthumbnail, plot=scrapedplot, folder=False) )

    
    # Extrae el paginador
    

    patronvideos  = '<a href="([^"]+)" rel="next">siguiente &#187;</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
       # corrige "&" para la paginación
       next_page = matches[0].replace("amp;","")
       scrapedurl = urlparse.urljoin(item.url, next_page)
       itemlist.append( Item(channel=__channel__, action="finvideos", title="Página siguiente >>" , url=scrapedurl , folder=True) )



    return itemlist

