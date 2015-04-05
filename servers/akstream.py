# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector for akstream.net
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# by be4t5
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
from lib import mechanize

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[akstream.py] url="+page_url)
    video_urls = []
    headers = []
    headers.append( [ "User-Agent"     , "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17"] )
    headers.append(["referrer", "http://akstream.net/"])
    
    br = mechanize.Browser()
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.set_handle_robots(False)

    url="../viewprocess.php"
    r = br.open(page_url)
    req = br.click_link(url=url)
    data = br.open(req)
    data= data.read()
 

    
    # URL 
    url = scrapertools.find_single_match(data,'<source src="([^"]+)" type="video/mp4"')
    logger.info("url="+url)

    # URL del vídeo
    video_urls.append( [ ".mp4" + " [Akstream]",url ] )

    for video_url in video_urls:
       logger.info("[akstream.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

	#http://akstream.net/v/iwbe6genso37
    patronvideos  = 'http://akstream.net/v/([a-z0-9]+)'
    logger.info("[akstream.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[Akstream]"
        url = "http://akstream.net/v/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'akstream' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)        
					
	
	#http://cineblog01.pw/HR/go.php?id=6475
    temp  = text.split('<strong>Streaming')
    if (len(temp)>1):
        tem = temp[1].split('Download')
        patronvideos  = '(?:HR)/go.php\?id\=([A-Z0-9]+)'
        matches = re.compile(patronvideos,re.DOTALL).findall(tem[0])
    else:
        matches=[]
    
    br = mechanize.Browser()
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.set_handle_robots(False)
    page = scrapertools.find_single_match(text,'rel="canonical" href="([^"]+)"')

    for match in matches:
        titulo = "[Akstream]"
        url = "http://cineblog01.pw/HR/go.php?id="+match
        r = br.open(page)
        req = br.click_link(url=url)
        data = br.open(req)
        data= data.read()
        id = scrapertools.find_single_match(data,'http://akstream.net/v/([^"]+)"?')
        url = "http://akstream.net/v/"+id
        if url not in encontrados and id != "":
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'akstream' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    	#http://vcrypt.net/sak/0a8hqibleus5
        #Filmpertutti.eu
    patronvideos  = 'http://vcrypt.net/sak/([^"]+)'
    matches = re.compile(patronvideos,re.DOTALL).findall(text)
    page = scrapertools.find_single_match(text,'rel="canonical" href="([^"]+)"')

    for match in matches:
        titulo = "[Akstream]"
        url = "http://vcrypt.net/sak/"+match
        r = br.open(url)
        data= r.read()
        id = scrapertools.find_single_match(data,'akstream.net/v/([^"]+)"')
        url = "http://akstream.net/v/"+id
        if url not in encontrados and id != "":
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'akstream' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    

    return devuelve

def test():
    video_urls = get_video_url("http://akstream.net/v/8513acv2alss")

    return len(video_urls)>0
