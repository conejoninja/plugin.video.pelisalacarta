# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para video4you
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
from core import jsunpack

def test_video_exists( page_url ):
    logger.info("[video4you.py] test_video_exists(page_url='%s')" % page_url)

    data = scrapertools.cache_page(page_url)
    
    if "The file is being converted" in data:
        return False,"El fichero está en proceso"

    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[video4you.py] url="+page_url)

    data = scrapertools.cache_page( page_url )
    unpacked = jsunpack.unpack(data)
    logger.info("unpacked="+unpacked)
    media_url = scrapertools.get_match(unpacked,'file\:"([^"]+)"')

    video_urls = []
    video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:]+" [video4you]",media_url])

    for video_url in video_urls:
        logger.info("[streamcloud.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    # Añade manualmente algunos erróneos para evitarlos
    encontrados = set()
    encontrados.add("http://video4you.me/embed-theme.html")
    encontrados.add("http://video4you.me/embed-jquery.html")
    encontrados.add("http://video4you.me/embed-s.html")
    encontrados.add("http://video4you.me/embed-images.html")
    encontrados.add("http://video4you.me/embed-faq.html")
    encontrados.add("http://video4you.me/embed-embed.html")
    encontrados.add("http://video4you.me/embed-ri.html")
    encontrados.add("http://video4you.me/embed-d.html")
    encontrados.add("http://video4you.me/embed-css.html")
    encontrados.add("http://video4you.me/embed-js.html")
    encontrados.add("http://video4you.me/embed-player.html")
    encontrados.add("http://video4you.me/embed-cgi.html")
    encontrados.add("http://video4you.me/embed-new.html")
    encontrados.add("http://video4you.me/embed-make.html")
    encontrados.add("http://video4you.me/embed-contact.html")
    encontrados.add("http://video4you.me/embed-privacy.html")
    encontrados.add("http://video4you.me/embed-dmca.html")
    encontrados.add("http://video4you.me/embed-tos.html")
    devuelve = []

    #http://video4you.me/embed-z3nnqbspjyne
    patronvideos  = 'video4you.me/embed-([a-z0-9A-Z]+)'
    logger.info("[video4you.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[video4you]"
        url = "http://video4you.me/embed-"+match+".html"
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'video4you' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://video4you.me/z3nnqbspjyne
    patronvideos  = 'video4you.me/([a-z0-9A-Z]+)'
    logger.info("[video4you.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[video4you]"
        url = "http://video4you.me/embed-"+match+".html"
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'video4you' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve

def test():

    video_urls = get_video_url("http://video4you.me/gi41jbazz8tj")

    return len(video_urls)>0