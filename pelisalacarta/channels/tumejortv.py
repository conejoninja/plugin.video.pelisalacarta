# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para tumejortv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "tumejortv"
__category__ = "F,S"
__type__ = "generic"
__title__ = "tumejortv.com"
__language__ = "ES"

DEBUG = config.get_setting("debug")

BASE_URL = "http://www.tumejortv.com"

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.channels.tumejortv mainlist")
    
    itemlist = []

    itemlist.append( Item(channel=__channel__, action="submenu" , title="Peliculas"    , url=BASE_URL+"/directorio/peliculas", extra="peliculas"))
    itemlist.append( Item(channel=__channel__, action="submenu" , title="Peliculas VO" , url=BASE_URL+"/directorio/peliculas_vo", extra="peliculas"))
    itemlist.append( Item(channel=__channel__, action="submenu" , title="Series"       , url=BASE_URL+"/directorio/series", extra="series"))
    itemlist.append( Item(channel=__channel__, action="submenu" , title="Series VO"    , url=BASE_URL+"/directorio/series_vo", extra="series"))

    return itemlist

def search(item,texto):
    logger.info("pelisalacarta.channels.tumejortv search")
    texto = texto.replace(" ","+")
    if item.url=="":
        item.url=BASE_URL+"/directorio/peliculas"
    try:
        if "peliculas_vo" in item.url:
            item.url="http://www.tumejortv.com/directorio/videos/buscar"
            item.extra = "antlo_buscar="+texto+"&antlo_buscar_donde=3"
            return peliculas(item)
        elif "series_vo" in item.url:
            item.url="http://www.tumejortv.com/directorio/videos/buscar"
            item.extra = "antlo_buscar="+texto+"&antlo_buscar_donde=4"
            return series(item)
        elif "peliculas" in item.url:
            item.url="http://www.tumejortv.com/directorio/videos/buscar"
            item.extra = "antlo_buscar="+texto+"&antlo_buscar_donde=1"
            return peliculas(item)
        elif "series" in item.url:
            item.url="http://www.tumejortv.com/directorio/videos/buscar"
            item.extra = "antlo_buscar="+texto+"&antlo_buscar_donde=2"
            return series(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def submenu(item):
    logger.info("pelisalacarta.channels.tumejortv submenu")
    
    itemlist = []

    itemlist.append( Item(channel=__channel__, action=item.extra        , title="Novedades"                  , url=item.url))
    itemlist.append( Item(channel=__channel__, action="alfabetico" , title="Todas por orden alfabetico" , url=item.url, extra=item.extra))
    itemlist.append( Item(channel=__channel__, action="search" , title="Buscar..." , url=item.url, extra=item.extra))

    return itemlist

def alfabetico(item):
    logger.info("pelisalacarta.channels.tumejortv alfabetico")
    
    itemlist=[]
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for letra in alfabeto:
        itemlist.append( Item(channel=item.channel, action=item.extra, title=str(letra), url = item.url + "/filtro_letras/"+letra))

    itemlist.append( Item(channel=item.channel, action=item.extra, title="0-9", url = item.url + "/filtro_letras/0"))

    return itemlist

# Listado de novedades de la pagina principal
def peliculas(item):
    logger.info("pelisalacarta.channels.tumejortv peliculas")

    url = item.url
    # Descarga la pagina
    if item.extra=="":
        data = scrapertools.cachePage(url)
    else:
        data = scrapertools.cachePage(url,post=item.extra)
    #logger.info(data)

    # Extrae las peliculas
    patron  = '<div class="antlo_dir_all_container">'
    patron += '<div rel="tag" data-href="([^"]+)".*?'
    patron += '<div class="antlo_dir_img_container"><a[^<]+<img src="([^"]+)"[^>]+></a>'
    patron += '<div class="antlo_pic_more_info"><span class="color1">([^>]+)<img src="[^"]+" alt="([^"]+)".*?</span></div></div><p>'
    patron += '<div class="antlo_dir_box_text_container"><h3 class="antlo_dir_video_title"><span[^<]+</span><br/><a[^>]+>([^<]+)</a></h3>'
    patron += '<span class="antlo_dir_video_cat">([^<]+)</span><h5 class="antlo_dir_video_calidad">([^<]+)</h5>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for url,thumbnail,tipo,idioma,titulo,categoria,calidad in matches:
        scrapedtitle = titulo+" ("+idioma.strip()+") ("+calidad+")"
        scrapedurl = url+"enlaces/"
        scrapedthumbnail = thumbnail
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideospeliculas" , title=scrapedtitle , fulltitle=scrapedtitle, url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    # Ordena los listados alfabeticos
    if "filtro_letras" in item.url:
        itemlist = sorted(itemlist, key=lambda Item: Item.title)    

    # Extrae la pagina siguiente
    patron = '<a href="([^"]+)">SIGUIENTE</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        scrapedtitle = ">> Pagina siguiente"
        scrapedurl = matches[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="peliculas" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

def series(item,extended=True):
    logger.info("pelisalacarta.channels.tumejortv series")

    url = item.url
    # Descarga la pagina
    if item.extra=="":
        data = scrapertools.cachePage(url)
    else:
        data = scrapertools.cachePage(url,post=item.extra)
    #logger.info(data)

    # Extrae las series
    '''
    <div class="antlo_dir_all_container">
    <div rel="tag" data-href="http://www.tumejortv.com/series/G-C-B---Golfas--Cursis-Y-Beatas-/" class="antlo_dir_pic_container color2" alt="G.C.B. (Golfas, Cursis Y Beatas)" title="G.C.B. (Golfas, Cursis Y Beatas)">
    <div class="antlo_dir_bandera"><img src="http://www.tumejortv.com/images/flags/f_estrenos_nuevo.png" alt="G.C.B. (Golfas, Cursis Y Beatas)" title="G.C.B. (Golfas, Cursis Y Beatas)"/></div>
    <div class="antlo_dir_img_container"><a href="http://www.tumejortv.com/series/G-C-B---Golfas--Cursis-Y-Beatas-/"><img src="http://www.tumejortv.com/images/posters/bXc4yUxJvPx4Hszf.jpeg" alt="G.C.B. (Golfas, Cursis Y Beatas)"/></a>
    <div class="antlo_pic_more_info"><span class="color2">Serie  <img src="http://www.tumejortv.com/images/idioma/antlo-es.png" alt="EspaÃÂ±ol" title="EspaÃÂ±ol"/><img src="http://www.tumejortv.com/images/general/posee_trailer.png" alt="Trailer" title="Trailer" style="margin: 0 3px;"/></span></div></div><p>
    <div class="antlo_dir_box_text_container"><h3 class="antlo_dir_video_title"><span style="font-size:1px;color:#3E3E3E;">Serie </span><br/><a href="http://www.tumejortv.com/series/G-C-B---Golfas--Cursis-Y-Beatas-/"> G.C.B. (Golfas, Cursis Y Beata...</a></h3>
    <h4 class="antlo_dir_video_cat">Temporada <span class="white">1</span> CapÃÂ­tulo <span class="white">10</span></h4><h5 class="antlo_dir_video_calidad">HDTV</h5></div></p></div></div>
    '''
    patron  = '<div class="antlo_dir_all_container">'
    patron += '<div rel="tag" data-href="([^"]+)".*?'
    patron += '<div class="antlo_dir_img_container"><a[^<]+<img src="([^"]+)"[^>]+></a>'
    patron += '<div class="antlo_pic_more_info"><span class="col[^"]+">([^>]+)<img src="[^"]+" alt="([^"]+)".*?</span></div></div><p>'
    patron += '<div class="antlo_dir_box_text_container"><h3 class="antlo_dir_video_title"><span[^<]+</span><br/><a[^>]+>([^<]+)</a></h3>'
    patron += '<h4 class="antlo_dir_video_cat">(.*?)<h5 class="antlo_dir_video_calidad">([^<]+)</h5'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for url,thumbnail,tipo,idioma,titulo,categoria,calidad in matches:
        scrapedtitle = titulo.strip()
        if extended:
            scrapedtitle = scrapedtitle +" ("+idioma.strip()+") ("+scrapertools.htmlclean(calidad)+")"
        scrapedurl = url+"capitulos/"
        scrapedthumbnail = thumbnail
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findepisodios" , title=scrapedtitle , fulltitle=scrapedtitle, url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=titulo.strip()))

    # Ordena los listados alfabeticos
    if "filtro_letras" in item.url:
        itemlist = sorted(itemlist, key=lambda Item: Item.title)    

    # Extrae la pagina siguiente
    patron = '<a href="([^"]+)">SIGUIENTE</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        scrapedtitle = ">> Pagina siguiente"
        scrapedurl = matches[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="series" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

def findepisodios(item):
    logger.info("pelisalacarta.channels.tumejortv findepisodios")
    
    itemlist=[]
    
    if item.url.startswith("http://www.tumejortv.com"):
        item.url=item.url.replace("http://www.tumejortv.com",BASE_URL)
    logger.info("url="+item.url)
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    #<a href="#" class="antlo_temporadas_li" title="Haga clic para ver listado de capitulos"><img src="http://www.tumejortv.com/images/general/more.png" /> TEMPORADA 1<span style="float:right;"><img src="http://www.tumejortv.com/images/general/estreno.png" alt="EstrenoT"/></span></a><div><table class="antlo_links_table">
    patron = '" class="antlo_temporadas_li" title="Haga clic[^"]+"><img[^>]+>( TEMPORADA [^<]+)<(.*?)</table>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    for temporada,episodios in matches:
        logger.info("temporada="+temporada+", episodios="+episodios)
        #<tr><td></td><td style="background-color:#f2f2f2;"><a title="Descargar - Ver" alt="Descargar - Ver" href="http://www.tumejortv.com/series/The-walking-Dead-2/temporada-3/capitulo-2/"> <img src="http://www.tumejortv.com/images/general/acceder.gif"><br />Descargar</a></td><td>2</td><td>107</td><td><a title="Descargar - Ver" alt="Descargar - Ver" href="http://www.tumejortv.com/series/The-walking-Dead-2/temporada-3/capitulo-2/"></a></td></tr>
        #patronepisodio = '<tr><td></td><td[^>]+><a title="[^"]+" alt="[^"]+" href="([^"]+)"> <img[^>]+><br />[^<]+</a></td><td>([^<]+)</td><td>([^<]+)</td><td><a[^>]+>([^<]+)</a></td></tr>'
        
        #<tr><td> <a href="http://www.tumejortv.com/series/90210-La-Nueva-Geracion-/trailers/826" alt="Ver Trailer" title="Ver trailer"><img src="http://www.tumejortv.com/images/general/trailer.png" alt="Trailer"/></a></td><td style="background-color:#f2f2f2;"><a title="Descargar - Ver" alt="Descargar - Ver" href="http://www.tumejortv.com/series/90210-La-Nueva-Geracion-/temporada-3/capitulo-1/"> <img src="http://www.tumejortv.com/images/general/acceder.gif"><br />Descargar</a></td><td>1</td><td>52</td><td><a title="Descargar - Ver" alt="Descargar - Ver" href="http://www.tumejortv.com/ser
        patronepisodio = '<tr>(.*?)</tr>'
        matches2 = re.compile(patronepisodio,re.DOTALL).findall(episodios)
        
        for match2 in matches2:
            
            try:
                url = scrapertools.get_match(match2,'<a title="Descargar - Ver" alt="Descargar - Ver" href="([^"]+)"')
            except:
                url=""
            try:
                episodio = scrapertools.get_match(match2,'</a></td><td>([^<]+)</td>')
            except:
                episodio = ""
            try:
                #</a></td><td>2</td><td>107</td>
                num_enlaces = scrapertools.get_match(match2,'</a></td><td[^<]+</td><td>([^<]+)</td>')
            except:
                num_enlaces = ""
            try:
                titulo = scrapertools.get_match(match2,'<a[^>]+>([^<]+)</a></td></tr>')
            except:
                titulo = ""

            if url!="":
                temporada = temporada.replace("TEMPORADA","").strip()
                if len(episodio)<2:
                    episodio = "0"+episodio
                itemlist.append( Item(channel=__channel__, action="findvideos" , title=temporada+"x"+episodio+" "+titulo+" ("+num_enlaces+" enlaces)" , url=url, thumbnail=item.thumbnail, show=item.show, plot=item.plot, folder=True, fulltitle=item.title+" "+temporada+"x"+episodio+" "+titulo))

    if config.get_platform().startswith("xbmc") or config.get_platform().startswith("boxee"):
        itemlist.append( Item(channel=item.channel, title="Añadir esta serie a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="findepisodios", show=item.show) )

    return itemlist

def findvideos(item):
    logger.info("pelisalacarta.channels.tumejortv findvideos")
    
    if item.url.startswith("http://www.tumejortv.com"):
        item.url=item.url.replace("http://www.tumejortv.com",BASE_URL)

    data = scrapertools.cache_page(item.url)
    itemlist=[]
    '''
    from servers import servertools
    itemlist = servertools.find_video_items(data=data)
    for videoitem in itemlist:
        videoitem.channel=__channel__
        videoitem.action="play"
        videoitem.folder=False
        videoitem.title = "["+videoitem.server+"]"
        videoitem.fulltitle=item.fulltitle
    '''
    '''
    <tr>
    <td  style="background-color:#F4FFF5;"  width="5px">
    <img src="http://www.tumejortv.com/images/general/estreno2.png" alt="Estreno2"/>
    </td>
    <td style="background-color:#f2f2f2;padding:5px;">
    <a href="http://www.vidxden.com/tt4vyii9k1r8" target="_blank" rel="nofollow">
    <img src="http://www.tumejortv.com/images/general/acceder.gif">
    <br /> Ver </a></td><td style="background-color:#F4FFF5;" >
    <a rel="nofollow" title=" Ver " href="http://www.vidxden.com/tt4vyii9k1r8" target="_blank">
    <img src="http://www.tumejortv.com/images/gestores/hmaSfmTfLQ3xULF2.png" alt="IMG" height="20px">
    <br>vidxden</a></td>
    <td style="background-color:#F4FFF5;" >1</td>
    <td style="background-color:#F4FFF5;" >HDTV 720p AC3 5.1</td><td style="background-color:#F4FFF5;" >
    <img src="http://www.tumejortv.com/resize_image.php?img=images/idioma/antlo-es.png&mw=80&mh=24" alt="EspaÃ±ol" title="EspaÃ±ol"/>
    </td><td style="background-color:#F4FFF5;" >
    <img src="http://www.tumejortv.com/resize_image.php?img=images/idioma/mM7jVs9QPgMysjip.png&mw=80&mh=24" alt="No" title="No"/>
    </td>
    <td style="background-color:#F4FFF5;" >Carlitos(o)</td>
    <td style="background-color:#F4FFF5;" ><a rel="nofollow" href="http://www.vidxden.com/tt4vyii9k1r8" target="_blank" title=" Ver ">Capitulo 306</a></td></tr>
    '''
    #<label class="text_link">ONLINE</label>(.*?)<div id="antlo_listado_capitulos">
    data = scrapertools.get_match(data,'<label class="text_link">ONLINE</label>(.*?)<div id="antlo_listado_capitulos">')
    #patron = '<a title="[^>]+" href="(http://www.tumejortv.com/.*?/url/\d+)"[^>]+>([^<]+)</a></td><td>([^<]+)</td><td><img src="[^"]+" alt="([^"]+)"'
    patron = '<tr>(.*?)</tr>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    for match in matches:
        
        try:
            #
            url = scrapertools.get_match(match,'<a rel="nofollow" href="([^"]+)" target="_blank" title=" Ver "')
        except:
            try:
                url = scrapertools.get_match(match,'<a rel="nofollow" title=" Bajar " href="([^"]+)"')
            except:
                logger.info("No encuentro la url en #"+match+"#")
                url=""
        try:
            #<br>vidxden</a></td>
            #<td style="background-color:#F4FFF5;" >1</td>
            #<td style="background-color:#F4FFF5;" >HDTV 720p AC3 5.1</td><td style="background-color:#F4FFF5;" >
            ### Modificado 03-07-2014
            #calidad = scrapertools.get_match(match,'<br>[^<]+</a></td[^<]+<td[^<]+</td[^<]+<td[^>]+>([^<]+)</td>')
            calidad = scrapertools.get_match(match,'</abbr></td><td[^>]+>([^<]+)</td>')
        except:
            logger.info("No encuentro la calidad en #"+match+"#")
            calidad=""
        ### Añadido 03-07-2014
        try:
            servidor = scrapertools.get_match(match,'<br>([^<]+)</a>').strip()
        except:
            logger.info("No encuentro el servidor en #"+match+"#")
            servidor=""
        try:
            ### Modificado 03-07-2014
            #idioma = scrapertools.get_match(match,'<br>[^<]+</a></td[^<]+<td[^<]+</td[^<]+<td[^<]+</td><td[^<]+<img src="[^"]+" alt="([^"]+)"')
            idioma = scrapertools.get_match(match,'<td[^>]+><img.*?images/idioma.*?title="([^"]+)"/></td>')

        except:
            logger.info("No encuentro el idioma en #"+match+"#")
            idioma=""

        if url!="":
            #http://www.tumejortv.com/peliculas/A-Roma-con-amor--2012--2/url/364905
            ### Modificado 03-07-2014
            #itemlist.append( Item(channel=__channel__, action="play" , title=scrapertools.get_domain_from_url(url).strip()+" ("+idioma+") ("+calidad+")" , url=url, thumbnail=item.thumbnail, plot=item.plot, folder=False, fulltitle=item.title))
            itemlist.append( Item(channel=__channel__, action="play" , title=scrapertools.get_domain_from_url(url).strip()+" ("+idioma+") ("+calidad+") ("+servidor+")" , url=url, thumbnail=item.thumbnail, plot=item.plot, folder=False, fulltitle=item.title))

    return itemlist

def findvideospeliculas(item):
    logger.info("pelisalacarta.channels.tumejortv findvideospeliculas")

    if item.url.startswith("http://www.tumejortv.com"):
        item.url=item.url.replace("http://www.tumejortv.com",BASE_URL)

    data = scrapertools.cache_page(item.url)
    itemlist=[]
    
    data = scrapertools.get_match(data,'DEO ONLINE</label>(.*?)<div id="antlo_panel_derecho">')
    patron = '<tr>(.*?)</tr>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        '''
        <td  style="background-color:#F4FFF5;"  width="5px"></td>
        <td style="background-color:#f2f2f2;padding:5px;">
          <a href="http://www.putlocker.com/file/5F69DEDC53BDB38B" target="_blank" rel="nofollow"> 
          <img src="http://www.tumejortv.com/images/general/acceder.gif">
          <br /> Ver </a>
        </td>
        <td style="background-color:#F4FFF5;" >
          <a rel="nofollow" title=" Ver " href="http://www.putlocker.com/file/5F69DEDC53BDB38B" target="_blank">
          <img src="http://www.tumejortv.com/images/gestores/Kd4wAuVbUUh8gg4q.png" alt="IMG" height="20px"><br>putlocker</a></td>
        <td style="background-color:#F4FFF5;" ><abbr title="1 Partes">1</abbr></td>
        <td style="background-color:#F4FFF5;" >BluRay-RIP</td>
        <td style="background-color:#F4FFF5;" ><img src="http://www.tumejortv.com/resize_image.php?img=images/idioma/tRGyYHsBvDCDBBGk.png&mw=80&mh=24" alt="Latino" title="Latino"/></td>
        <td style="background-color:#F4FFF5;" ><img src="http://www.tumejortv.com/resize_image.php?img=images/idioma/mM7jVs9QPgMysjip.png&mw=80&mh=24" alt="No" title="No"/></td>
        <td style="background-color:#F4FFF5;" >gonkus</td><td style="background-color:#F4FFF5;" ><a rel="nofollow" href="http://www.putlocker.com/file/5F69DEDC53BDB38B" target="_blank" title=" Ver ">Oz un mundo de ...</a></td>
        '''
        try:
            url = scrapertools.get_match(match,'<a rel="nofollow" title=" Ver " href="([^"]+)"')
        except:
            try:
                url = scrapertools.get_match(match,'<a rel="nofollow" title=" Bajar " href="([^"]+)"')
            except:
                logger.info("No encuentro la url en #"+match+"#")
                url=""
        try:
            #<br>vidxden</a></td>
            #<td style="background-color:#F4FFF5;" >1</td>
            #<td style="background-color:#F4FFF5;" >HDTV 720p AC3 5.1</td><td style="background-color:#F4FFF5;" >
            calidad = scrapertools.get_match(match,'<br>[^<]+</a></td[^<]+<td[^<]+<abbr[^<]+</abbr[^<]+</td[^<]+<td[^>]+>([^<]+)</td>')
        except:
            logger.info("No encuentro la calidad en #"+match+"#")
            calidad=""

        try:
            servidor = scrapertools.get_match(match,'<br>([^<]+)</a></td')
        except:
            logger.info("No encuentro el servidor en #"+match+"#")
            servidor=""

        try:
            idioma = scrapertools.get_match(match,'<br>[^<]+</a></td[^<]+<td[^<]+<abbr[^<]+</abbr[^<]+</td[^<]+<td[^<]+</td><td[^<]+<img src="[^"]+" alt="([^"]+)"')
        except:
            logger.info("No encuentro el idioma en #"+match+"#")
            idioma=""

        if url!="":
            if "www.tumejortv.com" in url:
                itemlist.append( Item(channel=__channel__, action="findvideos_partes" , title=scrapertools.get_domain_from_url(url).strip()+" ("+idioma+") ("+calidad+") ("+servidor+")" , url=url, thumbnail=item.thumbnail, plot=item.plot, folder=True, fulltitle=item.title))
            else:
                itemlist.append( Item(channel=__channel__, action="play" , title=scrapertools.get_domain_from_url(url).strip()+" ("+idioma+") ("+calidad+") ("+servidor+")" , url=url, thumbnail=item.thumbnail, plot=item.plot, folder=False, fulltitle=item.title))

    return itemlist

def findvideos_partes(item):
    logger.info("pelisalacarta.channels.tumejortv findvideospeliculas")

    if item.url.startswith("http://www.tumejortv.com"):
        item.url=item.url.replace("http://www.tumejortv.com",BASE_URL)

    data = scrapertools.cache_page(item.url)
    itemlist = servertools.find_video_items(data=data)
    for videoitem in itemlist:
        videoitem.channel = __channel__

    return itemlist

def play(item):
    logger.info("pelisalacarta.channels.tumejortv play")

    from servers import servertools
    itemlist = servertools.find_video_items(data=item.url)
    for videoitem in itemlist:
        videoitem.channel=__channel__
        videoitem.action="play"
        videoitem.folder=False

    return itemlist

def test():
    from servers import servertools
    
    # mainlist
    mainlist_items = mainlist(Item())
    submenu_items = submenu(mainlist_items[0])
    peliculas_items = peliculas(submenu_items[0])
    bien = False
    for pelicula_item in peliculas_items:
        mirrors = findvideospeliculas(item=pelicula_item)
        if len(mirrors)>0:
            bien = True
            break

    return bien