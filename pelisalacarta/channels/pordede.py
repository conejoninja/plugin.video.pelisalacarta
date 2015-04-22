# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para pordede
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
__title__ = "Pordede"
__channel__ = "pordede"
__language__ = "ES"
__creationdate__ = "20140615"

DEFAULT_HEADERS = []
DEFAULT_HEADERS.append( ["User-Agent","Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; es-ES; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12"] )
DEFAULT_HEADERS.append( ["Referer","http://www.pordede.com"] )

def isGeneric():
    return True

def login():
    url = "http://www.pordede.com/site/login"
    post = "LoginForm[username]="+config.get_setting("pordedeuser")+"&LoginForm[password]="+config.get_setting("pordedepassword")
    headers = DEFAULT_HEADERS[:]
    data = scrapertools.cache_page(url,headers=headers,post=post)

def mainlist(item):
    logger.info("pelisalacarta.channels.pordede mainlist")

    itemlist = []

    if config.get_setting("pordedeaccount")!="true":
        itemlist.append( Item( channel=__channel__ , title="Habilita tu cuenta en la configuración..." , action="openconfig" , url="" , folder=False ) )
    else:
        login()
        itemlist.append( Item(channel=__channel__, action="menuseries"    , title="Series"              , url="" ))
        itemlist.append( Item(channel=__channel__, action="menupeliculas" , title="Películas"           , url="" ))
        itemlist.append( Item(channel=__channel__, action="listas_sigues" , title="Listas que sigues"   , url="http://www.pordede.com/lists/following" ))
        itemlist.append( Item(channel=__channel__, action="tus_listas"    , title="Tus listas"          , url="http://www.pordede.com/lists/yours" ))
        itemlist.append( Item(channel=__channel__, action="listas_sigues" , title="Top listas"          , url="http://www.pordede.com/lists" ))
       
    return itemlist

def openconfig(item):
    if "xbmc" in config.get_platform() or "boxee" in config.get_platform():
        config.open_settings( )
    return []

def menuseries(item):
    logger.info("pelisalacarta.channels.pordede menuseries")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Novedades"            , url="http://www.pordede.com/series/loadmedia/offset/0/showlist/hot" ))
    itemlist.append( Item(channel=__channel__, action="generos"   , title="Por géneros"          , url="http://www.pordede.com/series" ))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Siguiendo"            , url="http://www.pordede.com/series/following" ))
    itemlist.append( Item(channel=__channel__, action="siguientes" , title="Siguientes Capítulos" , url="http://www.pordede.com/index2.php" ))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Favoritas"            , url="http://www.pordede.com/series/favorite" ))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Pendientes"           , url="http://www.pordede.com/series/pending" ))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Terminadas"           , url="http://www.pordede.com/series/seen" ))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Recomendadas"         , url="http://www.pordede.com/series/recommended" ))
    itemlist.append( Item(channel=__channel__, action="search"    , title="Buscar..."            , url="http://www.pordede.com/series" ))
  
    return itemlist

def menupeliculas(item):
    logger.info("pelisalacarta.channels.pordede menupeliculas")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Novedades"            , url="http://www.pordede.com/pelis/loadmedia/offset/0/showlist/hot" ))
    itemlist.append( Item(channel=__channel__, action="generos" , title="Por géneros"            , url="http://www.pordede.com/pelis" ))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Favoritas"            , url="http://www.pordede.com/pelis/favorite" ))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Pendientes"           , url="http://www.pordede.com/pelis/pending" ))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Vistas"               , url="http://www.pordede.com/pelis/seen" ))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Recomendadas"         , url="http://www.pordede.com/pelis/recommended" ))
    itemlist.append( Item(channel=__channel__, action="search"  , title="Buscar..."              , url="http://www.pordede.com/pelis" ))
  
    return itemlist

