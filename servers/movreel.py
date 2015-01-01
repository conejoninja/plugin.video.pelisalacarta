# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para movreel
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
from core import jsunpack

def test_video_exists( page_url ):
    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[movreel.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []

    data = scrapertools.cache_page(page_url)

    op = scrapertools.get_match(data,'<input type="hidden" name="op" value="([^"]+)">')
    file_code = scrapertools.get_match(data,'<input type="hidden" name="file_code" value="([^"]+)">')
    w = scrapertools.get_match(data,'<input type="hidden" name="w" value="([^"]+)">')
    h = scrapertools.get_match(data,'<input type="hidden" name="h" value="([^"]+)">')
    method_free = scrapertools.get_match(data,'<input type="submit" name="method_free" value="([^"]+)">')

    #op=video_embed&file_code=yrwo5dotp1xy&w=600&h=400&method_free=Close+Ad+and+Watch+as+Free+User
    post = urllib.urlencode( {"op":op,"file_code":file_code,"w":w,"h":h,"method_free":method_free} )

    data = scrapertools.cache_page(page_url,post=post)
    data = jsunpack.unpack(data)
    logger.info("data="+data)

    media_url = scrapertools.get_match(data,'file\:"([^"]+)"')
    video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:]+" [movreel]",media_url])

    for video_url in video_urls:
        logger.info("[movreel.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    #http://movreel.com/embed/l8ondvel8ynb
    data = urllib.unquote(data)
    patronvideos  = 'movreel.com/embed/([a-z0-9]+)'
    logger.info("[movreel.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[movreel]"
        url = "http://movreel.com/embed/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'movreel' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http%3A%2F%2Fwww.movreel.com%2Fuau47ktbg4dx
    data = urllib.unquote(data)
    patronvideos  = 'movreel.com/([a-z0-9]+)'
    logger.info("[movreel.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[movreel]"
        url = "http://movreel.com/embed/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'movreel' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
