# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cinetube
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os,sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "cinetube"
__category__ = "F,S,A,D"
__type__ = "generic"
__title__ = "Cinetube"
__language__ = "ES"

#DEBUG = config.get_setting("debug")
DEBUG = False
'''
SESION = config.get_setting("session","cinetube")
LOGIN = config.get_setting("login","cinetube")
PASSWORD = config.get_setting("password","cinetube")
'''

def isGeneric():
    return True

def mainlist(item):
    logger.info("[cinetube.py] getmainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Películas"                , action="menupeliculas"))
    itemlist.append( Item(channel=__channel__, title="Series"                   , action="menuseries"))
    itemlist.append( Item(channel=__channel__, title="Documentales"             , action="menudocumentales"))
    itemlist.append( Item(channel=__channel__, title="Anime"                    , action="menuanime"))
    
    #itemlist.append( Item(channel=__channel__, title="Buscar"                   , action="search") )   
    #itemlist.append( Item(channel=__channel__, title="Buscar por Actor/Director", action="search" , url="actor-director") )

    '''
    if SESION=="true":
        perform_login(LOGIN,PASSWORD)
        itemlist.append( Item(channel=__channel__, title="Cerrar sesion ("+LOGIN+")", action="logout"))
    else:
        itemlist.append( Item(channel=__channel__, title="Iniciar sesion", action="login"))
    '''
    
    return itemlist

def menupeliculas(item):
    logger.info("[cinetube.py] menupeliculas")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Películas - Novedades"        , action="peliculas"        , url="http://www.cinetube.es/peliculas/"))
    #itemlist.append( Item(channel=__channel__, title="Películas - Estrenos de Cine" , action="documentales"     , url="http://www.cinetube.es/peliculas/estrenos-de-cine/"))
    #itemlist.append( Item(channel=__channel__, title="Películas - Estrenos en DVD"  , action="documentales"     , url="http://www.cinetube.es/peliculas/estrenos-dvd/"))
    #itemlist.append( Item(channel=__channel__, title="Películas - Nueva Calidad"    , action="documentales"     , url="http://www.cinetube.es/peliculas/nueva-calidad/"))
    itemlist.append( Item(channel=__channel__, title="Películas - A-Z"              , action="letras"           , url="http://www.cinetube.es/peliculas/"))
    itemlist.append( Item(channel=__channel__, title="Películas - Categorías"       , action="categorias"       , url="http://www.cinetube.es/peliculas/"))
    
    #itemlist.append( Item(channel=__channel__, title="Buscador..."                  , action="search"           , url="peliculas") )

    return itemlist


def peliculas(item,paginacion=True):
    logger.info("[cinetube.py] peliculas")

    url = item.url

    # Descarga la página
    data = scrapertools.cachePage(url)

    # Extrae las entradas
    patronvideos  = '<div class="imgmov[^<]+'
    patronvideos += '<i[^<]+</i[^<]+'
    patronvideos += '<img src="([^"]+)"[^<]+'
    patronvideos += '<a href="([^"]+)"[^<]+<i[^<]+</i[^<]+'
    patronvideos += '<strong>([^<]+)</strong[^<]+'
    patronvideos += '<span[^>]+>(.*?)</span>'

    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for scrapedthumbnail,scrapedurl,scrapedtitle,scrapedplot in matches:
        title = scrapedtitle.strip()+" ("+scrapertools.htmlclean(scrapedplot).strip()+")"
        title = title.replace("Calidad:","")
        title = title.replace("Idiomas :","")
        title = re.compile("\s+",re.DOTALL).sub(" ",title)
        url = urlparse.urljoin(item.url,scrapedurl)
        plot = ""
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        if "serie" not in url:
            action="findvideos"
        else:
            action="capitulos"

        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action=action, title=title , fulltitle=title , url=url , thumbnail=thumbnail , plot=plot ) )

    # Extrae el paginador
    try:
        next_page_url = scrapertools.get_match(data,'<a class="lnne icob" href="([^"]+)">Siguientes</a>')
        itemlist.append( Item(channel=__channel__, action="peliculas", title=">> Página siguiente" , url=urlparse.urljoin(item.url,next_page_url) ) )
    except:
        pass
        
    return itemlist

