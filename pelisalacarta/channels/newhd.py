# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para newhd
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "newhd"
__category__ = "F"
__type__ = "generic"
__title__ = "NewHD"
__language__ = "ES"
__creationdate__ = "20110505"


DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[newhd.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Español", action="idioma", url="http://www.newhd.org/"))
    itemlist.append( Item(channel=__channel__, title="Inglés",  action="idioma", url="http://www.newhd.org/en/"))
    itemlist.append( Item(channel=__channel__, title="Latino",  action="idioma", url="http://www.newhd.org/lat/"))
    itemlist.append( Item(channel=__channel__, title="VOS",     action="novedades", url="http://www.newhd.org/sub/"))
    itemlist.append( Item(channel=__channel__, title="Buscar"  ,action="search" , url="http://www.newhd.org/"))
    return itemlist

def idioma(item):
    logger.info("[newhd.py] idioma")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Novedades", action="novedades", url=item.url+"index.php?do=cat&category=online"))
    itemlist.append( Item(channel=__channel__, title="Listado Alfabético", action="alfa", url=item.url+"index.php?do=cat&category=online"))
    itemlist.append( Item(channel=__channel__, title="Listado por Categorías", action="cat", url=item.url+"index.php?do=cat&category=online"))

    return itemlist

def search(item,texto):
    logger.info("[newhd.py] search")
    itemlist = []
    item.url = "http://www.newhd.org/index.php?do=search&subaction=search&story=%s" %texto
    itemlist.extend(searchlist(item))
    return itemlist
    
def novedades(item):
    logger.info("[newhd.py] novedades")

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas
    '''
    <table width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color:#ffffff;cursor:pointer;"
    id="9111" 
    onmouseover="colorFade('9111','background','ffffff','eff6f9')" 
    onmouseout="colorFade('9111','background','eff6f9','ffffff',25,50)">
    <tr valign="middle">
    <td width="1%" class="box" bgcolor="#FFFFFF"><div onClick="desplegarContraer('911',this);" class="linkContraido"><img src="/templates/newhd/images/mas.png" border="0"></div></td>
    <td width="85%" height="100%" class="box"><div onClick="desplegarContraer('911',this);" class="linkContraido">&nbsp;&nbsp;<font color="#83a0ba"><a>Salvar al soldado Ryan</a></font> </div></td>
    <td width="14%" align="right"><div align="right"><a href="http://www.newhd.org/online/online-belico/911-salvar-al-soldado-ryan.html"><img src="/templates/newhd/images/completo.png" onMouseOver="this.src='/templates/newhd/images/completoon.png';" onMouseOut="this.src='/templates/newhd/images/completo.png';" width="129" height="15" border="0"/></a></div></td>
    </tr>
    <td height="1" colspan="4" background="/templates/newhd/images/dotted.gif"><img src="/templates/newhd/images/spacer.gif" width="1" height="1" /></td>
    </tr>
    </table>
    <div id="911" class='elementoOculto'><table width="100%" class="box"><br><tr>
    <td width="14%" rowspan="6" align="left" valign="top"><img src="/uploads/thumbs/1319662843_salvar_al_soldado_ryan-738956437-large.jpg" width="112" height="154" border="0" align="top" /></td>
    <td height="122" colspan="4" valign="top"><div id="news-id-911" style="display:inline;">Durante la invasión de Normandía, en plena Segunda Guerra Mundial, a un grupo de soldados americanos se le encomienda una peligrosa misión: poner a salvo al soldado James Ryan. Los hombres de la patrulla del capitán John Miller deben arriesgar sus vidas para encontrar a este soldado, cuyos tres hermanos han muerto en la guerra. Lo único que se sabe del soldado Ryan es que se lanzó con su escuadrón de paracaidistas detrás de las líneas enemigas.</div><font style="text-transform: uppercase;">&nbsp;</font></td>
    <tr>
    <tr>
    <td height="20" valign="bottom" class="rating"><img src="/templates/newhd/images/floder.gif" width="20" height="16" align="absbottom" />&nbsp;Category: <font style="text-transform: uppercase;"><a href="http://www.newhd.org/online/">HD Online</a> &raquo; <a href="http://www.newhd.org/online/online-belico/">Belico</a></font></td>
    <td align="right" valign="bottom"> <a href="http://nowtrailer.tv/view/1060/Saving-Private-Ryan-1998-Official-Trailer.html" target="_blank"><img src="/templates/newhd/images/trailer.gif" alt="Trailer" width="37" height="15" border="0"></a> </td>
    <tr>
    <td height="1" background="/templates/newhd/images/dot_dark.gif"></td>    
    <td height="1"  background="/templates/newhd/images/dot_dark.gif"></td>
    <tr>
    <td width="73%" height="20" valign="bottom" class="rating"><div id='ratig-layer-911'><div class="rating" style="float:left;">
    <ul class="unit-rating">
    <li class="current-rating" style="width:0px;">0</li>
    <li><a href="#" title="Bad" class="r1-unit" onclick="dleRate('1', '911'); return false;">1</a></li>
    <li><a href="#" title="Poor" class="r2-unit" onclick="dleRate('2', '911'); return false;">2</a></li>
    <li><a href="#" title="Fair" class="r3-unit" onclick="dleRate('3', '911'); return false;">3</a></li>
    <li><a href="#" title="Good" class="r4-unit" onclick="dleRate('4', '911'); return false;">4</a></li>
    <li><a href="#" title="Excellent" class="r5-unit" onclick="dleRate('5', '911'); return false;">5</a></li>
    </ul>
    </div>
    
    patron  = '<table width="100\%" border="0" cellspacing="0" cellpadding="0".*?'
    patron += '<font[^<]+<a>([^<]+)</a>.*?'
    patron += '<a href="(http://www.newhd.org/online/[^"]+)"><img.*?<img.*?'
    patron += '<img src="([^"]+)".*?'
    patron += '<div id="news-id[^"]+" style="display\:inline\;">([^<]+)<'
    '''
    patron = '<tr valign="middle">(.*?)</a></font></td>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        try:
            scrapedurl = re.compile(r'href="(.+?)"').findall(match)[0]
        except:continue
        try:
            scrapedtitle = re.compile(r'<a>(.+?)</a>').findall(match)[0]
        except:
            scrapedtitle = "untitle"
        try:
            scrapedthumbnail = urlparse.urljoin(item.url,re.compile(r'html"><img src="([^"]+)" width=').findall(match)[0])
        except:
            scrapedthumbnail = ""
        try:
            scrapedplot = re.compile(r'(<td height="122".+?)<').findall(match)[0]
            scrapedplot = re.sub("<[^>]+>"," ",scrapedplot).strip()
        except:
            scrapedplot = ""
        logger.info(scrapedtitle)

        # Añade al listado
        itemlist.append( Item(channel=__channel__, action="videos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot ,context='4', folder=True) )

    # Extrae la marca de siguiente página
    patronvideos = '<a href="([^"]+)"><span class="thide pnext">Next</span>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedtitle = "Página siguiente"
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        scrapedthumbnail = ""
        itemlist.append( Item( channel=__channel__ , title=scrapedtitle , action="novedades" , url=scrapedurl , thumbnail=scrapedthumbnail, folder=True ) )

    return itemlist

def videos(item):

	logger.info("[newhd.py] videos")
	# Descarga la página
	data = scrapertools.cachePage(item.url)
	title= item.title
	scrapedthumbnail = item.thumbnail
	scrapedplot = item.plot
	listavideos = servertools.findvideos(data)

	itemlist = []
	for video in listavideos:
		scrapedtitle = title.strip() + " - " + video[0]
		videourl = video[1]
		server = video[2]
		#logger.info("videotitle="+urllib.quote_plus( videotitle ))
		#logger.info("plot="+urllib.quote_plus( plot ))
		#plot = ""
		#logger.info("title="+urllib.quote_plus( title ))
		if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+videourl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		itemlist.append( Item(channel=__channel__, action="play", title=scrapedtitle , url=videourl , thumbnail=scrapedthumbnail , plot=scrapedplot , server=server , folder=False) )

	return itemlist

def alfa(item):
    
    logger.info("[newhd.py] alfa")
    
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    
    # Extrae las entradas
    patronvideos  = '<a href="([^"]+)" class="blue">(.)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    
    itemlist = []
    for match in matches:
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedurl = scrapedurl.replace("&amp;","&")
        scrapedtitle = match[1]
        scrapedthumbnail = ""
        scrapedplot = ""
        logger.info(scrapedtitle)

        # Añade al listado
        itemlist.append( Item(channel=__channel__, action="novedades", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
        
    return itemlist

def cat(item):
    
    logger.info("[newhd.py] cat")
    
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    
    # Extrae las entradas
    patronvideos  = '<a title="([^"]+)" href="(/index.php\?do\=cat\&category\=[^"]+)">'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    
    itemlist = []
    for match in matches:
        scrapedurl = urlparse.urljoin(item.url,match[1])
        scrapedtitle = match[0]
        scrapedthumbnail = ""
        scrapedplot = ""

        # Añade al listado
        itemlist.append( Item(channel=__channel__, action="novedades", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
        
    return itemlist

def searchlist(item):
    logger.info("[newhd.py] searchlist")
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    
    # Extrae las entradas
    patronvideos  = 'class="newstitle">N&deg(.*?)</div></td>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    
    itemlist = []
    for match in matches:
        try:
            scrapedurl = re.compile(r'href="(.+?)"').findall(match)[0]
        except:continue
        try:
            scrapedtitle = re.compile(r'html" >(.+?)</a>').findall(match)[0]
        except:
            scrapedtitle = "untitle"
        try:
            scrapedthumbnail = urlparse.urljoin(item.url,re.compile(r'<img src="([^"]+)" width=').findall(match)[0])
        except:
            scrapedthumbnail = ""
        try:
            scrapedplot = re.compile(r'(<div id=.+?)</div></td>').findall(match)[0]
            scrapedplot = re.sub("<[^>]+>"," ",scrapedplot).strip()
        except:
            scrapedplot = ""
        logger.info(scrapedtitle)

        # Añade al listado
        itemlist.append( Item(channel=__channel__, action="videos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot ,context='4' , folder=True) )
        
    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    espanol_items = idioma(mainlist_items[0])
    novedades_items = novedades(espanol_items[0])
    bien = False
    for novedades_item in novedades_items:
        mirrors = servertools.find_video_items( item=novedades_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien