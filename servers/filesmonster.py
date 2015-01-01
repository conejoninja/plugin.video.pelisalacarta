# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para uploaz
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[filesmonster.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []
    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://uploaz.com/file/
    patronvideos  = '"filesmonster.com/download(.*?)"'
    logger.info("[filemonster.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[filesmonster]"
        url = "http://filesmonster.com/download"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'filemonster' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