def letras(item):
    logger.info("[cinetube.py] listalfabetico("+item.url+")")
    
    if "peliculas" in item.url or "documentales" in item.url:
        action = "peliculas"
    elif "series" in item.url:
        action="series"
    elif "peliculas-anime" in item.url:
        action="documentales"
    
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'<ul class="lstabc[^>]+>(.*?)</ul>')

    # Extrae las entradas
    patron = '<li><a href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    itemlist = []
    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        plot = ""
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        # Añade al listado
        itemlist.append( Item(channel=__channel__, action=action, title=title , url=url , thumbnail=thumbnail , plot=plot) )

    return itemlist

def categorias(item):
    logger.info("[cinetube.py] listcategorias")

    if "peliculas" in item.url or "documentales" in item.url:
        action = "peliculas"
    elif "series" in item.url:
        action="series"
    elif "peliculas-anime" in item.url:
        action="documentales"
    
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'<h3 class="tibk bgwh fx pore"><strong>Temáticas</strong></h3>(.*?)</ul>')

    # Extrae las entradas
    patron = '<li><a href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    logger.info(str(matches))
    itemlist = []
    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        plot = ""
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        # Añade al listado
        itemlist.append( Item(channel=__channel__, action=action, title=title , url=url , thumbnail=thumbnail , plot=plot) )

    return itemlist

def menuseries(item):
    logger.info("[cinetube.py] menuseries")

    itemlist = []

    itemlist.append( Item(channel=__channel__, title="Series - Novedades"           , action="series"           , url="http://www.cinetube.es/series/"))
    itemlist.append( Item(channel=__channel__, title="Series - A-Z"                 , action="letras"   , url="http://www.cinetube.es/series/"))
    #itemlist.append( Item(channel=__channel__, title="Series - Listado completo"    , action="completo"         , url="http://www.cinetube.es/series-todas/"))
    itemlist.append( Item(channel=__channel__, title="Series - Categorías"          , action="categorias"   , url="http://www.cinetube.es/series/"))

    #itemlist.append( Item(channel=__channel__, title="Buscar Series"                , action="search"           , url="series") )

    return itemlist

def series(item,paginacion=True):
    logger.info("[cinetube.py] series")

    url = item.url

    # Descarga la página
    data = scrapertools.cachePage(url)

    # Extrae las entradas
    patronvideos  = '<div class="imgmov[^<]+'
    #patronvideos += '<i[^<]+</i[^<]+'
    patronvideos += '<img src="([^"]+)"[^<]+'
    patronvideos += '<a href="([^"]+)"[^<]+<i[^<]+</i[^<]+'
    patronvideos += '<strong>([^<]+)</strong[^<]+'
    patronvideos += '<span[^>]+>(.*?)</span>'

    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for scrapedthumbnail,scrapedurl,scrapedtitle,scrapedplot in matches:
        title = scrapedtitle.strip()+" ("+scrapertools.htmlclean(scrapedplot).strip()+")"
        title = title.replace("Calidad:","")
        title = title.replace("Idiomas :","")
        title = re.compile("\s+",re.DOTALL).sub(" ",title)
        url = urlparse.urljoin(item.url,scrapedurl)
        plot = ""
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        logger.info(url)
        
        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action="temporadas", title=title , fulltitle=title , url=url , thumbnail=thumbnail , plot=plot ) )

    # Extrae el paginador
    try:
        next_page_url = scrapertools.get_match(data,'<a class="lnne icob" href="([^"]+)">Siguientes</a>')
        itemlist.append( Item(channel=__channel__, action="peliculas", title=">> Página siguiente" , url=urlparse.urljoin(item.url,next_page_url) ) )
    except:
        pass
        
    return itemlist

