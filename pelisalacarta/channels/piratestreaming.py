# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para piratestreaming
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "piratestreaming"
__category__ = "F"
__type__ = "generic"
__title__ = "piratestreaming"
__language__ = "IT"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[piratestreaming.py] mainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Novità"     , action="peliculas", url="http://www.piratestreaming.co/film-aggiornamenti.php"))
    itemlist.append( Item(channel=__channel__, title="Per genere" , action="categorias", url="http://www.piratestreaming.co/"))
    itemlist.append( Item(channel=__channel__, title="Cerca", action="search"))
    return itemlist
    
def search(item,texto):
    logger.info("[piratestreaming.py] search "+texto)
    itemlist = []
    texto = texto.replace(" ","%20")
    item.url = "http://www.piratestreaming.co/cerca.php?all="+texto
    item.extra = ""

    try:
        return peliculas(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def categorias(item):
    '''
    <a href="#">Film</a> 
    <ul> 
    <li><a href="http://www.piratestreaming.co/film-aggiornamenti.php">AGGIORNAMENTI</a></li> 
    <li><a href="http://www.web-streaming-mania.net/" target=_blank><strong><font color="red">&#171;FILM PORNO&#187;</font></a></strong></li> 
    <li><a href="http://www.piratestreaming.co/categoria/film/animazione.html">ANIMAZIONE</a></li> 
    <li><a href="http://www.piratestreaming.co/categoria/film/avventura.html">AVVENTURA</a></li> 
    <li><a href="http://www.piratestreaming.co/categoria/film/azione.html">AZIONE</a></li> 
    <li><a href="http://www.piratestreaming.co/categoria/film/biografico.html">BIOGRAFICO</a></li> 
    <li><a href="http://www.piratestreaming.co/categoria/film/comico.html">COMICO</a></li> 
    <li><a href="http://www.piratestreaming.co/categoria/film/commedia.html">COMMEDIA</a></li> 
    <li><a href="http://www.piratestreaming.co/categoria/film/documentario.html">DOCUMENTARIO</a></li> 
    <li><a href="http://www.piratestreaming.co/categoria/film/drammatico.html">DRAMMATICO</a></li> 
    <li><a href="http://www.piratestreaming.co/categoria/film/erotico.html">EROTICO</a></li> 
    <li><a href="http://www.piratestreaming.co/categoria/film/fantascienza.html">FANTASCIENZA</a></li> 
    <li><a href="http://www.piratestreaming.co/categoria/film/fantasy.html">FANTASY</a></li> 
    <li><a href="http://www.piratestreaming.co/categoria/film/giallo.html">GIALLO</a></li> 
    <li><a href="http://www.piratestreaming.co/categoria/film/grottesco.html">GROTTESCO</a></li> 
    <li><a href="http://www.piratestreaming.co/categoria/film/guerra.html">GUERRA</a></li> 
    <li><a href="http://www.piratestreaming.co/categoria/film/horror.html">HORROR</a></li> 
    <li><a href="http://www.piratestreaming.co/categoria/film/musical.html">MUSICAL</a></li> 
    <li><a href="http://www.piratestreaming.co/categoria/film/poliziesco.html">POLIZIESCO</a></li> 
    <li><a href="http://www.piratestreaming.co/categoria/film/romantico.html">ROMANTICO</a></li> 
    <li><a href="http://www.piratestreaming.co/categoria/film/romanzo.html">ROMANZO</a></li> 
    <li><a href="http://www.piratestreaming.co/categoria/film/sentimentale.html">SENTIMENTALE</a></li> 
    <li><a href="http://www.piratestreaming.co/categoria/film/storico.html">STORICO</a></li> 
    <li><a href="http://www.piratestreaming.co/categoria/film/thriller.html">THRILLER</a></li> 
    <li><a href="http://www.piratestreaming.co/categoria/film/western.html">WESTERN</a></li> 
    </ul>
    '''
    itemlist = []
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<a href="#">Film</a>[^<]+<ul>(.*?)</ul>' )
    patron  = '<li><a href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="peliculas", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def peliculas(item):
    logger.info("[piratestreaming.py] peliculas")
    itemlist = []

    # Descarga la p�gina
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas (carpetas)
    '''
    <div class="featuredItem"> <a href=http://www.imagerip.net/images/ilregnodig.jpg class="featuredImg img" rel="featured"><img src=http://www.imagerip.net/images/ilregnodig.jpg alt="featured item" style="width: 80.8px; height: 109.6px;" /></a>
    <div class="featuredText">
    <b><a href=http://www.piratestreaming.co/film/il-regno-di-gia-la-leggenda-dei-guardiani-streaming-ita.html>Il Regno di Ga' Hoole La leggenda dei guardiani  Ita </a></b> <br /><g:plusone size="small" href=http://www.piratestreaming.co/film/il-regno-di-gia-la-leggenda-dei-guardiani-streaming-ita.html></g:plusone>
    <div id="fb-root"></div><fb:like href="http://www.piratestreaming.co/film/il-regno-di-gia-la-leggenda-dei-guardiani-streaming-ita.html" send="false" layout="button_count" show_faces="false" action="like" colorscheme="dark" font=""></fb:like>    </b>      
    </div>
    </div>
    
    <div class="featuredItem"> 
    <a href="http://www.piratestreaming.co/film/paris-manhattan.html" class="featuredImg img rounded" rel="featured" style="border-top-left-radius: 4px; border-top-right-radius: 4px; border-bottom-right-radius: 4px; border-bottom-left-radius: 4px; ">
    <img src="http://www.imagerip.net/images/Of6FN.jpg" alt="Locandina Film" style="width: 80.8px; height: 109.6px;"></a>
    <div class="featuredText">
    <b> <a href="http://www.piratestreaming.co/film/paris-manhattan.html">Paris Manhattan </a><br><div style="height: 15px; width: 70px; display: inline-block; text-indent: 0px; margin: 0px; padding: 0px; background-color: transparent; border-style: none; float: none; line-height: normal; font-size: 1px; vertical-align: baseline; background-position: initial initial; background-repeat: initial initial; " id="___plusone_0"><iframe allowtransparency="true" frameborder="0" hspace="0" marginheight="0" marginwidth="0" scrolling="no" style="position: static; top: 0px; width: 70px; margin: 0px; border-style: none; left: 0px; visibility: visible; height: 15px; " tabindex="0" vspace="0" width="100%" id="I0_1352901511754" name="I0_1352901511754" src="https://plusone.google.com/_/+1/fastbutton?bsv&amp;size=small&amp;hl=en-US&amp;origin=http%3A%2F%2Fwww.piratestreaming.com&amp;url=http%3A%2F%2Fwww.piratestreaming.com%2Ffilm%2Fparis-manhattan.html&amp;jsh=m%3B%2F_%2Fapps-static%2F_%2Fjs%2Fgapi%2F__features__%2Frt%3Dj%2Fver%3Dmq7ez1ykxXY.it.%2Fsv%3D1%2Fam%3D!9YrXPIrxx2-ITyEIjA%2Fd%3D1%2Frs%3DAItRSTOgKZowsoksby8_wLnRD0d_umAXMQ#_methods=onPlusOne%2C_ready%2C_close%2C_open%2C_resizeMe%2C_renderstart%2Concircled&amp;id=I0_1352901511754&amp;parent=http%3A%2F%2Fwww.piratestreaming.com" title="+1"></iframe></div>
    <div id="fb-root"></div><fb:like href="http://www.piratestreaming.co/film/paris-manhattan.html" send="false" layout="button_count" show_faces="false" action="like" colorscheme="dark" font="" fb-xfbml-state="rendered" class="fb_edge_widget_with_comment fb_iframe_widget"><span style="height: 20px; width: 98px; "><iframe id="f2834df314" name="f2e5c9573" scrolling="no" style="border: none; overflow: hidden; height: 20px; width: 98px; " title="Like this content on Facebook." class="fb_ltr" src="http://www.facebook.com/plugins/like.php?api_key=&amp;locale=it_IT&amp;sdk=joey&amp;channel_url=http%3A%2F%2Fstatic.ak.facebook.com%2Fconnect%2Fxd_arbiter.php%3Fversion%3D17%23cb%3Df2495f47c%26origin%3Dhttp%253A%252F%252Fwww.piratestreaming.com%252Ff153526b2c%26domain%3Dwww.piratestreaming.com%26relation%3Dparent.parent&amp;href=http%3A%2F%2Fwww.piratestreaming.com%2Ffilm%2Fparis-manhattan.html&amp;node_type=link&amp;width=90&amp;layout=button_count&amp;colorscheme=dark&amp;action=like&amp;show_faces=false&amp;send=false&amp;extended_social_context=false"></iframe></span></fb:like>  <a href="http://www.piratestreaming.co/video1" target="_blank" rel="nofollow"><img src="http://www.imagerip.net/images/W57R.png"></a>  </b>      
    </div>
    </div>
    '''
    patron  = '<div class="featuredItem">\s*'
    patron += '<a[^>]*>'
    patron += '<img src="([^"]+)"[^<]+</a>[^<]+'
    patron += '<div class="featuredText">.*?'
    patron += '<a href=([^>]+)>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedthumbnail,scrapedurl,scrapedtitle in matches:
        scrapedplot = ""
        logger.info("scrapedurl="+scrapedurl)
        if scrapedurl.startswith("\""):
            scrapedurl=scrapedurl[1:-1]
        logger.info("scrapedurl="+scrapedurl)

        try:
            res = urllib2.urlopen(scrapedurl)
            daa = res.read()
            da = daa.split('justify;">');
            da = da[1].split('</p>')
            scrapedplot = scrapertools.htmlclean(da[0]).strip()
        except:
            scrapedplot= "Trama non disponibile"
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    '''
    <div class="featuredItem"> <a href=http://www.piratestreaming.co/film/supercondriaco-ridere-fa-bene-alla-salute.html class="featuredImg img" rel="featured"><img src=http://imagerip.net/images/2014/06/19/Supercondriaco.jpg alt="featured item" style="width: 80.8px; height: 109.6px;" /></a>
    <div class="featuredText">
    <b><a href=http://www.piratestreaming.co/film/supercondriaco-ridere-fa-bene-alla-salute.html>Supercondriaco - Ridere fa bene alla salute </b><br /><g:plusone size="medium" href=http://www.piratestreaming.co/film/supercondriaco-ridere-fa-bene-alla-salute.html rel="nofollow"></g:plusone>
    <div id="fb-root"></div><fb:like href="http://www.piratestreaming.co/film/supercondriaco-ridere-fa-bene-alla-salute.html" send="false" layout="button_count" show_faces="false" action="like" colorscheme="dark" font=""></fb:like> 
    </div>
    </div>
    '''
    patron  = '<div class="featuredItem"[^<]+'
    patron += '<a href=(.*?) [^<]+'
    patron += '<img src=(.*?) [^<]+</a[^<]+'
    patron += '<div class="featuredText"[^<]+'
    patron += '<b><a[^>]+>([^<]+)'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        logger.info("scrapedurl="+scrapedurl)
        if scrapedurl.startswith("\""):
            scrapedurl=scrapedurl[1:-1]
        logger.info("scrapedurl="+scrapedurl)

        try:
            res = urllib2.urlopen(scrapedurl)
            daa = res.read()
            da = daa.split('justify;">');
            da = da[1].split('</p>')
            scrapedplot = scrapertools.htmlclean(da[0]).strip()
        except:
            scrapedplot= "Trama non disponibile"
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], plot=["+scrapedplot+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # Extrae el paginador
    patronvideos  = '<td align="center">[^<]+</td>[^<]+<td align="center">\s*<a href="([^"]+)">[^<]+</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="peliculas", title="Next Page >>" , url=scrapedurl , folder=True) )

    return itemlist

# Verificaci�n autom�tica de canales: Esta funci�n debe devolver "True" si est� ok el canal.
def test():
    from servers import servertools
    
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los v�deos de "Novedades" devuelve mirrors
    novedades_items = peliculas(mainlist_items[0])
    bien = False
    for novedades_item in novedades_items:
        mirrors = servertools.find_video_items( item=novedades_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien
