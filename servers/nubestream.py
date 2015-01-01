# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para nubestream
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def test_video_exists( page_url ):
    logger.info("[nubestream.py] test_video_exists(page_url='%s')" % page_url)

    # No existe / borrado: http://allmyvideos.net/8jcgbrzhujri
    data = scrapertools.cache_page(page_url)
    #logger.info("data="+data)
    if "{name}" in data:
        return False,"No existe o ha sido borrado de allmyvideos"
    
    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[nubestream.py] get_video_url(page_url='%s')" % page_url)

    # Lo pide una vez
    headers = [['User-Agent','Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10']]
    data = scrapertools.cache_page( page_url , headers=headers )
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

    video_urls = []
    video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:]+" [nubestream]",media_url])

    for video_url in video_urls:
        logger.info("[nubestream.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://www.nubestream.com/?v=TYPOREI3
    patronvideos  = '(http://www.nubestream.com/\?v=[A-Z0-9]+)'
    logger.info("[nubestream.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[nubestream]"
        url = match.replace('?v=','player_config.php?mdid=')
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'nubestream' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve

def test():

    video_urls = get_video_url("http://www.nubestream.com/?v=2LP8VX18")

    return len(video_urls)>0