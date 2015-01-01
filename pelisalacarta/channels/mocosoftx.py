# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para mocosoftx
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "mocosoftx"
__category__ = "F"
__type__ = "generic"
__title__ = "MocosoftX"
__language__ = "ES"
__adult__ = "true"

DEBUG = config.get_setting("debug")

MAIN_HEADERS = []
MAIN_HEADERS.append( ["Host","mocosoftx.com"] )
MAIN_HEADERS.append( ["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0) Gecko/20100101 Firefox/8.0"] )
MAIN_HEADERS.append( ["Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"] )
MAIN_HEADERS.append( ["Accept-Language","es-es,es;q=0.8,en-us;q=0.5,en;q=0.3"] )
MAIN_HEADERS.append( ["Accept-Charset","ISO-8859-1,utf-8;q=0.7,*;q=0.7"] )
MAIN_HEADERS.append( ["Connection","keep-alive"] )

# Login:
# <form action="http://mocosoftx.com/foro/login2/" method="post" accept-charset="ISO-8859-1" onsubmit="hashLoginPassword(this, '3e468fdsab5d9');" >
# pst: user=blablabla&passwrd=&cookielength=-1&hash_passwrd=78e88DSe408508d22f
# doForm.hash_passwrd.value = hex_sha1(hex_sha1(doForm.user.value.php_to8bit().php_strtolower() + doForm.passwrd.value.php_to8bit()) + cur_session_id);

def isGeneric():
    return True

def login():

    # Averigua el id de sesión
    data = scrapertools.cache_page("http://www.mocosoftx.com/foro/index.php")
    cur_session_id = scrapertools.get_match(data,'form action="[^"]+" method="post" accept-charset="ISO-8859-1" onsubmit="hashLoginPassword\(this, \'([a-z0-9]+)\'')
    logger.info("cur_session_id="+cur_session_id)

    # Calcula el hash del password
    LOGIN = config.get_setting("mocosoftxuser")
    PASSWORD = config.get_setting("mocosoftxpassword")
    logger.info("LOGIN="+LOGIN)
    logger.info("PASSWORD="+PASSWORD)
    
    #doForm.hash_passwrd.value = hex_sha1(hex_sha1(doForm.user.value.php_to8bit().php_strtolower() + doForm.passwrd.value.php_to8bit()) + cur_session_id);
    hash_passwrd = scrapertools.get_sha1( scrapertools.get_sha1( LOGIN.lower() + PASSWORD.lower() ) + cur_session_id)
    logger.info("hash_passwrd="+hash_passwrd)

    # Hace el submit del login
    post = "user="+LOGIN+"&passwrd=&cookielength=-1&hash_passwrd="+hash_passwrd
    logger.info("post="+post)

    data = scrapertools.cache_page("http://mocosoftx.com/foro/login2/" , post=post, headers=MAIN_HEADERS)

    return True

def mainlist(item):
    logger.info("[mocosoftx.py] mainlist")
    itemlist = []
    
    if config.get_setting("mocosoftxaccount")!="true":
        itemlist.append( Item( channel=__channel__ , title="Habilita tu cuenta en la configuración..." , action="" , url="" , folder=False ) )
    else:
        if login():
            item.url = "http://mocosoftx.com/foro/forum/"
            return foro(item)
        else:
            itemlist.append( Item( channel=__channel__ , title="Cuenta incorrecta, revisa la configuración..." , action="" , url="" , folder=False ) )

    return itemlist

def foro(item):
    logger.info("[mocosoftx.py] foro")
    itemlist = []
    
    # Descarga la página
    data = scrapertools.cache_page(item.url,headers=MAIN_HEADERS)
    
    # Extrae los foros y subforos
    patron  = '<h4><a href="([^"]+)"[^>]+>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedurl,scrapedtitle in matches:
        scrapedtitle = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")
        title = ">> Foro "+scrapedtitle
        url = urlparse.urljoin(item.url,scrapedurl)
        #http://mocosoftx.com/foro/fotos-hentai/?PHPSESSID=nflddqf9nvbm2dd92
        if "PHPSESSID" in url:
            url = scrapertools.get_match(url,"(.*?)\?PHPSESSID=")
        thumbnail = ""
        plot = ""
        itemlist.append( Item( channel=__channel__ , title=title , action="foro" , url=url , plot=plot, thumbnail=thumbnail, folder=True ) )
    
    # Extrae los hilos individuales
    patron = '<td class="icon2 windowbgb">[^<]+'
    patron += '<img src="([^"]+)"[^<]+'
    patron += '</td>[^<]+'
    patron += '<td class="subject windowbgb2">[^<]+'
    patron += '<div >[^<]+'
    patron += '<span id="msg_\d+"><a href="([^"]+)">([^>]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedthumbnail,scrapedurl,scrapedtitle in matches:
        title = scrapedtitle
        url = urlparse.urljoin(item.url,scrapedurl)
        if "PHPSESSID" in url:
            url = scrapertools.get_match(url,"(.*?)\?PHPSESSID=")
        thumbnail = scrapedthumbnail
        plot = ""
        itemlist.append( Item( channel=__channel__ , title=title , action="findvideos" , url=url , plot=plot, thumbnail=thumbnail, folder=True ) )

    # Extrae la marca de siguiente página
    #<a class="navPages" href="http://mocosoftx.com/foro/peliculas-xxx-online-(completas)/20/?PHPSESSID=rpejdrj1trngh0sjdp08ds0ef7">2</a>
    patronvideos = '<strong>\d+</strong[^<]+<a class="navPages" href="([^"]+)">'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    if len(matches)>0:
        scrapedtitle = ">> Página siguiente"
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        if "PHPSESSID" in scrapedurl:
            scrapedurl = scrapertools.get_match(scrapedurl,"(.*?)\?PHPSESSID=")
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append( Item( channel=__channel__ , title=scrapedtitle , action="foro" , url=scrapedurl , plot=scrapedplot, thumbnail=scrapedthumbnail, folder=True ) )

    return itemlist

def findvideos(item):
    logger.info("[mocosoftx.py] findvideos")
    itemlist=[]

    # Busca el thumbnail y el argumento
    data = scrapertools.cache_page(item.url)
    
    try:
        thumbnail = scrapertools.get_match(data,'<div class="post">.*?<img src="([^"]+)"')
    except:
        thumbnail = ""
    
    plot = ""
    
    # Ahora busca los vídeos
    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        videoitem.channel = __channel__
        videoitem.plot = plot
        videoitem.thumbnail = thumbnail
        videoitem.fulltitle = item.title

        parsed_url = urlparse.urlparse(videoitem.url)
        fichero = parsed_url.path
        partes = fichero.split("/")
        titulo = partes[ len(partes)-1 ]
        videoitem.title = titulo + " - [" + videoitem.server+"]"

    return itemlist
