# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cinehanwer
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core import jsontools
from core.item import Item
from servers import servertools

DEBUG = config.get_setting("debug")

__category__ = "A"
__type__ = "generic"
__title__ = "cinehanwer"
__channel__ = "cinehanwer"
__language__ = "ES"
__creationdate__ = "20140615"

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.channels.cinehanwer mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Estrenos"            , url="http://cinehanwer.com/estrenos/" ))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Novedades"            , url="http://cinehanwer.com" ))
    itemlist.append( Item(channel=__channel__, action="calidades" , title="Por calidad"          , url="http://cinehanwer.com/estrenos/" ))
    itemlist.append( Item(channel=__channel__, action="generos" , title="Por género"          , url="http://cinehanwer.com/estrenos/" ))
    itemlist.append( Item(channel=__channel__, action="search"  , title="Buscar..."            , url="http://cinehanwer.com/estrenos/" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="Series"            , url="http://series.cinehanwer.com" ))
      
    return itemlist
    
def series(item):
    logger.info("pelisalacarta.channels.cinehanwer series")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="series_new"  , title="Novedades Series"            , url="http://series.cinehanwer.com" ))
    itemlist.append( Item(channel=__channel__, action="series_list"  , title="Listado Series"            , url="http://series.cinehanwer.com/series/" ))
    itemlist.append( Item(channel=__channel__, action="search"  , title="Buscar..."            , url="http://series.cinehanwer.com" ))
  
    return itemlist

def calidades(item):
    logger.info("pelisalacarta.channels.cinehanwer calidades")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    data = scrapertools.find_single_match(data,'<div class="titc[^>]+>Buscar por C(.*?)</ul>')
    logger.info("data="+data)

    # Extrae las entradas (carpetas)
    patron  = '<li><a title="[^"]+" href="([^"]+)"><strong>([^<]+)</strong></a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        thumbnail = ""
        plot = ""
        url = urlparse.urljoin(item.url,scrapedurl)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="peliculas" , title=title , url=url, thumbnail=thumbnail, plot=plot, fulltitle=title))

    return itemlist

def generos(item):
    logger.info("pelisalacarta.channels.cinehanwer generos")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    data = scrapertools.find_single_match(data,'<div class="titc[^>]+>Buscar por G(.*?)</ul>')
    logger.info("data="+data)

    # Extrae las entradas (carpetas)
    patron  = '<li><a href="([^"]+)"[^>]+>([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        thumbnail = ""
        plot = ""
        url = urlparse.urljoin(item.url,scrapedurl)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="peliculas" , title=title , url=url, thumbnail=thumbnail, plot=plot, fulltitle=title))

    return itemlist
'''
def search(item,texto):
    logger.info("pelisalacarta.channels.cinehanwer search")

    if item.url=="":
        item.url="http://www.cinehanwer.com/pelis"

    texto = texto.replace(" ","-")

    # Mete el referer en item.extra
    item.extra = item.url
    item.url = item.url+"/search/query/"+texto+"/years/1950/on/undefined/showlist/all"
    try:
        return buscar(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []
'''

def search(item,texto):
    logger.info("pelisalacarta.channels.cinehanwer search")
    texto = texto.replace(" ","-")
    if item.url=="":
        item.url="http://www.cinehanwer.com/estrenos"
    if item.url=="http://www.cinehanwer.com/estrenos":
        # Mete el referer en item.extra
        item.extra = item.url
        item.url = item.url+"/search/query/"+texto+"/years/1950/on/undefined/showlist/all"
        try:
            return buscar(item)
        # Se captura la excepción, para no interrumpir al buscador global si un canal falla
        except:
            import sys
            for line in sys.exc_info():
                logger.error( "%s" % line )
            return []
    if item.url=="http://series.cinehanwer.com":
        item.extra = item.url
        item.url = "http://series.cinehanwer.com/wp-admin/admin-ajax.php?action=dwls_search&s="+texto
        try:
            return series_buscar(item)
        # Se captura la excepción, para no interrumpir al buscador global si un canal falla
        except:
            import sys
            for line in sys.exc_info():
                logger.error( "%s" % line )
            return []

        
