# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cinetux
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "cinetux"
__category__ = "F"
__type__ = "generic"
__title__ = "Cinetux"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[cinetux.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Destacadas o actualizadas" , url="http://www.cinetux.org/destacados", fanart="http://pelisalacarta.mimediacenter.info/fanart/cinetux.jpg" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Novedades" , url="http://www.cinetux.org/", fanart="http://pelisalacarta.mimediacenter.info/fanart/cinetux.jpg" ))
    itemlist.append( Item(channel=__channel__ , action="bloque", title="Novedades subtitulado" , url="http://www.adsctx.net/sub.html", extra="Nuevo Sub", fanart="http://pelisalacarta.mimediacenter.info/fanart/cinetux.jpg" ))
    itemlist.append( Item(channel=__channel__ , action="bloque", title="Novedades DVD" , url="http://www.adsctx.net/dvdrip.html", extra="ltimo DVDRIP", fanart="http://pelisalacarta.mimediacenter.info/fanart/cinetux.jpg" ))
    itemlist.append( Item(channel=__channel__ , action="bloque", title="Novedades latino" , url="http://www.adsctx.net/latino.html", extra="Nuevo Latino", fanart="http://pelisalacarta.mimediacenter.info/fanart/cinetux.jpg" ))
    itemlist.append( Item(channel=__channel__ , action="bloque", title="Novedades castellano" , url="http://www.adsctx.net/castellano.html", extra="Nuevo Castellano", fanart="http://pelisalacarta.mimediacenter.info/fanart/cinetux.jpg" ))
    itemlist.append( Item(channel=__channel__ , action="bloque", title="Nueva calidad disponible" , url="http://www.adsctx.net/calidad.html", extra="Nueva Calidad", fanart="http://pelisalacarta.mimediacenter.info/fanart/cinetux.jpg" ))
    itemlist.append( Item(channel=__channel__ , action="generos", title="Por géneros" , url="http://www.cinetux.org/", fanart="http://pelisalacarta.mimediacenter.info/fanart/cinetux.jpg" ))

    return itemlist

def peliculas(item):
    logger.info("[cinetux.py] peliculas")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    '''
    <div style="width: 620px; padding: 0; margin-left: 10px;"><center><div id="post-18159">
    <!--PELICULA--><div class="movielist textcenter">
    <div id="titlecat"><a href="http://www.cinetux.org/2013/03/ver-pelicula-juramento-de-venganza-online-gratis-2009.html" rel="bookmark" title="Ver Película Juramento de Venganza Online Gratis (2009)"><img style="border: 1px solid #FDC101; padding: 1px;" width="130" height="190" src=http://1.bp.blogspot.com/_qNP_wQsK6pg/S4bJOWtjwII/AAAAAAAAALQ/3L0f3yP5c4g/s320/197276.jpg />
    <div style="margin-top:2px;">Ver Película Juramen...</div>
    </a></div>
    <div style="margin-top:5px;margin-bottom:5px;"><span class="rating"><img src="http://www.cinetux.org/wp-content/plugins/wp-postratings/images/stars_crystal/rating_off.png" alt="0 votes, average: 0,00 out of 5" title="0 votes, average: 0,00 out of 5" class="post-ratings-image" /><img src="http://www.cinetux.org/wp-content/plugins/wp-postratings/images/stars_crystal/rating_off.png" alt="0 votes, average: 0,00 out of 5" title="0 votes, average: 0,00 out of 5" class="post-ratings-image" /><img src="http://www.cinetux.org/wp-content/plugins/wp-postratings/images/stars_crystal/rating_off.png" alt="0 votes, average: 0,00 out of 5" title="0 votes, average: 0,00 out of 5" class="post-ratings-image" /><img src="http://www.cinetux.org/wp-content/plugins/wp-postratings/images/stars_crystal/rating_off.png" alt="0 votes, average: 0,00 out of 5" title="0 votes, average: 0,00 out of 5" class="post-ratings-image" /><img src="http://www.cinetux.org/wp-content/plugins/wp-postratings/images/stars_crystal/rating_off.png" alt="0 votes, average: 0,00 out of 5" title="0 votes, average: 0,00 out of 5" class="post-ratings-image" /></span></div>
    <center><span class="linkcat"><a href="http://www.cinetux.org/genero/thriller" title="Ver todas las entradas en Thriller" rel="category tag">Thriller</a></span></center>
    </div>
    <!--FIN PELICULA-->
    </div><!-- POST META 18159 END -->
    </center></div>
    '''

    # Extrae las entradas (carpetas)
    patron  = '<!--PELICULA--><div class="movielist textcenter[^<]+'
    patron += '<div id="titlecat[^<]+<a href="([^"]+)" rel="bookmark" title="([^"]+)"><img style="[^"]+" width="[^"]+" height="[^"]+" src=(.*?) /[^<]+'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,title,thumbnail in matches:
        scrapedplot = ""
        scrapedthumbnail = thumbnail[:-2]
        scrapedtitle = title[14:]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , fulltitle=scrapedtitle, url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , viewmode="movie", fanart="http://pelisalacarta.mimediacenter.info/fanart/cinetux.jpg", folder=True) )


    '''
    <div class="peli_item textcenter">
    <div class="pelicula_img"><a href="http://www.cinetux.org/2013/01/ver-pelicula-la-matanza-de-texas-3d-online-gratis-2013.html"><img alt="" src="http://1.bp.blogspot.com/-Rg9cCqo9Akg/UWub17Y4jVI/AAAAAAAAFo0/jp-8bQVxTB4/s200/La+Masacre+De+Texas+3D.jpg" width="104" height="150" /></a></div>
    <div class="dvdrip"> </div>
    <p><span class="rosa">DVD-RIP</span><br /><span class="icos_lg"><img style="border: 0pt none;" alt="" src="http://4.bp.blogspot.com/-qVqs0f0dsoM/UVJ2-nPN6MI/AAAAAAAAB_8/NkYdkmM-uvY/s320/lat.png" /><img style="border: 0pt none;" alt="" src="http://3.bp.blogspot.com/-t8w6a8_Hk-w/TeA7nd5Ad9I/AAAAAAAADNI/UYV40sR_sfc/s16/online.png" /><img style="border: 0pt none;" alt="" src="https://lh5.googleusercontent.com/-35yef7ubBv8/TeA7nNfUXJI/AAAAAAAADM0/RCQqAiWLX9o/s16/descarga.png" /></span></p>
    <div class="calidad5"> </div>
    <p>&nbsp;</p>
    </div>
    '''

    patron  = '<div class="peli_item textcenter"[^<]+'
    patron += '<div class="pelicula_img"[^<]+'
    patron += '<a href="([^"]+)[^<]+<img alt="" src="([^"]+)".*?'
    patron += '<span class="rosa">(.*?)</span>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedthumbnail,calidad in matches:
        partes = scrapedurl.split("/")
        titulo = partes[len(partes)-1]
        titulo = titulo.replace("ver-pelicula","")
        titulo = titulo.replace("online-gratis","")
        titulo = titulo.replace(".html","")
        titulo = titulo.replace("-"," ")
        titulo = titulo.strip().capitalize()

        scrapedplot = ""
        scrapedtitle = titulo + " ["+calidad+"]"
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , fulltitle=scrapedtitle, url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , viewmode="movie", fanart="http://pelisalacarta.mimediacenter.info/fanart/cinetux.jpg",  folder=True) )

    '''
    <div id="post-57573">
    <div class="itemarchive itemarchive_ie"><a href="http://www.cinetux.org/2014/08/ver-pelicula-tron-legacy-online-gratis-2010.html" rel="bookmark" title="Ver Película TRON: Legacy Online Gratis (2010)"><img style="border: 1px solid #FFFF00; padding: 2px;" width="150" height="205" src=http://4.bp.blogspot.com/_HeR0kdSfWC4/TSPIYcDNW4I/AAAAAAAALDY/WhA3qs_-jvo/s320/tron_legacy9.jpg /></a></div>
    </div><!-- POST META 57573 END -->
    '''
    patron  = '<div id="post-\d+"[^<]+'
    patron += '<div class="i[^<]+'
    patron += '<a href="([^"]+)" rel="[^"]+" title="([^"]+)"[^<]+'
    patron += '<img style="[^"]+" width="\d+" height="\d+" src=([^>]+)>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,title,thumbnail in matches:
        scrapedplot = ""
        scrapedthumbnail = thumbnail[:-2]
        scrapedtitle = title[14:]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , fulltitle=scrapedtitle, url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , viewmode="movie", fanart="http://pelisalacarta.mimediacenter.info/fanart/cinetux.jpg", folder=True) )

    # Extrae el paginador
    next_page_link = scrapertools.find_single_match(data,'<a href="([^"]+)"[^<]+<strong>Siguiente</strong>')
    if next_page_link!="":
        itemlist.append( Item(channel=__channel__, action="peliculas", title="Página siguiente >>" , url=next_page_link , fanart="http://pelisalacarta.mimediacenter.info/fanart/cinetux.jpg", folder=True) )

    return itemlist

def bloque(item):
    logger.info("[cinetux.py] bloque")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #data = scrapertools.get_match(data,item.extra+'</h6>(.*?)</div>')
    
    #<a target="_blank" href="http://www.cinetux.org/2013/04/ver-pelicula-dark-skies-online-gratis-2013.html"><img style="border:1px solid #FDC101;" src="http://4.bp.blogspot.com/-UlKHsLS3Tsk/URJotTqg-_I/AAAAAAAAA5c/8lhe3kY4jzc/s80/Dark+Skies+%282013%29+Movie+Review.jpg" height="75" width="47">
    patron = '<a target="_blank" href="([^"]+)"><img style="[^"]+" src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedthumbnail in matches:
        scrapedplot = ""
        
        parsed_url = urlparse.urlparse(scrapedurl)
        fichero = parsed_url.path
        partes = fichero.split("/")
        scrapedtitle = partes[ len(partes)-1 ]
        scrapedtitle = scrapedtitle.replace("ver-pelicula-","")
        scrapedtitle = scrapedtitle.replace("-online-gratis","")
        scrapedtitle = scrapedtitle.replace(".html","")
        scrapedtitle = scrapedtitle.replace("-"," ")
        scrapedtitle = scrapedtitle.capitalize()

        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , fulltitle=scrapedtitle, url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , viewmode="movie", fanart="http://pelisalacarta.mimediacenter.info/fanart/cinetux.jpg" , folder=True) )

    return itemlist

def generos(item):
    logger.info("[cinetux.py] generos")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'neros</h6>(.*?)</div>')
    
    patron = '<a href="([^"]+)">([^<]+)<'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="peliculas", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , fanart="http://pelisalacarta.mimediacenter.info/fanart/cinetux.jpg" , folder=True) )

    return itemlist

def tags(item):
    logger.info("[cinetux.py] tags")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'Tags</h6>(.*?)</div>')
    patron = "<a href='([^']+)'[^>]+>([^<]+)<"
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="peliculas", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , fanart="http://pelisalacarta.mimediacenter.info/fanart/cinetux.jpg" , folder=True) )

    return itemlist

def findvideos(item):
    logger.info("[cinetux.py] findvideos")
    itemlist=[]

    # Busca el argumento
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    '''
    <tr class="tabletr">
    <td class="episode-server" align="left"><img src="http://www.cinetux.org/imagenes/veronline.png" alt="" width="22" height="22" />Opción 01</td>
    <td class="episode-server-img" align="center">PutLocker</td>
    <td class="episode-lang" align="center">Español</td>
    <td align="center">DVD-SCR</td>
    <td class="center" align="center"><a rel="nofollow" target="_blank" class="myButtonLink" href="http://www.putlocker.com/file/BADCD9ACA395E318"></a></td>
    <td align="center">Anónimo</td>
    </tr>
    '''
    patron  = '<tr class="tabletr">[^<]+'
    patron += '<td class="opcion-td"><img[^>]+>([^>]+)</td>[^<]+'
    patron += '<td class="server-td[^>]+>([^<]+)</td>[^<]+'
    patron += '<td class="idioma-td[^>]+>([^>]+)</td>[^<]+'
    patron += '<td class="calidad-td[^<]+</td>[^<]+'
    patron += '<td class="fuente-td[^>]+>([^<]+)</td>[^<]+'
    patron += '<td class="link-td">(.*?)</td>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedtitle,scrapedserver,scrapedlanguage,scrapedquality,scrapedlink in matches:
        title = "Ver "+scrapedtitle+" en "+scrapedserver+" ("+scrapedlanguage+") ("+scrapedquality+")"
        url = scrapedlink
        thumbnail = item.thumbnail
        plot = ""
        itemlist.append( Item(channel=__channel__, action="play", title=title , fulltitle=item.fulltitle+" ["+scrapedlanguage+"]["+scrapedquality+"]", url=url , thumbnail=thumbnail , plot=plot , fanart="http://pelisalacarta.mimediacenter.info/fanart/cinetux.jpg" , folder=False) )

    patron  = '<tr class="tabletr">[^<]+'
    patron += '<td class="opcion-td"><img[^>]+>([^>]+)</td>[^<]+'
    patron += '<td class="server-td[^>]+>([^<]+)</td>[^<]+'
    patron += '<td class="idioma-td[^>]+>([^<]+)</td>[^<]+'
    patron += '<td class="fuente-td[^>]+>([^<]+)</td>[^<]+'
    patron += '<td class="link-td">(.*?)</td>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedtitle,scrapedserver,scrapedlanguage,scrapedquality,scrapedlink in matches:
        title = "Ver "+scrapedtitle+" en "+scrapedserver+" ("+scrapedlanguage+") ("+scrapedquality+")"
        url = scrapedlink
        thumbnail = item.thumbnail
        plot = ""
        itemlist.append( Item(channel=__channel__, action="play", title=title , fulltitle=item.fulltitle+" ["+scrapedlanguage+"]["+scrapedquality+"]", url=url , thumbnail=thumbnail , plot=plot , fanart="http://pelisalacarta.mimediacenter.info/fanart/cinetux.jpg" , folder=False) )

    patron  = '<tr class="tabletr">[^<]+'
    patron += '<td class="episode-server[^>]+><img[^>]+>([^>]+)</td>[^<]+'
    patron += '<td class="episode-server-img[^>]+>([^<]+)</td>[^<]+'
    patron += '<td class="episode-lang[^>]+>([^>]+)</td>[^<]+'
    patron += '<td align="center">([^<]+)</td>[^<]+'
    patron += '<td(.*?)</td>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedtitle,scrapedserver,scrapedlanguage,scrapedquality,scrapedlink in matches:
        title = "Ver "+scrapedtitle+" en "+scrapedserver+" ("+scrapedlanguage+") ("+scrapedquality+")"
        url = scrapedlink
        thumbnail = item.thumbnail
        plot = ""
        itemlist.append( Item(channel=__channel__, action="play", title=title , fulltitle=item.fulltitle+" ["+scrapedlanguage+"]["+scrapedquality+"]", url=url , thumbnail=thumbnail , plot=plot , folder=False) )

    if len(itemlist)==0:
        itemlist = servertools.find_video_items(data=data)
        i=1
        for videoitem in itemlist:
            videoitem.title = "Ver Opción %d en %s" % (i,videoitem.server)
            videoitem.fulltitle = item.fulltitle
            videoitem.channel=channel=__channel__

    return itemlist

def play(item):
    logger.info("[cinetux.py] play item.url="+item.url)
    itemlist=[]
    itemlist = servertools.find_video_items(data=item.url)
    i=1
    for videoitem in itemlist:
        videoitem.title = "Mirror %d%s" % (i,videoitem.title)
        videoitem.fulltitle = item.fulltitle
        videoitem.channel=channel=__channel__
        i=i+1

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    novedades_items = peliculas(mainlist_items[0])
    bien = False
    for novedades_item in novedades_items:
        mirrors = findvideos( item=novedades_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien