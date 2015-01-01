# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para mcanime
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os,sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "mcanime"
__category__ = "A"
__type__ = "generic"
__title__ = "MCAnime"
__language__ = "ES"

DEBUG = config.get_setting("debug")


def isGeneric():
    return True

def mainlist(item):
    logger.info("[gnula.py] mainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Novedades"                            , action="home"       ,url="http://www.mcanime.net/"))
    itemlist.append( Item(channel=__channel__, title="Foro anime en línea"                  , action="forum"      ,url="http://www.mcanime.net/foro/viewforum.php?f=113"))
    itemlist.append( Item(channel=__channel__, title="Descarga directa - Novedades"         , action="ddnovedades",url="http://www.mcanime.net/descarga_directa/anime"))
    itemlist.append( Item(channel=__channel__, title="Descarga directa - Listado alfabético", action="ddalpha"    ,url="http://www.mcanime.net/descarga_directa/anime"))
    itemlist.append( Item(channel=__channel__, title="Descarga directa - Categorías"        , action="ddcat"      ,url="http://www.mcanime.net/descarga_directa/anime"))
    itemlist.append( Item(channel=__channel__, title="Enciclopedia - Estrenos"              , action="estrenos"   ,url="http://www.mcanime.net/enciclopedia/estrenos/anime"))
    return itemlist

def estrenos(item):
    logger.info("[mcanime.py] estrenos")
    itemlist=[]
    
    # Descarga la p·gina
    data = scrapertools.cache_page(item.url)
    #logger.info(data)

    # Extrae las entradas (carpetas)
    '''
    <dl id="addRow9203" class="min row1">
    <dd class="thumb">    
    <img src="/images/anime/th_9203.jpg" width="75" height="100" alt="" />
    </dd>
    <dt><a href="/enciclopedia/anime/cobra_the_animation_rokunin_no_yuushi/9203">Cobra The Animation: Rokunin no Yuushi</a> <i>(Serie)</i></dt>
    <dd>Cobra es un conocido pirata espacial, pero decide cambiar su cara y borrar todas sus memorias. El ahora es un hombre normal, con un trabajo normal y una vida aburrida, pero comienza a recordar su verdadera identidad y sus aventuras comienzan de nuevo. <a href="/enciclopedia/anime/cobra_the_animation_rokunin_no_yuushi/9203">leer m·s.</a></dd>
    <dd class="small mgn"><a href="/descarga_directa/anime/cobra_the_animation_rokunin_no_yuushi/9203" class="srch_dd">Descargar&nbsp;&nbsp;<img width="14" height="14" src="/images/dds/download_icon.gif" alt="[DD]" /></a></dd>                </dl>
    '''
    patron = '<dl id="[^"]+" class="min row.">(.*?)</dl>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for match in matches:
        data = match
        patron  = '<dd class="thumb">[^<]+'
        patron += '<img src="([^"]+)"[^>]+>[^<]+'
        patron += '</dd>[^<]+'
        patron += '<dt><a href="[^"]+">([^<]+)</a>\s*<i>([^<]+)</i>\s*</dt>[^<]+'
        matches2 = re.compile(patron,re.DOTALL).findall(data)
        if len(matches2)>0:
            scrapedtitle = matches2[0][1].strip() + " " + matches2[0][2].strip()
            scrapedthumbnail = urlparse.urljoin(item.url,matches2[0][0])
            scrapedplot = ""
            scrapedurl = ""
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        patron = '</dt>(.*?)<dd class="small mgn"><a href="([^"]+)"'
        matches2 = re.compile(patron,re.DOTALL).findall(data)
        if len(matches2)>0:
            try:
                scrapedplot = unicode( matches2[0][0].strip(), "utf-8" ).encode("iso-8859-1")
            except:
                scrapedplot = matches2[0][0].strip()
            scrapedplot = scrapertools.htmlclean(scrapedplot)
            scrapedplot = scrapedplot.replace("\n"," ")
            scrapedplot = scrapedplot.replace("\r"," ")
            scrapedplot = scrapedplot.replace("\r\n"," ")
            
            scrapedurl = urlparse.urljoin(item.url,matches2[0][1])

        # AÒade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action='ddseriedetail', title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True ) )

    return itemlist

def home(item):
    logger.info("[mcanime.py] home")
    itemlist=[]
    
    # Descarga la p·gina
    data = scrapertools.cache_page(item.url)
    #logger.info(data)

    # Extrae las entradas (carpetas)
    patronvideos  = '<div class="release" style="background-image.url\(\'([^\']+)\'\)\;">[^<]+'
    patronvideos += '<h4>([^<]+)<a href="([^"]+)">([^<]+)</a> <span class="date">([^<]+)</span></h4>[^<]+'
    patronvideos += '<div class="rimg"><img src="([^"]+)"[^>]+></div>[^<]+'
    patronvideos += '<div class="rtext">(.*?)</div>[^<]+'
    patronvideos += '<div class="rfinfo">(.*?)</div>[^<]+'
    patronvideos += '<div class="rflinks">(.*?)</div>[^<]+'
    patronvideos += '<div class="rinfo">(.*?)</div>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        if match[0].endswith("anime.gif"):
            scrapedtitle = match[3].strip() + " " + match[1].strip() + " (" + match[4] + ")"
            scrapedurl = urlparse.urljoin(item.url,match[2])
            scrapedthumbnail = urlparse.urljoin(item.url,match[5])
            scrapedplot = scrapertools.htmlclean(match[6])
            scrapedextra = match[8]
            scrapedtitle = scrapedtitle.replace("[CR]"," CR ")
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
            itemlist.append( Item(channel=__channel__, action='findvideos', title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra = scrapedextra , folder=True ) )

    # Extrae la marca de siguiente p·gina
    patronvideos = '<span class="next"><a href="([^"]+)">Anteriores</a>...</span>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedtitle = "P·gina siguiente"
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append( Item(channel=__channel__, action='home', title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True ) )

    return itemlist

def ddnovedades(item):
    logger.info("[mcanime.py] ddnovedades")
    itemlist=[]
    
    # Descarga la p·gina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)
    patronvideos  = '<ul class="dd_row">[^<]+'
    patronvideos += '<li class="dd_type dd_anime"><img[^>]+></li>[^<]+'
    patronvideos += '<li class="dd_update"><img[^>]+>([^<]+)</li>[^<]+'
    patronvideos += '<li class="dd_update"><a[^>]+>[^<]+</a></li>[^<]+'
    patronvideos += '<li class="dd_title">[^<]+'
    patronvideos += '<h5><a href="([^"]+)">([^<]+)</a></h5>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        # Atributos
        scrapedtitle = match[2].strip() + " ("+match[0].strip()+")"
        scrapedurl = urlparse.urljoin(item.url,match[1])
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action='ddpostdetail', title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True ) )

    # Extrae la marca de siguiente p·gina
    patronvideos = '<span class="current">[^<]+</span><a href="([^"]+)">[^<]+</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedtitle = ">> Pagina siguiente"
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append( Item(channel=__channel__, action='ddnovedades', title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True ) )

    return itemlist

def ddalpha(item):
    logger.info("[mcanime.py] ddalpha")
    itemlist=[]
    
    # Descarga la p·gina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)
    patronvideos  = '<a href="(/descarga_directa/anime/lista/[^"]+)">([^<]+)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        # Atributos
        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action='ddlist', title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True ) )

    return itemlist

def ddcat(item):
    logger.info("[mcanime.py] ddcat")
    itemlist=[]
    
    # Descarga la p·gina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)
    patronvideos  = '<a href="(/descarga_directa/anime/genero/[^"]+)">([^<]+)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        # Atributos
        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # AÒade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action='ddlist', title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True ) )

    return itemlist

def ddlist(item):
    logger.info("[mcanime.py] ddlist")
    itemlist=[]
    
    # Descarga la p·gina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)
    patronvideos  = '<li class="dd_title"><h5><a href="([^"]+)">(.*?)</a>\s*<i>([^<]+)</i>\s*</h5></li>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        # Atributos
        scrapedtitle = match[1].strip().replace("<b>","").replace("</b>","")
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # AÒade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action='ddseriedetail', title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True ) )

    return itemlist

def ddseriedetail(item):
    logger.info("[mcanime.py] ddseriedetail")
    itemlist=[]
    
    # Descarga la p·gina
    data = scrapertools.cache_page(item.url)

    # Foto de la serie de la enciclopedia
    patron = '<img src="([^"]+)" width="300".*?class="title_pic" />'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        item.thumbnail = matches[0]

    # Argumento
    patron = '<h6>Sinopsis.*?</h6>(.*?)<h6>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        item.plot = matches[0]
        item.plot = item.plot.replace("\n"," ")
        item.plot = item.plot.replace("\r"," ")
        item.plot = item.plot.replace("\r\n"," ")
        item.plot = item.plot.strip()
        item.plot = scrapertools.htmlclean(matches[0])

    # Fansubs
    patron  = '<h6 class="m">Fansubs que trabajan esta serie</h6>[^<]+'
    patron += '<div id="user_actions">(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    if len(matches)>0:
        data = matches[0]
        #logger.info("[mcanime.py] data="+data)
        patron = '<ul class="dd_row">[^<]+'
        patron += '<li class="dd_type"><img[^>]+></li>[^<]+'
        patron += '<li class="dd_update"> <img[^>]+>([^<]+)</li>[^<]+'
        patron += '<li class="dd_title">[^<]+'
        patron += '<h5><a href="([^"]+)">([^<]+)</a></h5>'
        matches = re.compile(patron,re.DOTALL).findall(data)

        for match in matches:
            # Atributos
            scrapedtitle = match[2].strip()+" ("+match[0].strip()+")"
            scrapedurl = urlparse.urljoin(item.url,match[1])
            scrapedthumbnail = item.thumbnail
            scrapedplot = item.plot
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

            # AÒade al listado de XBMC
            itemlist.append( Item(channel=__channel__, action='ddpostdetail', title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True ) )
    
    # Aportaciones de los usuarios
    patron  = '<h6 class="m">Por los Usuarios</h6>[^<]+'
    patron += '<div id="user_actions">(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    if len(matches)>0:
        data = matches[0]
        #logger.info("[mcanime.py] data="+data)
        patron = '<ul class="dd_row">[^<]+'
        patron += '<li class="dd_type"><img[^>]+></li>[^<]+'
        patron += '<li class="dd_update"> <img[^>]+>([^<]+)</li>[^<]+'
        patron += '<li class="dd_title">[^<]+'
        patron += '<h5><a href="([^"]+)">([^<]+)</a></h5>'
        matches = re.compile(patron,re.DOTALL).findall(data)

        for match in matches:
            # Atributos
            scrapedtitle = match[2].strip()+" ("+match[0].strip()+")"
            scrapedurl = urlparse.urljoin(item.url,match[1])
            scrapedthumbnail = item.thumbnail
            scrapedplot = item.plot
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

            # AÒade al listado de XBMC
            itemlist.append( Item(channel=__channel__, action='ddpostdetail', title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True ) )

    return itemlist

def ddpostdetail(item):
    logger.info("[mcanime.py] ddpostdetail")
    itemlist=[]
    
    # Descarga la p·gina
    data = scrapertools.cache_page(item.url)
    #logger.info(data)

    # Foto de la serie de la enciclopedia
    patron = '<img src="([^"]+)" width="300".*?class="title_pic" />'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        item.thumbnail = matches[0]
    
    # Argumento - texto del post
    patron = '<div id="download_detail">(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        item.plot = scrapertools.htmlclean(matches[0])
        item.plot = item.plot.replace("\r\n"," ")
        item.plot = item.plot.replace("\r"," ")
        item.plot = item.plot.replace("\n"," ")
        item.plot = item.plot.strip()

    # ------------------------------------------------------------------------------------
    # Busca los enlaces a los videos
    # ------------------------------------------------------------------------------------
    i = 1
    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        videoitem.channel = __channel__
        videoitem.action="play"
        videoitem.folder=False
        try:
            fulltitle = unicode( item.title.strip() + " (%d) " + videoitem.title, "utf-8" ).encode("iso-8859-1")
            fulltitle = fulltitle % i
        except:
            validchars = " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!#$&'()-@^_`."
            stripped = ''.join(c for c in item.title if c in validchars)
            fulltitle = stripped.strip() + " (%d) " + videoitem.title
            fulltitle = fulltitle % i
        i = i + 1

    return itemlist

