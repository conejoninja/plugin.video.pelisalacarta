# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para peliculasyonkis
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# Adaptado por Boludiko basado en el canal seriesyonkis V9 Por Truenon y Jesus
# v11
#------------------------------------------------------------
import urlparse,urllib2,urllib,re

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "peliculasyonkis_generico"
__category__ = "F"
__type__ = "generic"
__title__ = "Peliculasyonkis"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[peliculasyonkis_generico.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="lastepisodes"   , title="Utimas Peliculas" , url="http://www.peliculasyonkis.sx"))
    itemlist.append( Item(channel=__channel__, action="listalfabetico" , title="Listado alfabetico", url="http://www.peliculasyonkis.sx/lista-de-peliculas"))
    itemlist.append( Item(channel=__channel__, action="listcategorias" , title="Listado por Categorias",url="http://www.peliculasyonkis.sx/") )

    return itemlist

def listcategorias(item):
    logger.info("[peliculasyonkis_generico.py] listcategorias")
    itemlist=[]
    # Descarga la pagina
    data = scrapertools.cachePage(item.url)
    data = scrapertools.find_single_match(data,"<h2>Géneros</h2>(.*?)</ul>")
    logger.info("data="+data)
    
    # Extrae las entradas (carpetas)
    #<li><a href="http://www.peliculasyonkis.sx/genero/fantastico/" title="Listado del género Fantástico"><span>Fantástico</span>
    patronvideos  = '<li><a href="([^"]+)"[^>]+><span>([^<]+)</span>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = match[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item ( channel=__channel__ , action="peliculascat" , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot ) )

    return itemlist
   
def peliculascat(item):
    logger.info("[peliculasyonkis_generico.py] series")
    itemlist = []

    data = scrapertools.cachePage(item.url)
   
    #Paginador
    matches = re.compile('<div class="paginator">.*?<a href="([^"]+)">&gt;</a>.*?</div>', re.S).findall(data)
    if len(matches)>0:
        paginador = Item(channel=__channel__, action="peliculascat" , title="!Pagina siguiente" , url=urlparse.urljoin(item.url,matches[0]), thumbnail=item.thumbnail, plot="", extra = "" , show=item.show)
    else:
        paginador = None
    
    if paginador is not None:
        itemlist.append( paginador )

    matches = re.compile('<li class=.*?title="([^"]+)" href="([^"]+)".*?</li>', re.S).findall(data)
    #scrapertools.printMatches(matches)

    for match in matches:
        itemlist.append( Item(channel=__channel__, action="findvideos" , title=match[0] , fulltitle=match[0], url=urlparse.urljoin(item.url,match[1]), thumbnail="", plot="", extra = "" , show=match[1] ))

    if paginador is not None:
        itemlist.append( paginador )

    return itemlist
   
def search(item,texto):
    logger.info("[peliculasyonkis_generico.py] search")
    itemlist = []

    if item.url=="":
        item.url = "http://www.peliculasyonkis.sx/buscar/pelicula"
    url = "http://www.peliculasyonkis.sx/buscar/pelicula" # write ur URL here
    post = 'keyword='+texto[0:18]+'&search_type=pelicula'
    
    data = scrapertools.cache_page(url,post=post)
    
    import seriesyonkis
    itemlist = seriesyonkis.getsearchresults(item, data, "findvideos")
    for item in itemlist:
        item.channel=__channel__

    return itemlist

def lastepisodes(item):
    logger.info("[peliculasyonkis_generico.py] lastepisodes")

    data = scrapertools.cache_page(item.url)

    patron  = '<li class="thumb-episode"[^<]+'
    patron += '<a title="([^"]+)" href="([^"]+)"[^<]+'
    patron += '<img width="\d+" height="\d+" src="([^"]+)"'
    matches = re.compile(patron, re.S).findall(data)
    #scrapertools.printMatches(matches)
    itemlist = []
    for match in matches:               
        scrapedtitle = match[0] 
        scrapedurl = urlparse.urljoin(item.url,match[1])
        scrapedthumbnail = urlparse.urljoin(item.url,match[2])
        scrapedplot = ""

        # Depuracion
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")            
        itemlist.append( Item(channel=__channel__, action="findvideos" , title=scrapedtitle , fulltitle=scrapedtitle, url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle, context="4|5"))

    return itemlist  

