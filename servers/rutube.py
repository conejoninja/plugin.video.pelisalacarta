# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para rutube
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def test_video_exists( page_url ):
    try:
        code = scrapertools.get_match(page_url,"http://rutube.ru/video/embed/(\d+)")
    except:
        return False,"Variante de URL de rutube no compatible"

    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[rutube.py] url="+page_url)
    video_urls = []

    code = scrapertools.get_match(page_url,"http://rutube.ru/video/embed/(\d+)")
    logger.info("code="+code)

    #http://rutube.ru/play/embed/6481197?skinColor=22547a&sTitle=false&sAuthor=false
    url = "http://rutube.ru/play/embed/"+code+"?skinColor=22547a&sTitle=false&sAuthor=false"
    data = scrapertools.cache_page( url )
    logger.info("data="+data)

    #"m3u8": "http://bl.rutube.ru/f12b3390f7fd497ea00e3e50a350b2c0.m3u8"
    mediaurl = scrapertools.get_match(data,'"m3u8"\s*\:\s*"([^"]+)"')
    logger.info("mediaurl="+mediaurl)

    video_urls.append(["m3u8 [rutube]",mediaurl])

    for video_url in video_urls:
        logger.info("[rutube.py] %s - %s" % (video_url[0],video_url[1]))
    
    return video_urls

# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # http://video.rutube.ru/91203fc46405f06c2cadb98c9052dd68
    patronvideos  = '(http://video.rutube.ru/[a-z0-9]+)'
    logger.info("[rutube.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[rutube]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'rutube' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # http://rutube.ru/video/embed/6302367?p=ATQKgmK0YweoP2JPwj07Ww
    patronvideos  = '(rutube.ru/video/embed/[a-z0-9]+)'
    logger.info("[rutube.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[rutube]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'rutube' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)


    return devuelve
