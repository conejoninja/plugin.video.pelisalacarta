# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para jkanime
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
__title__ = "JKanime"
__channel__ = "jkanime"
__language__ = "ES"
__creationdate__ = "20121015"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[jkanime.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="ultimos" , title="Últimos"           , url="http://jkanime.net/" ))
    itemlist.append( Item(channel=__channel__, action="letras"  , title="Listado Alfabetico", url="http://jkanime.net/" ))
    itemlist.append( Item(channel=__channel__, action="generos" , title="Listado por Genero", url="http://jkanime.net/" ))
    itemlist.append( Item(channel=__channel__, action="search"  , title="Buscar" ))
  
    return itemlist

def search(item,texto):
    logger.info("[jkanime.py] search")
    if item.url=="":
        item.url="http://jkanime.net/buscar/%s/"
    texto = texto.replace(" ","+")
    item.url = item.url % texto
    try:
        return series(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def ultimos(item):
    logger.info("[jkanime.py] ultimos")
    itemlist = []
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<ul class="latestul">(.*?)</ul>')
    
    patron = '<a href="([^"]+)">([^<]+)<'
    matches = re.compile(patron,re.DOTALL).findall(data)    

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="episodios" , title=title , url=url, thumbnail=thumbnail, plot=plot))        

    return itemlist

def generos(item):
    logger.info("[jkanime.py] generos")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<div class="genres">(.*?)</div>')
    
    patron = '<a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)    

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="series" , title=title , url=url, thumbnail=thumbnail, plot=plot))        

    return itemlist

def letras(item):
    logger.info("[jkanime.py] letras")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<ul class="animelet">(.*?)</ul>')
    
    patron = '<a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)    

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="series" , title=title , url=url, thumbnail=thumbnail, plot=plot))        

    return itemlist

