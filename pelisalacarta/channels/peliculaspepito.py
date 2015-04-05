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

__channel__ = "peliculaspepito"
__category__ = "F"
__type__ = "generic"
__title__ = "PeliculasPepito"
__language__ = "ES"

DEBUG = config.get_setting("debug")

ENLACESPEPITO_REQUEST_HEADERS = [
    ["User-Agent" , "Mozilla/5.0 (Windows NT 6.1; rv:28.0) Gecko/20100101 Firefox/28.0"],
    ["Accept-Encoding","gzip, deflate"],
    ["Accept-Language" , "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3"],
    ["Accept" , "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"],
    ["Cookie" , "__test"],
    ["Cookie" , "_ga=GA1.2.2034841797.1402481351"],
    ["Referer" , "http://the-invisible-woman.peliculaspepito.com/"],
    ["Connection" , "keep-alive"]
]

SERIES_PEPITO    = 0
PELICULAS_PEPITO = 1

def isGeneric():
    return True

def mainlist(item):
    logger.info("[seriespepito.py] mainlist")

    itemlist = []
	
    itemlist.append( Item(channel=__channel__, action="novedades"        , title="Estrenos", url="http://www.peliculaspepito.com/"))
    itemlist.append( Item(channel=__channel__, action="nuevas"        , title="Últimas añadidas", url="http://www.peliculaspepito.com/"))
    itemlist.append( Item(channel=__channel__, action="listalfabetico"   , title="Listado alfabético"))
    itemlist.append( Item(channel=__channel__, action="lomasvisto"    , title="Lo mas visto",    url="http://www.peliculaspepito.com/"))
    itemlist.append( Item(channel=__channel__, action="allserieslist"    , title="Listado completo"))
    itemlist.append( Item(channel=__channel__, action="buscar"        , title="Buscador", url="http://www.peliculaspepito.com/"))
    
    return itemlist

def buscar(item):
    keyboard = xbmc.Keyboard()
    keyboard.doModal()
    busqueda=keyboard.getText()
    data = scrapertools.cachePage("http://www.peliculaspepito.com/buscador/" + busqueda + "/")
    data = scrapertools.get_match(data,'<ul class="lp">(.*?)</ul>')
    patron  = '<li>'
    patron += '<a.*?href="([^"]+)">'
    patron += '<img.*?alt="([^"]+)" src="([^"]+)"[^>]+>'
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    itemlist = []
    for scrapedurl,scrapedtitle,scrapedthumbnail in matches:
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
        
        itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , url=url, thumbnail=thumbnail, plot=plot, show=title, viewmode="movie", fanart="http://pelisalacarta.mimediacenter.info/fanart/seriespepito.jpg"))

    return itemlist


   