def forum(item):
    logger.info("[mcanime.py] forum")
    itemlist=[]
    
    # Descarga la p·gina
    data = scrapertools.cache_page(item.url)
    #logger.info(data)

    # Extrae las entradas del foro (series / pelis)
    patronvideos  = '<ul class="topic_row">[^<]+<li class="topic_type"><img.*?'
    patronvideos += '<li class="topic_title"><h5><a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        # Extrae
        try:
            scrapedtitle = unicode( match[1], "utf-8" ).encode("iso-8859-1")
        except:
            scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin(item.url,match[0].replace("&amp;","&"))
        scrapedthumbnail = ""
        scrapedplot = ""

        # Depuracion
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # AÒade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action='forumdetail', title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True ) )

    # Extrae la siguiente p·gina
    patronvideos  = '<a href="([^"]+)" class="next">(Siguiente &raquo;)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = "P·gina siguiente"
        scrapedurl = urlparse.urljoin(item.url,match[0].replace("&amp;","&"))
        scrapedthumbnail = ""
        scrapedplot = ""

        # Depuracion
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        
        # AÒade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action='forum', title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True ) )

    return itemlist

def forumdetail(item):
    logger.info("[mcanime.py] forumdetail")
    itemlist=[]
    
    # Descarga la p·gina
    data = scrapertools.cache_page(item.url)
    #logger.info(data)

    # ------------------------------------------------------------------------------------
    # Busca los enlaces a los mirrors, paginas, o capÌtulos de las series...
    # ------------------------------------------------------------------------------------
    patronvideos  = '([^"]+)" class="next">Siguiente'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    for match in matches:
        logger.info("Encontrada pagina siguiente")
        itemlist.append( Item(channel=__channel__, action='list', title=">> Página siguiente" , url=urlparse.urljoin(item.url,match).replace("&amp;","&") , folder=True ) )

    # ------------------------------------------------------------------------------------
    # Busca los enlaces a los videos
    # ------------------------------------------------------------------------------------
    # Saca el cuerpo del post
    #logFile.info("data="+data)
    #patronvideos  = '<div class="content">.*?<div class="poster">.*?</div>(.*?)</div>'
    patronvideos  = '<div class="content">(.*?)<div class="content">'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    datapost=""
    if len(matches)>0:
        datapost=matches[0]
    else:
        datapost = ""
    #logFile.info("dataPost="+dataPost)

    # Saca el thumbnail
    patronvideos  = '<img src="([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(datapost)
    thumbnailurl=""
    logger.info("thumbnails")
    for match in matches:
        logger.info(match)
    if len(matches)>0:
        thumbnailurl=matches[0]

    patronvideos  = '<img.*?>(.*?)<a'
    matches = re.compile(patronvideos,re.DOTALL).findall(datapost)
    descripcion = ""
    if len(matches)>0:
        descripcion = matches[0]
        descripcion = descripcion.replace("<br />","")
        descripcion = descripcion.replace("<br/>","")
        descripcion = descripcion.replace("\r","")
        descripcion = descripcion.replace("\n"," ")
        descripcion = re.sub("<[^>]+>"," ",descripcion)
    logger.info("descripcion="+descripcion)
    
    itemlist.extend( servertools.find_video_items(data=datapost) )

    for video in itemlist:
        if video.folder==False:
            video.channel = __channel__
            video.title = re.sub("<[^>]+>","",item.title)
            video.action = "play"

    return itemlist


# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    novedades_items = home(mainlist_items[0])
    bien = False
    for novedad_item in novedades_items:
        mirrors = servertools.find_video_items( item=novedad_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien