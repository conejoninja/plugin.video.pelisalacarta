# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para yaske
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "yaske"
__category__ = "F"
__type__ = "generic"
__title__ = "yaske.net"
__language__ = "ES"

DEBUG = config.get_setting("debug")

HEADER = [
    ["Host","www.yaske.to"],
    ["Connection","keep-alive"],
    ["Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"],
    ["User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36"],
    ["Referer","http://www.yaske.to/"],
    ["Accept-Encoding","gzip,deflate,sdch"],
    ["Accept-Language","es-ES,es;q=0.8"],
    ["Cookie","__cfduid=dcf14adcea14f105833e0c38de7999a861410939223081"],
    ["Cookie","cf_clearance=2dc08b26953b29da13be0c136b312edc1280ed39-1414787651-900"]
]

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.yaske mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Novedades"          , action="peliculas",       url="http://www.yaske.to/"))
    itemlist.append( Item(channel=__channel__, title="Por año"            , action="menu_buscar_contenido",      url="http://www.yaske.to/", extra="year"))
    itemlist.append( Item(channel=__channel__, title="Por género"         , action="menu_buscar_contenido", url="http://www.yaske.to/", extra="gender"))
    itemlist.append( Item(channel=__channel__, title="Por calidad"        , action="menu_buscar_contenido",  url="http://www.yaske.to/", extra="quality"))
    itemlist.append( Item(channel=__channel__, title="Por idioma"         , action="menu_buscar_contenido",    url="http://www.yaske.to/", extra="language"))
    itemlist.append( Item(channel=__channel__, title="Buscar"             , action="search") )

    return itemlist

def search(item,texto):

    logger.info("pelisalacarta.yaske search")
    itemlist = []

    try:
        item.url = "http://www.yaske.to/es/peliculas/search/%s"
        item.url = item.url % texto
        item.extra = ""
        itemlist.extend(peliculas(item))
        itemlist = sorted(itemlist, key=lambda Item: Item.title) 

        return itemlist

    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def peliculas(item):
    logger.info("pelisalacarta.yaske listado")

    data = scrapertools.cache_page(item.url,headers=HEADER)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)

    # Extrae las entradas
    '''
    <li class="item-movies c8"><a class="image-block" href="http://www.yaske.to/es/pelicula/0005346/ver-transformers-4-online.html" title="Transformers 4: La era de la extinci&oacute;n"><img src="http://www.yaske.to/upload/images/59481937cedbdd789cec00aab9f7ed8b.jpg" width="140" height="200" /></a><ul class="bottombox"><li title="Transformers 4: La era de la extinci&oacute;n"><a href="http://www.yaske.to/es/pelicula/0005346/ver-transformers-4-online.html" title="Transformers 4: La era de la extinci&oacute;n">Transformers 4: La&hellip;</a></li><li>Accion, ciencia Ficcion</li><li><img src='http://www.yaske.to/theme/01/data/images/flags/es_es.png' title='Spanish ' width='25'/> <img src='http://www.yaske.to/theme/01/data/images/flags/en_es.png' title='English SUB Spanish' width='25'/> <img src='http://www.yaske.to/theme/01/data/images/flags/la_la.png' title='Latino ' width='25'/> </li><li><a rel="lyteframe" rev="width: 600px; height: 380px; scrolling: no;" youtube="trailer" href="http://www.youtube.com/v/&amp;hl&amp;autoplay=1" target="_blank"><img src="http://2.bp.blogspot.com/-hj7moVFACQU/UBoi0HAFeyI/AAAAAAAAA9o/2I2KPisYtsk/s1600/vertrailer.png" height="22" border="0"></a></li></ul><div class="quality">Hd Real 720</div><div class="view"><span>view: 335482</span></div></li>
    '''
    patron  = '<li class="item-movies[^"]+">'
    patron += '<a class="image-block" href="([^"]+)" title="([^"]+)">'
    patron += '<img src="([^"]+)"[^/]+/></a>'
    patron += '<ul class="bottombox">.*?<li>(<img.*?)</li>.*?</ul>'
    patron += '<div class="quality">([^<]+)</div>'
 
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []

    for scrapedurl, scrapedtitle, scrapedthumbnail, idiomas, calidad in matches:

        patronidiomas = "<img src='[^']+' title='([^']+)'"
        matchesidiomas = re.compile(patronidiomas,re.DOTALL).findall(idiomas)

        idiomas_disponibles = ""
        for idioma in matchesidiomas:
            idiomas_disponibles = idiomas_disponibles + idioma.strip() + "/"

        if len(idiomas_disponibles)>0:
            idiomas_disponibles = "["+idiomas_disponibles[:-1]+"]"
        
        title = scrapedtitle.strip()+" "+idiomas_disponibles+"["+calidad+"]"
        title = scrapertools.htmlclean(title)

        url = scrapedurl

        thumbnail = scrapedthumbnail
        scrapedplot = ""

        itemlist.append( Item(channel=__channel__, action="findvideos", title=title , url=url , thumbnail=thumbnail , plot=scrapedplot , fulltitle=scrapertools.htmlclean(scrapedtitle.strip()), viewmode="movie", folder=True) )

    # Extrae el paginador
    patronvideos  = "<a href='([^']+)'>\&raquo\;</a>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="peliculas", title=">> Página siguiente" , url=scrapedurl , folder=True) )

    return itemlist

def menu_buscar_contenido(item):
    logger.info("pelisalacarta.yaske menu_categorias")

    data = scrapertools.cache_page(item.url,headers=HEADER)
    logger.info("data="+data)

    data = scrapertools.get_match(data,'<select name="'+item.extra+'"(.*?)</select>')
    logger.info("data="+data)

    # Extrae las entradas
    patron  = "<option value='([^']+)'>([^<]+)</option>"
    matches = re.compile(patron,re.DOTALL).findall(data)

    itemlist = []

    for scrapedurl,scrapedtitle in matches:
        scrapedthumbnail = ""
        scrapedplot = ""

        url = "http://www.yaske.net/es/peliculas/custom/?"+item.extra+"="+scrapedurl

        itemlist.append( Item(channel=__channel__, action="peliculas", title=scrapedtitle , url=url , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def findvideos(item):
    logger.info("pelisalacarta.yaske findvideos url="+item.url)

    # Descarga la página
    data = scrapertools.cache_page(item.url,headers=HEADER)

    # Extrae las entradas
    '''
    <tr bgcolor="">
    <td height="32" align="center"><a class="btn btn-mini enlace_link" style="text-decoration:none;" rel="nofollow" target="_blank" title="Ver..." href="http://www.yaske.net/es/reproductor/pelicula/2141/44446/"><i class="icon-play"></i><b>&nbsp; Opcion &nbsp; 04</b></a></td>
    <td align="left"><img src="http://www.google.com/s2/favicons?domain=played.to"/>played</td>
    <td align="center"><img src="http://www.yaske.net/theme/01/data/images/flags/la_la.png" width="21">Lat.</td>
    <td align="center" class="center"><span title="" style="text-transform:capitalize;">hd real 720</span></td>
    <td align="center"><div class="star_rating" title="HD REAL 720 ( 5 de 5 )">
    <ul class="star"><li class="curr" style="width: 100%;"></li></ul>
    </div>
    </td> <td align="center" class="center">2553</td> </tr>
    '''

    patron  = '<tr bgcolor=(.*?)</tr>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    itemlist = []

    #n = 1
    for tr in matches:
        logger.info("tr="+tr)
        try:
            title = scrapertools.get_match(tr,'<b>([^<]+)</b>')
            server = scrapertools.get_match(tr,'"http\://www.google.com/s2/favicons\?domain\=([^"]+)"')

            # <td align="center"><img src="http://www.yaske.net/theme/01/data/images/flags/la_la.png" width="19">Lat.</td>
            idioma = scrapertools.get_match(tr,'<img src="http://www.yaske.[a-z]+/theme/01/data/images/flags/([a-z_]+).png"[^>]+>[^<]*<')
            subtitulos = scrapertools.get_match(tr,'<img src="http://www.yaske.[a-z]+/theme/01/data/images/flags/[^"]+"[^>]+>([^<]*)<')
            calidad = scrapertools.get_match(tr,'<td align="center" class="center"[^<]+<span title="[^"]*" style="text-transform.capitalize.">([^<]+)</span></td>')
            
            #<a [....] href="http://api.ysk.pe/noref/?u=< URL Vídeo >">
            url = scrapertools.get_match(tr,'<a.*?href="([^"]+)"').split("=")[1]

            # Para extraer netutv se necesita en la actualidad pasar por varias páginas con lo que relentiza mucho la carga.
            # De momento mostrará "No hay nada que reproducir"
            '''
            if "/netu/tv/" in url:
                import base64
                ###################################################
                # Añadido 17-09-14
                ###################################################
                try: data = scrapertools.cache_page(url,headers=getSetCookie(url1))
                except: data = scrapertools.cache_page(url)
                ###################################################
                match_b64_1 = 'base64,([^"]+)"'
                b64_1 = scrapertools.get_match(data, match_b64_1)
                utf8_1 = base64.decodestring(b64_1)
                match_b64_inv = "='([^']+)';"
                b64_inv = scrapertools.get_match(utf8_1, match_b64_inv)
                b64_2 = b64_inv[::-1]
                utf8_2 = base64.decodestring(b64_2).replace("%","\\").decode('unicode-escape')
                id_video = scrapertools.get_match(utf8_2,'<input name="vid" id="text" value="([^"]+)">')
                url = "http://netu.tv/watch_video.php?v="+id_video
            '''

            thumbnail = ""
            plot = ""

            title = title.replace("&nbsp;","")

            if "es_es" in idioma:
                scrapedtitle = title + " en "+server.strip()+" [Español]["+calidad+"]"
            elif "la_la" in idioma:
                scrapedtitle = title + " en "+server.strip()+" [Latino]["+calidad+"]"
            elif "en_es" in idioma:
                scrapedtitle = title + " en "+server.strip()+" [Inglés SUB Español]["+calidad+"]"
            else:
                scrapedtitle = title + " en "+server.strip()+" ["+idioma+" / "+subtitulos+"]["+calidad+"]"
            scrapedtitle = scrapertools.entityunescape(scrapedtitle)
            scrapedtitle = scrapedtitle.strip()

            scrapedurl = url

            scrapedthumbnail = thumbnail
            scrapedplot = plot

            itemlist.append( Item(channel=__channel__, action="play", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , fulltitle=item.fulltitle , folder=False) )
        except:
            import traceback
            logger.info("Excepcion: "+traceback.format_exc())

    return itemlist

def play(item):
    logger.info("pelisalacarta.yaske play item.url="+item.url)
    
    itemlist=[]

    data = item.url

    itemlist = servertools.find_video_items(data=data)
    for newitem in itemlist:
        newitem.fulltitle = item.fulltitle
    
    return itemlist


# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    peliculas_items = peliculas(mainlist_items[0])
    bien = False
    for pelicula_item in peliculas_items:
        mirrors = findvideos( item=pelicula_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien