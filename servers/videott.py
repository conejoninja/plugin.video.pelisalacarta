# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para videott
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os
import random

from core import scrapertools
from core import logger
from core import config

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[videott.py] url="+page_url)

    video_urls = []

    # URL del vídeo
    videoid = scrapertools.find_single_match(page_url,"video.tt/e/([A-Za-z0-9]+)")
    timestamp=str(random.randint(1000000000,9999999999))
    hexastring = scrapertools.get_sha1(page_url) + scrapertools.get_sha1(page_url) + scrapertools.get_sha1(page_url) + scrapertools.get_sha1(page_url)
    hexastring = hexastring[:96]

    media_url = "http://gs.video.tt/s?v="+videoid+"&r=1&t="+timestamp+"&u=&c="+hexastring+"&start=0"
    video_urls.append( [ "mp4 [videott]",media_url ] )    

    for video_url in video_urls:
        logger.info("[videott.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # http://video.tt/e/vHDKmK32U
    patronvideos  = 'video.tt/e/([A-Za-z0-9]+)'
    logger.info("[videott.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[videott]"
        url = "http://video.tt/e/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'videott' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
    return devuelve

def test():

    video_urls = get_video_url("http://video.tt/e/vHDKmK32U")

    return len(video_urls)>0