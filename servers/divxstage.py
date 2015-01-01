# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para videos externos de divxstage
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
# Credits:
# Unwise and main algorithm taken from Eldorado url resolver
# https://github.com/Eldorados/script.module.urlresolver/blob/master/lib/urlresolver/plugins/divxstage.py

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
from core import unwise

def test_video_exists( page_url ):
    logger.info("[divxstage.py] test_video_exists(page_url='%s')" % page_url)
    
    data = scrapertools.cache_page( url = page_url )
    if "<h3>This file no longer exists" in data:
        return False,"El archivo no existe<br/>en divxstage o ha sido borrado."
    else:
        return True,""

    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[divxstage.py] get_video_url(page_url='%s')" % page_url)

    video_id = scrapertools.get_match(page_url,"http://www.divxstage.net/video/([a-z0-9]+)")
    data = scrapertools.cache_page(page_url)

    data = scrapertools.cache_page(page_url)

    try:
        location = scrapertools.get_match(data,'<param name="src" value="(.+?)"')
    except:
        data = unwise.unwise_process(data)
        filekey = unwise.resolve_var(data, "flashvars.filekey")
        
        page_url = 'http://www.divxstage.eu/api/player.api.php?user=undefined&key='+filekey+'&pass=undefined&codes=1&file='+video_id
        data = scrapertools.cache_page(page_url)
        location = scrapertools.get_match(data,'url=(.+?)&')

    video_urls = []
    video_urls.append( [ scrapertools.get_filename_from_url(location)[-4:]+" [divxstage]" , location ] )

    for video_url in video_urls:
        logger.info("[divxstage.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # divxstage http://www.divxstage.net/video/of7ww1tdv62gf"
    patronvideos  = 'http://www.divxstage.[\w]+/video/([\w]+)'
    logger.info("[divxstage.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[Divxstage]"
        url = "http://www.divxstage.net/video/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'divxstage' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
            
    return devuelve

def test():
    video_urls = get_video_url("http://www.divxstage.net/video/of7ww1tdv62gf")

    return len(video_urls)>0