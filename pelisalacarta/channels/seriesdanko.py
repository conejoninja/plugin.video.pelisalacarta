# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para seriesdanko.com
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

PLUGIN_NAME = "pelisalacarta"

__channel__ = "seriesdanko"
__category__ = "S"
__type__ = "generic"
__title__ = "Seriesdanko"
__language__ = "ES"

DEBUG = config.get_setting("debug")

if config.get_system_platform() == "xbox":
    MaxResult = "55"
else:
    MaxResult = "500"

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.channels.seriesdanko mainlist")
    item.url = 'http://seriesdanko.com/'

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Novedades", action="novedades"   , url=item.url))
    itemlist.append( Item(channel=__channel__, title="A-Z", action="letras", url=item.url))
    itemlist.append( Item(channel=__channel__, title="Listado completo", action="allserieslist", url=item.url))
    itemlist.append( Item(channel=__channel__, title="Buscar", action="search" , url=item.url, thumbnail="http://www.mimediacenter.info/xbmc/pelisalacarta/posters/buscador.png"))

    return itemlist

def search(item,texto):
    logger.info("pelisalacarta.channels.seriesdanko search")
    item.url = "http://seriesdanko.com/pag_search.php?q1="+texto

    return series(item)

def novedades(item):
    logger.info("pelisalacarta.channels.seriesdanko novedades")

    itemlist = []
    extra = ""
    # Descarga la página
    data = scrapertools.downloadpageGzip(item.url).replace("\n","")
    #print data
    '''
    <h3 class='post-title entry-title'>The Good Wife 4x01 Sub.espa&ntildeol</h3>
    <div class='comentariosyfechas'>
    <a href='#D' title='¿Deje un comentario?'>&#191;Deje un comentario?</a>
    <span class='etiquetineditar'>2012-10-01 a las 16:33:04</span>
    </div>
    <div class='post-header'>
    <br /><a href="serie.php?serie=553" title='TODO-TITLE'><img class='ict' style='display: block; border: 3px solid #616161; opacity: 1; margin: 0px auto 10px; text-align: center; cursor: pointer; width: 400px; height: 500px; 'src='http://1.bp.blogspot.com/-YJMaorkbMtU/UGmpQZqIhiI/AAAAAAAAWPA/IXywwgXawFY/s400/the-good-wife-julianna-margulies-4.jpg' alt='TODO-alt' title='TODO-title' /></a><div face='trebuchet ms' style='text-align: center;'><a href='serie.php?serie=553'>
    <span style='font-weight: bold;'> </span> 
    <span style='font-weight: bold;'>Ya Disponible en V.O.S.E para ver online y descargar,aqui en SeriesDanko.com</span></a>
    <span style='font-weight: bold;'></span></div><div class='post-header-line-1'></div>
    </div>
    <div class='post-body entry-content'>
    '''
    patronvideos = "(<h3 class='post-title entry-title'>.*?<div class='post-body entry-content')"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    totalItems = len(matches)
    for match in matches:
        try:
            scrapedurl = urlparse.urljoin(item.url,re.compile(r"href=\"(serie.+?)\">").findall(match)[0])
        except:continue
        try:
            scrapedthumbnail = re.compile(r"src='(.+?)'").findall(match)[0]
        except:
            scrapedthumbnail = ""
        try:
            scrapedtitle = re.compile(r"class='post-title entry-title'>(.+?)<").findall(match)[0]
            scrapedtitle = decodeHtmlentities(scrapedtitle)
        except:
            scrapedtitle = "sin titulo"
        scrapedplot = ""
        itemlist.append( Item(channel=__channel__, action="episodios", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra = extra , folder=True , totalItems = totalItems ) )
    
    return itemlist

def allserieslist(item):
    logger.info("pelisalacarta.channels.seriesdanko allserieslist")

    Basechars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    BaseUrl = "http://seriesdanko.com/series.php?id=%s"
    action = "series"

    itemlist = []

    # Descarga la página
    data = scrapertools.downloadpageGzip(item.url)
    #logger.info(data)

    # Extrae el bloque de las series
    patronvideos = "Listado de series disponibles</h2>(.*?)<div class='clear'></div>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    data = matches[0]
    scrapertools.printMatches(matches)

    # Extrae las entradas (carpetas)
    patronvideos  = "<a href='([^']+)'.+?>([^<]+)</a>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    totalItems = len(matches)
    for url,title in matches:
        scrapedtitle = title.replace("\n","").replace("\r","")
        scrapedurl = url
        scrapedurl = urlparse.urljoin(item.url,scrapedurl.replace("\n","").replace("\r",""))
        scrapedthumbnail = ""
        scrapedplot = ""

        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        if title in Basechars or title == "0-9":
            
            scrapedurl = BaseUrl % title
        else:
            action = "episodios"

        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action=action , title=scrapedtitle , show=scrapedtitle, url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, fulltitle = scrapedtitle , totalItems = totalItems))

    return itemlist

