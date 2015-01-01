# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para playedto
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def test_video_exists( page_url ):
    logger.info("[playedto.py] test_video_exists(page_url='%s')" % page_url)

    data = scrapertools.cache_page(page_url,timeout=1)

    if "Reason for deletion" in data:
        return False,"El archivo ha sido borrado de played.to."

    if "The file is being converted" in data:
        return False,"El fichero está en proceso"

    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[playedto.py] url="+page_url)

    # Lo pide una vez
    headers = [['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14']]

    data = scrapertools.cache_page( page_url , headers=headers,timeout=1 )

    #import time
    #time.sleep(10)

    # Lo pide una segunda vez, como si hubieras hecho click en el banner
    #op=download1&usr_login=&id=z3nnqbspjyne&fname=Coriolanus_DVDrip_Castellano_by_ARKONADA.avi&referer=&hash=nmnt74bh4dihf4zzkxfmw3ztykyfxb24&imhuman=Continue+to+Video
    op = scrapertools.get_match(data,'<input type="hidden" name="op" value="([^"]+)"')
    id = scrapertools.get_match(data,'<input type="hidden" name="id" value="([^"]+)"')
    fname = scrapertools.get_match(data,'<input type="hidden" name="fname" value="([^"]+)"')
    hashstring = scrapertools.get_match(data,'<input type="hidden" name="hash" value="([^"]*)"')
    imhuman = scrapertools.get_match(data,'<input type="submit" name="imhuman" value="([^"]+)"').replace(" ","+")

    post = "op="+op+"&usr_login=&id="+id+"&fname="+fname+"&referer=&hash="+hashstring+"&imhuman="+imhuman
    headers.append(["Referer",page_url])

    data = scrapertools.cache_page( page_url , post=post, headers=headers,timeout=1 )

    logger.info("data="+data)

    # Extrae la URL
    media_url = scrapertools.get_match( data , 'file: "([^"]+)"' )

    video_urls = []
    video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:]+" [playedto]",media_url])

    for video_url in video_urls:
        logger.info("[playedto.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    # Añade manualmente algunos erróneos para evitarlos
    encontrados = set()
    encontrados.add("http://played.to/embed-theme.html")
    encontrados.add("http://played.to/embed-jquery.html")
    encontrados.add("http://played.to/embed-s.html")
    encontrados.add("http://played.to/embed-images.html")
    encontrados.add("http://played.to/embed-faq.html")
    encontrados.add("http://played.to/embed-embed.html")
    encontrados.add("http://played.to/embed-ri.html")
    encontrados.add("http://played.to/embed-d.html")
    encontrados.add("http://played.to/embed-css.html")
    encontrados.add("http://played.to/embed-js.html")
    encontrados.add("http://played.to/embed-player.html")
    encontrados.add("http://played.to/embed-cgi.html")
    encontrados.add("http://played.to/embed-new.html")
    encontrados.add("http://played.to/embed-make.html")
    encontrados.add("http://played.to/embed-contact.html")
    encontrados.add("http://played.to/embed-privacy.html")
    encontrados.add("http://played.to/embed-dmca.html")
    encontrados.add("http://played.to/embed-tos.html")
    devuelve = []

    #http://played.to/z3nnqbspjyne
    patronvideos  = 'played.to/([a-z0-9A-Z]+)'
    logger.info("[playedto.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[playedto]"
        url = "http://played.to/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'playedto' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://played.to/embed-z3nnqbspjyne.html
    patronvideos  = 'played.to/embed-([a-z0-9A-Z]+)'
    logger.info("[playedto.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[playedto]"
        url = "http://played.to/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'playedto' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve

def test():

    video_urls = get_video_url("http://played.to/z3nnqbspjyne")

    return len(video_urls)>0
