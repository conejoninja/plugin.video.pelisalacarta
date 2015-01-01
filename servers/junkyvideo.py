# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para junkyvideo
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config



USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:18.0) Gecko/20100101 Firefox/18.0"

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[junkyvideo.py] url="+page_url)
    video_urls=[]
    import time
    opener = urllib2.build_opener()
    page = opener.open(page_url)
    page = page.read()
    hash1 = scrapertools.find_single_match(page,'name="hash" value="([^<]+)"')
    idd = scrapertools.find_single_match(page,'name="id" value="([^<]+)"')
    time.sleep(6)
    params = {'op': 'download1', 'usr_login': '', 'id': idd, 'fname': '', 'referer': '', 'hash': hash1}
    data = urllib.urlencode(params)
    res = urllib2.Request(page_url, data)
    response =opener.open(res) 
    page = response.read()
    page = page.split('file: "')
    link = page[1].split('"')

    video_urls.append(["[junkyvideo]" ,link[0]])
    
    return video_urls

# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []
            
    
    #http://www.junkyvideo.com/r5z9g1kwg9jt
    patronvideos  = 'junkyvideo.com/([A-Za-z0-9]+).htm'
    logger.info("[junkyvideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[junkyvideo]"
        url = "http://www.junkyvideo.com/"+match+".htm"
        d = scrapertools.cache_page(url)
        ma = scrapertools.find_single_match(d,'<h2>Watch ([^<]+)</h2>')
        ma=titulo+" "+ma
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ ma , url , 'junkyvideo' ] )

            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)


    return devuelve

def test():

    video_urls = get_video_url("http://www.junkyvideo.com/embed/sy6wen17")

    return len(video_urls)>0
