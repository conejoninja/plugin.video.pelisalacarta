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

def isGeneric():
    return True

def login():

    url = "http://www.pordede.com/site/login"
    post = "LoginForm[username]="+config.get_setting("pordedeuser")+"&LoginForm[password]="+config.get_setting("pordedepassword")
    data = scrapertools.cache_page(url,post=post)

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

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)

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
    headers.append(["Referer",item.extra])
    headers.append(["X-Requested-With","XMLHttpRequest"])
    data = scrapertools.cache_page(item.url,headers=headers)
    logger.info("data="+data)

    # Extrae las entradas (carpetas)  
    json_object = jsontools.load_json(data)
    logger.info("html="+json_object["html"])
    data = json_object["html"]

    return parse_mixed_results(item,data,False)

def parse_mixed_results(item,data,sort):
    patron  = '<a class="defaultLink extended" href="([^"]+)"[^<]+'
    patron += '<div class="coverMini shadow tiptip" title="([^"]+)"[^<]+'
    patron += '<img class="centeredPic.*?src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    itemsort = []
    
    for scrapedurl,scrapedtitle,scrapedthumbnail in matches:
        title = scrapertools.htmlclean(scrapedtitle)
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        plot = ""
        #http://www.pordede.com/peli/the-lego-movie
        #http://www.pordede.com/links/view/slug/the-lego-movie/what/peli?popup=1

        if "/peli/" in scrapedurl:
            referer = urlparse.urljoin(item.url,scrapedurl)
            url = referer.replace("/peli/","/links/view/slug/")+"/what/peli"
            if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
            if sort:
                itemsort.append({'action': "findvideos", 'title': title, 'extra': referer, 'url': url, 'thumbnail': thumbnail, 'plot': plot, 'fulltitle': title})
            else:
                itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , extra=referer, url=url, thumbnail=thumbnail, plot=plot, fulltitle=title, viewmode="movie"))
        else:
            referer = item.url
            url = urlparse.urljoin(item.url,scrapedurl)
            if sort:
                itemsort.append({'action': "episodios", 'title': title, 'extra': referer, 'url': url, 'thumbnail': thumbnail, 'plot': plot, 'fulltitle': title})
            else:
                itemlist.append( Item(channel=__channel__, action="episodios" , title=title , extra=referer, url=url, thumbnail=thumbnail, plot=plot, fulltitle=title, viewmode="movie"))

    if sort:
        itemsort = sorted(itemsort, key=lambda k: k['title'])
        for item in itemsort:
            itemlist.append( Item(channel=__channel__, action=item['action'] , title=item['title'] , extra=item['extra'] , url=item['url'] , thumbnail=item['thumbnail'] , plot=item['plot'] , fulltitle=item['fulltitle'] , viewmode="movie"))

    return itemlist

def peliculas(item):
    logger.info("pelisalacarta.channels.pordede peliculas")

    # Descarga la pagina
    headers = DEFAULT_HEADERS[:]
    headers.append(["Referer",item.extra])
    headers.append(["X-Requested-With","XMLHttpRequest"])
    data = scrapertools.cache_page(item.url,headers=headers)
    logger.info("data="+data)

    # Extrae las entradas (carpetas)  
    json_object = jsontools.load_json(data)
    logger.info("html="+json_object["html"])
    data = json_object["html"]

    patron  = '<a class="defaultLink extended" href="([^"]+)"[^<]+'
    patron += '<div class="coverMini shadow tiptip" title="([^"]+)"[^<]+'
    patron += '<img class="centeredPic.*?src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for scrapedurl,scrapedtitle,scrapedthumbnail in matches:
        title = scrapertools.htmlclean(scrapedtitle)
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        plot = ""
        #http://www.pordede.com/peli/the-lego-movie
        #http://www.pordede.com/links/view/slug/the-lego-movie/what/peli?popup=1

        referer = urlparse.urljoin(item.url,scrapedurl)
        if "/peli" in item.url:
            url = referer.replace("/peli/","/links/view/slug/")+"/what/peli"
            itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , extra=referer, url=url, thumbnail=thumbnail, plot=plot, fulltitle=title, viewmode="movie"))
        else:
            url = referer
            itemlist.append( Item(channel=__channel__, action="episodios" , title=title , url=url, thumbnail=thumbnail, plot=plot, fulltitle=title, viewmode="movie"))

        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

    #http://www.pordede.com/pelis/loadmedia/offset/30/showlist/hot?popup=1
    if "offset" in item.url:
        old_offset = scrapertools.find_single_match(item.url,"offset/(\d+)/")
        new_offset = int(old_offset)+30
        url = item.url.replace("offset/"+old_offset,"offset/"+str(new_offset))
        itemlist.append( Item(channel=__channel__, action="peliculas" , title=">> Página siguiente" , extra=item.extra, url=url))

    return itemlist

