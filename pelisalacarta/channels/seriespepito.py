# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para seriespepito
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys
import hashlib

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "seriespepito"
__category__ = "S"
__type__ = "generic"
__title__ = "Seriespepito"
__language__ = "ES"

DEBUG = config.get_setting("debug")

ENLACESPEPITO_REQUEST_HEADERS = [
    ["User-Agent" , "Mozilla/5.0 (Windows NT 6.1; rv:28.0) Gecko/20100101 Firefox/28.0"],
    ["Accept-Encoding","gzip, deflate"],
    ["Accept-Language" , "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3"],
    ["Accept" , "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"],
    ["Cookie" , "__test"],
    ["Cookie" , "_ga=GA1.2.1328656124.1402475801"],
    ["Referer" , "http://star-trek-voyager.seriespepito.com/temporada-1/capitulo-5/"],
    ["Connection" , "keep-alive"]
]

SERIES_PEPITO    = 0
PELICULAS_PEPITO = 1

def isGeneric():
    return True

def mainlist(item):
    logger.info("[seriespepito.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="novedades"        , title="Novedades", url="http://www.seriespepito.com/nuevos-capitulos/",fanart="http://pelisalacarta.mimediacenter.info/fanart/seriespepito.jpg"))
    itemlist.append( Item(channel=__channel__, action="lomasvisto"        , title="Lo más visto", url="http://www.seriespepito.com/nuevos-capitulos/",fanart="http://pelisalacarta.mimediacenter.info/fanart/seriespepito.jpg"))
    itemlist.append( Item(channel=__channel__, action="listalfabetico"   , title="Listado alfabético",fanart="http://pelisalacarta.mimediacenter.info/fanart/seriespepito.jpg"))
    itemlist.append( Item(channel=__channel__, action="allserieslist"    , title="Listado completo",    url="http://www.seriespepito.com/",fanart="http://pelisalacarta.mimediacenter.info/fanart/seriespepito.jpg"))

    return itemlist

def novedades(item):
    logger.info("[seriespepito.py] novedades")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'<ul class="lista_series">(.*?)</ul>')
    
    '''
    <li><a title="Ripper Street" href="http://ripper-street.seriespepito.com/">
    <img alt="Ripper Street" src="http://www.seriespepito.com/uploads/series/1659-ripper-street-thumb.jpg" />
    Ripper Street</a><br/><a title="Temporada 5 de Ripper Street" href="http://ripper-street.seriespepito.com/temporada-5/">Temp: 5</a>&nbsp;<a title="Capítulo 5 Temporada 5 de Ripper Street" href="http://ripper-street.seriespepito.com/temporada-5/capitulo-5/">Cap: 5</a></li>
    '''
    patron  = '<li[^<]+'
    patron += '<a title="[^"]+" href="([^"]+)"[^<]+'
    patron += '<img alt="[^"]+" src="([^"]+)"[^>]+>(.*?)</li>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []
    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        logger.info("title="+scrapedtitle)
        title = scrapertools.htmlclean(scrapedtitle).strip()
        title = title.replace("\r","").replace("\n","")
        #title = unicode( title, "iso-8859-1" , errors="replace" ).encode("utf-8")
        title = re.compile("\s+",re.DOTALL).sub(" ",title)
        logger.info("title="+title)

        url = scrapedurl
        thumbnail = scrapedthumbnail
        plot = ""
        plot = unicode( plot, "iso-8859-1" , errors="replace" ).encode("utf-8")
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="episodios" , title=title , url=url, thumbnail=thumbnail, plot=plot, show=title, viewmode="movie", fanart="http://pelisalacarta.mimediacenter.info/fanart/seriespepito.jpg"))

    return itemlist

