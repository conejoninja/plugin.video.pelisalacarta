# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para flashx
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
# Credits:

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def test_video_exists( page_url ):
    return False,"Conector no soportado por pelisalacarta"

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[flashx.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []

    # http://play.flashx.tv/player/embed.php?hash=4KB84GO238XX&width=600&height=370&autoplay=no
    data = scrapertools.cache_page(page_url)
    logger.info("data="+data)
    logger.info("        ")
    logger.info("----------------------------------------------------------------------")
    logger.info("        ")

    '''
    <form method="POST" action="playfx.php" />
      <input name="yes" type="hidden" value="m8fr27GmfHRrmr/CpqVpiouM79zY5plvaZaomdzXmpmb2rWmq6JXpZjJ4NTn2m5il8jb2NWiYpeZyKqo2aRimGzM2qPXp2pol5ewqq2jlliU2+zi5N6Sq3Df3eaa56SXpc/osKurX2NnmqanqaBiaGeM59/Y5pqfmKOppqylY2Vql6qk">
      <input name="sec" type="hidden" value="Z7G6q6i5gGRmntDL">
      <a href="" onclick="document.forms[0].submit();popup('http://free-stream.tv/','adsf','810','450','yes');return false;" class="auto-style3"><strong><font color="red">PLAY NOW (CLICK HERE)</font></strong></a></span><br />
    </form>
    '''
    bloque = scrapertools.get_match(data,'<form method="POST" action="playfx.php"(.*?)</form>')
    logger.info("bloque="+bloque)
    yes = scrapertools.get_match(data,'<input name="yes" type="hidden" value="([^"]+)">')
    sec = scrapertools.get_match(data,'<input name="sec" type="hidden" value="([^"]+)">')

    # POST http://play.flashx.tv/player/playfx.php
    # yes=m8fr27GmfHRrmr%2FCpqVpiouM79zY5plvaZaomdzXmpmb2rWmq6JXpZjJ4NTn2m5il8jb2NWiYpeZyKqo2aRimGzM2qPXp2pol5ewqq2jlliU2%2Bzi5N6Sq3Df3eaa56SXpc%2FosKurX2NnmqanqaBiaGeM59%2FY5pqfmKOppqylY2Vql6qk&sec=Z7G6q6i5gGRmntDL
    post = urllib.urlencode( {"yes":yes,"sec":sec})
    url = "http://play.flashx.tv/player/playfx.php"
    data = scrapertools.cache_page(url,post=post)
    logger.info("data="+data)
    logger.info("        ")
    logger.info("----------------------------------------------------------------------")
    logger.info("        ")

    '''
    <object id="nuevoplayer" width="'+ww+'" height="'+hh+'" data="http://embed.flashx.tv/nuevo/player/fxplay.swf?config=http://play.flashx.tv/nuevo/player/play.php?str=4MfrzrWaw6iwmr.1qpmwvtA=" type="application/x-shockwave-flash"
    '''
    url = scrapertools.get_match(data,'(http://play.flashx.tv/nuevo/player/play.php\?str=[^"]+)"')
    data = scrapertools.cache_page(url,post=post)
    logger.info("data="+data)
    logger.info("        ")
    logger.info("----------------------------------------------------------------------")
    logger.info("        ")

    #http://play.flashx.tv/nuevo/player/play.php?str=4MfrzrWaw6iwmr.1qpmwvtA=
    #<file>http://fx021.flashx.tv:8080/video/2012/12/16---xYUbI3bSDzihXs9IP6eNRw---1383258808---1355698331547fb.flv</file>

    media_url = scrapertools.get_match(data,"<file>([^<]+)</file>")
    video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:]+" [flashx]",media_url])

    for video_url in video_urls:
        logger.info("[flashx.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    #http://flashx.tv/video/4KB84GO238XX/themakingofalady720phdtvx264-bia
    #http://play.flashx.tv/player/embed.php?hash=NGHKGW2OA1Y9&width=620&height=400
    data = urllib.unquote(data)
    
    patronvideos  = 'play.flashx.tv/player/embed.php[^h]+hash=([A-Z0-9]+)'
    logger.info("[flashx.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[flashx]"
        url = "http://play.flashx.tv/player/embed.php?hash="+match+"&width=600&height=370&autoplay=no"
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'flashx' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    patronvideos  = 'flashx.tv/video/([A-Z0-9]+)/[a-z0-9\-]+'
    logger.info("[flashx.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[flashx]"
        url = "http://play.flashx.tv/player/embed.php?hash="+match+"&width=600&height=370&autoplay=no"
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'flashx' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve

def test():
    video_urls = get_video_url("http://play.flashx.tv/player/embed.php?hash=4KB84GO238XX&width=600&height=370&autoplay=no")

    return len(video_urls)>0