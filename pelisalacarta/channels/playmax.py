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
from core import jsontools
from core.item import Item
from servers import servertools

DEBUG = config.get_setting("debug")

__category__ = "F"
__type__ = "generic"
__title__ = "PlayMax"
__channel__ = "playmax"
__language__ = "ES"
__creationdate__ = "20141217"

host = "http://playmax.es/"

sendHeader = [
    ['User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0']
]

def isGeneric():
    return True

def openconfig(item):
    if "xbmc" in config.get_platform() or "boxee" in config.get_platform():
        config.open_settings( )
    return []

def mainlist(item):
    logger.info("pelisalacarta.channels.playmax mainlist")

    itemlist = []

    if config.get_setting("playmaxaccount")!="true":
        itemlist.append( Item( channel=__channel__ , title="Habilita tu cuenta en la configuración..." , action="openconfig" , url="" , folder=False ) )
    else:
        itemlist.append( Item(channel=__channel__, action="series", title="Series", url=host + "catalogo.php?tipo=1" ))

    return itemlist

def series(item):
    logger.info("pelisalacarta.channels.playmax menuseries")

    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|<br>","",data)
    data = re.sub(r"<!--.*?-->","",data)

    #<div class="divjustify" id="35615" name="1" style="position: relative; margin-bottom: 5px; height:225px; width: 135px; margin-left: 19px; margin-right: 19px; text-align: center; sans-serif; color: #333;">
    #<a href="./better-call-saul-f35615">
    #<img title="Better Call Saul" style="border-radius: 3px; height:200px;" src="./caratula35615">
    #</a>
    #<span style="text-overflow: ellipsis;overflow: hidden;width: 145px;white-space: nowrap;word-wrap: normal;text-align: center;display: block; margin-left: -5px;">Better Call Saul</span>
    #<div style="position: absolute;top: 0px;width: 30px; height: 30px;right: 0px;font-size: 13px; font-weight: bold; color: #f77f00; text-align: center; line-height: 30px; background-color: rgba(255, 255, 255, 0); border-bottom-left-radius: 3px;"></div>
    #</div>

    patron = '<div class="divjustify" id="\d+" name="\d+"[^>]+>'
    patron+= '<a href="([^"]+)">'
    patron+= '<img title="([^"]+)".*?src="([^"]+)">'

    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        itemlist.append( Item(channel=__channel__, title=scrapedtitle, url=urlparse.urljoin(host,scrapedurl), action="episodios", thumbnail=urlparse.urljoin(host,scrapedthumbnail), show=scrapedtitle) )

    # paginación
    patron = '<a href="([^"]+)">Siguiente</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        itemlist.append( Item(channel=__channel__, title=">> Página siguiente", url=urlparse.urljoin(host,matches[0].replace("amp;","")), action="series") )

    return itemlist