def lomasvisto(item):
    logger.info("[seriespepito.py] lomasvisto")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'s visto de esta semana en Pepito</div><ul(.*?)</ul>')

    patron  = '<a title="([^"]+)" href="([^"]+)"[^<]+'
    patron += '<img.*?src="([^"]+)"'

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []
    for scrapedtitle,scrapedurl,scrapedthumbnail in matches:
        logger.info("title="+scrapedtitle)
        title = scrapertools.htmlclean(scrapedtitle).strip()
        title = title.replace("\r","").replace("\n","")
        #title = unicode( title, "iso-8859-1" , errors="replace" ).encode("utf-8")
        title = re.compile("\s+",re.DOTALL).sub(" ",title)
        logger.info("title="+title)

        url = scrapedurl
        thumbnail = scrapedthumbnail
        plot = ""
        plot = unicode( plot, "iso-8859-1" , errors="replace" ).encode("utf-8")
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="episodios" , title=title , url=url, thumbnail=thumbnail, plot=plot, show=title, viewmode="movie", fanart="http://pelisalacarta.mimediacenter.info/fanart/seriespepito.jpg"))

    return itemlist

def allserieslist(item):
    logger.info("[seriespepito.py] completo()")
    itemlist = []

    # Carga el menú "Alfabético" de series
    item = Item(channel=__channel__, action="listalfabetico")
    items_letras = listalfabetico(item)
    
    # Para cada letra
    for item_letra in items_letras:
        # Lee las series
        items_programas = series(item_letra)
        itemlist.extend( items_programas )

    return itemlist

def listalfabetico(item):
    logger.info("[seriespepito.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="series" , title="0-9",url="http://www.seriespepito.com/lista-series-num/"))
    for letra in ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']:
        itemlist.append( Item(channel=__channel__, action="series" , title=letra,url="http://www.seriespepito.com/lista-series-"+letra.lower()+"/",fanart="http://pelisalacarta.mimediacenter.info/fanart/seriespepito.jpg"))

    return itemlist

def series(item):
    logger.info("[seriespepito.py] series")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'<ul class="lista_series">(.*?)</ul>')

    patron = '<li><a title="([^"]+)" href="([^"]+)"[^<]+<img alt="[^"]+" src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []
    for scrapedtitle,scrapedurl,scrapedthumbnail in matches:
        #title = unicode( scrapedtitle.strip(), "iso-8859-1" , errors="replace" ).encode("utf-8")
        title = scrapedtitle.strip()
        url = scrapedurl
        thumbnail = scrapedthumbnail
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="episodios" , title=title , url=url, thumbnail=thumbnail, plot=plot, show=title,viewmode="movie", fanart="http://pelisalacarta.mimediacenter.info/fanart/seriespepito.jpg"))

    return itemlist


def detalle_programa(item,data=""):
    if data=="":
        data = scrapertools.cachePage(item.url)
    
    #<img class="img-polaroid imgcolserie" alt="Battlestar Galactica 2003" src="http://www.seriespepito.com/uploads/series/121-battlestar-galactica-2003.jpg"></center>
    try:
        data2 = scrapertools.get_match(data,'<img class="img-polaroid imgcolserie" alt="[^"]+" src="([^"]+)"')
        item.thumbnail = data2.replace("%20"," ")
    except:
        pass

    # Argumento
    try:
        data2 = scrapertools.get_match(data,'<div class="subtitulo">\s+Sinopsis.*?</div>(.*?)</div>')
        item.plot = scrapertools.htmlclean(data2)
    except:
        pass

    return item

def episodios(item):
    logger.info("[seriespepito.py] list")

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    
    # Completa plot y thumbnail
    item = detalle_programa(item,data)

    data = scrapertools.get_match(data,'<div class="accordion"(.*?)<div class="subtitulo">')
    logger.info(data)

    # Extrae los capítulos
    '''
    <tbody>
    <tr>
    <td>
    <a class="asinenlaces" title="&nbsp;0x01&nbsp;-&nbsp;Battlestar Galactica 2003&nbsp;-&nbsp;Capitulo 1" href="http://battlestar-galactica-2003.seriespepito.com/temporada-0/capitulo-1/">
    <i class="icon-film"></i>&nbsp;&nbsp;
    <strong>0x01</strong>
    &nbsp;-&nbsp;Battlestar Galactica 2003&nbsp;-&nbsp;Capitulo 1&nbsp;</a><button id="capvisto_121_0_1" class="btn btn-warning btn-mini sptt pull-right bcapvisto ctrl_over" data-tt_my="left center" data-tt_at="right center" data-tt_titulo="Marca del último capítulo visto" data-tt_texto="Este es el último capítulo que has visto de esta serie." data-id="121" data-tem="0" data-cap="1" type="button"><i class="icon-eye-open"></i></button></td></tr><tr><td><a  title="&nbsp;0x02&nbsp;-&nbsp;Battlestar Galactica 2003&nbsp;-&nbsp;Capitulo 2" href="http://battlestar-galactica-2003.seriespepito.com/temporada-0/capitulo-2/"><i class="icon-film"></i>&nbsp;&nbsp;<strong>0x02</strong>&nbsp;-&nbsp;Battlestar Galactica 2003&nbsp;-&nbsp;Capitulo 2&nbsp;<span class="flag flag_0"></span></a><button id="capvisto_121_0_2" class="btn btn-warning btn-mini sptt pull-right bcapvisto ctrl_over" data-tt_my="left center" data-tt_at="right center" data-tt_titulo="Marca del último capítulo visto" data-tt_texto="Este es el último capítulo que has visto de esta serie." data-id="121" data-tem="0" data-cap="2" type="button"><i class="icon-eye-open"></i></button></td></tr></tbody>
    '''
    patron  = '<tr>'
    patron += '<td>'
    patron += '<a.*?href="([^"]+)"[^<]+'
    patron += '<i[^<]+</i[^<]+'
    patron += '<strong>([^<]+)</strong>'
    patron += '([^<]+)<(.*?)<button'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []
    for scrapedurl,scrapedepisode,scrapedtitle,idiomas in matches:
        #title = unicode( scrapedtitle.strip(), "iso-8859-1" , errors="replace" ).encode("utf-8")
        title = scrapedepisode + " " + scrapedtitle.strip()
        title = scrapertools.entityunescape(title)
        if "flag_0" in idiomas:
            title = title + " (Español)"
        if "flag_1" in idiomas:
            title = title + " (Latino)"
        if "flag_2" in idiomas:
            title = title + " (VO)"
        if "flag_3" in idiomas:
            title = title + " (VOS)"
        url = scrapedurl
        thumbnail = item.thumbnail
        plot = item.plot
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , url=url, thumbnail=thumbnail, plot=plot, show=item.show, viewmode="movie_with_plot"))

    if (config.get_platform().startswith("xbmc") or config.get_platform().startswith("boxee")) and len(itemlist)>0:
        itemlist.append( Item(channel=item.channel, title="Añadir esta serie a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="episodios", show=item.show,fanart="http://pelisalacarta.mimediacenter.info/fanart/seriespepito.jpg"))
        itemlist.append( Item(channel=item.channel, title="Descargar todos los episodios de la serie", url=item.url, action="download_all_episodes", extra="episodios", show=item.show,fanart="http://pelisalacarta.mimediacenter.info/fanart/seriespepito.jpg"))

    return itemlist

def findvideos(item):
    logger.info("[seriespepito.py] findvideos")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cachePage(item.url)
    #logger.info(data)
    '''
    <tr>
    <td class="tdidioma"><span class="flag flag_2"></span></td>
    <td>25/06/2012</td>
    <td class="tdservidor"><img src="http://www.seriespepito.com/uploads/servidores/76-imagen_img.png" alt="Moevideos" />&nbsp;Moevideos</td>
    <td class="tdenlace"><a class="btn btn-mini enlace_link" rel="nofollow" target="_blank" title="Ver..." href="http://falling-skies.seriespepito.com/temporada-2/capitulo-3/385944/"><i class="icon-play"></i>&nbsp;&nbsp;Ver</a></td>
    <td class="tdusuario"><a id="a_ava_71" href="http://www.seriespepito.com/usuarios/perfil/d02560dd9d7db4467627745bd6701e809ffca6e3">mater</a></td>
    <td class="tdcomentario"></td>
    <td class="tdreportar"><button class="btn btn-danger btn-mini hide sptt breportar" data-tt_my="left center" data-tt_at="right center" data-tt_titulo="Reportar problemas..." data-tt_texto="¿Algún problema con el enlace?, ¿esta roto?, ¿el audio esta mal?, ¿no corresponde el contenido?, repórtalo y lo revisaremos, ¡gracias!." data-enlace="385944" type="button"><i class="icon-warning-sign icon-white"></i></button></td>
    </tr>
    '''
    '''
    <tr>
    <td class="tdidioma"><span class="flag flag_3"></span></td>
    <td>28/12/2011</td>
    <td class="tdservidor"><img src="http://www.seriespepito.com/uploads/servidores/44-imagen_img.png" alt="Uploaded" />&nbsp;Uploaded</td>
    <td class="tdenlace"><a class="btn btn-mini enlace_link" rel="nofollow" target="_blank" title="Bajar..." href="http://rizzoli-and-isles.seriespepito.com/temporada-2/capitulo-15/329503/"><i class="icon-download"></i>&nbsp;Bajar</a></td>
    <td class="tdusuario"><a href="http://www.seriespepito.com/usuarios/perfil/9109c85a45b703f87f1413a405549a2cea9ab556">Pepito</a></td>
    <td class="tdcomentario"></td>
    <td class="tdreportar"><button class="btn btn-danger btn-mini hide sptt breportar" data-tt_my="left center" data-tt_at="right center" data-tt_titulo="Reportar problemas..." data-tt_texto="¿Algún problema con el enlace?, ¿esta roto?, ¿el audio esta mal?, ¿no corresponde el contenido?, repórtalo y lo revisaremos, ¡gracias!." data-enlace="329503" type="button"><i class="icon-warning-sign icon-white"></i></button></td>
    '''
    # Listas de enlaces
    patron  = '<tr[^<]+'
    patron += '<td class="tdidioma"><span class="([^"]+)".*?'
    patron += '<td class="tdservidor"><img src="([^"]+)"[^>]+>([^<]+)</td[^<]+'
    # patron += '<td class="tdenlace"><a class="btn btn-mini enlace_link" data-servidor="([^"]+)" rel="nofollow" target="_blank" title="[^"]+" href="([^"]+)"'
    patron += '<td class="tdenlace"><a class="btn btn-mini enlace_link" data-servidor="([^"]+)" rel="nofollow" target="_blank" title="[^"]+" href="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for idiomas,scrapedthumbnail,servidor,dataservidor,scrapedurl in matches:
        url = urlparse.urljoin(item.url,scrapedurl)
        title = "Ver en "+scrapertools.entityunescape(servidor).strip()
        plot = ""

        if "flag_0" in idiomas:
            title = title + " (Español)"
        if "flag_1" in idiomas:
            title = title + " (Latino)"
        if "flag_2" in idiomas:
            title = title + " (VO)"
        if "flag_3" in idiomas:
            title = title + " (VOS)"

        itemlist.append( Item(channel=__channel__, action="play" , title=title , url=url, thumbnail=item.thumbnail, plot=item.plot, show=item.show, folder=False,fanart="http://pelisalacarta.mimediacenter.info/fanart/seriespepito.jpg"))

    return itemlist

def play(item):
    logger.info("[seriespepito.py] play")
    itemlist=[]
    
    mediaurl = get_server_link_series(item.url)
    # Busca el vídeo
    videoitemlist = servertools.find_video_items(data=mediaurl)
    i=1
    for videoitem in videoitemlist:
        if not "favicon" in videoitem.url:
            videoitem.title = "Mirror %d%s" % (i,videoitem.title)
            videoitem.fulltitle = item.fulltitle
            videoitem.channel=channel=__channel__
            videoitem.show = item.show
            itemlist.append(videoitem)
            i=i+1

    return itemlist

def get_cookie(html):
    import cookielib

    ficherocookies = os.path.join( config.get_setting("cookies.dir"), 'cookies.dat' )
    cj = cookielib.MozillaCookieJar()
    cj.load(ficherocookies,ignore_discard=True)

    cookie_pat = "cookie\('([a-zA-Z0-9]+)'\);"
    cookie_name = scrapertools.find_single_match(html, cookie_pat)

    cookie_value = ""

    for cookie in cj:
        if cookie.name == cookie_name:
            cookie_value = cookie.value
            break

    return cookie_value

# Busca el enlace correcto y lo procesa capturando los caracteres
# y posiciones del Javascript
#
def convert_link(html, link_type):

    hash_seed = get_cookie(html);
    logger.info("[seriespepito.py] hash_seed="+hash_seed)

    HASH_PAT = 'CryptoJS\.(\w+)\('
    hash_func = scrapertools.find_single_match(html, HASH_PAT).lower()

    if hash_func == "md5":
        hash = hashlib.md5(hash_seed).hexdigest()
    else:
        hash = hashlib.sha256(hash_seed).hexdigest()

    if link_type == PELICULAS_PEPITO:
        hash += '0'
    logger.info("[seriespepito.py] hash="+hash)

    HREF_SEARCH_PAT = '<a class=".' + hash + '".*?href="http://www.enlacespepito.com\/([^\.]*).html"><i class="icon-(?:play|download)">'
    logger.info("[seriespepito.py] HREF_SEARCH_PAT="+HREF_SEARCH_PAT)

    href = list(scrapertools.find_single_match(html, HREF_SEARCH_PAT))
    logger.info("[seriespepito.py] href="+repr(href))
    CHAR_REPLACE_PAT = '[a-z]\[(\d+)\]="(.)";'

    matches = re.findall(CHAR_REPLACE_PAT , html, flags=re.DOTALL|re.IGNORECASE)
    logger.info("[seriespepito.py] matches="+repr(matches))

    for match in matches:
        href[int(match[0])] = match[1]

    href = ''.join(href)

    return 'http://www.enlacespepito.com/' + href + '.html'

def get_server_link(first_link, link_type):
    logger.info("[seriespepito.py] first_link="+str(first_link)+", link_type="+str(link_type))

    html = scrapertools.downloadpage(first_link, headers = ENLACESPEPITO_REQUEST_HEADERS)
    logger.info("[seriespepito.py] html="+html)

    fixed_link = convert_link(html, link_type)
    logger.info("[seriespepito.py] fixed_link="+fixed_link)

    # Sin el Referer da 404
    #ENLACESPEPITO_REQUEST_HEADERS.append(['Referer', first_link])

    return scrapertools.get_header_from_response(fixed_link, header_to_get="location", headers = ENLACESPEPITO_REQUEST_HEADERS)

# Estas funciones son las únicas que deberían llamarse desde fuera
#
def get_server_link_series(first_link):
    return get_server_link(first_link, SERIES_PEPITO)

def get_server_link_peliculas(first_link):

    return get_server_link(first_link, PELICULAS_PEPITO)





# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    
    # mainlist
    mainlist_items = mainlist(Item())
    
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    series_items = novedades(mainlist_items[0])
    bien = False
    for serie_item in series_items:
        episode_items = episodios( item=serie_item )

        for episode_item in episode_items:
            mediaurls = findvideos( episode_item )
            for mediaurl in mediaurls:
                if len( play(mediaurl) )>0:
                    return True

    return False