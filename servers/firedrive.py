# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para firedrive
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def test_video_exists( page_url ):
    logger.info("[firedrive.py] test_video_exists(page_url='%s')" % page_url)

    data = scrapertools.cache_page(page_url)

    if '<div class="sad_face_image">' in data and '404:' in data:
        return False,"El video ha sido borrado de Firedrive"

    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[firedrive.py] url="+page_url)
    video_urls = []
    headers = []
    headers.append( [ "User-Agent"     , "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17"] )
    headers.append( [ "Accept"         , "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" ])
    headers.append( [ "Accept-Charset" , "ISO-8859-1,utf-8;q=0.7,*;q=0.3" ])
    headers.append( [ "Accept-Encoding", "gzip,deflate,sdch" ])
    headers.append( [ "Accept-Language", "es-ES,es;q=0.8" ])
    headers.append( [ "Cache-Control"  , "max-age=0" ])
    headers.append( [ "Connection"     , "keep-alive" ])
    headers.append( [ "Origin"         , "http://www.firedrive.com" ])
 
    # Primer acceso
    data = scrapertools.cache_page(page_url,headers=headers)
    #logger.info("data="+data)

    # Simula el "continue to video"
    confirm = scrapertools.find_single_match(data,'<input type="hidden" name="confirm" value="([^"]+)"')
    post = urllib.urlencode({'confirm':confirm})
    logger.info("post="+post)
    headers.append( ["Referer",page_url] )
    headers.append( ["Content-Type","application/x-www-form-urlencoded"])
    data = scrapertools.cache_page( page_url , post=post, headers=headers )
    logger.info("data="+data)
    
    # URL del descriptor
    url = scrapertools.find_single_match(data,"file\: loadURL\('([^']+)'")
    logger.info("url="+url)

    # URL del vídeo
    media_url = scrapertools.get_header_from_response(url,header_to_get="location")
    video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:] + " [firedrive]",media_url ] )    

    for video_url in video_urls:
        logger.info("[firedrive.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # http://www.peliculasaudiolatino.com/show/firedrive.php?url=CEE0B3A7DDFED758
    patronvideos  = '(?:firedrive|putlocker).php\?url=([A-Z0-9]+)'
    logger.info("[firedrive.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[firedrive]"
        url = "http://www.firedrive.com/embed/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'firedrive' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
    # http://www.firedrive.com/embed/CEE0B3A7DDFED758 | http://www.firedrive.com/file/CEE0B3A7DDFED758
    patronvideos  = '(?:firedrive|putlocker).com/(?:file|embed)/([A-Z0-9]+)'
    logger.info("[firedrive.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[firedrive]"
        url = "http://www.firedrive.com/embed/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'firedrive' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #//www.cinezer.com/firedrive/CD6003D971725774
    patronvideos  = '/(?:firedrive|putlocker)/([A-Z0-9]+)'
    logger.info("[firedrive.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[firedrive]"
        url = "http://www.firedrive.com/embed/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'firedrive' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://www.firedrive.ch/file/0e6f1eeb473e0d87b390a71cd50c24a2/
    patronvideos  = '((?:firedrive|putlocker).ch/file/[a-z0-9]+)'
    logger.info("[firedrive.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[firedrive]"
        url = "http://www."+match+"/"
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'firedrive' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://www.player3k.info/firedrive/?id=92FA671A11CA7A05
    patronvideos  = '/(?:firedrive|putlocker)/\?id\=([A-Z0-9]+)'
    logger.info("[firedrive.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[firedrive]"
        url = "http://www.firedrive.com/embed/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'firedrive' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
    
    #http://www.yaske.net/archivos/firedrive/play.php?v=D68E78CBA144AE59
    patronvideos  = '(?:firedrive|putlocker)/play.php\?v\=([A-Z0-9]+)'
    logger.info("[firedrive.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[firedrive]"
        url = "http://www.firedrive.com/embed/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'firedrive' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://www.cinetux.org/video/firedrive.php?id=31A2C1B48C5F8969
    patronvideos  = '(?:firedrive|putlocker).php\?id\=([A-Z0-9]+)'
    logger.info("[firedrive.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[firedrive]"
        url = "http://www.firedrive.com/embed/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'firedrive' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)    
    
    return devuelve

def test():

    video_urls = get_video_url("http://www.firedrive.com/embed/C31F4FD09113E884")

    return len(video_urls)>0