def novedades(item):
    logger.info("[peliculaspepito.py] novedades")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #data = scrapertools.get_match(data,'<ul class="lista_peliculas">(.*?)</ul>')
    data = scrapertools.get_match(data,'<ul class="lp">(.*?)</ul>')
    
    '''
    [06-06-2014]
    <ul class="lp"><li><a class="tilcelpel" title="X-Men: Dias del futuro pasado" href="http://x-men-dias-del-futuro-pasado.peliculaspepito.com/"><img id="img_11020" data-id="11020" alt="X-Men: Dias del futuro pasado" src="http://s.peliculaspepito.com/peliculas/11020-x-men-dias-del-futuro-pasado-124853-thumb.jpg" /></a><div class="pfestrenoportada"><span class="text-warning">06-06-2014</span></div><div id="imgtilinforat11020" class="til_info_rat "><p><i class="icon-star icon-white"></i>8.6</p></div><div id="imgtilinfo11020" class="til_info"><p><a title="X-Men: Dias del futuro pasado" href="http://x-men-dias-del-futuro-pasado.peliculaspepito.com/">X-Men: Dias del futuro pasado</a></p><p class="pcalidi"><span class="flag flag_0"></span></p><p class="pidilis">TS&nbsp;Screener</p></div><a title="X-Men: Dias del futuro pasado" href="http://x-men-dias-del-futuro-pasado.peliculaspepito.com/"><div data-id="11020" id="til_info_sensor11020" data-on="0" data-an="0" class="til_info_sensor"></div></a></li>
    [.....]
    </ul>
    '''
    patron  = '<li>'
    #patron += '<a.*?href="([^"]+)"[^<]+'
    patron += '<a.*?href="([^"]+)">'
    patron += '<img.*?alt="([^"]+)" src="([^"]+)"[^>]+>.*?<p class="pidilis">(.*?)</p>'


    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []
    for scrapedurl,scrapedtitle,scrapedthumbnail, scrapedquality in matches:
        logger.info("title="+scrapedtitle)
        title = scrapertools.htmlclean(scrapedtitle).strip()
        title = title.replace("\r","").replace("\n","")+ ' [' + scrapedquality.replace("&nbsp;","") + ']'
        #title = unicode( title, "iso-8859-1" , errors="replace" ).encode("utf-8")
        title = re.compile("\s+",re.DOTALL).sub(" ",title)
        logger.info("title="+title)

        url = scrapedurl
        thumbnail = scrapedthumbnail
        plot = ""
        plot = unicode( plot, "iso-8859-1" , errors="replace" ).encode("utf-8")
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , url=url, thumbnail=thumbnail, plot=plot, show=title, viewmode="movie", fanart="http://pelisalacarta.mimediacenter.info/fanart/seriespepito.jpg"))

    return itemlist
	
def nuevas(item):
    logger.info("[peliculaspepito.py] novedades")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'<div class="subtitulo">Nuevos contenidos(.*?)</ul>')
    
    '''
   <li>
   <a class="tilcelpel" title="El diablo metió la mano" href="http://el-diablo-metio-la-mano.peliculaspepito.com/">
   <img id="img_2834" data-id="2834" alt="El diablo metió la mano" src="http://s.peliculaspepito.com/peliculas/2834-el-diablo-metio-la-mano-thumb.jpg" />
   </a>
   <div id="imgtilinfo2834" class="til_info">
   <p>
   <a title="El diablo metió la mano" href="http://el-diablo-metio-la-mano.peliculaspepito.com/">El diablo metió la mano</a>
   </p>
   <p class="pcalidi"><span class="flag flag_0"></span></p><p class="pidilis">DVD&nbsp;RIP</p></div>
   <a title="El diablo metió la mano" href="http://el-diablo-metio-la-mano.peliculaspepito.com/">
   <div data-id="2834" id="til_info_sensor2834" data-on="0" data-an="0" class="til_info_sensor">
   </div></a></li>
   '''
    patron  = '<li>'
    patron += '<a.*?href="([^"]+)"[^<]+'
    patron += '<img.*?alt="([^"]+)" src="([^"]+)"[^>]+>'
    patron += '.*?<p class="pidilis">([^<]+)</p>.*?</div>'


    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []
    for scrapedurl,scrapedtitle,scrapedthumbnail, scrapedquality in matches:
        logger.info("title="+scrapedtitle)
        title = scrapertools.htmlclean(scrapedtitle).strip()
        title = title.replace("\r","").replace("\n","")+ ' [' + scrapedquality.replace("&nbsp;"," ")+ ']'
        #title = unicode( title, "iso-8859-1" , errors="replace" ).encode("utf-8")
        title = re.compile("\s+",re.DOTALL).sub(" ",title)
        logger.info("title="+title)

        url = scrapedurl
        thumbnail = scrapedthumbnail
        plot = ""
        plot = unicode( plot, "iso-8859-1" , errors="replace" ).encode("utf-8")
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , url=url, thumbnail=thumbnail, plot=plot, show=title, viewmode="movie", fanart="http://pelisalacarta.mimediacenter.info/fanart/seriespepito.jpg"))

    return itemlist

def lomasvisto(item):
    logger.info("[seriespepito.py] lomasvisto")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'Lo más visto ayer(.*?)</ul>')
    #<a class="clearfix top" href="http://arrow.seriespepito.com/"><img class="thumb_mini" alt="Arrow" src="http://www.seriespepito.com/uploads/series/1545-arrow-thumb.jpg" />Arrow</a></li>
    '''
	<li>
	<a class="clearfix top" title="Ocho apellidos vascos con 1.215 visitas." href="http://ocho-apellidos-vascos.peliculaspepito.com/">
	<img class="thumb_mini" alt="Ocho apellidos vascos" src="http://s.peliculaspepito.com/peliculas/13558-ocho-apellidos-vascos-thumb.jpg" />Ocho apellidos vascos
	</a>
	</li>
    '''
    patron  = '<a.*?href="([^"]+)"[^<]+'
    patron += '<img.*?src="([^"]+)"[^>]+>([^<]+)</a>'

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

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , url=url, thumbnail=thumbnail, plot=plot, show=title, viewmode="movie", fanart="http://pelisalacarta.mimediacenter.info/fanart/seriespepito.jpg"))

    return itemlist

def allserieslist(item):
    logger.info("[peliculaspepito.py] completo()")
    itemlist = []

    # Carga el menú "Alfabético" de peliculas
    item = Item(channel=__channel__, action="listalfabetico")
    items_letras = listalfabetico(item)
    
    # Para cada letra
    for item_letra in items_letras:
        # Lee las series
        items_programas = peliculas(item_letra)
        itemlist.extend( items_programas )

    return itemlist

