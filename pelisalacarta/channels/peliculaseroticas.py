# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para peliculaseroticas
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re,time
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "peliculaseroticas"
__category__ = "F"
__type__ = "generic"
__title__ = "PeliculasEroticas"
__language__ = "ES"
__adult__ = "true"

from xml.dom import minidom
from xml.dom import EMPTY_NAMESPACE

DEBUG = config.get_setting("debug")

ATOM_NS = 'http://www.w3.org/2005/Atom'

def isGeneric():
    return True
    
def mainlist(item):
    logger.info("[peliculaseroticas.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="novedades"  , title="Novedades"  , url="http://www.blogger.com/feeds/6886871729120330561/posts/default?start-index=1&max-results=25" ))
    return itemlist
    
def novedades(item):
    logger.info("[peliculaseroticas.py] novedades")
    url = item.url
    data = None
    thumbnail = ""
    xmldata = urllib2.urlopen(url,data)
    
    xmldoc = minidom.parse(xmldata)
    xmldoc.normalize()
    #print xmldoc.toxml().encode('utf-8')
    xmldata.close()
    c = 0
    itemlist = []
    plot = ""
    for entry in xmldoc.getElementsByTagNameNS(ATOM_NS, u'entry'):
    #First title element in doc order within the entry is the title
        entrytitle = entry.getElementsByTagNameNS(ATOM_NS, u'title')[0]
        entrylink = entry.getElementsByTagNameNS(ATOM_NS, u'link')[2]
        entrythumbnail = entry.getElementsByTagNameNS(ATOM_NS, u'content')[0]
        etitletext = get_text_from_construct(entrytitle)
        elinktext = entrylink.getAttributeNS(EMPTY_NAMESPACE, u'href')
        ethumbnailtext = get_text_from_construct(entrythumbnail)
        regexp = re.compile(r'src="([^"]+)"')
        match = regexp.search(ethumbnailtext)
        if match is not None:
            thumbnail = match.group(1)
        regexp = re.compile(r'/><br />([^<]+)<')
        match = regexp.search(ethumbnailtext)
        if match is not None:
            plot = match.group(1)
        regexp = re.compile(r'</span><a href="([^"]+)"')
        match = regexp.search(ethumbnailtext)
        if match is not None:
            elinktext = match.group(1)		
        
        # Depuracion
        if (DEBUG):
            logger.info("scrapedtitle="+etitletext)
            logger.info("scrapedurl="+elinktext)
            logger.info("scrapedthumbnail="+thumbnail)
                
        #print etitletext, '(', elinktext, thumbnail,plot, ')'
        #xbmctools.addnewfolder( __channel__ , "detail" , category ,  etitletext,  elinktext, thumbnail, plot )
        itemlist.append( Item(channel=__channel__, action="detail" , title=etitletext , url=elinktext, thumbnail=thumbnail, plot=plot))
        c +=1
    
    if c >= 25:
        regexp = re.compile(r'start-index=([^\&]+)&')
        match = regexp.search(url)
        if match is not None:
            start_index = int(match.group(1)) + 25
        scrapedtitle = "Página siguiente"
        scrapedurl =  "http://www.blogger.com/feeds/6886871729120330561/posts/default?start-index="+str(start_index)+"&max-results=25"
        scrapedthumbnail = ""
        scrapedplot = ""
        #xbmctools.addnewfolder( __channel__ , "novedades" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )
        itemlist.append( Item(channel=__channel__, action="novedades", title=scrapedtitle , url=scrapedurl , folder=True) )
    
    return itemlist

def get_text_from_construct(element):
    '''
    Return the content of an Atom element declared with the
    atomTextConstruct pattern.  Handle both plain text and XHTML
    forms.  Return a UTF-8 encoded string.
    '''
    if element.getAttributeNS(EMPTY_NAMESPACE, u'type') == u'xhtml':
        #Grab the XML serialization of each child
        childtext = [ c.toxml('utf-8') for c in element.childNodes ]
        #And stitch it together
        content = ''.join(childtext).strip()
        return content
    else:
        return element.firstChild.data.encode('utf-8')

def detail(item):
    logger.info("[peliculaseroticas.py] detail")

    itemlist = []
    if "videobb" in item.url:
        itemlist.append( Item(channel=__channel__, action="play" , title=item.title , url=item.url, thumbnail=item.thumbnail, plot=item.plot, server="videobb", folder=False))
        return itemlist
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    
    # ------------------------------------------------------------------------------------
    # Busca los enlaces a los videos
    # ------------------------------------------------------------------------------------
    listavideos = servertools.findvideos(data)

    for video in listavideos:

        titulo = item.title.replace("%28"," ")
        titulo = titulo.replace("%29"," ")
        scrapedtitle = titulo.strip().replace("(Megavideo)","").replace("+"," ") +" - "+video[0]
        server = video[2]
        scrapedurl = video[1]
        #	xbmctools.addvideo( __channel__ , video[0], video[1] , category ,         #plot )
        #xbmctools.addnewvideo( __channel__ , "play" , category , server , titulo.strip().replace("(Megavideo)","").replace("+"," ") +" - "+video[0]  , video[1] ,thumbnail, plot )
        itemlist.append( Item(channel=__channel__, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=item.thumbnail, plot=item.plot, server=server, folder=False))
        # ------------------------------------------------------------------------------------

    # Extrae los enlaces a los vídeos (Directo)

     # Extrae los videos para el servidor mystream.to

    patronvideos = '(http://www.mystream.to/.*?)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    #logger.info(data)
    #logger.info("[peliculaseroticas.py] matches="+matches[0])  
    if len(matches)>0:
        data1 = scrapertools.cachePage(matches[0])
        patronvideos = 'flashvars" value="file=(.*?)"'
        videosdirecto = re.compile(patronvideos,re.DOTALL).findall(data1)
        #logger.info("[peliculaseroticas.py] videosdirecto="+videosdirecto[0])
        if len(videosdirecto)>0:
            scrapedtitle = item.title +" - Directo con mystream.to"
            scrapedurl = videosdirecto[0]
            #xbmctools.addnewvideo( __channel__ , "play" , category , "Directo" , title+" - Directo con mystream.to"  , videosdirecto[0] ,thumbnail, plot )
            itemlist.append( Item(channel=__channel__, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=item.thumbnail, plot=item.plot, server="Directo", folder=False))

    patronvideos = "<div class='post-body entry-content'>.*?</span><a href=\"(.*?)\" target="
    matches = re.compile(patronvideos,re.DOTALL).findall(data) 
    if len(matches)>0: 
        # extrae los videos para servidor movshare
        data1 = scrapertools.cachePage(matches[0])
        patronvideos ='param name="src" value="http://stream.movshare.net/(.*?).avi'   
        videosdirecto = re.compile(patronvideos,re.DOTALL).findall(data1)
        #logger.info("[peliculaseroticas.py] videosdirecto="+videosdirecto[0])
        if len(videosdirecto)>0:
            from servers import movshare
            mediaurl = "http://www.movshare.net/video/" + videosdirecto[0]
            logger.info("[peliculaseroticas.py] mediaurl = "+ mediaurl)
            
            scrapedtitle = item.title +" - Video en movshare" 
            # xbmctools.addnewvideo( __channel__ , "play" , category , "Directo" , title+" - Video en movshare"  , mediaurl ,thumbnail, plot )
            itemlist.append( Item(channel=__channel__, action="play" , title=scrapedtitle , url=mediurl, thumbnail=item.thumbnail, plot=item.plot, server="Movshare", folder=False))

    patronvideos = 'file=(http://www.wildscreen.tv.*?)\?'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        #xbmctools.addnewvideo( __channel__ , "play" , category , "Directo" , title+" - Video en wildscreen.tv"  , matches[0] ,thumbnail, plot )
        scrapedtitle = item.title +" - Video en wildscreen.tv"
        itemlist.append( Item(channel=__channel__, action="play" , title=scrapedtitle , url=matches[0], thumbnail=item.thumbnail, plot=item.plot, server="Directo", folder=False))


    # extrae los videos para servidor myspacecdn      

    #data = scrapertools.cachePage(url)
    patronvideos = 'flashvars.*?file=(.*?.flv).*?'
    videosdirecto = re.compile(patronvideos,re.DOTALL).findall(data)
    #logger.info("[peliculaseroticas.py] videosdirecto="+videosdirecto[0])
    if len(videosdirecto)>0:
        #xbmctools.addnewvideo( __channel__ , "play" , category , "Directo" , title+" - Video en myspacecdn"  , videosdirecto[0] ,thumbnail, plot )
        itemlist.append( Item(channel=__channel__, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=item.thumbnail, plot=item.plot, server=server, folder=False))
    # --------------------------------------------------------------------------------

    # extrae los videos para del servidor adnstream.com
      
    patronvideos = '<a href=\"http://www.adnstream.tv/video/(.*?)/.*?"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    #logger.info("[peliculaseroticas.py] matches="+matches[0])
    if len(matches)>0:

        logger.info("[peliculaseroticas.py] videocode = "+ matches[0])
        crapedtitle = item.title +" - Video en adnstream.tv"
        #xbmctools.addnewvideo( __channel__ , "play" , category , "Directo" , title+" - Video en adnstream.tv"  , matchvideo[0] ,thumbnail, plot )
        itemlist.append( Item(channel=__channel__, action="play" , title=scrapedtitle , url=matches[0], thumbnail=item.thumbnail, plot=item.plot, server="adnstream", folder=False))

    patronvideos = 'src="(http://vk[^\/]+\/video_ext.php[^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        print " encontro VK.COM :%s" %matches[0]
        scrapedtitle = item.title + " [VKServer]"
        videourl = matches[0]
        itemlist.append( Item(channel=__channel__, action="play" , title=scrapedtitle , url=videourl, thumbnail=item.thumbnail, plot=item.plot, server="vk", folder=False))
    
    patronvideos = 'http://static.xvideos.com.*?id_video=([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        videourl = matches[0]
        scrapedtitle = item.title + " [Xvideos]"
        itemlist.append( Item(channel=__channel__, action="play" , title=scrapedtitle , url=videourl, thumbnail=item.thumbnail, plot=item.plot, server="xvideos", folder=False))
    '''
    patronvideos = '<embed src="http://www.userporn.com/e/([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        from servers import userporn
        
        videourl = userporn.geturl(matches[0])
        scrapedtitle = item.title + " [Userporn]"
        itemlist.append( Item(channel=__channel__, action="play" , title=scrapedtitle , url=videourl, thumbnail=item.thumbnail, plot=item.plot, server="Directo", folder=False))
    '''
        
    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    mainlist_items = mainlist(Item())
    novedades_items = novedades(mainlist_items[0])

    bien = False
    for novedades_item in novedades_items:
        mirrors = detail( item=novedades_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien