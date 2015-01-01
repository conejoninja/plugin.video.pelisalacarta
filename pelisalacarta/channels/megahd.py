# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para megahd
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

__channel__ = "megahd"
__category__ = "F"
__type__ = "generic"
__title__ = "Megahd"
__language__ = "ES"
__adult__ = "true"

DEBUG = config.get_setting("debug")

MAIN_HEADERS = []
MAIN_HEADERS.append( ["Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"] )
MAIN_HEADERS.append( ["Accept-Encoding","gzip, deflate"] )
MAIN_HEADERS.append( ["Accept-Language","es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3"] )
MAIN_HEADERS.append( ["Connection","keep-alive"] )
MAIN_HEADERS.append( ["Host","megahd.me"] )
MAIN_HEADERS.append( ["Referer","http://megahd.me/index.php"] )
MAIN_HEADERS.append( ["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36"] )

def isGeneric():
    return True

def login():
    logger.info("channels.megahd login")

    # Averigua el id de sesión
    data = scrapertools.cache_page("http://megahd.me/login/", headers=MAIN_HEADERS)
    #<form action="http://megahd.me/login2/" name="frmLogin" id="frmLogin" method="post" accept-charset="UTF-8"  onsubmit="hashLoginPassword(this, 'd3c3d7467c05a4058e9361996daeaed4');">
    cur_session_id = scrapertools.get_match(data,'onsubmit\="hashLoginPassword\(this, \'([a-z0-9]+)\'')
    logger.info("channels.megahd cur_session_id="+cur_session_id)

    # Calcula el hash del password
    LOGIN = config.get_setting("megahduser")
    PASSWORD = config.get_setting("megahdpassword")
    logger.info("channels.megahd LOGIN="+LOGIN)
    logger.info("channels.megahd PASSWORD="+PASSWORD)
    
    #doForm.hash_passwrd.value = hex_sha1(hex_sha1(doForm.user.value.php_to8bit().php_strtolower() + doForm.passwrd.value.php_to8bit()) + cur_session_id);
    hash_passwrd = scrapertools.get_sha1( scrapertools.get_sha1( LOGIN.lower() + PASSWORD.lower() ) + cur_session_id)
    logger.info("channels.megahd hash_passwrd="+hash_passwrd)

    # Hace el submit del login
    post = "user="+LOGIN+"&passwrd=&cookieneverexp=on&hash_passwrd="+hash_passwrd
    logger.info("channels.megahd post="+post)

    data = scrapertools.cache_page("http://megahd.me/login2/" , post=post, headers=MAIN_HEADERS)

    return True

def mainlist(item):
    logger.info("channels.megahd mainlist")
    itemlist = []
    
    if config.get_setting("megahdaccount")!="true":
    
        itemlist.append( Item( channel=__channel__ , title="Habilita tu cuenta en la configuración..." , action="openconfig" , url="" , folder=False ) )
    else:
        if login():
            itemlist.append( Item( channel=__channel__ , title="Películas" , action="foro" , url="http://megahd.me/peliculas/" , folder=True ) )
            itemlist.append( Item( channel=__channel__ , title="Anime" , action="foro" , url="http://megahd.me/anime/" , folder=True ) )
            itemlist.append( Item( channel=__channel__ , title="Series" , action="foro" , url="http://megahd.me/series/" , folder=True ) )
            itemlist.append( Item( channel=__channel__ , title="Documentales y Deportes" , action="foro" , url="http://megahd.me/documentales/" , folder=True ) )
            itemlist.append( Item( channel=__channel__ , title="Zona Infantil" , action="foro" , url="http://megahd.me/zona-infantil/" , folder=True ) )
        else:
            itemlist.append( Item( channel=__channel__ , title="Cuenta incorrecta, revisa la configuración..." , action="" , url="" , folder=False ) )
    return itemlist

def openconfig(item):
    if "xbmc" in config.get_platform() or "boxee" in config.get_platform():
        config.open_settings( )
    return []

def foro(item):
    logger.info("channels.megahd foro")
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    
    if '<h3 class="catbg">Subforos</h3>' in data:
        patron = '<a class="subje(.*?)t" href="([^"]+)" name="[^"]+">([^<]+)</a>&nbsp' # HAY SUBFOROS
        action = "foro"
    else:
        patron = '<td class="subject windowbg2">.*?<div >.*?<span id="([^"]+)"> <a href="([^"]+)".*?>([^<]+)</a> </span>'
        action = "findvideos"
       
    matches = re.compile(patron,re.DOTALL).findall(data)
    for scrapedmsg, scrapedurl,scrapedtitle in matches:
            scrapedmsg = scrapedmsg.replace("msg_","msg=")
            url = urlparse.urljoin(item.url,scrapedurl)
            scrapedtitle = scrapertools.htmlclean(scrapedtitle)
            title = scrapedtitle
            thumbnail = ""
            plot = scrapedmsg
            # Añade al listado
            itemlist.append( Item(channel=__channel__, action=action, title= title, url=url , thumbnail=thumbnail , plot=plot , folder=True) )
    
    # EXTREA EL LINK DE LA SIGUIENTE PAGINA
    patron = '<div class="pagelinks">Páginas:.*?\[<strong>[^<]+</strong>\].*?<a class="navPages" href="(?!\#bot)([^"]+)">[^<]+</a>.*?</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for match in matches:
        if len(matches) > 0:
            url = match
            title = ">> Página Siguiente"
            thumbnail = ""
            plot = ""
            # Añade al listado
            itemlist.append( Item(channel=__channel__, action="foro", title=title , url=url , thumbnail=thumbnail , plot=plot , folder=True) )
    return itemlist


    
def findvideos(item):
  logger.info("channels.megahd findvideos url="+item.url+", title="+item.title)

  show = item.title.replace("Añadir esta serie a la biblioteca de XBMC","")
  data = scrapertools.cache_page(item.url)

  itemlist=[]
	
  if '?action=thankyou;'+item.plot in data:
    logger.info("channels.megahd findvideos thankyou needed")
    item.plot = item.plot.replace("msg=","?action=thankyou;msg=")
    item.url = item.url + item.plot
    data = scrapertools.cache_page(item.url)

  logger.info("data="+data)
		
  if 'MegaHD' in data:
    patronimage = '<div class="inner" id="msg_\d{1,9}".*?<img src="([^"]+)".*?mega.co.nz/\#\![A-Za-z0-9\-\_]+\![A-Za-z0-9\-\_]+'
    matches = re.compile(patronimage,re.DOTALL).findall(data)
    if len(matches)>0:
      thumbnail = matches[0]
      thumbnail = scrapertools.htmlclean(thumbnail)
      thumbnail = unicode( thumbnail, "iso-8859-1" , errors="replace" ).encode("utf-8")
      item.thumbnail = thumbnail
   
    from servers import servertools
    itemlist.extend(servertools.find_video_items(data=data))
    for videoitem in itemlist:
     videoitem.channel=__channel__
     videoitem.action="play"
     videoitem.folder=False
     videoitem.thumbnail=item.thumbnail
     videoitem.show = show
    if config.get_platform().startswith("xbmc") or config.get_platform().startswith("boxee"):
       itemlist.append( Item(channel=item.channel, title="Añadir esta serie a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="findvideos") )
    return itemlist   
  else:
    item.thumbnail = ""
    item.plot = ""
    from servers import servertools
    itemlist.extend(servertools.find_video_items(data=data))
    for videoitem in itemlist:
     videoitem.channel=__channel__
     videoitem.action="play"
     videoitem.folder=False
     videoitem.thumbnail=item.thumbnail
    return itemlist  

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    # Navega hasta la lista de películas
    mainlist_items = mainlist(Item())
    menupeliculas_items = menupeliculas(mainlist_items[0])
    peliculas_items = peliculas(menupeliculas_items[0])
    # Si encuentra algún enlace, lo da por bueno
    for pelicula_item in peliculas_items:
        itemlist = findbitly_link(pelicula_item)
        if not itemlist is None and len(itemlist)>=0:
            return True
    return False

    