def listalfabetico(item):
    logger.info("[peliculaspepito.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="0-9",url="http://www.peliculaspepito.com/lista-peliculas/num/"))
    for letra in ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']:
        itemlist.append( Item(channel=__channel__, action="peliculas" , title=letra,url="http://www.peliculaspepito.com/lista-peliculas/"+letra.lower()+"/"))

    return itemlist

def peliculas(item):
    logger.info("[peliculaspepito.py] peliculas")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'<ul class="ullistadoalfa">(.*?)</ul>')

    patron = '<li><a title="([^"]+)" href="([^"]+)"[^<]'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []
    for scrapedtitle,scrapedurl in matches:
        #title = unicode( scrapedtitle.strip(), "iso-8859-1" , errors="replace" ).encode("utf-8")
        title = scrapedtitle.strip()
        url = scrapedurl
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , url=url, plot=plot, show=title,viewmode="movie", fanart="http://pelisalacarta.mimediacenter.info/fanart/seriespepito.jpg"))

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
        itemlist.append( Item(channel=item.channel, title="Añadir esta serie a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="episodios", show=item.show))
        itemlist.append( Item(channel=item.channel, title="Descargar todos los episodios de la serie", url=item.url, action="download_all_episodes", extra="episodios", show=item.show))

    return itemlist

def findvideos(item):
    logger.info("[peliculaspepito.py] findvideos")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cachePage(item.url)
    #logger.info(data)
    '''	
	<tr>
	<td id="tdidioma193869" class="tdidioma"><span class="flag flag_0">0</span></td>
	<td id="tdcalidad193869" class="tdcalidad">DVD&nbsp;RIP</td>
	<td class="tdfecha">24/03/2014</td>
	<td id="tdservidor193869" class="tdservidor"><img src="http://s.peliculaspepito.com/servidores/41-63845.png" alt="Magnovideo" />&nbsp;Magnovideo</td>
	<td class="tdenlace"><a class="btn btn_link" data-servidor="41" rel="nofollow" target="_blank" title="Ver&nbsp;(1)..." href="http://www.enlacespepito.com/02dead0f64bd970839e781f51eb48e86/193869/ef86bada70b2d0b58e3c21650195102e/c5529e8146dc4e3e642d647a91906e95/8d0e3e03b693eeb8dd20b35566362828/e1beb13340a813596ba87569b325ca67/9c98233803c502d86dcaad2fc6a31a4a/41f845928fd331b6e1478488e9864c8eaf15e2cc595c2e4e8259c02e44ac19ee1e7218f96bf81b32d52479b76992c12d/cefebb79e4d90ed1e8a2702c331025bf/57b22bd2a1f634dafd55ae1437daacb0/3d7eae712706ec33cc3a7566ac937114.html"><i class="icon-play"></i>&nbsp;&nbsp;Ver&nbsp;(1)</a></td>
	<td class="tdusuario"><a  title="Barbie"  href="http://www.peliculaspepito.com/usuarios/perfil/472b07b9fcf2c2451e8781e944bf5f77cd8457c8">Barbie</a></td>
			<td class="tdcomentario"></td>
			<td class="tdreportar">
				<button data-envio="193869" class="btn btn-danger btn-mini hide sptt pull-right breportar" data-tt_my="left center" data-tt_at="right center" data-tt_titulo="Reportar problemas..." data-tt_texto="¿Algún problema con el enlace?, ¿esta roto?, ¿el audio esta mal?, ¿no corresponde el contenido?, repórtalo y lo revisaremos, ¡gracias!." type="button"><i class="icon-warning-sign icon-white"></i></button>			</td>
			</tr>	
    '''

    # Listas de enlaces
    patron = '<td id="tdidioma[^"]+" class="tdidioma"><span class="[^"]+">(.*?)</span></td>.*?'
    patron += '<td id="tdservidor[^"]+" class="tdservidor"><img src="([^"]+)"[^>]+>([^<]+)</td[^<]+'
	# patron += '<td class="tdenlace"><a class="btn btn-mini enlace_link" data-servidor="([^"]+)" rel="nofollow" target="_blank" title="[^"]+" href="([^"]+)"'
    patron += '<td class="tdenlace"><a class="btn btn_link" data-servidor="([^"]+)" rel="nofollow" target="_blank" title="([^"]+)" href="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for idiomas,scrapedthumbnail,servidor,dataservidor,scrapedtitle, scrapedurl in matches:
        url = urlparse.urljoin(item.url,scrapedurl)
        title = item.title + " [" + servidor.replace("&nbsp;","") + "]"
        plot = ""

        if "0" in idiomas:
            title = title + " [Español]"
        if "1" in idiomas:
            title = title + " [Latino]"
        if "2" in idiomas:
            title = title + " [VO]"
        if "3" in idiomas:
            title = title + " [VOS]"

        itemlist.append( Item(channel=__channel__, action="play" , title=title , url=url, thumbnail=item.thumbnail, plot=item.plot, show=item.show, folder=False))

    # STRM para todos los enlaces de servidores disponibles
    # Si no existe el archivo STRM de la peícula muestra el item ">> Añadir a la biblioteca..."
    try: itemlist.extend( file_cine_library(item) )
    except: pass

    return itemlist

def file_cine_library(item):
    import os
    from platformcode.xbmc import library
    librarypath = os.path.join(config.get_library_path(),"CINE")
    archivo = library.title_to_folder_name(item.title.strip())
    strmfile = archivo+".strm"
    strmfilepath = os.path.join(librarypath,strmfile)

    if not os.path.exists(strmfilepath):
        itemlist.append( Item(channel=item.channel, title=">> Añadir a la biblioteca...", url=item.url, action="add_file_cine_library", extra="episodios", show=archivo) )

    return itemlist

def add_file_cine_library(item):
    from platformcode.xbmc import library, xbmctools
    library.savelibrary( titulo=item.show , url=item.url , thumbnail=item.thumbnail , server=item.server , plot=item.plot , canal=item.channel , category="Cine" , Serie="" , verbose=False, accion="play_from_library", pedirnombre=False, subtitle=item.subtitle )

    itemlist = []
    itemlist.append(Item(title='El vídeo '+item.show+' se ha añadido a la biblioteca'))
    xbmctools.renderItems(itemlist, "", "", "")

    return

def play(item):
    logger.info("[seriespepito.py] play")
    itemlist=[]

    mediaurl = get_server_link_peliculas(item.url)

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