def temporadas(item, paginacion=True):

    logger.info("[cinetube.py] temporadas")

    url = item.url
    logger.info(url)
    end=item.url.find('temporada')
    url=item.url[:end]
    logger.info(url)

    if url[-1]!='/': url=url+'/'

    # Descarga la página
    data = scrapertools.cachePage(url)

    # Extrae las entradas


    patron = '<a class="rpdbtn hide" href="([^"]+)">Ver temporada</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    logger.info("hay %d matches" % len(matches))
    logger.info(str(matches))

    itemlist = []
    for match in matches:
        title = match[match.find('temporada'):-1].replace('-', ' ').replace("t","T")
        url = "http://www.cinetube.es"+match
        plot = ""
        thumbnail = item.thumbnail
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        
        
        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action="capitulos", title=title , fulltitle=title , url=url , thumbnail=thumbnail , plot=plot ) )

    # Extrae el paginador
    try:
        next_page_url = scrapertools.get_match(data,'<a class="lnne icob" href="([^"]+)">Siguientes</a>')
        itemlist.append( Item(channel=__channel__, action="peliculas", title=">> Página siguiente" , url=urlparse.urljoin(item.url,next_page_url) ) )
    except:
        pass
        
    return itemlist

def capitulos(item, paginacion=True):

    logger.info("[cinetube.py] capitulos")

    url = item.url

    # Descarga la página
    data = scrapertools.cachePage(url)

    # Extrae las entradas


    patron = '<a href="([^"]+)"><span class="vistbot'
    matches = re.compile(patron,re.DOTALL).findall(data)
    logger.info("hay %d matches" % len(matches))
    logger.info(str(matches))

    itemlist = []
    for match in matches:
        if match == "#": continue

        title = match[match.find('capitulo'):-1].replace('-', ' ').replace("c","C")
        url = "http://www.cinetube.es"+match
        plot = ""
        thumbnail = item.thumbnail
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        
        
        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action="findvideos", title=title , fulltitle=title , url=url , thumbnail=thumbnail , plot=plot ) )

    # Extrae el paginador
    try:
        next_page_url = scrapertools.get_match(data,'<a class="lnne icob" href="([^"]+)">Siguientes</a>')
        itemlist.append( Item(channel=__channel__, action="peliculas", title=">> Página siguiente" , url=urlparse.urljoin(item.url,next_page_url) ) )
    except:
        pass
        
    return itemlist



def menudocumentales(item):
    logger.info("[cinetube.py] menudocumentales")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Documentales - Novedades"         , action="peliculas"     , url="http://www.cinetube.es/documentales/"))
    itemlist.append( Item(channel=__channel__, title="Documentales - A-Z"               , action="letras"   , url="http://www.cinetube.es/documentales/"))
    #itemlist.append( Item(channel=__channel__, title="Documentales - Listado completo"  , action="completo"         , url="http://www.cinetube.es/documentales-todos/"))
    itemlist.append( Item(channel=__channel__, title="Documentales - Categorías"        , action="categorias"   , url="http://www.cinetube.es/documentales/"))

    #itemlist.append( Item(channel=__channel__, title="Buscar Documentales"              , action="search"           , url="documentales") )

    return itemlist

    

def menuanime(item):
    logger.info("[cinetube.py] menuanime")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Series Anime - Novedades"             , action="series"           , url="http://www.cinetube.es/series-anime/"))
    itemlist.append( Item(channel=__channel__, title="Series Anime - A-Z"                   , action="letras"   , url="http://www.cinetube.es/series-anime/" ))
    #itemlist.append( Item(channel=__channel__, title="Series Anime - Listado completo"      , action="categorias"         , url="http://www.cinetube.es/series-anime/"))
    itemlist.append( Item(channel=__channel__, title="Series Anime - Categorías"            , action="categorias"   , url="http://www.cinetube.es/series-anime/"))              
    itemlist.append( Item(channel=__channel__, title="Peliculas Anime - Novedades"          , action="peliculas"     , url="http://www.cinetube.es/peliculas-anime/") )
    itemlist.append( Item(channel=__channel__, title="Películas Anime - A-Z"                , action="letras"   , url="http://www.cinetube.es/peliculas-anime/" ))
    #itemlist.append( Item(channel=__channel__, title="Películas Anime - Listado completo"   , action="completo"         , url="http://www.cinetube.es/peliculas-anime-todas/"))
    itemlist.append( Item(channel=__channel__, title="Películas Anime - Categorías"         , action="categorias"   , url="http://www.cinetube.es/peliculas-anime/"))

    #itemlist.append( Item(channel=__channel__, title="Buscar Anime"                         , action="search"           , url="anime") )

    return itemlist