def mostviewed(item):
    logger.info("[peliculasyonkis_generico.py] mostviewed")
    data = scrapertools.cachePage(item.url)

    matches = re.compile('<li class="thumb-episode"> <a href="([^"]+)" title="([^"]+)".*?src="([^"]+)".*?</li>', re.S).findall(data)
    #scrapertools.printMatches(matches)
    itemlist = []
    for match in matches:               
        scrapedtitle = match[1] 
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = urlparse.urljoin(item.url,match[2])
        scrapedplot = ""

        # Depuracion
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")            
        itemlist.append( Item(channel=__channel__, action="findvideos" , title=scrapedtitle , fulltitle=scrapedtitle, url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle))

    return itemlist

def peliculas(item):
    logger.info("[peliculasyonkis_generico.py] series")
    itemlist = []

    data = scrapertools.cachePage(item.url)
   
    #Paginador
    matches = re.compile('<div class="paginator">.*?<a href="([^"]+)">&gt;</a>.*?</div>', re.S).findall(data)
    if len(matches)>0:
        paginador = Item(channel=__channel__, action="peliculas" , title="!Pagina siguiente" , url=urlparse.urljoin(item.url,matches[0]), thumbnail=item.thumbnail, plot="", extra = "" , show=item.show)
    else:
        paginador = None
    
    if paginador is not None:
        itemlist.append( paginador )

    #<div id="main-section" class="lista-series">.*?</div>
    #matches = re.compile('<div id="main-section" class="lista-series">.*?</div>', re.S).findall(data)
    matches = re.compile('<ul id="list-container".*?</ul>', re.S).findall(data)    
    #scrapertools.printMatches(matches)
    for match in matches:
        data=match
        break
    
    #<li><a href="/serie/al-descubierto" title="Al descubierto">Al descubierto</a></li>
    matches = re.compile('<li>.*?href="([^"]+)".*?title="([^"]+)".*?</li>', re.S).findall(data)
    #scrapertools.printMatches(matches)

    for match in matches:
        itemlist.append( Item(channel=__channel__, action="findvideos" , title=match[1] , fulltitle=match[1], url=urlparse.urljoin(item.url,match[0]), thumbnail="", plot="", extra = "" , show=match[1] ))

    if paginador is not None:
        itemlist.append( paginador )

    return itemlist