def generos(item):
    logger.info("pelisalacarta.channels.pordede generos")

    headers = DEFAULT_HEADERS[:]
    
    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)
    if (DEBUG): logger.info("data="+data)

    # Extrae las entradas (carpetas)
    data = scrapertools.find_single_match(data,'<div class="section genre">(.*?)</div>')
    patron  = '<a class="mediaFilterLink" data-value="([^"]+)" href="([^"]+)">([^<]+)<span class="num">\((\d+)\)</span></a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for textid,scrapedurl,scrapedtitle,cuantos in matches:
        title = scrapedtitle.strip()+" ("+cuantos+")"
        thumbnail = ""
        plot = ""
        #http://www.pordede.com/pelis/loadmedia/offset/30/genre/science%20fiction/showlist/all?popup=1
        if "/pelis" in item.url:
            url = "http://www.pordede.com/pelis/loadmedia/offset/0/genre/"+textid.replace(" ","%20")+"/showlist/all"
        else:
            url = "http://www.pordede.com/series/loadmedia/offset/0/genre/"+textid.replace(" ","%20")+"/showlist/all"
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="peliculas" , title=title , url=url, thumbnail=thumbnail, plot=plot, fulltitle=title))

    return itemlist

def search(item,texto):
    logger.info("pelisalacarta.channels.pordede search")

    if item.url=="":
        item.url="http://www.pordede.com/pelis"

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

def buscar(item):
    logger.info("pelisalacarta.channels.pordede buscar")

    # Descarga la pagina
    headers = DEFAULT_HEADERS[:]
    #headers.append(["Referer",item.extra])
    headers.append(["X-Requested-With","XMLHttpRequest"])
    data = scrapertools.cache_page(item.url,headers=headers)
    if (DEBUG): logger.info("data="+data)

    # Extrae las entradas (carpetas)  
    json_object = jsontools.load_json(data)
    if (DEBUG): logger.info("html="+json_object["html"])
    data = json_object["html"]

    return parse_mixed_results(item,data)

def parse_mixed_results(item,data):
    patron  = '<a class="defaultLink extended" href="([^"]+)"[^<]+'
    patron += '<div class="coverMini shadow tiptip" title="([^"]+)"[^<]+'
    patron += '<img class="centeredPic.*?src="([^"]+)"'
    patron += '[^<]+<img[^<]+<div class="extra-info">'
    patron += '<span class="year">([^<]+)</span>'
    patron += '<span class="value"><i class="icon-star"></i>([^<]+)</span>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []

    for scrapedurl,scrapedtitle,scrapedthumbnail,scrapedyear,scrapedvalue in matches:
        title = scrapertools.htmlclean(scrapedtitle)
        if scrapedyear != '':
            title += " ("+scrapedyear+")"
        if scrapedvalue != '':
            title += " ("+scrapedvalue+")"
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        plot = ""
        #http://www.pordede.com/peli/the-lego-movie
        #http://www.pordede.com/links/view/slug/the-lego-movie/what/peli?popup=1

        if "/peli/" in scrapedurl:
            referer = urlparse.urljoin(item.url,scrapedurl)
            url = referer.replace("/peli/","/links/view/slug/")+"/what/peli"
            if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
            itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , extra=referer, url=url, thumbnail=thumbnail, plot=plot, fulltitle=title, viewmode="movie"))
        else:
            referer = item.url
            url = urlparse.urljoin(item.url,scrapedurl)
            itemlist.append( Item(channel=__channel__, action="episodios" , title=title , extra=referer, url=url, thumbnail=thumbnail, plot=plot, fulltitle=title, show=title, viewmode="movie"))

    if "offset/" in item.url:
        old_offset = scrapertools.find_single_match(item.url,"offset/(\d+)/")
        new_offset = int(old_offset)+30
        url = item.url.replace("offset/"+old_offset,"offset/"+str(new_offset))
        itemlist.append( Item(channel=__channel__, action="lista" , title=">> Página siguiente" , extra=item.extra, url=url))

    try:
        import xbmcplugin
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_UNSORTED)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
    except:
        pass

    return itemlist

def siguientes(item):
    logger.info("pelisalacarta.channels.pordede siguientes")

    # Descarga la pagina
    headers = DEFAULT_HEADERS[:]
    #headers.append(["Referer",item.extra])
    headers.append(["X-Requested-With","XMLHttpRequest"])

    data = scrapertools.cache_page(item.url,headers=headers)
    if (DEBUG): logger.info("data="+data)

    # Extrae las entradas (carpetas)  
    json_object = jsontools.load_json(data)
    if (DEBUG): logger.info("html2="+json_object["html"])
    data = json_object["html"]
    patron = ''
    patron += '<div class="coverMini shadow tiptip" title="([^"]+)">[^<]+'
    patron += '<img class="centeredPic centeredPicFalse"  onerror="[^"]+"  src="([^"]+)"[^<]+'
    patron += '<img src="/images/loading-mini.gif" class="loader"/>[^<]+'
    patron += '<div class="extra-info"><span class="year">[^<]+'
    patron += '</span><span class="value"><i class="icon-star"></i>[^<]+'
    patron += '</span></div>[^<]+'
    patron += '</div>[^<]+'
    patron += '</a>[^<]+'
    patron += '<a class="userepiinfo defaultLink" href="([^"]+)">(\d+)x(\d+)'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    #for scrapedurl,scrapedtitle,scrapedthumbnail in matches:
    for scrapedtitle,scrapedthumbnail,scrapedurl,scrapedsession,scrapedepisode in matches:
        title = scrapertools.htmlclean(scrapedtitle)
        session = scrapertools.htmlclean(scrapedsession)
        episode = scrapertools.htmlclean(scrapedepisode)
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        plot = ""
        title = session + "x" + episode + " - " + title
        #http://www.pordede.com/peli/the-lego-movie
        #http://www.pordede.com/links/view/slug/the-lego-movie/what/peli?popup=1

        referer = urlparse.urljoin(item.url,scrapedurl)
        url = referer
        #itemlist.append( Item(channel=__channel__, action="episodios" , title=title , url=url, thumbnail=thumbnail, plot=plot, fulltitle=title, show=title, viewmode="movie"))
        itemlist.append( Item(channel=__channel__, action="episodio" , title=title , url=url, thumbnail=thumbnail, plot=plot, fulltitle=title, show=title, viewmode="movie", extra=session+"|"+episode))

        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

    return itemlist