def perform_login(login,password):
    # Invoca al login, y con eso se quedarán las cookies de sesión necesarias
    login = login.replace("@","%40")
    data = scrapertools.cache_page("http://www.cinetube.es/login.php",post="usuario=%s&clave=%s" % (login,password))

def logout(item):
    nombre_fichero_config_canal = os.path.join( config.get_data_path() , __channel__+".xml" )
    config_canal = open( nombre_fichero_config_canal , "w" )
    config_canal.write("<settings>\n<session>false</session>\n<login></login>\n<password></password>\n</settings>")
    config_canal.close();

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Sesión finalizada", action="mainlist"))
    return itemlist

def login(item):
    if config.get_platform() in ("wiimc", "rss", "mediaserver"):
        login = config.get_setting("cinetubeuser")
        password = config.get_setting("cinetubepassword")
        if login<>"" and password<>"":
            url="http://www.cinetube.es/login.php"
            data = scrapertools.cache_page("http://www.cinetube.es/login.php",post="usuario=%s&clave=%s" % (login,password))
            itemlist = []
            itemlist.append( Item(channel=__channel__, title="Sesión iniciada", action="mainlist"))
    else:
        import xbmc
        keyboard = xbmc.Keyboard("","Login")
        keyboard.doModal()
        if (keyboard.isConfirmed()):
            login = keyboard.getText()

        keyboard = xbmc.Keyboard("","Password")
        keyboard.doModal()
        if (keyboard.isConfirmed()):
            password = keyboard.getText()

        nombre_fichero_config_canal = os.path.join( config.get_data_path() , __channel__+".xml" )
        config_canal = open( nombre_fichero_config_canal , "w" )
        config_canal.write("<settings>\n<session>true</session>\n<login>"+login+"</login>\n<password>"+password+"</password>\n</settings>")
        config_canal.close();

        itemlist = []
        itemlist.append( Item(channel=__channel__, title="Sesión iniciada", action="mainlist"))
    return itemlist

# Al llamarse "search" la función, el launcher pide un texto a buscar y lo añade como parámetro
def search(item,texto,categoria=""):
    logger.info("[cinetube.py] "+item.url+" search "+texto)
    itemlist = []
    url = item.url
    texto = texto.replace(" ","+")
    if "*" in categoria:
        url = "none"
    elif "F" in categoria:
        url = "peliculas"
    elif "S" in categoria:
        url = "series"
    logger.info("categoria: "+categoria+" url: "+url)
    try:
        # Series
        if url=="series" or url=="" or url=="none":
            item.url="http://www.cinetube.es/buscar/series/?palabra=%s&categoria=&valoracion="
            item.url = item.url % texto
            itemlist.extend(series(item))
        
        # Películas
        if url=="peliculas" or url=="" or url=="none":
            item.url="http://www.cinetube.es/buscar/peliculas/?palabra=%s&categoria=&valoracion="
            item.url = item.url % texto
            itemlist.extend(peliculas(item))
        
        # Documentales
        if item.url=="documentales" or url=="" or url=="none":
            item.url="http://www.cinetube.es/buscar/peliculas/?palabra=%s&categoria=&valoracion="
            item.url = item.url % texto
            itemlist.extend(documentales(item))
            
        # Anime
        if url=="anime" or url=="" or url=="none" or "F" in categoria:
            # Peliculas-anime
            item.url="http://www.cinetube.es/buscar/peliculas-anime/?palabra=%s&categoria=&valoracion="
            item.url = item.url % texto
            itemlist.extend(documentales(item))
        if url=="anime" or url=="" or url=="none" or "S" in categoria:
            # Series-anime
            item.url="http://www.cinetube.es/buscar/series-anime/?palabra=%s&categoria=&valoracion="
            item.url = item.url % texto
            itemlist.extend(series(item))

        # Actor/Director
        if url=="actor-director":
            item.url="http://www.cinetube.es/buscar/actor-director/?palabra=%s&categoria=&valoracion="
            item.url = item.url % texto
            itemlist.extend(peliculas(item))          
    
        return itemlist
        
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []



def completo(item):
    logger.info("[cinetube.py] completo()")
    
    url = item.url
    siguiente = True
    itemlist = []
    
    data = scrapertools.cachePage(url)
    patronpag  = '<li class="navs"><a class="pag_next" href="([^"]+)"></a></li>'
    while siguiente==True:
    
        patron = '<!--SERIE-->.*?<a href="([^"]+)" .*?>([^<]+)</a></span></li>.*?<!--FIN SERIE-->'
        matches = re.compile(patron,re.DOTALL).findall(data)
        for match in matches:
            scrapedtitle = match[1]
            # Convierte desde UTF-8 y quita entidades HTML
            scrapedtitle = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")
            scrapedtitle = scrapertools.entityunescape(scrapedtitle)
            fulltitle = scrapedtitle
            
            scrapedplot = ""
            scrapedurl = urlparse.urljoin(url,match[0])
            scrapedthumbnail = ""    

            itemlist.append( Item(channel=__channel__, action="temporadas", title=scrapedtitle , fulltitle=fulltitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle, show=scrapedtitle) )

        # Extrae el paginador
        matches = re.compile(patronpag,re.DOTALL).findall(data)
        if len(matches)==0:
            siguiente = False
        else:
            data = scrapertools.cachePage(urlparse.urljoin(url,matches[0]))

    return itemlist




def findvideos(item):
    logger.info("[cinetube.py] findvideos")

    # Descarga la pagina
    data = scrapertools.cachePage(item.url)

    # Busca el argumento
    try:
        scrapedplot = scrapertools.get_match(data,'<meta name="description" content="([^"]+)"')
    except:
        scrapedplot = ""

    # Busca los enlaces a los mirrors, o a los capitulos de las series...
    patron  = '<li class="rwbd ovhd"[^<]+'
    patron += '<div class="cld2 flol"><img src="[^"]+"><span>([^<]+)</span></div[^<]+'
    patron += '<div class="cld3 flol">(.*?)</div[^<]+'
    patron += '<div class="cld4 flol"><img src="([^"]+)"><a class="rpdbtn hide" href="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)

    itemlist = []
    for idioma,calidad,imgservidor,scrapedurl in matches:
        title = "Ver en "+imgservidor.replace("/img/cnt/servidor/","").replace(".png","")+" ("+scrapertools.htmlclean(calidad)+" "+idioma+")"
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = urlparse.urljoin(item.url,imgservidor)
        plot = scrapedplot
        itemlist.append( Item(channel=__channel__, action="play", title=title , fulltitle=item.title , url=url , thumbnail=thumbnail, plot=plot, folder=True) )

    return itemlist

def play(item):
    logger.info("[cinetube.py] play")

    # Lee el iframe
    data = scrapertools.cache_page(item.url)
    patron = 'ct_url_decode\("([^"]+)"\)'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    # Decodifica el bloque donde están los enlaces
    if len(matches)>0:
        data = matches[0]
        logger.info("-------------------------------------------------------------------------------------")
        logger.info(data)
        logger.info("-------------------------------------------------------------------------------------")
        data = ct_url_decode(data)

    logger.info("-------------------------------------------------------------------------------------")
    logger.info(data)
    logger.info("-------------------------------------------------------------------------------------")

    itemlist = servertools.find_video_items(data=data)
    
    for videoitem in itemlist:
        videoitem.title = item.title
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist    

def ct_url_decode(C):
    if not(C):
        return C
    
    C = C[::-1]
    X = 4-len(C)%4;
    if X in range(1,4):
        for z in range(X):
            C = C+"="
    
    import base64
    return base64.decodestring(C)

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True
    
    # mainlist
    mainlist_items = mainlist(Item())
    menupeliculas_items = menupeliculas(mainlist_items[0])

    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    peliculas_items = peliculas(menupeliculas_items[0])
    
    bien = False
    for pelicula_item in peliculas_items:
        mirrors = findvideos(item=pelicula_item)
        if len(mirrors)>=0 and len( play(mirrors[0]) )>0:
            bien = True
            break
    
    return bien