def findvideos(item):
    logger.info("[peliculasyonkis_generico.py] findvideos")
    itemlist = []

    data = scrapertools.cachePage(item.url)

    #<tr>
    #<td class="episode-server" data-value="0">
    #<a href="http://www.peliculasyonkis.sx/enlace.php?t=1&p=Sr+y+Sra+Smith&h=allmyvideos_net&u=http%3A%2F%2Fallmyvideos.net%2Fy6tgdqihnmj3" title="" target="_blank" rel="nofollow">
    #<img src="http://www.peliculasyonkis.sx/wp-content/themes/SeriesYonkis/img/veronline.png" alt="Ver Online" height="22" width="22"> Reproducir</a>
    #<span class="public_sprite like_green vote_link_positive" title="Voto positivo">[positivo]</span>
    #<span class="public_sprite dislike_red vote_link_negative" title="Voto negativo">[negativo]</span>
    #</td>
    #<td class="episode-uploader"><span title="Anónimo">Anónimo</span></td>
    #<td class="episode-server-img">
    #<a href="http://www.peliculasyonkis.sx/enlace.php?t=1&p=Sr+y+Sra+Smith&h=allmyvideos_net&u=http%3A%2F%2Fallmyvideos.net%2Fy6tgdqihnmj3" title="" target="_blank" rel="nofollow">
    #<span class="server allmyvideos_net"></span>
    #</a>
    #</td>
    #<td class="episode-lang">
    #<span class="flags es" title="Español">Español</span>
    #</td>
    #<td class="episode-error bug center"><a href="#" class="errorlink"><img src="http://www.peliculasyonkis.sx/wp-content/themes/SeriesYonkis/img/bug.png" alt="error"></a></td>
    #</tr>

    patron = '<td class="episode-server" data-value="0">.*?'
    patron+= 'href="[^&]+&p=([^&]+)&h=([^&]+)&u=([^"]+)" title="" target="_blank" rel="nofollow">.*?'
    patron+= 'alt="([^"]+)".*?'
    patron+= '<span class="flags[^>]+>([^<]+)</span>.*?'

    matches = re.compile(patron,re.DOTALL).findall(data)

    for title,server,url,medio,idioma in matches:

        title = urllib.unquote(title).replace("+"," ")
        server = server.split("_")
        if len(server)>2: server = server[1]
        else: server = server[0]

        url = urllib.unquote(url)

        title = medio + " " + title + " en " + server + " " + idioma
        itemlist.append( Item(channel=__channel__, action="play" , title=title , url=url, thumbnail=item.thumbnail, plot=item.plot, folder=False))

    return itemlist

def play(item):
    logger.info("[peliculasyonkis_generico.py] play")

    #data = scrapertools.cache_page(item.url)

    itemlist = servertools.find_video_items(data=item.url)

    for videoitem in itemlist:
        videoitem.title = item.title
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist    

def listalfabetico(item):
    logger.info("[peliculasyonkis_generico.py] listalfabetico")
       
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="A"  , url="http://www.peliculasyonkis.sx/search/listado-A"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="B"  , url="http://www.peliculasyonkis.sx/search/listado-B"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="C"  , url="http://www.peliculasyonkis.sx/search/listado-C"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="D"  , url="http://www.peliculasyonkis.sx/search/listado-D"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="E"  , url="http://www.peliculasyonkis.sx/search/listado-E"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="F"  , url="http://www.peliculasyonkis.sx/search/listado-F"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="G"  , url="http://www.peliculasyonkis.sx/search/listado-G"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="H"  , url="http://www.peliculasyonkis.sx/search/listado-H"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="I"  , url="http://www.peliculasyonkis.sx/search/listado-I"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="J"  , url="http://www.peliculasyonkis.sx/search/listado-J"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="K"  , url="http://www.peliculasyonkis.sx/search/listado-K"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="L"  , url="http://www.peliculasyonkis.sx/search/listado-L"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="M"  , url="http://www.peliculasyonkis.sx/search/listado-M"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="N"  , url="http://www.peliculasyonkis.sx/search/listado-N"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="O"  , url="http://www.peliculasyonkis.sx/search/listado-O"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="P"  , url="http://www.peliculasyonkis.sx/search/listado-P"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Q"  , url="http://www.peliculasyonkis.sx/search/listado-Q"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="R"  , url="http://www.peliculasyonkis.sx/search/listado-R"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="S"  , url="http://www.peliculasyonkis.sx/search/listado-S"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="T"  , url="http://www.peliculasyonkis.sx/search/listado-T"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="U"  , url="http://www.peliculasyonkis.sx/search/listado-U"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="V"  , url="http://www.peliculasyonkis.sx/search/listado-V"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="W"  , url="http://www.peliculasyonkis.sx/search/listado-W"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="X"  , url="http://www.peliculasyonkis.sx/search/listado-X"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Y"  , url="http://www.peliculasyonkis.sx/search/listado-Y"))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Z"  , url="http://www.peliculasyonkis.sx/search/listado-Z"))

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    episode_items = lastepisodes(mainlist_items[0])
    bien = False
    for episode_item in episode_items:
        mediaurls = findvideos( episode_item )
        if len(mediaurls)>0:
            return True

    return False