def letras(item):
    logger.info("pelisalacarta.channels.seriesdanko letras")

    itemlist=[]
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for letra in alfabeto:
        itemlist.append( Item(channel=item.channel, action="series", title=str(letra), url = "http://seriesdanko.com/series.php?id=%s" % letra))

    itemlist.append( Item(channel=item.channel, action="series", title="0-9", url = "http://seriesdanko.com/series.php?id=0"))

    return itemlist

def detalle_programa(item):
    data = scrapertools.cachePage(item.url)

    # Argumento
    '''
    Informaci&oacuten de A c&aacutemara s&uacuteper lenta</b><div style="margin-top: 10px; height: 10px; border-top: 1px dotted #999999;"></div><Br />La revolucionaria serie de Discovery Channel nos revela el mundo de manera <Br>espectacular y asombrosa al modificar radicalmente un factor esencial: el <Br>tiempo. ¿C&oacutemo se contrae el rostro de una persona cuando un boxeador le da un <Br>pu&ntildeetazo en la cara? ¿Qu&eacute ocurre cuando se dispara una bala y atraviesa una  <Br> manzana?<Br /><Br><img style='float:right; margin:0 0 10px 10px;cursor:pointer; cursor:hand; width: 150px; height: 200px;border: 3px solid #616161; ' src=http://2.bp.blogspot.com/-9imlR7oVyK0/TomeSfjpmqI/AAAAAAAADz4/aDFpk_U_sMk/s400/a-camara-super-lenta-seriesdanko.jpg'' /><Br><Br /><BR /><span style="color:#ffc029;">G&eacutenero:</span><br><span style="color:#ffc029;">Pa&iacutes de origen:</span><br><span style="color:#ffc029;">Duraci&oacuten:</span><br><span style="color:#ffc029;">Idioma/s:</span><br><span style="color:#ffc029;">Episodios:</span><br><span style="color:#ffc029;">Temporadas:</span><br><span style="color:#ffc029;">Director:</span><br><span style="color:#ffc029;">Producci&oacuten:</span><div style='clear: both;'></div>
    '''
    patron = '<div style="[^"]+"></div>(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        item.plot = scrapertools.htmlclean(matches[0])

    return item

def series(item,data=""):
    logger.info("pelisalacarta.channels.seriesdanko series")
    itemlist = []
    
    # Descarga la página
    if data=="":
        data = scrapertools.cache_page(item.url)
        #logger.info("data="+data)

    # Averigua el encoding
    try:
        patronvideos = "charset=(.+?)'"
        charset = re.compile(patronvideos,re.DOTALL).findall(matches[0])
    except:
        logger.info("charset desconocido")
        charset = "utf-8"

    #<div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=748' title='Capitulos de: Aaron Stone'><img class='ict' src='http://3.bp.blogspot.com/-0m9BHsd1Etc/To2PMvCRNeI/AAAAAAAAD1Y/ax3KPRNnJjY/s400/aaron-stone.jpg' alt='Capitulos de: Aaron Stone' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=748' style='font-size: 11px;'>Capitulos de: Aaron Stone</a></div><br><br></div><div style='float:left;widt
    patronvideos = "<div[^<]+<a href='(serie.php[^']+)' title='Capitulos de\: ([^']+)'><img class='ict' src='([^']+)'"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
    if len(matches)==0:
        #<div style='float:left;width: 33%;text-align:center;'><a href='../serie.php?serie=938' title='Capitulos de: Tron: Uprising'><img class='ict' src='http://2.bp.blogspot.com/-N1ffDX9Cf_s/T7qPkVEoFgI/AAAAAAAALmM/EN_vA-UCJJY/s1600/tron--uprising.jpg' alt='Capitulos de: Tron: Uprising' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='../serie.php?serie=938' style='font-size: 11px;'>Capitulos de: Tron: Uprising'</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='../serie.php?serie=966' title='Capitulos de: Pablo Escobar El Patron del Mal '><img class='ict' src='http://2.bp.blogspot.com/-5Ten6N_ytgU/T-7569pKe5I/AAAAAAAAMnY/nfVNFd9W5Oo/s1600/Escobar-el-patron-del-mal.jpg' alt='Capitulos de: Pablo Escobar El Patron del Mal ' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='../serie.php?serie=966' style='font-size: 11px;'>Capitulos de: Pablo Escobar El Patron del Mal '</a></div><br><br></div></div></td></tr></tbody></table><div style='clear: both;'></div>
        patronvideos = "<div[^<]+<a href='(../serie.php[^']+)' title='Capitulos de\: ([^']+)'><img class='ict' src='([^']+)'"
        matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        scrapedtitle = unicode(scrapedtitle,"utf-8",errors="replace").encode("utf-8")
        scrapedtitle = scrapedtitle.replace("&aacute","&aacute;")
        scrapedtitle = scrapedtitle.replace("&eacute","&eacute;")
        scrapedtitle = scrapedtitle.replace("&iacute","&iacute;")
        scrapedtitle = scrapedtitle.replace("&oacute","&oacute;")
        scrapedtitle = scrapedtitle.replace("&uacute","&uacute;")
        scrapedtitle = scrapertools.entityunescape(scrapedtitle)
        scrapedurl = urlparse.urljoin( item.url , scrapedurl )
        itemlist.append( Item(channel=__channel__, action="episodios", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot="", show=scrapedtitle , folder=True) )

    return itemlist

def episodios(item):
    logger.info("pelisalacarta.channels.seriesdanko episodios")
    
    if config.get_platform()=="xbmc" or config.get_platform()=="xbmcdharma":
        import xbmc
        if config.get_setting("forceview")=="true":
            xbmc.executebuiltin("Container.SetViewMode(53)")  #53=icons
            #xbmc.executebuiltin("Container.Content(Movies)")
        
    if "|" in item.url:
        url = item.url.split("|")[0]
        sw = True
    else:
        url = item.url
        sw = False
    # Descarga la página
    if item.extra:
        
        contenidos = item.extra
        #print contenidos
    else:
        data = scrapertools.downloadpageWithoutCookies(url)

    # Extrae las entradas
        if sw:
            try:
                datadict = eval( "(" + data + ")" )    
                data = urllib.unquote_plus(datadict["entry"]["content"]["$t"].replace("\\u00","%"))
                matches=[]
                matches.append(data)
            except:
                matches = []
        else:
            patronvideos = "entry-content(.*?)<div class='blog-pager' id='blog-pager'>"
            matches = re.compile(patronvideos,re.DOTALL).findall(data)
            
        if len(matches)>0:
            contenidos = matches[0].replace('"',"'").replace("\n","")
        else:
            contenidos = item.url
            if sw:
                url = item.url.split("|")[1]
                if not url.startswith("http://"):
                    url = urlparse.urljoin("http://seriesdanko.com",url)
                # Descarga la página
                data = scrapertools.downloadpageGzip(url)
                patronvideos  = "entry-content(.*?)<div class='post-footer'>"
                matches = re.compile(patronvideos,re.DOTALL).findall(data)
                if len(matches)>0:
                    contenidos = matches[0]
                
    patronvideos  = "<a href='([^']+)'>([^<]+)</a> <img(.+?)/>"
    matches = re.compile(patronvideos,re.DOTALL).findall(contenidos.replace('"',"'"))
    #print contenidos        
    try:
        plot = re.compile(r'(Informac.*?/>)</div>').findall(contenidos)[0]
        if len(plot)==0:
            plot = re.compile(r"(Informac.*?both;'>)</div>").findall(contenidos)[0]
        plot = re.sub('<[^>]+>'," ",plot)
    except:
        plot = ""

    itemlist = []
    for match in matches:
        scrapedtitle = match[1].replace("\n","").replace("\r","")
        logger.info("scrapedtitle="+scrapedtitle)
        ## Eliminado para la opción "Añadir esta serie a la biblioteca de XBMC" (15-12-2014)
        #scrapedtitle = scrapertools.remove_show_from_title(scrapedtitle,item.show)
        
        episode_code = scrapertools.find_single_match(scrapedtitle,"(\d+X\d+)")
        logger.info("episode_code="+episode_code)
        if episode_code!="":
            season_number = scrapertools.find_single_match(scrapedtitle,"(\d+)X\d+")
            logger.info("season_number="+season_number)
            episode_number = scrapertools.find_single_match(scrapedtitle,"\d+X(\d+)")
            logger.info("episode_number="+episode_number)
            new_episode_code = season_number+"x"+episode_number
            logger.info("new_episode_code="+new_episode_code)
            scrapedtitle = scrapedtitle.replace(episode_code,new_episode_code)
            logger.info("scrapedtitle="+scrapedtitle)

        #[1x01 - Capitulo 01]
        #patron = "(\d+x\d+) - Capitulo \d+"
        #matches = re.compile(patron,re.DOTALL).findall(scrapedtitle)
        #print matches
        #if len(matches)>0 and len(matches[0])>0:
        #    scrapedtitle = matches[0]

        if "es.png" in match[2]:
            subtitle = " (Español)"
        elif "la.png" in match[2]:
            subtitle = " (Latino)"
        elif "vo.png" in match[2]:
            subtitle = " (VO)"
        elif "vos.png" in match[2]:
            subtitle = " (VOS)"
        elif "ca.png"  in match[2]:
            subtitle = " (Catalan)"
        elif "ga.jpg"  in match[2]:
            subtitle = " (Gallego)"
        elif "eu.jpg"  in match[2]:
            subtitle = " (Euskera)"
        elif "ba.png"  in match[2]:
            subtitle = " (Bable)"
        else:
            subtitle = ""
        scrapedplot = plot
        scrapedurl = urlparse.urljoin(item.url,match[0]).replace("\n","").replace("\r","")
        if not item.thumbnail:
            try:
                scrapedthumbnail = re.compile(r"src=([^']+)'").findall(contenidos)[0]
            except:
                    scrapedthumbnail = ""
        else:
            scrapedthumbnail = item.thumbnail
        scrapedthumbnail = scrapedthumbnail.replace("\n","").replace("\r","")
        if item.fulltitle == '':
            item.fulltitle = scrapedtitle + subtitle 
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        ## Añadido show para la opción "Añadir esta serie a la biblioteca de XBMC" (15-12-2014)
        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle+subtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , fulltitle = item.fulltitle, context="4", show=item.show, folder=True) )

    if (config.get_platform().startswith("xbmc") or config.get_platform().startswith("boxee")) and len(itemlist)>0:
        itemlist.append( Item(channel=item.channel, title="Añadir esta serie a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="episodios###", show=item.show))
        itemlist.append( Item(channel=item.channel, title="Descargar todos los episodios de la serie", url=item.url, action="download_all_episodes", extra="episodios###", show=item.show))

    #xbmc.executebuiltin("Container.Content(Movies)")
    
    if len(itemlist)==0:
        listvideos = servertools.findvideos(contenidos)
        
        for title,url,server in listvideos:
            
            if server == "youtube":
                scrapedthumbnail = "http://i.ytimg.com/vi/" + url + "/0.jpg"
            else:
                scrapedthumbnail = item.thumbnail
            scrapedtitle = title
            scrapedplot = ""
            scrapedurl = url
            
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

            # Añade al listado de XBMC
            itemlist.append( Item(channel=__channel__, action="play", server=server, title=item.title +" "+ scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot, fulltitle = scrapedtitle , folder=False) )

    return itemlist

def findvideos(item):
    logger.info("pelisalacarta.channels.seriesdanko findvideos")
    
    # Descarga la página
    if config.get_platform()=="xbmceden":
        from core.subtitletools import saveSubtitleName
        saveSubtitleName(item)
    
    if "seriesdanko.com" in item.url:
        data = scrapertools.downloadpageGzip(item.url).replace("\n","")
        patronvideos = "<tr><td class=('tam12'>.*?)</td></tr>"
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        #for match in matches:
            #print match
        itemlist = []
        for match in matches:
            try:
                scrapedurl = urlparse.urljoin(item.url,re.compile(r"href='(.+?)'").findall(match)[0])
            except:continue
           
            ## Modificado para que se vea el servidor en el título (15-12-2014)
            try:
                scrapedthumbnail = re.compile(r"src='(.+?)'").findall(match)[1]
                servidor = re.compile(r"servidores/([^\.]+)\.").findall(scrapedthumbnail)[0]
                servidor = " [" + servidor + "]"
                #if "megavideo" in scrapedthumbnail:
                #    mega = " [Megavideo]"
                #elif "megaupload" in scrapedthumbnail:
                #    mega = " [Megaupload]"
                #else:
                #    mega = ""
                if not scrapedthumbnail.startswith("http"):
                    scrapedthumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
            #except:continue
            except: servidor = ""
            try:
                subtitle = re.compile(r"src='(.+?)'").findall(match)[0]
                if "es.png" in subtitle:
                    subtitle = " (Español)"
                elif "la.png" in  subtitle:
                    subtitle = " (Latino)"
                elif "vo.png" in  subtitle:
                    subtitle = " (Version Original)"
                elif "vos.png" in  subtitle:
                    subtitle = " (Subtitulado)"
                elif "ca.png"  in match[2]:
                    subtitle = " (Catalan)"
                elif "ga.jpg"  in match[2]:
                    subtitle = " (Gallego)"
                elif "eu.jpg"  in match[2]:
                    subtitle = " (Euskera)"
                elif "ba.png"  in match[2]:
                    subtitle = " (Bable)"
                else:
                    subtitle = "(desconocido)"
                
                try:
                    opcion = re.compile(r"(Ver|Descargar)").findall(match)[0]
                except:
                    opcion = "Ver"
                
                ## Modificado para que se vea el servidor en el título (15-12-2014)
                #scrapedtitle = opcion + " video " + subtitle + mega
                scrapedtitle = opcion + " video " + subtitle + servidor
            except:
                scrapedtitle = item.title
            scrapedplot = ""
            #scrapedthumbnail = item.thumbnail
            #if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
    
            # Añade al listado de XBMC
            itemlist.append( Item(channel=__channel__, action="play", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot, fulltitle = item.fulltitle, extra = item.thumbnail , fanart=item.thumbnail , folder=False) )    
    
    else:
        from core import servertools
        itemlist = servertools.find_video_items( item )
    
    return itemlist

def play(item):
    logger.info("pelisalacarta.channels.seriesdanko play (url="+item.url+", server="+item.server+")" )

    # Descarga la página
    if "seriesdanko" in item.url:
        data = scrapertools.downloadpageGzip(item.url)
    else:
        data = item.url
    return servertools.find_video_items(data=data)

def decodeHtmlentities(string):
    string = entitiesfix(string)
    import re
    entity_re = re.compile("&(#?)(\d{1,5}|\w{1,8});")

    def substitute_entity(match):
        from htmlentitydefs import name2codepoint as n2cp
        ent = match.group(2)
        if match.group(1) == "#":
            return unichr(int(ent)).encode('utf-8')
        else:
            cp = n2cp.get(ent)

            if cp:
                return unichr(cp).encode('utf-8')
            else:
                return match.group()
                
    return entity_re.subn(substitute_entity, string)[0]
    
def entitiesfix(string):
    # Las entidades comienzan siempre con el símbolo & , y terminan con un punto y coma ( ; ).
    string = string.replace("&aacute","&aacute;")
    string = string.replace("&eacute","&eacute;")
    string = string.replace("&iacute","&iacute;")
    string = string.replace("&oacute","&oacute;")
    string = string.replace("&uacute","&uacute;")
    string = string.replace("&Aacute","&Aacute;")
    string = string.replace("&Eacute","&Eacute;")
    string = string.replace("&Iacute","&Iacute;")
    string = string.replace("&Oacute","&Oacute;")
    string = string.replace("&Uacute","&Uacute;")
    string = string.replace("&uuml"  ,"&uuml;")
    string = string.replace("&Uuml"  ,"&Uuml;")
    string = string.replace("&ntilde","&ntilde;")
    string = string.replace("&#191"  ,"&#191;")
    string = string.replace("&#161"  ,"&#161;")
    string = string.replace(";;"     ,";")
    return string

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    novedades_items = novedades(mainlist_items[0])
    bien = False
    for novedades_item in novedades_items:
        episodios_items = episodios(novedades_item)
        
        for episodio_item in episodios_items:
            
            mirrors_items = findvideos(episodio_item)
            
            for mirror_item in mirrors_items:
                videoitems = play(mirror_item)
                if len(videoitems)>0:
                    return True

    return False