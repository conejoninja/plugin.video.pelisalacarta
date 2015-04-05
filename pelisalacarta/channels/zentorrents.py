# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para zentorrents
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "zentorrents"
__category__ = "F"
__type__ = "generic"
__title__ = "Zentorrents"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.zentorrents mainlist")
    
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Películas"      , action="peliculas", url="http://www.zentorrents.com/peliculas" ,thumbnail="http://www.navymwr.org/assets/movies/images/img-popcorn.png", fanart="http://s18.postimg.org/u9wyvm809/zen_peliculas.jpg"))
    itemlist.append( Item(channel=__channel__, title="MicroHD" , action="peliculas", url="http://www.zentorrents.com/tags/microhd" ,thumbnail="http://s11.postimg.org/5s67cden7/microhdzt.jpg", fanart="http://s9.postimg.org/i5qhadsjj/zen_1080.jpg"))
    itemlist.append( Item(channel=__channel__, title="HDrip"  , action="peliculas", url="http://www.zentorrents.com/tags/hdrip", thumbnail="http://s10.postimg.org/pft9z4c5l/hdripzent.jpg", fanart="http://s15.postimg.org/5kqx9ln7v/zen_720.jpg"))
    itemlist.append( Item(channel=__channel__, title="Series"         , action="peliculas", url="http://www.zentorrents.com/series",  thumbnail="http://data2.whicdn.com/images/10110324/original.jpg", fanart="http://s10.postimg.org/t0xz1t661/zen_series.jpg"))
    itemlist.append( Item(channel=__channel__, title="Buscar..."      , action="search"   , url="http://www.zentorrents.com/buscar", thumbnail="http://newmedia-art.pl/product_picture/full_size/bed9a8589ad98470258899475cf56cca.jpg", fanart="http://s23.postimg.org/jdutugvrf/zen_buscar.jpg"))
    
    
    return itemlist

def search(item,texto):
    logger.info("pelisalacarta.palasaka search")
    itemlist = []
    
    try:
        texto = texto.replace(" ","+")
        item.url = item.url+"/buscar?searchword=%s&ordering=&searchphrase=all&limit=\d+"
        item.url = item.url % texto
        itemlist.extend(buscador(item))
        
        return itemlist
    
    except:
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def buscador(item):
    logger.info("pelisalacarta.zentorrents buscador")
    itemlist = []
    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    #data = scrapertools.get_match(data,'</form>(<table class="contentpaneopen">.*?</table>)')
    if "highlight" in data:
        searchword = scrapertools.get_match(data,'<span class="highlight">([^<]+)</span>')
        data = re.sub(r'<span class="highlight">[^<]+</span>',searchword,data)
    #<fieldset><div class="resultimage"><a title="Carmina Y Amén" href="/peliculas/15188-carmina-y-amen"><img alt="Carmina Y Amén" class="thumbnailresult" src="http://zentorrents.palasaka.net/images/articles/15/15188t.jpg"/></a></div><div class="resulttitle"><a class="contentpagetitle" href="/peliculas/15188-carmina-y-amen">Carmina Y Amén</a><br /><span class="small">(Descargas/Películas)</span></div><div class="resultinfo">Carmina y Aménarranca con la muerte súbita del marido de la protagonista, que convence a su hija (María León) de no dar parte de la defunción hasta pasados dos días para poder cobrar la paga doble que...</div></fieldset>

    patron = '<div class="moditemfdb">'       # Empezamos el patrón por aquí para que no se cuele nada raro
    patron+= '<a title="([^"]+)" '                       # scrapedtitulo
    patron+= 'href="([^"]+)".*?'                         # scrapedurl
    patron+= 'src="([^"]+)".*?'                          # scrapedthumbnail
    patron+= '<p>([^<]+)</p>'
    
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedtitulo, scrapedurl, scrapedthumbnail, scrapedplot in matches:
        scrapedtitulo= scrapedtitulo.replace(scrapedtitulo,"[COLOR white]"+scrapedtitulo+"[/COLOR]")
        torrent_tag="[COLOR pink] (Torrent)[/COLOR]"
        scrapedtitulo = scrapedtitulo + torrent_tag
        scrapedurl = "http://zentorrents.com" + scrapedurl
        scrapedplot = scrapedplot.replace("&aacute;","á")
        scrapedplot = scrapedplot.replace("&iacute;","í")
        scrapedplot = scrapedplot.replace("&eacute;","é")
        scrapedplot = scrapedplot.replace("&oacute;","ó")
        scrapedplot = scrapedplot.replace("&uacute;","ú")
        scrapedplot = scrapedplot.replace("&ntilde;","ñ")
        scrapedplot = scrapedplot.replace("&Aacute;","Á")
        scrapedplot = scrapedplot.replace("&Iacute;","Í")
        scrapedplot = scrapedplot.replace("&Eacute;","É")
        scrapedplot = scrapedplot.replace("&Oacute;","Ó")
        scrapedplot = scrapedplot.replace("&Uacute;","Ú")
        scrapedplot = scrapedplot.replace("&Ntilde;","Ñ")
        
        itemlist.append( Item(channel=__channel__, title=scrapedtitulo, url=scrapedurl, action="fanart", thumbnail=scrapedthumbnail, fulltitle=scrapedtitulo, plot=scrapedplot, fanart="http://s11.postimg.org/qu66qpjz7/zentorrentsfanart.jpg", folder=True) )





    return itemlist




