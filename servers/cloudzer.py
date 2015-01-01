# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para cloudzer
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def test_video_exists( page_url ):
    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[cloudzer.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []
    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    #http://cloudzer.net/file/u71da1tk
    patronvideos  = '(cloudzer.net/file/[a-z0-9]+)'
    logger.info("[cloudzer.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[cloudzer.py]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'cloudzer' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
    #http://clz.to/mjphp9hl
    patronvideos  = '(clz.to/[a-zA-Z0-9]+)'
    logger.info("[cloudzer.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[cloudzer.net]"
        url = match.replace("clz.to/","http://cloudzer.net/file/")
        if url!="http://cloudzer.net/file/file" and url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'cloudzer' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)       
            

    return devuelve