def episodio(item):
    logger.info("pelisalacarta.channels.pordede episodio")
    itemlist = []
    
    headers = DEFAULT_HEADERS[:]

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)
    if (DEBUG): logger.info("data="+data)

    session = str(int(item.extra.split("|")[0]))
    episode = str(int(item.extra.split("|")[1]))
    patrontemporada = '<div class="checkSeason"[^>]+>Temporada '+session+'<div class="right" onclick="controller.checkSeason(.*?)\s+</div></div>'
    matchestemporadas = re.compile(patrontemporada,re.DOTALL).findall(data)

    for bloque_episodios in matchestemporadas:
        if (DEBUG): logger.info("bloque_episodios="+bloque_episodios)

        # Extrae los episodios
        patron  = '<span class="title defaultPopup" href="([^"]+)"><span class="number">'+episode+' </span>([^<]+)</span>(\s*</div>\s*<span[^>]*><span[^>]*>[^<]*</span><span[^>]*>[^<]*</span></span><div[^>]*><button[^>]*><span[^>]*>[^<]*</span><span[^>]*>[^<]*</span></button><div class="action([^"]*)" data-action="seen">)?'
        matches = re.compile(patron,re.DOTALL).findall(bloque_episodios)
        
        for scrapedurl,scrapedtitle,info,visto in matches:
            visto_string = "[visto] " if visto.strip()=="active" else ""
            numero=episode
            title = visto_string+session+"x"+numero+" "+scrapertools.htmlclean(scrapedtitle)
            thumbnail = ""
            plot = ""
            #http://www.pordede.com/peli/the-lego-movie
            #http://www.pordede.com/links/view/slug/the-lego-movie/what/peli?popup=1
            #http://www.pordede.com/links/viewepisode/id/475011?popup=1
            epid = scrapertools.find_single_match(scrapedurl,"id/(\d+)")
            url = "http://www.pordede.com/links/viewepisode/id/"+epid
            itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , url=url, thumbnail=thumbnail, plot=plot, fulltitle=title, show=item.show))
            if (DEBUG): logger.info("Abrimos title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

    itemlist2 = []
    for capitulo in itemlist:
        itemlist2 = findvideos(capitulo)
    return itemlist2

def peliculas(item):
    logger.info("pelisalacarta.channels.pordede peliculas")

    # Descarga la pagina
    headers = DEFAULT_HEADERS[:]
    #headers.append(["Referer",item.extra])
    headers.append(["X-Requested-With","XMLHttpRequest"])
    data = scrapertools.cache_page(item.url,headers=headers)
    if (DEBUG): logger.info("data="+data)

    # Extrae las entradas (carpetas)  
    json_object = jsontools.load_json(data)
    if (DEBUG): logger.info("html="+json_object["html"])
    data = json_object["html"]

    return parse_mixed_results(item,data)

def episodios(item):
    logger.info("pelisalacarta.channels.pordede episodios")
    itemlist = []
    
    headers = DEFAULT_HEADERS[:]

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)
    if (DEBUG): logger.info("data="+data)

    patrontemporada = '<div class="checkSeason"[^>]+>([^<]+)<div class="right" onclick="controller.checkSeason(.*?)\s+</div></div>'
    matchestemporadas = re.compile(patrontemporada,re.DOTALL).findall(data)

    for nombre_temporada,bloque_episodios in matchestemporadas:
        if (DEBUG): logger.info("nombre_temporada="+nombre_temporada)
        if (DEBUG): logger.info("bloque_episodios="+bloque_episodios)

        # Extrae los episodios
        patron  = '<span class="title defaultPopup" href="([^"]+)"><span class="number">([^<]+)</span>([^<]+)</span>(\s*</div>\s*<span[^>]*><span[^>]*>[^<]*</span><span[^>]*>[^<]*</span></span><div[^>]*><button[^>]*><span[^>]*>[^<]*</span><span[^>]*>[^<]*</span></button><div class="action([^"]*)" data-action="seen">)?'
        matches = re.compile(patron,re.DOTALL).findall(bloque_episodios)
        
        for scrapedurl,numero,scrapedtitle,info,visto in matches:
            visto_string = "[visto] " if visto.strip()=="active" else ""
            title = visto_string+nombre_temporada.replace("Temporada ", "").replace("Extras", "Extras 0")+"x"+numero+" "+scrapertools.htmlclean(scrapedtitle)
            thumbnail = ""
            plot = ""
            #http://www.pordede.com/peli/the-lego-movie
            #http://www.pordede.com/links/view/slug/the-lego-movie/what/peli?popup=1
            #http://www.pordede.com/links/viewepisode/id/475011?popup=1
            epid = scrapertools.find_single_match(scrapedurl,"id/(\d+)")
            url = "http://www.pordede.com/links/viewepisode/id/"+epid
            itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , url=url, thumbnail=thumbnail, plot=plot, fulltitle=title, show=item.show))

            if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

    if config.get_platform().startswith("xbmc") or config.get_platform().startswith("boxee"):
        # con año y valoracion la serie no se puede actualizar correctamente, si ademas cambia la valoracion, creara otra carpeta
        # Sin año y sin valoración:
        show = re.sub(r"\s\(\d+\)\s\(\d+\.\d+\)", "", item.show)
        # Sin año:
        #show = re.sub(r"\s\(\d+\)", "", item.show)
        # Sin valoración:
        #show = re.sub(r"\s\(\d+\.\d+\)", "", item.show)
        itemlist.append( Item(channel='pordede', title="Añadir esta serie a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="episodios###", show=show) )
        itemlist.append( Item(channel='pordede', title="Descargar todos los episodios de la serie", url=item.url, action="download_all_episodes", extra="episodios", show=show))

    return itemlist

def parse_listas(item, patron):
    logger.info("pelisalacarta.channels.pordede parse_listas")

    # Descarga la pagina
    headers = DEFAULT_HEADERS[:]
    #headers.append(["Referer",item.extra])
    headers.append(["X-Requested-With","XMLHttpRequest"])
    data = scrapertools.cache_page(item.url,headers=headers)
    if (DEBUG): logger.info("data="+data)

    # Extrae las entradas (carpetas)  
    json_object = jsontools.load_json(data)
    if (DEBUG): logger.info("html="+json_object["html"])
    data = json_object["html"]

    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for scrapedurl,scrapedtitle,scrapeduser,scrapedfichas in matches:
        title = scrapertools.htmlclean(scrapedtitle + ' (' + scrapedfichas + ' fichas, por ' + scrapeduser + ')')
        url = urlparse.urljoin(item.url,scrapedurl) + "/offset/0/loadmedia"
        thumbnail = ""
        itemlist.append( Item(channel=__channel__, action="lista" , title=title , url=url))
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

    nextpage = scrapertools.find_single_match(data,'data-url="(/lists/loadlists/offset/[^"]+)"')
    if nextpage != '':
        url = urlparse.urljoin(item.url,nextpage)
        itemlist.append( Item(channel=__channel__, action="listas_sigues" , title=">> Página siguiente" , extra=item.extra, url=url))

    try:
        import xbmcplugin
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_UNSORTED)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
    except:
        pass

    return itemlist

def listas_sigues(item):
    logger.info("pelisalacarta.channels.pordede listas_sigues")

    patron  = '<div class="clearfix modelContainer" data-model="lista"[^<]+'
    patron += '<span class="title"><span class="name"><a class="defaultLink" href="([^"]+)">([^<]+)</a>'
    patron += '</span>[^<]+<a[^>]+>([^<]+)</a></span>\s+<div[^<]+<div[^<]+</div>\s+<div class="info">\s+<p>([0-9]+)'

    return parse_listas(item, patron)

def tus_listas(item):
    logger.info("pelisalacarta.channels.pordede tus_listas")

    patron  = '<div class="clearfix modelContainer" data-model="lista"[^<]+'
    patron += '<div class="right"[^<]+'
    patron += '<button[^<]+</button[^<]+'
    patron += '<button[^<]+</button[^<]+'
    patron += '</div[^<]+'
    patron += '<span class="title"><span class="name"><a class="defaultLink" href="([^"]+)">([^<]+)</a>'
    patron += '</span>[^<]+<a[^>]+>([^<]+)</a></span>\s+<div[^<]+<div[^<]+</div>\s+<div class="info">\s+<p>([0-9]+)'

    return parse_listas(item, patron)

def lista(item):
    logger.info("pelisalacarta.channels.pordede lista")

    # Descarga la pagina
    headers = DEFAULT_HEADERS[:]
    #headers.append(["Referer",item.extra])
    headers.append(["X-Requested-With","XMLHttpRequest"])
    data = scrapertools.cache_page(item.url,headers=headers)
    if (DEBUG): logger.info("data="+data)

    # Extrae las entradas (carpetas)  
    json_object = jsontools.load_json(data)
    if (DEBUG): logger.info("html="+json_object["html"])
    data = json_object["html"]

    return parse_mixed_results(item,data)

def findvideos(item, verTodos=False):
    logger.info("pelisalacarta.channels.pordede findvideos")

    # Descarga la pagina
    headers = DEFAULT_HEADERS[:]
    #headers.append(["Referer",item.extra])
    #headers.append(["X-Requested-With","XMLHttpRequest"])
    data = scrapertools.cache_page(item.url,headers=headers)
    if (DEBUG): logger.info("data="+data)

    # Extrae las entradas (carpetas)  
    #json_object = jsontools.load_json(data)
    #if (DEBUG): logger.info("html="+json_object["html"])
    #data = json_object["html"]

    sesion = scrapertools.find_single_match(data,'SESS = "([^"]+)";')
    if (DEBUG): logger.info("sesion="+sesion)

    patron  = '<a target="_blank" class="a aporteLink(.*?)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []

    if config.get_platform().startswith("xbmc") and "/what/peli" in item.url:
        itemlist.append( Item(channel=__channel__, action="infosinopsis" , title="INFO / SINOPSIS" , url=item.url, thumbnail=item.thumbnail,  folder=False ))

    itemsort = []
    sortlinks = config.get_setting("pordedesortlinks") # 0:no, 1:valoracion, 2:idioma, 3:calidad, 4:idioma+calidad, 5:idioma+valoracion, 6:idioma+calidad+valoracion
    sortlinks = int(sortlinks) if sortlinks != '' else 0
    showlinks = config.get_setting("pordedeshowlinks") # 0:todos, 1:ver online, 2:descargar
    showlinks = int(showlinks) if showlinks != '' else 0

    for match in matches:
        if (DEBUG): logger.info("match="+match)

        jdown = scrapertools.find_single_match(match,'<div class="jdownloader">[^<]+</div>')
        if (showlinks == 1 and jdown != '') or (showlinks == 2 and jdown == ''): # Descartar enlaces veronline/descargar
            continue

        idiomas = re.compile('<div class="flag([^"]+)">([^<]+)</div>',re.DOTALL).findall(match)
        idioma_0 = (idiomas[0][0].replace("&nbsp;","").strip() + " " + idiomas[0][1].replace("&nbsp;","").strip()).strip()
        if len(idiomas) > 1:
            idioma_1 = (idiomas[1][0].replace("&nbsp;","").strip() + " " + idiomas[1][1].replace("&nbsp;","").strip()).strip()
            idioma = idioma_0 + ", " + idioma_1
        else:
            idioma_1 = ''
            idioma = idioma_0

        calidad_video = scrapertools.find_single_match(match,'<div class="linkInfo quality"><i class="icon-facetime-video"></i>([^<]+)</div>')
        if (DEBUG): logger.info("calidad_video="+calidad_video)
        calidad_audio = scrapertools.find_single_match(match,'<div class="linkInfo qualityaudio"><i class="icon-headphones"></i>([^<]+)</div>')
        if (DEBUG): logger.info("calidad_audio="+calidad_audio)

        thumb_servidor = scrapertools.find_single_match(match,'<div class="hostimage"[^<]+<img\s*src="([^"]+)">')
        if (DEBUG): logger.info("thumb_servidor="+thumb_servidor)
        nombre_servidor = scrapertools.find_single_match(thumb_servidor,"popup_([^\.]+)\.png")
        if (DEBUG): logger.info("nombre_servidor="+nombre_servidor)
        
        title = ("Download " if jdown != '' else "Ver en ")+nombre_servidor+" ("+idioma+") (Calidad "+calidad_video.strip()+", audio "+calidad_audio.strip()+")"

        cuenta = []
        valoracion = 0
        for idx, val in enumerate(['1', '2', 'report']):
            nn = scrapertools.find_single_match(match,'<span\s+data-num="([^"]+)"\s+class="defaultPopup"\s+href="/likes/popup/value/'+val+'/')
            if nn != '0' and nn != '':
                cuenta.append(nn + ' ' + ['ok', 'ko', 'rep'][idx])
                valoracion += int(nn) if val == '1' else -int(nn)

        if len(cuenta) > 0:
            title += ' (' + ', '.join(cuenta) + ')'

        url = urlparse.urljoin( item.url , scrapertools.find_single_match(match,'href="([^"]+)"') )
        thumbnail = thumb_servidor
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        if sortlinks > 0:
            # orden1 para dejar los "downloads" detras de los "ver" al ordenar
            # orden2 segun configuración
            if sortlinks == 1:
                orden = valoracion
            elif sortlinks == 2:
                orden = valora_idioma(idioma_0, idioma_1)
            elif sortlinks == 3:
                orden = valora_calidad(calidad_video, calidad_audio)
            elif sortlinks == 4:
                orden = (valora_idioma(idioma_0, idioma_1) * 100) + valora_calidad(calidad_video, calidad_audio)
            elif sortlinks == 5:
                orden = (valora_idioma(idioma_0, idioma_1) * 1000) + valoracion
            elif sortlinks == 6:
                orden = (valora_idioma(idioma_0, idioma_1) * 100000) + (valora_calidad(calidad_video, calidad_audio) * 1000) + valoracion
            itemsort.append({'action': "play", 'title': title, 'url':url, 'thumbnail':thumbnail, 'plot':plot, 'extra':sesion+"|"+item.url, 'fulltitle':title, 'orden1': (jdown == ''), 'orden2':orden})
        else:
            itemlist.append( Item(channel=__channel__, action="play" , title=title , url=url, thumbnail=thumbnail, plot=plot, extra=sesion+"|"+item.url, fulltitle=title))

    if sortlinks > 0:
        numberlinks = config.get_setting("pordedenumberlinks") # 0:todos, > 0:n*5 (5,10,15,20,...)
        numberlinks = int(numberlinks) * 5 if numberlinks != '' else 0
        if numberlinks == 0:
            verTodos = True
        itemsort = sorted(itemsort, key=lambda k: (k['orden1'], k['orden2']), reverse=True)
        for i, subitem in enumerate(itemsort):
            if verTodos == False and i >= numberlinks:
                itemlist.append(Item(channel=__channel__, action='findallvideos' , title='Ver todos los enlaces', url=item.url, extra=item.extra ))
                break
            itemlist.append( Item(channel=__channel__, action=subitem['action'] , title=subitem['title'] , url=subitem['url'] , thumbnail=subitem['thumbnail'] , plot=subitem['plot'] , extra=subitem['extra'] , fulltitle=subitem['fulltitle'] ))

    return itemlist

def findallvideos(item):
    return findvideos(item, True)

def play(item):
    logger.info("pelisalacarta.channels.pordede play url="+item.url)

    # Marcar como visto
    checkseen(item.extra.split("|")[1])

    # Hace la llamada
    headers = DEFAULT_HEADERS[:]
    headers.append( ["Referer" , item.extra.split("|")[1] ])

    data = scrapertools.cache_page(item.url,post="_s="+item.extra.split("|")[0],headers=headers)
    if (DEBUG): logger.info("data="+data)
    #url = scrapertools.find_single_match(data,'<a href="([^"]+)" target="_blank"><button>Visitar enlace</button>')
    url = scrapertools.find_single_match(data,'<p class="links">\s+<a href="([^"]+)" target="_blank"')
    url = urlparse.urljoin(item.url,url)

    headers = DEFAULT_HEADERS[:]
    headers.append( ["Referer" , item.url ])

    #data2 = scrapertools.cache_page(url,headers=headers)
    #logger.info("pelisalacarta.channels.pordede play (interstitial) url="+url)
    #logger.info("data2="+data2)
    #url2 = scrapertools.find_single_match(data2,'<a href="([^"]+)"><button disabled>Ir al vídeo</button>')
    #url2 = urlparse.urljoin(item.url,url2)
    #headers = DEFAULT_HEADERS[:]
    #headers.append( ["Referer" , url2 ])

    media_url = scrapertools.downloadpage(url,headers=headers,header_to_get="location",follow_redirects=False)
    logger.info("media_url="+media_url)

    itemlist = servertools.find_video_items(data=media_url)

    for videoitem in itemlist:
        videoitem.title = item.title
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist    

def checkseen(item):
    logger.info("pelisalacarta.channels.pordede checkseen "+item)

    if "/viewepisode/" in item:
        headers = DEFAULT_HEADERS[:]
        episode = item.split("/")[-1]
        scrapertools.downloadpage("http://www.pordede.com/ajax/action", post="model=episode&id="+episode+"&action=seen&value=1")

    if "/what/peli" in item:
        headers = DEFAULT_HEADERS[:]
        data = scrapertools.cache_page(item, headers=headers)
        # GET MOVIE ID
        movieid = scrapertools.find_single_match(data,'href="/links/create/ref_id/([0-9]+)/ref_model/')
        scrapertools.downloadpage("http://www.pordede.com/ajax/mediaaction", post="model=peli&id="+movieid+"&action=status&value=3")


    return True

def infosinopsis(item):
    logger.info("pelisalacarta.channels.pordede infosinopsis")

    url_aux = item.url.replace("/links/view/slug/", "/peli/").replace("/what/peli", "")
    # Descarga la pagina
    headers = DEFAULT_HEADERS[:]
    #headers.append(["Referer",item.extra])
    #headers.append(["X-Requested-With","XMLHttpRequest"])
    data = scrapertools.cache_page(url_aux,headers=headers)
    if (DEBUG): logger.info("data="+data)

    scrapedtitle = scrapertools.find_single_match(data,'<h1>([^<]+)</h1>')
    scrapedvalue = scrapertools.find_single_match(data,'<span class="puntuationValue" data-value="([^"]+)"')
    scrapedyear = scrapertools.find_single_match(data,'<h2 class="info">[^<]+</h2>\s*<p class="info">([^<]+)</p>')
    scrapedduration = scrapertools.find_single_match(data,'<h2 class="info">[^<]+</h2>\s*<p class="info">([^<]+)</p>', 1)
    scrapedplot = scrapertools.find_single_match(data,'<div class="info text"[^>]+>([^<]+)</div>')
    #scrapedthumbnail = scrapertools.find_single_match(data,'<meta property="og:image" content="([^"]+)"')
    #thumbnail = scrapedthumbnail.replace("http://www.pordede.comhttp://", "http://").replace("mediacover", "mediathumb")
    scrapedgenres = re.compile('href="/pelis/index/genre/[^"]+">([^<]+)</a>',re.DOTALL).findall(data)
    scrapedcasting = re.compile('href="/star/[^"]+">([^<]+)</a><br/><span>([^<]+)</span>',re.DOTALL).findall(data)

    title = scrapertools.htmlclean(scrapedtitle)
    plot = "Año: [B]"+scrapedyear+"[/B]"
    plot += " , Duración: [B]"+scrapedduration+"[/B]"
    plot += " , Puntuación usuarios: [B]"+scrapedvalue+"[/B]"
    plot += "\nGéneros: "+", ".join(scrapedgenres)
    plot += "\n\nSinopsis:\n"+scrapertools.htmlclean(scrapedplot)
    plot += "\n\nCasting:\n"
    for actor,papel in scrapedcasting:
    	plot += actor+" ("+papel+"). "

    tbd = TextBox("DialogTextViewer.xml", os.getcwd(), "Default")
    tbd.ask(title, plot)
    del tbd
    return

try:
    import xbmcgui
    class TextBox( xbmcgui.WindowXML ):
        """ Create a skinned textbox window """
        def __init__( self, *args, **kwargs):
            pass
            
        def onInit( self ):
            try:
                self.getControl( 5 ).setText( self.text )
                self.getControl( 1 ).setLabel( self.title )
            except: pass
    
        def onClick( self, controlId ):
            pass
    
        def onFocus( self, controlId ):
            pass
    
        def onAction( self, action ):
            self.close()
    
        def ask(self, title, text ):
            self.title = title
            self.text = text
            self.doModal()
except:
    pass

# Valoraciones de enlaces, los valores más altos se mostrarán primero :

def valora_calidad(video, audio):
    prefs_video = [ 'hdmicro', 'hd1080', 'hd720', 'hdrip', 'dvdrip', 'rip', 'tc-screener', 'ts-screener' ]
    prefs_audio = [ 'dts', '5.1', 'rip', 'line', 'screener' ]

    video = ''.join(video.split()).lower()
    pts = (9 - prefs_video.index(video) if video in prefs_video else 1) * 10

    audio = ''.join(audio.split()).lower()
    pts += 9 - prefs_audio.index(audio) if audio in prefs_audio else 1

    return pts

def valora_idioma(idioma_0, idioma_1):
    prefs = [ 'spanish', 'spanish LAT', 'catalan', 'english', 'french' ]

    pts = (9 - prefs.index(idioma_0) if idioma_0 in prefs else 1) * 10
    if idioma_1 != '': # si hay subtítulos
        idioma_1 = idioma_1.replace(' SUB', '')
        pts += 8 - prefs.index(idioma_1) if idioma_1 in prefs else 1
    else:
        pts += 9 # sin subtítulos por delante
    return pts