def peliculas(item):
    logger.info("pelisalacarta.zentorrents peliculas")
    itemlist = []
    
    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|</p>|<p>|&amp;|amp;","",data)
    
    #<div class="blogitem "><a title="En Un Patio De Paris [DVD Rip]" href="/peliculas/17937-en-un-patio-de-paris-dvd-rip"><div class="thumbnail_wrapper"><img alt="En Un Patio De Paris [DVD Rip]" src="http://www.zentorrents.com/images/articles/17/17937t.jpg" onload="imgLoaded(this)" /></div></a><div class="info"><div class="title"><a title="En Un Patio De Paris [DVD Rip]" href="/peliculas/17937-en-un-patio-de-paris-dvd-rip" class="contentpagetitleblog">En Un Patio De Paris [DVD Rip]</a></div><div class="createdate">21/01/2015</div><div class="text">[DVD Rip][AC3 5.1 EspaÃ±ol Castellano][2014] Antoine es un m&uacute;sico de 40 a&ntilde;os que de pronto decide abandonar su carrera.</div></div><div class="clr"></div></div>
    
    patron =  '<div class="blogitem[^>]+>'
    patron += '<a title="([^"]+)" '
    patron += 'href="([^"]+)".*?'
    patron += 'src="([^"]+)".*?'
    patron += '<div class="createdate">([^<]+)</div>'
    
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    for scrapedtitulo, scrapedurl, scrapedthumbnail, scrapedcreatedate in matches:
        scrapedtitulo= scrapedtitulo.replace(scrapedtitulo,"[COLOR white]"+scrapedtitulo+"[/COLOR]")
        scrapedcreatedate= scrapedcreatedate.replace(scrapedcreatedate,"[COLOR bisque]"+scrapedcreatedate+"[/COLOR]")
        
        torrent_tag="[COLOR pink]Torrent:[/COLOR]"
        scrapedtitulo = scrapedtitulo +  "(" +torrent_tag + scrapedcreatedate + ")"
        scrapedurl = "http://zentorrents.com" + scrapedurl
        itemlist.append( Item(channel=__channel__, title=scrapedtitulo, url=scrapedurl, action="fanart", thumbnail=scrapedthumbnail, fulltitle=scrapedtitulo, fanart="http://s11.postimg.org/qu66qpjz7/zentorrentsfanart.jpg", folder=True) )
    # 1080,720 y seies

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|</p>|<p>|&amp;|amp;","",data)
    
    #<div class="blogitem "><a title="En Un Patio De Paris [DVD Rip]" href="/peliculas/17937-en-un-patio-de-paris-dvd-rip"><div class="thumbnail_wrapper"><img alt="En Un Patio De Paris [DVD Rip]" src="http://www.zentorrents.com/images/articles/17/17937t.jpg" onload="imgLoaded(this)" /></div></a><div class="info"><div class="title"><a title="En Un Patio De Paris [DVD Rip]" href="/peliculas/17937-en-un-patio-de-paris-dvd-rip" class="contentpagetitleblog">En Un Patio De Paris [DVD Rip]</a></div><div class="createdate">21/01/2015</div><div class="text">[DVD Rip][AC3 5.1 EspaÃ±ol Castellano][2014] Antoine es un m&uacute;sico de 40 a&ntilde;os que de pronto decide abandonar su carrera.</div></div><div class="clr"></div></div>
    
    patron =  '<div class="blogitem[^>]+>'
    patron += '<a href="([^"]+)".*? '
    patron += 'title="([^"]+)".*? '
    patron += 'src="([^"]+)".*?'
    patron += '<div class="createdate">([^<]+)</div>'

    
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    for scrapedurl, scrapedtitulo, scrapedthumbnail, scrapedcreatedate in matches:
        scrapedtitulo= scrapedtitulo.replace(scrapedtitulo,"[COLOR white]"+scrapedtitulo+"[/COLOR]")
        scrapedcreatedate= scrapedcreatedate.replace(scrapedcreatedate,"[COLOR bisque]"+scrapedcreatedate+"[/COLOR]")
        torrent_tag="[COLOR pink]Torrent:[/COLOR]"
        scrapedtitulo = scrapedtitulo +  "(" +torrent_tag + scrapedcreatedate + ")"
        scrapedurl = "http://zentorrents.com" + scrapedurl
        itemlist.append( Item(channel=__channel__, title=scrapedtitulo, url=scrapedurl, action="fanart", thumbnail=scrapedthumbnail, fulltitle=scrapedtitulo, fanart="http://s11.postimg.org/qu66qpjz7/zentorrentsfanart.jpg", folder=True) )

    # Extrae el paginador
    patronvideos  = '<a href="([^"]+)" title="Siguiente">Siguiente</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        title= "[COLOR chocolate]siguiente>>[/COLOR]"
        itemlist.append( Item(channel=__channel__, action="peliculas", title= title , url=scrapedurl , thumbnail="http://s6.postimg.org/9iwpso8k1/ztarrow2.png", fanart="http://s11.postimg.org/qu66qpjz7/zentorrentsfanart.jpg", folder=True) )
    
    return itemlist

def fanart(item):
    logger.info("pelisalacarta.peliculasdk fanart")
    itemlist = []
    url = item.url
    data = scrapertools.cachePage(url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    if "peliculas" in item.url:
    
        if "microhd" in url or "web" in url or "1080" in url or "bluray" in url or  "HDRip" in item.title:
            title= scrapertools.get_match(data,'<title>([^"]+) \[')
            title= re.sub(r"3D|[0-9]|SBS|-|","",title)
            title=title.replace('Perdón','perdon')
            title= title.replace(' ','%20')
            url="http://api.themoviedb.org/3/search/movie?api_key=57983e31fb435df4df77afb854740ea9&query=" + title + "&language=es&include_adult=false"
            data = scrapertools.cachePage(url)
            data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
            patron = '"page":1.*?"backdrop_path":"(.*?)".*?,"id"'
            matches = re.compile(patron,re.DOTALL).findall(data)
            if len(matches)==0:
               item.extra=item.thumbnail
               itemlist.append( Item(channel=__channel__, title =item.title , url=item.url, action="findvideos", thumbnail=item.thumbnail, fanart=item.extra, folder=True) )
            else:
                for fan in matches:
                    fanart="https://image.tmdb.org/t/p/original" + fan
                    item.extra= fanart
                    itemlist.append( Item(channel=__channel__, title =item.title , url=item.url, action="findvideos", thumbnail=item.thumbnail, fanart=item.extra, folder=True) )
        else:
                
                title= scrapertools.get_match(data,'<title>([^"]+) -')
                title= re.sub(r"3D|[0-9]|SBS|\(.*?\)|\[.*?\]|","",title)
                title=title.replace('Perdón','perdon')
                title= title.replace(' ','%20')
                url="http://api.themoviedb.org/3/search/movie?api_key=57983e31fb435df4df77afb854740ea9&query=" + title + "&language=es&include_adult=false"
                data = scrapertools.cachePage(url)
                data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
                patron = '"page":1.*?"backdrop_path":"(.*?)".*?,"id"'
                matches = re.compile(patron,re.DOTALL).findall(data)
                if len(matches)==0:
                    item.extra=item.thumbnail
                    itemlist.append( Item(channel=__channel__, title =item.title , url=item.url, action="findvideos", thumbnail=item.thumbnail, fanart=item.extra, folder=True) )
                else:
                    for fan in matches:
                        fanart="https://image.tmdb.org/t/p/original" + fan
                        item.extra= fanart
                        itemlist.append( Item(channel=__channel__, title =item.title , url=item.url, action="findvideos", thumbnail=item.thumbnail, fanart=item.extra, folder=True) )
        
       
    else:
        if "series" in item.url:
            if "hdtv" in item.url or "720" in item.title or "1080p" in item.title:
                title= scrapertools.get_match(data,'<title>([^"]+) \[')
                title= re.sub(r"3D|'|,|[0-9]|#|;|\[.*?\]|SBS|-|","",title)
                title= title.replace('Temporada','')
                title= title.replace('Fin','')
                title= title.replace('x','')
                title= title.replace('Heli','Helix')
                title= title.replace('Anatomía','Anatomia')
                title= title.replace(' ','%20')
            
                url="http://thetvdb.com/api/GetSeries.php?seriesname=" + title + "&language=es"
                if "Erase%20una%20vez%20%20" in item.title:
                    url ="http://thetvdb.com/api/GetSeries.php?seriesname=Erase%20una%20vez%20(2011)&language=es"
                data = scrapertools.cachePage(url)
                data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
                patron = '<Data><Series><seriesid>([^<]+)</seriesid>'
                matches = re.compile(patron,re.DOTALL).findall(data)
                if len(matches)==0:
                   item.extra=item.thumbnail
                   itemlist.append( Item(channel=__channel__, title =item.title , url=item.url, action="findvideos", thumbnail=item.thumbnail, fanart=item.extra, folder=True) )
                else:
                    for id in matches:
                        id_serie = id
                        url ="http://thetvdb.com/api/1D62F2F90030C444/series/"+id_serie+"/banners.xml"
                        data = scrapertools.cachePage(url)
                        data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
                        patron = '<Banners><Banner>.*?<VignettePath>(.*?)</VignettePath>'
                        matches = re.compile(patron,re.DOTALL).findall(data)
                        if len(matches)==0:
                           item.extra=item.thumbnail
                           itemlist.append( Item(channel=__channel__, title =item.title , url=item.url, action="findvideos", thumbnail=item.thumbnail, fanart=item.extra, folder=True) )
                    for fan in matches:
                        fanart="http://thetvdb.com/banners/" + fan
                        item.extra= fanart
                        itemlist.append( Item(channel=__channel__, title =item.title , url=item.url, action="findvideos", thumbnail=item.thumbnail, fanart=item.extra, folder=True) )
            else:
                title= scrapertools.get_match(data,'<title>([^"]+) -')
                title= re.sub(r"3D|'|,|[0-9]|#|;|´|SBS|\[.*?\]|-|","",title)
                title= title.replace('Temporada','')
                title= title.replace('Fin','')
                title= title.replace('x','')
                title= title.replace('Anatomía','Anatomia')
                title= title.replace(' ','%20')
                
                url="http://thetvdb.com/api/GetSeries.php?seriesname=" + title + "&language=es"
                if "Erase%20una%20vez%20%20" in title:
                    url ="http://thetvdb.com/api/GetSeries.php?seriesname=Erase%20una%20vez%20(2011)&language=es"
                data = scrapertools.cachePage(url)
                data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
                patron = '<Data><Series><seriesid>([^<]+)</seriesid>'
                matches = re.compile(patron,re.DOTALL).findall(data)
                if len(matches)==0:
                    item.extra=item.thumbnail
                    itemlist.append( Item(channel=__channel__, title =item.title , url=item.url, action="findvideos", thumbnail=item.thumbnail, fanart=item.extra, folder=True) )
                else:
                    for id in matches:
                        id_serie = id
                        url ="http://thetvdb.com/api/1D62F2F90030C444/series/"+id_serie+"/banners.xml"
                        data = scrapertools.cachePage(url)
                        data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
                        patron = '<Banners><Banner>.*?<VignettePath>(.*?)</VignettePath>'
                        matches = re.compile(patron,re.DOTALL).findall(data)
                        if len(matches)==0:
                            item.extra=item.thumbnail
                            itemlist.append( Item(channel=__channel__, title =item.title , url=item.url, action="findvideos", thumbnail=item.thumbnail, fanart=item.extra, folder=True) )
                    for fan in matches:
                        fanart="http://thetvdb.com/banners/" + fan
                        item.extra= fanart
                        itemlist.append( Item(channel=__channel__, title =item.title , url=item.url, action="findvideos", thumbnail=item.thumbnail, fanart=item.extra, folder=True) )
    
        else:

             title= scrapertools.get_match(data,'<title>([^"]+) -')
             title= re.sub(r"3D|[0-9]|SBS|-|\[.*?\]|","",title)
        
             title= title.replace(' ','%20')
             url="http://api.themoviedb.org/3/search/movie?api_key=57983e31fb435df4df77afb854740ea9&query=" + title + "&language=es&include_adult=false"
             data = scrapertools.cachePage(url)
             data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
             patron = '"page":1.*?"backdrop_path":"(.*?)".*?,"id"'
             matches = re.compile(patron,re.DOTALL).findall(data)
             if len(matches)==0:
                item.extra=item.thumbnail
                itemlist.append( Item(channel=__channel__, title =item.title , url=item.url, action="findvideos", thumbnail=item.thumbnail, fanart=item.extra, folder=True) )
             else:
                 for fan in matches:
                     fanart="https://image.tmdb.org/t/p/original" + fan
                     item.extra= fanart
             itemlist.append( Item(channel=__channel__, title =item.title , url=item.url, action="findvideos", thumbnail=item.thumbnail, fanart=item.extra, folder=True) )
    title ="Info"
    title = title.replace(title,"[COLOR skyblue]"+title+"[/COLOR]")
    itemlist.append( Item(channel=__channel__, action="info" , title=title , url=item.url, thumbnail=item.thumbnail, fanart=item.extra, folder=False ))
    return itemlist

def findvideos(item):
    logger.info("pelisalacarta.zentorrents findvideos")
    
    itemlist = []
    
    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|</p>|<p>|&amp;|amp;","",data)
    
    patron = '<div class="descargatext">.*?'
    patron += '<img alt="([^<]+)" '
    patron += 'src="([^"]+)".*?'
    patron += 'type.*?href="([^"]+)"'
    
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    for scrapedtitulo, scrapedthumbnail, scrapedurl in matches:
        infotitle= "[COLOR yellow][B]Ver--[/B][/COLOR]"
        scrapedtitulo= scrapedtitulo.replace(scrapedtitulo,"[COLOR white]"+scrapedtitulo+"[/COLOR]")
        title= infotitle + scrapedtitulo
        
        itemlist.append( Item(channel=__channel__, title =title , thumbnail=scrapedthumbnail, url=scrapedurl, fanart=item.fanart, action="play", folder=True) )
    
    
    return itemlist

def play(item):
    
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    itemlist = []

    link = scrapertools.get_match(data,"{ window.location = '([^']+)")
    link = urlparse.urljoin(item.url,link)
    logger.info("link="+link)
    
    
    itemlist.append( Item(channel=__channel__, action="play", server="torrent", title=item.title , url=link , fanart= item.extra, folder=False) )

    return itemlist

def info(item):
    logger.info("pelisalacarta.zentorrents info")
    
    url=item.url
    data = scrapertools.cachePage(url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    if  "web" in item.title or "1080" in item.title or "bluray" in item.title or  "HDRip" in item.title:
    
        title= scrapertools.get_match(data,'<title>([^"]+) \[')
    else:
        title= scrapertools.get_match(data,'<title>([^"]+) -')
        title = title.replace(title,"[COLOR aqua][B]"+title+"[/B][/COLOR]")
        plot = scrapertools.get_match(data,'onload="imgLoaded.*?</div>(.*?)<div class="zentorrents_download">')
        plot = plot.replace(plot,"[COLOR orange]"+plot+"[/COLOR]")
        plot = plot.replace("&aacute;","á")
        plot = plot.replace("&iacute;","í")
        plot = plot.replace("&eacute;","é")
        plot = plot.replace("&oacute;","ó")
        plot = plot.replace("&uacute;","ú")
        plot = plot.replace("&ntilde;","ñ")
        plot = plot.replace("&Aacute;","Á")
        plot = plot.replace("&Iacute;","Í")
        plot = plot.replace("&Eacute;","É")
        plot = plot.replace("&Oacute;","Ó")
        plot = plot.replace("&Uacute;","Ú")
        plot = plot.replace("&Ntilde;","Ñ")
        plot = plot.replace("<p>","")
        plot = plot.replace("</p>","")
        fanart="http://s11.postimg.org/qu66qpjz7/zentorrentsfanart.jpg"
        tbd = TextBox("DialogTextViewer.xml", os.getcwd(), "Default")
        tbd.ask(title, plot,fanart)
        del tbd
        return

try:
    import xbmc, xbmcgui
    class TextBox( xbmcgui.WindowXMLDialog ):
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
        
        def ask(self, title, text, image ):
            self.title = title
            self.text = text
            self.image = "http://s9.postimg.org/vc0l27qgf/smyasigue.png"
            self.doModal()

except:
    pass
    
        
