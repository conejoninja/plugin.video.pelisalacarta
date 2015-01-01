# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para mail.ru
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
from core import jsontools

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[mailru.py] get_video_url(page_url='%s')" % (page_url))

    video_urls = []

    # Lee el player
    data = scrapertools.cache_page(page_url)
    logger.info("data="+data)

    # Lee los metadatos
    json_url = scrapertools.get_match(data,'"metadataUrl"."([^"]+)"')
    logger.info("json_url="+json_url)

    json_data = scrapertools.cache_page(json_url)
    logger.info("json_data="+json_data)

    json_object = jsontools.load_json(json_data)
    logger.info("json_object="+repr(json_object))

    # Descarga el poster para conseguir la cookie
    poster_url = json_object["meta"]["poster"]
    logger.info("poster_url="+poster_url)

    poster_location = scrapertools.get_header_from_response(poster_url,header_to_get="location")
    logger.info("poster_location="+poster_location)

    #http://cdn29.my.mail.ru/sc04/52395649.jpg?sign=570be2ff6b48fc78868a11e23a5fbc90533391da&slave[]=s%3Ahttp%3A%2F%2F127.0.0.1%3A5010%2F52395649-sc04.jpg&p=f&video_key=c039fe28e1d0747b05297d9329c6a6496442e824&expire_at=1419886800&touch=1419721905
    video_key = scrapertools.get_match(poster_location,'video_key=([^\&]+)\&')
    logger.info("video_key="+video_key)

    for video in json_object["videos"]:
        video_quality = video["key"]
        media_url = video["url"]+"|Cookie=video_key="+video_key
        video_urls.append( [ video_quality + " " + scrapertools.get_filename_from_url(media_url)[-4:] + " [mail.ru]",media_url ] )

    for video_url in video_urls:
        logger.info("[mail.ru] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    logger.info("[mailru.py] find_videos") #(data='%s')" % (data))
    encontrados = set()
    devuelve = []
    
    # http://videoapi.my.mail.ru/videos/embed/mail/bartos1100/_myvideo/1136.html
    patronvideos  = 'videoapi.my.mail.ru/videos/embed/mail/([a-zA-Z0-9]+)/_myvideo/(\d+).html'
    logger.info("[mailru.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[mail.ru]"
        url = "http://videoapi.my.mail.ru/videos/embed/mail/"+match[0]+"/_myvideo/"+match[1]+".html"
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'mailru' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    '''
    titulo = "[mail.ru]"
    if "http://api.video.mail.ru/videos/embed/" in data:
        #http://api.video.mail.ru/videos/embed/gmail.com/un.usuario/2/2816.html
        url = scrapertools.find_single_match(data,"(http.//api.video.mail.ru/videos/embed/.*?.html)")
        url = url.replace("embed/","").replace(".html",".json")
    else:
        #http://videoapi.my.mail.ru/videos/embed/mail/bartos1100/_myvideo/1136.html
        id_page_url = scrapertools.get_match(data,'/_myvideo/(\d+).html')
        author_name = scrapertools.find_single_match(data,'/video/mail([^/]+)/')
        if author_name=="":
            author_name = scrapertools.find_single_match(data,'/videos/embed/mail/([^/]+)/')

        #http://videoapi.my.mail.ru/videos/mail/bartos1100/_myvideo/1136.json
        url = "http://videoapi.my.mail.ru/videos/mail/%s/_myvideo/%s.json" % (author_name,id_page_url)

    if url not in encontrados:
        logger.info("  url=%s" % (url))
        devuelve.append( [ titulo , url , 'mailru' ] )
        encontrados.add(url)
    else:
        logger.info("  url duplicada=%s" % (url))
    '''

    return devuelve