def episodios(item):
    logger.info("pelisalacarta.channels.playmax episodios")

    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|<br>","",data)
    data = re.sub(r"<!--.*?-->","",data)

    #function load_links(value){var url = './c_enlaces.php?ficha=259&id=' + value + '&key=ZHB6YXE=';
    #^_______API+Número de la ficha:______^______Lo que usaremos________^______No nos interesa_____^

    patron = "var url = '([^']+)'"
    enlace = scrapertools.find_single_match(data,patron)

    #Temporadas y bloque de episodios por temporada
    patron = '<divd class="tabbertab "><h2>T(\d+)</h2>(.*?)</divdd></divdd></divdd></divdd></divd>'
    temporadas = re.compile(patron,re.DOTALL).findall(data)

    for temporada, episodios in temporadas:
        patron = 'load_links\(([^\)]+)\)'
        patron+= '.*?'
        patron+= '<divd class="enlacesdos">(\d+)</divd>([^<]+)</divd>'
        matches = re.compile(patron,re.DOTALL).findall(episodios)

        for id, episodio, titulo in matches:
            title = temporada + "x" + episodio + " - " + titulo
            url = enlace + id + "&key=ZHp6ZG0="
            itemlist.append( Item(channel=__channel__, title=title, url=urlparse.urljoin(host,url), action="findvideos", thumbnail=item.thumbnail, show=item.show) )

    ## Opción "Añadir esta serie a la biblioteca de XBMC"
    if (config.get_platform().startswith("xbmc") or config.get_platform().startswith("boxee")) and len(itemlist)>0:
        itemlist.append( Item(channel=__channel__, title="Añadir esta serie a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="episodios", show=item.show) )

    return itemlist

def findvideos(item):
    logger.info("pelisalacarta.playmax findvideos")

    login()
    sendHeader = [
        ['Host','playmax.es'],
        ['User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0'],
        ['Accept','text/html, */*; q=0.01'],
        ['Accept-Language','es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3'],
        ['Accept-Encoding','gzip, deflate'],
        ['Cookie',get_cookies()],
        ['X-Requested-With','XMLHttpRequest'],
        ['Referer',item.url],
        ['Connection','keep-alive']
    ]

    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url, headers=sendHeader)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|<br>","",data)
    data = re.sub(r"<!--.*?-->","",data)

    '''
    <divdd class="capitulo">
    <a href="./redirect.php?url=aHR0cDovL2FsbG15dmlkZW9zLm5ldC81bTBhYTBpZmM4ejE=&id=259" target="_blank">
    <divd class="servidor"><img style="margin-top: 5px;" src="./styles/prosilver/imageset/allmyvideos.png"></divd>
    <divd class="calidad">480p HD</divd>
    <divd class="idioma">Castellano</divd>
    <divd class="subtitulos">Sin subtítulos</divd>
    <divd class="calidadaudio">...</divd>
    </a>
    '''

    patron = '<divdd class="capitulo">'
    patron+= '<a href="([^"]+)".*?'
    patron+= 'src="([^"]+)"></divd>'
    patron+= '<divd class="calidad">([^<]+)</divd>'
    patron+= '<divd class="idioma">([^<]+)</divd>'
    patron+= '<divd class="subtitulos">([^<]+)</divd>'
    patron+= '<divd class="calidadaudio">([^<]+)</divd>'

    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, calidad, idioma, subtitulos, calidadaudio in matches:
        servidor = scrapertools.get_match(scrapedthumbnail,'imageset/([^\.]+)\.')
        title = item.title + " [" + servidor + "] [" + calidad + "] [" + idioma + "] [" + subtitulos + "] [" + calidadaudio + "]"
        itemlist.append( Item(channel=__channel__, title =title, url=urlparse.urljoin(host,scrapedurl), action="play", thumbnail=urlparse.urljoin(host,scrapedthumbnail), fanart=item.thumbnail, show=item.show ) )

    return itemlist

def play(item):
    logger.info("pelisalacarta.channels.playmax play url="+item.url)

    url = scrapertools.get_header_from_response(item.url, header_to_get="location", headers=sendHeader)

    itemlist = servertools.find_video_items(data=url)

    for videoitem in itemlist:
        videoitem.title = item.title
        videoitem.channel = __channel__

    return itemlist

def get_cookies():

    login()

    import cookielib

    cookiesdat = os.path.join( config.get_setting("cookies.dir"), 'cookies.dat' )
    cj = cookielib.MozillaCookieJar()
    cj.load(cookiesdat,ignore_discard=True)

    cookies = ""

    for cookie in cj:
         if "playmax_" in cookie.name:
            cookies+= cookie.name+"="+cookie.value+"; "

    return cookies

def login():

    login_form = "ucp.php?mode=login"
    data = scrapertools.cache_page(urlparse.urljoin(host,login_form), headers=sendHeader)
    patron = '<input type="hidden" name="sid" value="([^"]+)" />'
    sid = scrapertools.find_single_match(data,patron)

    post = "username="+config.get_setting('playmaxuser')+"&password="+config.get_setting('playmaxpassword')+"&sid="+sid+"&redirect=index.php&login=Identificarse&redirect=.%2Fucp.php%3Fmode%3Dlogin"
    data = scrapertools.cache_page("http://playmax.es/ucp.php?mode=login",post=post, headers=sendHeader)
