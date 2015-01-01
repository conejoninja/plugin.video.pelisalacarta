# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para vidspot
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os
import re

from core import scrapertools
from core import logger
from core import config

def test_video_exists( page_url ):
    logger.info("[vidspot.py] test_video_exists(page_url='%s')" % page_url)

    # No existe / borrado: http://vidspot.net/8jcgbrzhujri
    data = scrapertools.cache_page(page_url)
    #logger.info("data="+data)
    if "<b>File Not Found</b>" in data or "<b>Archivo no encontrado</b>" in data or '<b class="err">Deleted' in data or '<b class="err">Removed' in data or '<font class="err">No such' in data:
        return False,"No existe o ha sido borrado de vidspot"
    else:
        # Existe: http://vidspot.net/6ltw8v1zaa7o
        patron  = '<META NAME="description" CONTENT="(Archivo para descargar[^"]+)">'
        matches = re.compile(patron,re.DOTALL).findall(data)
        
        if len(matches)>0:
            return True,""
    
    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[vidspot.py] url="+page_url)

    # Normaliza la URL
    videoid = scrapertools.get_match(page_url,"http://vidspot.net/([a-z0-9A-Z]+)")
    page_url = "http://vidspot.net/embed-"+videoid+"-728x400.html"
    data = scrapertools.cache_page(page_url)

    # Extrae la URL
    match = re.compile('"file" : "(.+?)",').findall(data)
    media_url = ""
    if len(match) > 0:
        for tempurl in match:
            if not tempurl.endswith(".png") and not tempurl.endswith(".srt"):
                media_url = tempurl

        if media_url == "":
            media_url = match[0]

    video_urls = []

    if media_url!="":
        media_url+= "&direct=false"
        video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:]+" [vidspot]",media_url])

    for video_url in video_urls:
        logger.info("[vidspot.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):

    # Añade manualmente algunos erróneos para evitarlos
    encontrados = set()
    encontrados.add("http://vidspot.net/embed-theme.html")
    encontrados.add("http://vidspot.net/embed-jquery.html")
    encontrados.add("http://vidspot.net/embed-s.html")
    encontrados.add("http://vidspot.net/embed-images.html")
    encontrados.add("http://vidspot.net/embed-faq.html")
    encontrados.add("http://vidspot.net/embed-embed.html")
    encontrados.add("http://vidspot.net/embed-ri.html")
    encontrados.add("http://vidspot.net/embed-d.html")
    encontrados.add("http://vidspot.net/embed-css.html")
    encontrados.add("http://vidspot.net/embed-js.html")
    encontrados.add("http://vidspot.net/embed-player.html")
    encontrados.add("http://vidspot.net/embed-cgi.html")
    encontrados.add("http://vidspot.net/embed-i.html")
    encontrados.add("http://vidspot.net/images")
    encontrados.add("http://vidspot.net/theme")
    encontrados.add("http://vidspot.net/xupload")
    encontrados.add("http://vidspot.net/s")
    encontrados.add("http://vidspot.net/js")
    encontrados.add("http://vidspot.net/jquery")
    encontrados.add("http://vidspot.net/login")
    encontrados.add("http://vidspot.net/make")
    encontrados.add("http://vidspot.net/i")
    encontrados.add("http://vidspot.net/faq")
    encontrados.add("http://vidspot.net/tos")
    encontrados.add("http://vidspot.net/premium")
    encontrados.add("http://vidspot.net/checkfiles")
    encontrados.add("http://vidspot.net/privacy")
    encontrados.add("http://vidspot.net/refund")
    encontrados.add("http://vidspot.net/links")
    encontrados.add("http://vidspot.net/contact")

    devuelve = []

    # http://vidspot.net/3sw6tewl21sn
    patronvideos  = 'vidspot.net/([a-z0-9]+)'
    logger.info("[vidspot.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        for match in matches:
            titulo = "[vidspot]"
            url = "http://vidspot.net/"+match
            if url not in encontrados and "embed" not in match:
                logger.info("  url="+url)
                devuelve.append( [ titulo , url , 'vidspot' ] )
                encontrados.add(url)
            else:
                logger.info("  url duplicada="+url)

    # http://vidspot.net/embed-3sw6tewl21sn.html
    patronvideos  = 'vidspot.net/embed-([a-z0-9]+).html'
    logger.info("[vidspot.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        for match in matches:
            titulo = "[vidspot]"
            url = "http://vidspot.net/"+match
            if url not in encontrados and "-728x400" not in match:
                logger.info("  url="+url)
                devuelve.append( [ titulo , url , 'vidspot' ] )
                encontrados.add(url)
            else:
                logger.info("  url duplicada="+url)

    # http://vidspot.net/embed-3sw6tewl21sn-728x400.html
    patronvideos  = 'vidspot.net/embed-([a-z0-9]+)-728x400.html'
    logger.info("[vidspot.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        for match in matches:
            titulo = "[vidspot]"
            url = "http://vidspot.net/"+match
            if url not in encontrados:
                logger.info("  url="+url)
                devuelve.append( [ titulo , url , 'vidspot' ] )
                encontrados.add(url)
            else:
                logger.info("  url duplicada="+url)

    # http://www.cinetux.org/video/vidspot.php?id=3sw6tewl21sn
    patronvideos  = 'vidspot.php\?id\=([a-z0-9]+)'
    logger.info("[vidspot.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        for match in matches:
            titulo = "[vidspot]"
            url = "http://vidspot.net/"+match
            if url not in encontrados:
                logger.info("  url="+url)
                devuelve.append( [ titulo , url , 'vidspot' ] )
                encontrados.add(url)
            else:
                logger.info("  url duplicada="+url)

    return devuelve

def test():

    video_urls = get_video_url("http://vidspot.net/uhah7dmq2ydp")

    return len(video_urls)>0