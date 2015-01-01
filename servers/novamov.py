
# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para novamov
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
# Credits:
# Unwise and main algorithm taken from Eldorado url resolver
# https://github.com/Eldorados/script.module.urlresolver/blob/master/lib/urlresolver/plugins/novamov.py

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
from core import unwise

def test_video_exists( page_url ):
    logger.info("[novamov.py] test_video_exists(page_url='%s')" % page_url)

    data = scrapertools.cache_page(page_url)
    
    if "This file no longer exists on our servers" in data:
        return False,"El fichero ha sido borrado de novamov"

    elif "is being converted" in data:
        return False,"El fichero está en proceso todavía"

    return True,""

def get_video_url( page_url , premium = False , user="" , password="" , video_password="" ):
    logger.info("[novamov.py] get_video_url(page_url='%s')" % page_url)

    media_id = scrapertools.get_match(page_url,"http://www.novamov.com/video/([a-z0-9]+)")

    html = scrapertools.cache_page(page_url)
    html = unwise.unwise_process(html)
    filekey = unwise.resolve_var(html, "flashvars.filekey")

    #get stream url from api
    api = 'http://www.novamov.com/api/player.api.php?key=%s&file=%s' % (filekey, media_id)
    html = scrapertools.cache_page(api)
    r = re.search('url=(.+?)&title', html)
    if r:
        stream_url = urllib.unquote(r.group(1))

    video_urls = []
    video_urls.append( [".flv [novamov]",stream_url])
    
    for video_url in video_urls:
        logger.info("[novamov.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

def find_videos(data):
    encontrados = set()
    devuelve = []

    patronvideos = 'novamov.com/video/([a-z0-9]{13})'
    logger.info("[novamov.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos).findall(data)

    for match in matches:
        titulo = "[novamov]"
        url = "http://www.novamov.com/video/"+match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'novamov' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # http://embed.novamov.com/embed.php?width=568&height=340&v=zadsdfoc0pirx&px=1
    # http://embed.novamov.com/embed.php?width=620&amp;height=348&amp;v=4f21e91a1f2f7&amp;px=1&amp;px=1
    patronvideos = 'http://embed.novamov.com/embed.php.*?v=([a-z0-9]{13})'
    logger.info("[novamov.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos).findall(data)

    for match in matches:
        titulo = "[novamov]"
        url = "http://www.novamov.com/video/"+match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'novamov' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve

def test():
    video_urls = get_video_url("http://www.novamov.com/video/nouxrlszuym2h")

    return len(video_urls)>0