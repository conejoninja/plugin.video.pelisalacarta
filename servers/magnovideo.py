# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para magnovideo
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[magnovideo.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []
    
    headers = []
    headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:17.0) Gecko/20100101 Firefox/17.0"])
    
    id_video = scrapertools.get_match(page_url,"\?v\=([A-Z0-9]+)")
    data = scrapertools.cache_page("http://www.magnovideo.com/player_config.php?mdid="+id_video+"&sml=1&autoplay=true")
    logger.info("data="+data)
    
    # Extrae la URL
    image_url = scrapertools.get_match( data , '<tile_thumbs>(.*?)</tile_thumbs>');
    part_url = scrapertools.get_match( data , '<opart>(.*?)</opart>');
    burst = scrapertools.get_match( data , '<movie_burst>(.*?)</movie_burst>' )
    u = scrapertools.get_match( data , '<burst_speed>(.*?)</burst_speed>' )
    md_e_1 = scrapertools.get_match( data , '<ste>(.*?)</ste>' )
    md_e_2 = scrapertools.get_match( data , '<sto>(.*?)</sto>' )
    storage_path = scrapertools.get_match( data , '<storage_path>(.*?)</storage_path>' )
    original_storage_path = scrapertools.get_match( data , '<original_storage_path>(.*?)</original_storage_path>' )
    video_name = scrapertools.get_match( data , '<video_name>(.*?)</video_name>' );

    media_url = image_url.replace('tmpsmall/tiles.jpg',video_name)
    if part_url != '5':
        md_e = md_e_2
    else:
        md_e = md_e_1
        media_url = media_url.replace(original_storage_path,storage_path)
        media_url = media_url.replace('/part5','')

    media_url = media_url+'?burst='+burst+'k&u='+u+'k&'+md_e

    video_urls.append( [scrapertools.get_filename_from_url(media_url)[-4:]+" [magnovideo]" , media_url] )

    for video_url in video_urls:
        logger.info("[magnovideo.py] %s - %s" % (video_url[0],video_url[1]))


    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []
    
    #print "DATO a buscar" + data
    # http://www.magnovideo.com/?v=QRATZ9UN
    patronvideos  = '(magnovideo.com/\?v\=[A-Z0-9]+)'
    logger.info("[magnovideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[magnovideo]"
        url = "http://www."+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'magnovideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://www.magnovideo.com/v.php?dl=ZTL2VDPV
    patronvideos  = 'magnovideo.com/v.php\?dl\=([A-Z0-9]+)'
    logger.info("[magnovideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[magnovideo]"
        url = "http://www.magnovideo.com/?v="+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'magnovideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    
    return devuelve
