# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para dailymotion
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

DEFAULT_HEADERS = []
DEFAULT_HEADERS.append( [ "User-Agent" , "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25" ] )

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("pelisalacarta.dailymotion get_video_url(page_url='%s')" % page_url)
    video_urls = []

    '''
    <meta property="og:url" content="http://www.dailymotion.com/video/x25ewpy_akame10_shortfilms" />    
    http://www.dailymotion.com/embed/video/x25ewpy_akame10_shortfilms?api=postMessage&autoplay=1&id=container_player_main&info=0&origin=http%3A%2F%2Fwww.dailymotion.com
    '''

    data = scrapertools.cache_page(page_url,headers=DEFAULT_HEADERS)
    logger.info("pelisalacarta.dailymotion data="+data)

    unique_url = scrapertools.find_single_match(data,'<meta property="og.url" content="([^"]+)"')
    logger.info("pelisalacarta.dailymotion unique_url="+unique_url)

    unique_url = unique_url.replace("/video/","/embed/video/")
    logger.info("pelisalacarta.dailymotion unique_url="+unique_url)

    url = unique_url+"?api=postMessage&autoplay=1&id=container_player_main&info=0&origin=http%3A%2F%2Fwww.dailymotion.com"
    DEFAULT_HEADERS.append( ["Referer","page_url"] )
    data = scrapertools.cache_page(url,headers=DEFAULT_HEADERS)
    logger.info("pelisalacarta.dailymotion data="+data)

    patron = '"stream_([a-z_0-9]+)_url"\:"([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for stream_name,stream_url in matches:
        video_urls.append( [ stream_name+" [dailymotion]", stream_url.replace("\\/","/") ] )

    for video_url in video_urls:
        logger.info("pelisalacarta.dailymotion %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://www.dailymotion.com/embed/video/xrva9o
    # http://www.dailymotion.com/swf/video/xocczx
    patronvideos  = 'dailymotion.com/(?:embed|swf)/video/([a-z0-9]+)'
    logger.info("pelisalacarta.dailymotion find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[dailymotion]"
        url = "http://www.dailymotion.com/video/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'dailymotion' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # http://www.dailymotion.com/video/xrva9o
    patronvideos  = 'dailymotion.com/video/([a-z0-9]+)'
    logger.info("pelisalacarta.dailymotion find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[dailymotion]"
        url = "http://www.dailymotion.com/video/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'dailymotion' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve

def test():
    video_urls = get_video_url("http://www.dailymotion.com/video/xrva9o")
    if len(video_urls)==0:
        return false

    # FLV (No soportado)
    #video_urls = get_video_url("http://www.dailymotion.com/video/xnu7n")
    #if len(video_urls)==0:
    #    return false;

    return True