def buscar(item):
    logger.info("pelisalacarta.channels.cinehanwer buscar")

    # Descarga la pagina
    headers = DEFAULT_HEADERS[:]
    headers.append(["Referer",item.extra])
    headers.append(["X-Requested-With","XMLHttpRequest"])
    data = scrapertools.cache_page(item.url,headers=headers)
    logger.info("data="+data)

    # Extrae las entradas (carpetas)  
    '''
    {"html":"\n\t<div class=\"ddItemContainer modelContainer\" data-model=\"serie\" data-id=\"13051\">\n\n\t\t<div data-action=\"status\" class=\"dropdownContainer desplegableAbstract\">\n\t\t\t<span><i class=\"icon-caret-down\"><\/i><\/span>\n\t\t\t<ul class=\"dropdown\">\n\t\t\t\t<li data-value=\"1\"><a href=\"#\"><i class=\"icon-check\"><\/i>Pendiente<\/a><\/li>\n\t\t\t\t<li data-value=\"2\"><a href=\"#\"><i class=\"icon-eye-open\"><\/i>Siguiendo<\/a><\/li>                <li data-value=\"3\"><a href=\"#\"><i class=\"icon-eye-close\"><\/i>Finalizada<\/a><\/li>\n                <li data-value=\"4\"><a href=\"#\"><i class=\"icon-heart\"><\/i>Favorita<\/a><\/li>\n                <li data-value=\"tolist\"><a href=\"\/serie\/attack-on-titan\/addtolist\"><i class=\"icon-list\"><\/i>A\u00f1adir a lista<\/a><\/li>\n\t\t\t\t<li data-value=\"0\" class=\"cancel\"><a href=\"#\" style=\"color:#999;\"><i class=\"icon-remove\"><\/i>Cancelar<\/a><\/li>\n\t\t\t<\/ul>\n\t\t<\/div>\n\n        <a class=\"defaultLink extended\" href=\"\/serie\/attack-on-titan\">\n\n\t\t\t<div class=\"coverMini shadow tiptip\" title=\"Ataque a los Titanes\">\n\n\n\t\t\t\t\t<img class=\"centeredPic centeredPicFalse\"  onerror=\"this.src='\/images\/cover-notfound.png';\"  src=\"\/content\/covers\/mediathumb-13051-5.png\"\/>\n\n                    <img src=\"\/images\/loading-mini.gif\" class=\"loader\"\/>\n\t\t\t<\/div>\n\t\t\t<span class=\"title\">Ataque a los Titanes<\/span>\n        <\/a>\n\n        \n\n\n        \t<\/div>\n\n\n\t<div class=\"ddItemContainer modelContainer\" data-model=\"serie\" data-id=\"4901\">\n\n\t\t<div data-action=\"status\" class=\"dropdownContainer desplegableAbstract\">\n\t\t\t<span><i class=\"icon-caret-down\"><\/i><\/span>\n\t\t\t<ul class=\"dropdown\">\n\t\t\t\t<li data-value=\"1\"><a href=\"#\"><i class=\"icon-check\"><\/i>Pendiente<\/a><\/li>\n\t\t\t\t<li data-value=\"2\"><a href=\"#\"><i class=\"icon-eye-open\"><\/i>Siguiendo<\/a><\/li>                <li data-value=\"3\"><a href=\"#\"><i class=\"icon-eye-close\"><\/i>Finalizada<\/a><\/li>\n                <li data-value=\"4\"><a href=\"#\"><i class=\"icon-heart\"><\/i>Favorita<\/a><\/li>\n                <li data-value=\"tolist\"><a href=\"\/serie\/huntik-secrets-&-seekers\/addtolist\"><i class=\"icon-list\"><\/i>A\u00f1adir a lista<\/a><\/li>\n\t\t\t\t<li data-value=\"0\" class=\"cancel\"><a href=\"#\" style=\"color:#999;\"><i class=\"icon-remove\"><\/i>Cancelar<\/a><\/li>\n\t\t\t<\/ul>\n\t\t<\/div>\n\n        <a class=\"defaultLink extended\" href=\"\/serie\/huntik-secrets-&-seekers\">\n\n\t\t\t<div class=\"coverMini shadow tiptip\" title=\"Huntik: Secrets &amp; Seekers\">\n\n\n\t\t\t\t\t<img class=\"centeredPic centeredPicFalse\"  onerror=\"this.src='\/images\/cover-notfound.png';\"  src=\"\/content\/covers\/mediathumb-4901-5.png\"\/>\n\n                    <img src=\"\/images\/loading-mini.gif\" class=\"loader\"\/>\n\t\t\t<\/div>\n\t\t\t<span class=\"title\">Huntik: Secrets &amp; Seekers<\/span>\n        <\/a>\n\n        \n\n\n        \t<\/div>\n\n<div class=\"loadingBar\" data-url=\"\/series\/loadmedia\/offset\/30\/showlist\/all\/years\/1950\/query\/titanes\/on\/undefined\">\n    <span class=\"text\">Cargar m\u00e1s    <\/span><i class=\"icon-caret-down text\"><\/i>\n    <img src=\"\/images\/loading.gif\">\n<\/div>","ready":"\n\t\tcontroller.userStatus(\"serie\", \"13051\", \"0\");\n\t\n\t\tcontroller.userStatus(\"serie\", \"4901\", \"0\");\n\t","error":"","title":"cinehanwer.com - Search Series - cinehanwer.com","data":[],"facets":"<a class=\"mediaFilterLink active\" data-value=\"0\" href=\"\/series\">Todos<\/a><a class=\"mediaFilterLink\" data-value=\"action and adventure\" href=\"\/series\/index\/genre\/action+and+adventure\">Acci\u00f3n y Aventura <span class=\"num\">(2)<\/span><\/a><a class=\"mediaFilterLink\" data-value=\"animation\" href=\"\/series\/index\/genre\/animation\">Animaci\u00f3n <span class=\"num\">(2)<\/span><\/a><a class=\"mediaFilterLink\" data-value=\"drama\" href=\"\/series\/index\/genre\/drama\">Drama <span class=\"num\">(1)<\/span><\/a><a class=\"mediaFilterLink\" data-value=\"fantasy\" href=\"\/series\/index\/genre\/fantasy\">Fantas\u00eda <span class=\"num\">(1)<\/span><\/a><a class=\"mediaFilterLink\" data-value=\"children\" href=\"\/series\/index\/genre\/children\">Infantil <span class=\"num\">(1)<\/span><\/a>","session":"1v1jo5vqu64g3obvnt44cdtl07","screenId":"screen-1739968202"}
    '''
    json_object = jsontools.load_json(data)
    logger.info("html="+json_object["html"])
    data = json_object["html"]

    '''
    <a class="defaultLink extended" href="/serie/huntik-secrets-&-seekers">
    <div class="coverMini shadow tiptip" title="Huntik: Secrets &amp; Seekers">
    <img class="centeredPic centeredPicFalse"  onerror="this.src='/images/cover-notfound.png';"  src="/content/covers/mediathumb-4901-5.png"/>
    <img src="/images/loading-mini.gif" class="loader"/>
    </div>
    <span class="title">Huntik: Secrets &amp; Seekers</span>
    </a>
    '''
    patron  = '<a class="defaultLink extended" href="([^"]+)"[^<]+'
    patron += '<div class="coverMini shadow tiptip" title="([^"]+)"[^<]+'
    patron += '<img class="centeredPic.*?src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for scrapedurl,scrapedtitle,scrapedthumbnail in matches:
        title = scrapertools.htmlclean(scrapedtitle)
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        plot = ""
        #http://www.cinehanwer.com/peli/the-lego-movie
        #http://www.cinehanwer.com/links/view/slug/the-lego-movie/what/peli?popup=1

        if "/peli/" in scrapedurl:
            referer = urlparse.urljoin(item.url,scrapedurl)
            url = referer.replace("/peli/","/links/view/slug/")+"/what/peli"
            if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
            itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , extra=referer, url=url, thumbnail=thumbnail, plot=plot, fulltitle=title, viewmode="movie"))
        else:
            referer = item.url
            url = urlparse.urljoin(item.url,scrapedurl)
            itemlist.append( Item(channel=__channel__, action="episodios" , title=title , extra=referer, url=url, thumbnail=thumbnail, plot=plot, fulltitle=title, viewmode="movie"))

    return itemlist