def series(item):
    logger.info("[jkanime.py] series")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas
    '''
    <table class="search">
    <tr>
    <td rowspan="2">
    <a href="http://jkanime.net/basilisk-kouga-ninpou-chou/"><img src="http://jkanime.net/assets/images/animes/thumbnail/basilisk-kouga-ninpou-chou.jpg" width="50" /></a>
    </td>
    <td><a class="titl" href="http://jkanime.net/basilisk-kouga-ninpou-chou/">Basilisk: Kouga Ninpou Chou</a></td>
    <td rowspan="2" style="width:50px; text-align:center;">Serie</td>
    <td rowspan="2" style="width:50px; text-align:center;" >24 Eps</td>
    </tr>
    <tr>
    <td><p>Basilisk, considerada una de las mejores series del genero ninja, nos narra la historia de dos clanes ninja separados por el odio entre dos familias. Los actuales representantes, Kouga Danjo del clan Kouga y Ogen del clan&#8230; <a class="next" href="http://jkanime.net/basilisk-kouga-ninpou-chou/">seguir leyendo</a></p></td>
    </tr>
    </table>
    '''
    patron  = '<table class="search[^<]+'
    patron += '<tr[^<]+'
    patron += '<td[^<]+'
    patron += '<a href="([^"]+)"><img src="([^"]+)"[^<]+</a>[^<]+'
    patron += '</td>[^<]+'
    patron += '<td><a[^>]+>([^<]+)</a></td>[^<]+'
    patron += '<td[^>]+>([^<]+)</td>[^<]+'
    patron += '<td[^>]+>([^<]+)</td>[^<]+'
    patron += '</tr>[^<]+'
    patron += '<tr>[^<]+'
    patron += '<td>(.*?)</td>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for scrapedurl, scrapedthumbnail,scrapedtitle,line1,line2,scrapedplot in matches:
        title = scrapedtitle.strip()+" ("+line1.strip()+") ("+line2.strip()+")"
        extra = line2.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = scrapedthumbnail
        plot = scrapertools.htmlclean(scrapedplot)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="episodios" , title=title , url=url, thumbnail=thumbnail, fanart=thumbnail, plot=plot, extra=extra, viewmode="movie_with_plot"))        

    try:
        siguiente = scrapertools.get_match(data,'<a class="listsiguiente" href="([^"]+)" >Resultados Siguientes')
        scrapedurl = urlparse.urljoin(item.url,siguiente)
        scrapedtitle = ">> Pagina Siguiente"
        scrapedthumbnail = ""
        scrapedplot = ""

        itemlist.append( Item(channel=__channel__, action="series", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
    except:
        pass
    return itemlist

def episodios(item):
    logger.info("[jkanime.py] episodios")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    
    scrapedplot = scrapertools.get_match(data,'<meta name="description" content="([^"]+)"/>')
    scrapedthumbnail = scrapertools.get_match(data,'<meta property="og.image" content="([^"]+)"/>')
    
    idserie = scrapertools.get_match(data,"ajax/pagination_episodes/(\d+)/")
    logger.info("idserie="+idserie)
    if " Eps" in item.extra:
        caps_x = item.extra
        caps_x = caps_x.replace(" Eps","")
        capitulos = int(caps_x)
        paginas = capitulos/10
        if capitulos%10>0:
            paginas += 1
    else:
        paginas = 1
    
    logger.info("idserie="+idserie)
    for numero in range(1,paginas + 1):

        numero_pagina = str(numero)
        headers = []
        headers.append( [ "User-Agent" , "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:16.0) Gecko/20100101 Firefox/16.0" ] )
        headers.append( [ "Referer" , item.url ] )
        data2 = scrapertools.cache_page("http://jkanime.net/ajax/pagination_episodes/"+idserie+"/"+numero_pagina+"/")
        logger.info("data2="+data2)
    
        '''
        [{"number":"1","title":"Rose of Versailles - 1"},{"number":"2","title":"Rose of Versailles - 2"},{"number":"3","title":"Rose of Versailles - 3"},{"number":"4","title":"Rose of Versailles - 4"},{"number":"5","title":"Rose of Versailles - 5"},{"number":"6","title":"Rose of Versailles - 6"},{"number":"7","title":"Rose of Versailles - 7"},{"number":"8","title":"Rose of Versailles - 8"},{"number":"9","title":"Rose of Versailles - 9"},{"number":"10","title":"Rose of Versailles - 10"}]
        [{"id":"14199","title":"GetBackers - 1","number":"1","animes_id":"122","timestamp":"2012-01-04 16:59:30"},{"id":"14200","title":"GetBackers - 2","number":"2","animes_id":"122","timestamp":"2012-01-04 16:59:30"},{"id":"14201","title":"GetBackers - 3","number":"3","animes_id":"122","timestamp":"2012-01-04 16:59:30"},{"id":"14202","title":"GetBackers - 4","number":"4","animes_id":"122","timestamp":"2012-01-04 16:59:30"},{"id":"14203","title":"GetBackers - 5","number":"5","animes_id":"122","timestamp":"2012-01-04 16:59:30"},{"id":"14204","title":"GetBackers - 6","number":"6","animes_id":"122","timestamp":"2012-01-04 16:59:30"},{"id":"14205","title":"GetBackers - 7","number":"7","animes_id":"122","timestamp":"2012-01-04 16:59:30"},{"id":"14206","title":"GetBackers - 8","number":"8","animes_id":"122","timestamp":"2012-01-04 16:59:30"},{"id":"14207","title":"GetBackers - 9","number":"9","animes_id":"122","timestamp":"2012-01-04 16:59:30"},{"id":"14208","title":"GetBackers - 10","number":"10","animes_id":"122","timestamp":"2012-01-04 16:59:30"}]
        '''
        patron = '"number"\:"(\d+)","title"\:"([^"]+)"'
        matches = re.compile(patron,re.DOTALL).findall(data2)
    
        #http://jkanime.net/get-backers/1/
        for numero,scrapedtitle in matches:
            title = scrapedtitle.strip()
            url = urlparse.urljoin(item.url,numero)
            thumbnail = scrapedthumbnail
            plot = scrapedplot
            if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

            itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , url=url, thumbnail=thumbnail, fanart=thumbnail, plot=plot))        

    if len(itemlist)==0:
        try:
            porestrenar = scrapertools.get_match(data,'<div[^<]+<span class="labl">Estad[^<]+</span[^<]+<span[^>]+>Por estrenar</span>')
            itemlist.append( Item(channel=__channel__, action="findvideos" , title="Serie por estrenar" , url="", thumbnail=scrapedthumbnail, fanart=scrapedthumbnail, plot=scrapedplot, server="directo", folder=False))
        except:
            pass

    return itemlist