def episodios(item):
    logger.info("pelisalacarta.channels.pordede episodios")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    #logger.info("data="+data)

    patrontemporada = '<div class="checkSeason"[^>]+>([^<]+)<div class="right" onclick="controller.checkSeason(.*?)\s+</div></div>'
    matchestemporadas = re.compile(patrontemporada,re.DOTALL).findall(data)

    for nombre_temporada,bloque_episodios in matchestemporadas:
        logger.info("nombre_temporada="+nombre_temporada)
        logger.info("bloque_episodios="+bloque_episodios)

        # Extrae los episodios
        patron  = '<span class="title defaultPopup" href="([^"]+)"><span class="number">([^<]+)</span>([^<]+)</span>(\s*</div>\s*<span[^>]*><span[^>]*>[^<]*</span><span[^>]*>[^<]*</span></span><div[^>]*><button[^>]*><span[^>]*>[^<]*</span><span[^>]*>[^<]*</span></button><div class="action([^"]*)" data-action="seen">)?'
        matches = re.compile(patron,re.DOTALL).findall(bloque_episodios)
        
        for scrapedurl,numero,scrapedtitle,info,visto in matches:
            visto_string = "[visto] " if visto.strip()=="active" else ""
            title = visto_string+nombre_temporada.replace("Temporada ", "")+"x"+numero+" "+scrapertools.htmlclean(scrapedtitle)
            thumbnail = ""
            plot = ""
            #http://www.pordede.com/peli/the-lego-movie
            #http://www.pordede.com/links/view/slug/the-lego-movie/what/peli?popup=1
            #http://www.pordede.com/links/viewepisode/id/475011?popup=1
            epid = scrapertools.find_single_match(scrapedurl,"id/(\d+)")
            url = "http://www.pordede.com/links/viewepisode/id/"+epid
            itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , url=url, thumbnail=thumbnail, plot=plot, fulltitle=title))

            if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

    return itemlist

def listas_sigues(item):
    logger.info("pelisalacarta.channels.pordede listas_sigues")

    # Descarga la pagina
    headers = DEFAULT_HEADERS[:]
    headers.append(["Referer",item.extra])
    headers.append(["X-Requested-With","XMLHttpRequest"])
    data = scrapertools.cache_page(item.url,headers=headers)
    logger.info("data="+data)

    # Extrae las entradas (carpetas)  
    json_object = jsontools.load_json(data)
    logger.info("html="+json_object["html"])
    data = json_object["html"]

    patron  = '<div class="clearfix modelContainer" data-model="lista"[^<]+'
    patron += '<span class="title"><span class="name"><a class="defaultLink" href="([^"]+)">([^<]+)</a>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for scrapedurl,scrapedtitle in matches:
        title = scrapertools.htmlclean(scrapedtitle)
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        itemlist.append( Item(channel=__channel__, action="lista" , title=title , url=url))

        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

    return itemlist

def tus_listas(item):
    logger.info("pelisalacarta.channels.pordede tus_listas")

    # Descarga la pagina
    headers = DEFAULT_HEADERS[:]
    headers.append(["Referer",item.extra])
    headers.append(["X-Requested-With","XMLHttpRequest"])
    data = scrapertools.cache_page(item.url,headers=headers)
    logger.info("data="+data)

    # Extrae las entradas (carpetas)  
    json_object = jsontools.load_json(data)
    logger.info("html="+json_object["html"])
    data = json_object["html"]

    patron  = '<div class="clearfix modelContainer" data-model="lista"[^<]+'
    patron += '<div class="right"[^<]+'
    patron += '<button[^<]+</button[^<]+'
    patron += '<button[^<]+</button[^<]+'
    patron += '</div[^<]+'
    patron += '<span class="title"><span class="name"><a class="defaultLink" href="([^"]+)">([^<]+)</a>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    itemsort = []
    
    for scrapedurl,scrapedtitle in matches:
        title = scrapertools.htmlclean(scrapedtitle)
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        if (config.get_setting("pordedesortlist")=='true'):
            itemsort.append({'title': title, 'url' : url})
        else:
            itemlist.append( Item(channel=__channel__, action="lista" , title=title , url=url))

    if (config.get_setting("pordedesortlist")=='true'):
        itemsort = sorted(itemsort, key=lambda k: k['title'])
        for item in itemsort:
            itemlist.append( Item(channel=__channel__, action="lista" , title=item['title'] , url=item['url']))

    return itemlist

def lista(item):
    logger.info("pelisalacarta.channels.pordede lista")

    # Descarga la pagina
    headers = DEFAULT_HEADERS[:]
    headers.append(["Referer",item.extra])
    headers.append(["X-Requested-With","XMLHttpRequest"])
    data = scrapertools.cache_page(item.url,headers=headers)
    logger.info("data="+data)

    # Extrae las entradas (carpetas)  
    json_object = jsontools.load_json(data)
    logger.info("html="+json_object["html"])
    data = json_object["html"]

    return parse_mixed_results(item,data,(config.get_setting("pordedesortlist")=='true'))

def findvideos(item):
    logger.info("pelisalacarta.channels.pordede findvideos")

    # Descarga la pagina
    headers = DEFAULT_HEADERS[:]
    #headers.append(["Referer",item.extra])
    #headers.append(["X-Requested-With","XMLHttpRequest"])
    data = scrapertools.cache_page(item.url,headers=headers)
    #logger.info("data="+data)

    # Extrae las entradas (carpetas)  
    #json_object = jsontools.load_json(data)
    #logger.info("html="+json_object["html"])
    #data = json_object["html"]


    sesion = scrapertools.find_single_match(data,'SESS = "([^"]+)";')
    logger.info("sesion="+sesion)

    patron  = '<a target="_blank" class="a aporteLink(.*?)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for match in matches:
        logger.info("match="+match)
        idioma_1 = scrapertools.find_single_match(match,'<div class="flag([^"]+)">[^<]+</div>')
        logger.info("idioma_1="+idioma_1)
        idioma_2 = scrapertools.find_single_match(match,'<div class="flag[^"]+">([^<]+)</div>')
        logger.info("idioma_2="+idioma_2)
        idioma_1=idioma_1.replace("&nbsp;","")
        idioma_2=idioma_2.replace("&nbsp;","")

        idioma = idioma_1.strip()+" "+idioma_2.strip()
        idioma = idioma.strip()

        calidad_video = scrapertools.find_single_match(match,'<div class="linkInfo quality"><i class="icon-facetime-video"></i>([^<]+)</div>')
        logger.info("calidad_video="+calidad_video)
        calidad_audio = scrapertools.find_single_match(match,'<div class="linkInfo qualityaudio"><i class="icon-headphones"></i>([^<]+)</div>')
        logger.info("calidad_audio="+calidad_audio)


        thumb_servidor = scrapertools.find_single_match(match,'<div class="hostimage"[^<]+<img src="([^"]+)">')
        logger.info("thumb_servidor="+thumb_servidor)
        nombre_servidor = scrapertools.find_single_match(thumb_servidor,"popup_([^\.]+)\.png")
        logger.info("nombre_servidor="+nombre_servidor)
        
        title = "Ver en "+nombre_servidor+" ("+idioma+") (Calidad "+calidad_video.strip()+", audio "+calidad_audio.strip()+")"
        url = urlparse.urljoin( item.url , scrapertools.find_single_match(match,'href="([^"]+)"') )
        thumbnail = thumb_servidor
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="play" , title=title , url=url, thumbnail=thumbnail, plot=plot, extra=sesion+"|"+item.url, fulltitle=title))

    return itemlist


def play(item):
    logger.info("pelisalacarta.channels.pordede play url="+item.url)

    # Marcar como visto
    checkseen(item.extra.split("|")[1])

    # Hace la llamada
    headers = DEFAULT_HEADERS[:]
    headers.append( ["Referer" , item.extra.split("|")[1] ])

    data = scrapertools.cache_page(item.url,post="_s="+item.extra.split("|")[0],headers=headers)
    logger.info("data="+data)
    url = scrapertools.find_single_match(data,'<a href="([^"]+)" target="_blank"><button>Visitar enlace</button>')
    url = urlparse.urljoin(item.url,url)

    headers = DEFAULT_HEADERS[:]
    headers.append( ["Referer" , item.url ])

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
        data = scrapertools.cache_page(item)
        # GET MOVIE ID
        movieid = scrapertools.find_single_match(data,'href="/links/create/ref_id/([0-9]+)/ref_model/')
        scrapertools.downloadpage("http://www.pordede.com/ajax/mediaaction", post="model=peli&id="+movieid+"&action=status&value=3")


    return True