def series_buscar(item):
    logger.info("pelisalacarta.channels.cinehanwer series_buscar")

    # Descarga la pagina
    headers = DEFAULT_HEADERS[:]
    headers.append(["Referer",item.extra])
    headers.append(["X-Requested-With","XMLHttpRequest"])
    data = scrapertools.cache_page(item.url,headers=headers)
    logger.info("data="+data)

    # Extrae las entradas (carpetas)  
    '''
    {"searchTerms":"yes","results":[{"ID":4501,"post_author":"1","post_date":"mayo 23, 2014","post_date_gmt":"2014-05-23 17:56:47","post_title":"4x06 - Leyes de dioses y hombres","post_excerpt":"<p>La historia de Canci\u00f3n de Hielo y Fuego se sit\u00faa en un mundo ficticio medieval. Hay tres l\u00edneas [...]<\/p>\n","post_status":"publish","comment_status":"open","ping_status":"open","post_password":"","post_name":"4x06-leyes-de-dioses-y-hombres","to_ping":"","pinged":"","post_modified":"2014-05-23 19:56:47","post_modified_gmt":"2014-05-23 17:56:47","post_content_filtered":"","post_parent":0,"guid":"http:\/\/series.cinehanwer.com\/?p=4501","menu_order":0,"post_type":"post","post_mime_type":"","comment_count":"0","filter":"raw","post_author_nicename":"admin","permalink":"http:\/\/series.cinehanwer.com\/4x06-leyes-de-dioses-y-hombres\/","attachment_thumbnail":"http:\/\/series.cinehanwer.com\/wp-content\/uploads\/2013\/04\/\u00edndice-150x150.jpg","show_more":true},{"ID":4424,"post_author":"1","post_date":"mayo 16, 2014","post_date_gmt":"2014-05-16 09:02:06","post_title":"1x20 - El hacedor de reyes","post_excerpt":"<p>El criminal m\u00e1s buscado del mundo, Thomas Raymond Reddington (James Spader, se entrega [...]<\/p>\n","post_status":"publish","comment_status":"open","ping_status":"open","post_password":"","post_name":"1x20-el-hacedor-de-reyes","to_ping":"","pinged":"","post_modified":"2014-05-16 11:02:06","post_modified_gmt":"2014-05-16 09:02:06","post_content_filtered":"","post_parent":0,"guid":"http:\/\/series.cinehanwer.com\/?p=4424","menu_order":0,"post_type":"post","post_mime_type":"","comment_count":"0","filter":"raw","post_author_nicename":"admin","permalink":"http:\/\/series.cinehanwer.com\/1x20-el-hacedor-de-reyes\/","attachment_thumbnail":"http:\/\/series.cinehanwer.com\/wp-content\/uploads\/2014\/01\/The-Blacklist-128x128.jpeg","show_more":true}],"displayPostMeta":true}
    '''
    json_object = jsontools.load_json(data)
    logger.info("results="+json_object["results"])
    data = json_object["results"]
    
    for entries in data:
        title = scrapertools.htmlclean(entries["post_title"])
        thumbnail = scrapertools.htmlclean(entries["attachment_thumbnail"])
        url = scrapertools.htmlclean(entries["permalink"])
        plot = ""
   
        itemlist.append( Item(channel=__channel__, action="findvideos_series" , title=title , url=url, thumbnail=thumbnail, plot=plot, fulltitle=title, viewmode="movie"))
 
    return itemlist    
    
def peliculas(item):
    logger.info("pelisalacarta.channels.cinehanwer peliculas")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)

    # Extrae las entradas
    '''
    <a href="/pelicula/3708/tarzan.html" title="Tarzan" >
    <img style="margin-top:0;" src="/files/uploads/3708.jpg" alt="" />
    <cite><center>Tarzan<br/><br><br><span class="txcnhd cowh dino" style=" color: #fff; ">
    <strong>Genero:</strong> Animacion<br>
    <strong>A&ntilde;o:</strong> 2014<br>
    <strong>Calidad:</strong> BR-Screener<br>
    <strong>Idiomas :</strong>  Espa&ntilde;ol
    '''
    patron  = '<a href="([^"]+)" title="([^"]+)"[^<]+'
    patron += '<img style="[^"]+" src="([^"]+)"[^<]+'
    patron += '<cite>(.*?)</cite>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for scrapedurl,scrapedtitle,scrapedthumbnail,scrapedplot in matches:
        title = scrapedtitle.strip()
        title = scrapertools.htmlclean(title)
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        plot = scrapertools.htmlclean(scrapedplot)
        url = urlparse.urljoin(item.url,scrapedurl)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , url=url, thumbnail=thumbnail, plot=plot, fulltitle=title, viewmode="movie"))

    #</b></span></a></li[^<]+<li><a href="?page=2">
    next_page = scrapertools.find_single_match(data,'</b></span></a></li[^<]+<li><a href="([^"]+)">')
    if next_page!="":
    #    itemlist.append( Item(channel=__channel__, action="peliculas" , title=">> Página siguiente" , url=item.url+next_page, folder=True))
        itemlist.append( Item(channel=__channel__, action="peliculas" , title=">> Página siguiente" , url=urlparse.urljoin(item.url,next_page), folder=True))
      
    return itemlist
    
def series_new(item):
    logger.info("pelisalacarta.channels.cinehanwer series_new")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)

    # Extrae las entradas

    patron = '<div class="show-thumbnail">[^<]+<a href="([^"]+)">[\s\S]+?<img src="([^"]+)"[\s\S]+?<h3><a[\s\S]+?title="([^"]+?)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        #title = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")
        title = scrapedtitle
        title = title.strip()
        title = scrapertools.htmlclean(title)
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        plot = ""
        url = urlparse.urljoin(item.url,scrapedurl)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos_series" , title=title , url=url, thumbnail=thumbnail, plot=plot, fulltitle=title, viewmode="movie"))
      
    return itemlist
    
def series_list(item):
    logger.info("pelisalacarta.channels.cinehanwer series_list")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)

    # Extrae las entradas

    patron = '<li><a href="([^"]+)">([^"]+)<\/a><\/li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for scrapedurl, scrapedtitle in matches:
        #title = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")
        title = scrapedtitle
        title = title.strip()
        title = scrapertools.htmlclean(title)
        thumbnail = ""
        plot = ""
        url = "http://series.cinehanwer.com/wp-content/themes/bueno/ajax/seriesajaxresp_get.php?serie="+scrapedurl+"&status=0"
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="series_seasons"  , title=title ,  url=url, thumbnail=thumbnail, plot=plot, fulltitle=title))
        #itemlist.append( Item(channel=__channel__, action="findvideos_series" , title=title , url=url, thumbnail=thumbnail, plot=plot, fulltitle=title, viewmode="movie"))
      
    return itemlist
    