def findvideos(item):
    logger.info("[jkanime.py] episodios")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    #180upload: sp1.e=hh7pmxk553kj
    try:
        code = scrapertools.get_match(data,"sp1.e=([a-z0-9]+)")
        mediaurl = "http://180upload.com/"+code
        itemlist.append( Item(channel=__channel__, action="play" , title="Ver en 180upload" , url=mediaurl, thumbnail=item.thumbnail, fanart=item.thumbnail, plot=item.plot, server="one80upload", folder=False))
    except:
        pass
    
    #upafile: spu.e=idyoybh552bf
    try:
        code = scrapertools.get_match(data,"spu.e=([a-z0-9]+)")
        mediaurl = "http://upafile.com/"+code
        itemlist.append( Item(channel=__channel__, action="play" , title="Ver en upafile" , url=mediaurl, thumbnail=item.thumbnail, fanart=item.thumbnail, plot=item.plot, server="upafile", folder=False))
    except:
        pass

    try:
        mediaurl = scrapertools.get_match(data,'flashvars\="file\=([^\&]+)\&')
        itemlist.append( Item(channel=__channel__, action="play" , title="Ver en jkanime" , url=mediaurl, thumbnail=item.thumbnail, fanart=item.thumbnail, plot=item.plot, server="directo", folder=False, extra=item.url))
    except:
        pass
    
    try:
        mediaurl = scrapertools.get_match(data,"url\: '(http://jkanime.net/stream/jkget/[^']+)'")
        itemlist.append( Item(channel=__channel__, action="play" , title="Ver en jkanime" , url=mediaurl, thumbnail=item.thumbnail, fanart=item.thumbnail, plot=item.plot, server="directo", folder=False, extra=item.url))
    except:
        pass

    return itemlist

def play(item):
    logger.info("[jkanime.py] play url="+item.url)
    
    itemlist = []

    if item.server=="directo":
        location = item.url
        '''
        body,headers = scrapertools.read_body_and_headers(item.url,follow_redirects=False)
        logger.info("jkanime headers="+repr(headers))

        location=""
        for header in headers:
            if header[0]=="location":
                location=header[1]
        '''
        '''
        GET /stream/jkmedia/717aa382aee2117d9762067125ac79e2/6ee0218e84b123c0c84e98310176fdfc/1/2364e7a4d358dfffeaca3410e73c5e76/?t=7 HTTP/1.1
        Host: jkanime.net
        Connection: keep-alive
        User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31
        Accept: */*
        Referer: http://jkanime.net/sukitte-ii-na-yo.-specials/1/
        Accept-Encoding: gzip,deflate,sdch
        Accept-Language: es-ES,es;q=0.8
        Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.3
        Cookie: ci_session=a%3A4%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%2294ef36f56048bf6394353e714505e100%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A13%3A%2288.12.106.177%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A50%3A%22Mozilla%2F5.0+%28Macintosh%3B+Intel+Mac+OS+X+10_8_2%29+App%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1364589959%3B%7D4263c499ebf728838ce9d8cb838cc55e; __cfduid=d6b6b16c05385bc35df57a09daa5e57e81364593644; flowplayer=3.2.8; gao_session_expiry=Sat, 30 Mar 2013 05:47:32 GMT; gao_skin_views=1; __utma=218181122.1870996415.1364593654.1364593654.1364593654.1; __utmb=218181122.1.10.1364593654; __utmc=218181122; __utmz=218181122.1364593654.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)
        ''' 
        #headers = []
        #headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:18.0) Gecko/20100101 Firefox/18.0"])
        #headers.append(["Referer",item.extra])
        #location = scrapertools.get_header_from_response( item.url , headers=headers , header_to_get="location" )
        #logger.info("location="+location)
        #location = scrapertools.get_header_from_response( item.url , headers=headers , header_to_get="location" )
        #logger.info("location="+location)
        #location = location + "|" + urllib.urlencode({'Referer':'http://jkanime.net/assets/images/players/jkplayer.swf'})
        #http://jkanime.net/stream/jkget/00e47553476031a35fd158881ca9d49f/32021b728c40bb5779190e0a95b72d40/?t=6e
        itemlist.append( Item(channel=__channel__, action="play" , title=item.title , url=location, thumbnail=item.thumbnail, fanart=item.thumbnail, plot=item.plot, server=item.server, folder=False))
    else:
        itemlist.append( Item(channel=__channel__, action="play" , title=item.title , url=item.url, thumbnail=item.thumbnail, fanart=item.thumbnail, plot=item.plot, server=item.server, folder=False))
    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True
    
    # mainlist
    mainlist_items = mainlist(Item())
    
    # Comprueba que todas las opciones tengan algo (excepto el buscador)
    for mainlist_item in mainlist_items:
        if mainlist_item.action!="search":
            exec "itemlist = "+mainlist_item.action+"(mainlist_item)"
            if len(itemlist)==0:
                return false
    
    # Comprueba si alguno de los vídeos de "Novedades" devuelve mirrors
    series_items = ultimos(mainlist_items[0])
    
    for serie_item in series_items:
        episodios_items = episodios(serie_item)

        bien = False
        for episodio_item in episodios_items:
            mirrors = findvideos(item=episodio_item)
            if len(mirrors)>0:
                bien = True
                break
        
    return bien