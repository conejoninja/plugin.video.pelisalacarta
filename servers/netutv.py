# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para yaske-netutv, netutv y hqqtv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os
import base64

from core import scrapertools
from core import logger
from core import config

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[netutv.py] url="+page_url)

    headers = [['User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0']]

    #"/netu/tv/"
    if "www.yaske.net" in page_url:

        urlEncode = urllib.quote_plus(page_url)
        id_video = scrapertools.get_match( page_url , "embed_([A-Za-z0-9]+)")
        data = scrapertools.cache_page( page_url , headers=headers )

        headers.append(['Referer', page_url])
        try:
            #-------------------------------------
            page_url_the_new_video_id = scrapertools.get_match( data , 'script src="([^"]+)"></script>')
            data_with_new_video_id = scrapertools.cache_page( page_url_the_new_video_id , headers=headers )
            #-------------------------------------
            new_id_video = scrapertools.get_match( data_with_new_video_id , "var vid='([^']+)';")
            #-------------------------------------
            # Petición a hqq.tv con la nueva id de vídeo
            page_url_hqq = "http://hqq.tv/player/embed_player.php?vid="+new_id_video+"&autoplay=no"
            data_page_url_hqq = scrapertools.cache_page( page_url_hqq , headers=headers )
            b64_data = scrapertools.get_match(data_page_url_hqq, 'base64,([^"]+)"')
            #-------------------------------------
            b64_data_inverse = b64(b64_data)
            b64_data_2 = scrapertools.get_match(b64_data_inverse, "='([^']+)';")
            utf8_data_encode = b64(b64_data_2,True)
            utf8_encode = scrapertools.get_match(utf8_data_encode, "='([^']+)';")
            utf8_decode = utf8_encode.replace("%","\\").decode('unicode-escape')
            utf8 = utf8_decode
            #-------------------------------------
        except:
            #-------------------------------------
            b64_data = scrapertools.get_match( data , '<script language="javascript" type="text/javascript" src="data:text/javascript;charset=utf-8;base64,([^"]+)"></script>')
            #-------------------------------------
            b64_data_inverse = b64(b64_data)
            b64_data_2 = scrapertools.get_match(b64_data_inverse, "='([^']+)';")
            utf8_data_encode = b64(b64_data_2,True)
            utf8_encode = scrapertools.get_match(utf8_data_encode, "='([^']+)';")
            utf8_decode = utf8_encode.replace("%","\\").decode('unicode-escape')
            #-------------------------------------
            new_id_video = scrapertools.get_match( utf8_decode , 'value="([^"]+)"')
            #-------------------------------------
            # Petición a hqq.tv con la nueva id de vídeo
            page_url_hqq = "http://hqq.tv/player/embed_player.php?vid="+new_id_video+"&autoplay=no"
            data_page_url_hqq = scrapertools.cache_page( page_url_hqq , headers=headers )
            b64_data = scrapertools.get_match(data_page_url_hqq, 'base64,([^"]+)"')
            #-------------------------------------
            b64_data_inverse = b64(b64_data)
            b64_data_2 = scrapertools.get_match(b64_data_inverse, "='([^']+)';")
            utf8_data_encode = b64(b64_data_2,True)
            utf8_encode = scrapertools.get_match(utf8_data_encode, "='([^']+)';")
            utf8_decode = utf8_encode.replace("%","\\").decode('unicode-escape')
            utf8 = utf8_decode
            #-------------------------------------
        #######################################################################
        ### at
        match_at = '<input name="at" id="text" value="([^"]+)">'
        at = scrapertools.get_match(utf8, match_at)

        ### m3u8
        page_url_hqq_2 = "http://hqq.tv/sec/player/embed_player.php?vid="+new_id_video+"&at="+at+"&autoplayed=yes&referer=on&http_referer="+urlEncode+"&pass="

        data_with_url_video = scrapertools.cache_page(page_url_hqq_2, headers=headers )

        match_b_m3u8 = '</div>[^<]+<script>[^"]+"([^"]+)"'
        b_m3u8 = urllib.unquote( scrapertools.get_match(data_with_url_video, match_b_m3u8) )

        match_b_m3u8_2 = '"#([^"]+)"'
        b_m3u8_2 = scrapertools.get_match(b_m3u8, match_b_m3u8_2)

        ### tb_m3u8
        j = 0
        s2 = ""
        while j < len(b_m3u8_2):
            s2+= "\\u0"+b_m3u8_2[j:(j+3)]
            j+= 3
        s2_m3u8 = s2.decode('unicode-escape')
        url_m3u8 = s2_m3u8.encode('ASCII', 'ignore')

        media_url = url_m3u8

    else:
        urlEncode = urllib.quote_plus( page_url.replace("netu","hqq") )

        ### at
        id_video = page_url.split("=")[1]

        url_1 = "http://hqq.tv/player/embed_player.php?vid=?vid="+id_video+"&autoplay=no"

        data = scrapertools.cache_page( url_1 , headers=headers )

        match_b64_1 = 'base64,([^"]+)"'
        b64_1 = scrapertools.get_match(data, match_b64_1)

        utf8_1 = base64.decodestring(b64_1)

        match_b64_inv = "='([^']+)';"
        b64_inv = scrapertools.get_match(utf8_1, match_b64_inv)

        b64_2 = b64_inv[::-1]

        utf8_2 = base64.decodestring(b64_2).replace("%","\\").decode('unicode-escape')

        match_at = '<input name="at" id="text" value="([^"]+)">'
        at = scrapertools.get_match(utf8_2, match_at)

        ### m3u8
        url_2 = "http://hqq.tv/sec/player/embed_player.php?vid="+id_video+"&at="+at+"&autoplayed=yes&referer=on&http_referer="+urlEncode+"&pass="

        headers.append(['Referer', page_url])
        data = scrapertools.cache_page(url_2, headers=headers )

        match_b_m3u8 = '</div>[^<]+<script>[^"]+"([^"]+)"'
        b_m3u8 = urllib.unquote( scrapertools.get_match(data, match_b_m3u8) )

        if b_m3u8 == "undefined": b_m3u8 = urllib.unquote( data )

        match_b_m3u8_2 = '"#([^"]+)"'
        b_m3u8_2 = scrapertools.get_match(b_m3u8, match_b_m3u8_2)

        ### tb_m3u8
        j = 0
        s2 = ""
        while j < len(b_m3u8_2):
            s2+= "\\u0"+b_m3u8_2[j:(j+3)]
            j+= 3
        s2 = s2.decode('unicode-escape')

        media_url = s2.encode('ASCII', 'ignore')

    video_urls = []
    video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:]+" [netu.tv]",media_url])

    for video_url in video_urls:
        logger.info("[netutv.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    ## yaske es propietario de netu.tv y hqq.tv

    # -- yaske ----------------------------------------------------
    # http://www.yaske.net/archivos/netu/tv/embed_54b15d2d41641.html
    # http://www.yaske.net/archivos/netu/tv/embed_54b15d2d41641.html?1
    patronvideos  = '/netu/tv/embed_(.*?$)'
    logger.info("[netutv.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[netu.tv]"
        url = "http://www.yaske.net/archivos/netu/tv/embed_"+match
        #url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'netutv' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
    # -------------------------------------------------------------

    # -- hqqtv ----------------------------------------------------
    # http://hqq.tv/player/embed_player.php?vid=498OYGN19D65&autoplay=no
    patronvideos  = 'hqq.tv/player/embed_player.php\?vid\=([A-Z0-9]+)'
    logger.info("[netutv.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[netu.tv]"
        url = "http://netu.tv/watch_video.php?v="+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'netutv' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # http://hqq.tv/watch_video.php?v=498OYGN19D65
    patronvideos  = 'hqq.tv/watch_video.php\?v\=([A-Z0-9]+)'
    logger.info("[netutv.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[netu.tv]"
        url = "http://netu.tv/watch_video.php?v="+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'netutv' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
    # -------------------------------------------------------------

    # -- netutv ---------------------------------------------------
    # http://netu.tv/player/embed_player.php?vid=82U4BRSOB4UU&autoplay=no
    patronvideos  = 'netu.tv/player/embed_player.php\?vid\=([A-Z0-9]+)'
    logger.info("[netutv.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[netu.tv]"
        url = "http://netu.tv/watch_video.php?v="+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'netutv' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # http://netu.tv/watch_video.php?v=96WDAAA71A8K
    patronvideos  = 'netu.tv/watch_video.php\?v\=([A-Z0-9]+)'
    logger.info("[netutv.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[netu.tv]"
        url = "http://netu.tv/watch_video.php?v="+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'netutv' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
    # -------------------------------------------------------------

    return devuelve

def test():

    #http://www.peliculasid.net/player/netu.php?id=NA44292KD53O
    video_urls = get_video_url("http://netu.tv/watch_video.php?v=NA44292KD53O")

    return len(video_urls)>0

def b64(text, inverse=False):
    if inverse:
        text = text[::-1]

    return base64.decodestring(text)