def series_seasons(item):
    logger.info("pelisalacarta.channels.cinehanwer series_seasons")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)

    # Extrae las entradas

    patron = '<li><a href="([^"]+)">([^"]+)<\/a><\/li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for scrapedurl, scrapedtitle in matches:
        #title = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")
        title = scrapedtitle
        title = title.strip()
        title = scrapertools.htmlclean(title)
        thumbnail = ""
        plot = ""
        url = "http://series.cinehanwer.com/wp-content/themes/bueno/ajax/seriesajaxresp_get.php?serie="+scrapedurl+"&status=1"
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="series_chapters"  , title=title ,  url=url, thumbnail=thumbnail, plot=plot, fulltitle=title))
        #itemlist.append( Item(channel=__channel__, action="findvideos_series" , title=title , url=url, thumbnail=thumbnail, plot=plot, fulltitle=title, viewmode="movie"))
      
    return itemlist
    
def series_chapters(item):
    logger.info("pelisalacarta.channels.cinehanwer series_chapters")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)

    # Extrae las entradas

    patron = '<li><a href="([^"]+)">([^"]+)<\/a><\/li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for scrapedurl, scrapedtitle in matches:
        #title = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")
        title = scrapedtitle
        title = title.strip()
        title = scrapertools.htmlclean(title)
        thumbnail = ""
        plot = ""
        url = "http://series.cinehanwer.com/wp-content/themes/bueno/ajax/seriesajaxresp_get.php?id="+scrapedurl+"&status=2"
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos_series"  , title=title ,  url=url, thumbnail=thumbnail, plot=plot, fulltitle=title))
        #itemlist.append( Item(channel=__channel__, action="findvideos_series" , title=title , url=url, thumbnail=thumbnail, plot=plot, fulltitle=title, viewmode="movie"))
      
    return itemlist


def findvideos(item):
    logger.info("pelisalacarta.channels.cinehanwer findvideos")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    #logger.info("data="+data)

    # Extrae las entradas (carpetas)  
    patron  = '<tr[^<]+'
    patron += '<td[^<]+<div[^<]+'
    patron += '<img[^<]+'
    patron += '<a href="([^"]+)"[^<]+</a></td[^<]+'
    patron += '<td[^<]+<img src="([^"]+)"</td[^<]+'
    patron += '<td[^<]+<img[^>]+>([^<]+)</td[^<]+'
    patron += '<td[^>]+>([^<]+)</td[^<]+'
    patron += '<td[^<]+</td[^<]+'
    patron += '<td[^<]+'
    patron += '<a title="Reportar este enlace"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for scrapedurl,serverthumb,idioma,calidad in matches:
        idioma = idioma.strip()
        calidad = calidad.strip()
        nombre_servidor = serverthumb.split("/")[-1]

        title = "Ver en "+nombre_servidor+" ("+idioma+") (Calidad "+calidad+")"
        url = scrapedurl
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="play" , title=title , url=url, thumbnail=thumbnail, plot=plot, folder=False))

    return itemlist

def findvideos_series(item):
    logger.info("pelisalacarta.channels.cinehanwer findvideos_series")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    #logger.info("data="+data)

    # Extrae las entradas (carpetas)  
    patron  = '<div class="download_buttton">[\s\S]+?<a href="([^"<]+)[\S\s]+?<img border="0" src="">[\s\S]+?<br>([^"<]+)'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for scrapedurl, title in matches:
        if (title == "") : title = scapedurl 
        title = title.strip()
        url = scrapedurl
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"]")
        itemlist.append( Item(channel=__channel__, action="play" , title=title , url=url, thumbnail=thumbnail, plot=plot, folder=False))
        
    # Extrae las entradas (links)
    patron  = '<iframe src="([^"<]+)'
    matches = re.compile(patron,re.DOTALL).findall(data)    
    # Extra las entradas dentro de un iframe
    for scrapedurl in matches:
        title = "Ver en "+ scrapedurl 
        title = title.strip()
        url = scrapedurl
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"]")
        itemlist.append( Item(channel=__channel__, action="play" , title=title , url=url, thumbnail=thumbnail, plot=plot, folder=False))
    
    return itemlist
    

def play(item):
    logger.info("pelisalacarta.channels.cinehanwer play url="+item.url)

    itemlist = servertools.find_video_items(data=item.url)

    for videoitem in itemlist:
        videoitem.title = item.title
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist    