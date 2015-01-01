# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para filenium
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re,time
import os
import base64
#import json

from core import scrapertools
from core import logger
from core import config
from urllib import urlencode

TIMEOUT=50

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("servers.filenium get_video_url")
    location=""
    logger.info("servers.filenium page_url="+page_url)
    page_url = correct_url(page_url)
    logger.info("servers.filenium page_url="+page_url)

    if premium:
        logger.info("servers.filenium ----------------------------------------------------------------------------------------")
        url = "http://filenium.com/welcome"
        post = "username=%s&password=%s" % (user,password)
        logger.info("servers.filenium post="+post)
        data = scrapertools.cache_page(url, post=post, timeout=TIMEOUT)
        logger.info("servers.filenium ----------------------------------------------------------------------------------------")

        logger.info("servers.filenium ----------------------------------------------------------------------------------------")
        link = urlencode({'filez':page_url})
        location = scrapertools.cache_page("http://filenium.com/?filenium&" + link, timeout=TIMEOUT)
        logger.info("servers.filenium ----------------------------------------------------------------------------------------")

        logger.info("servers.filenium ----------------------------------------------------------------------------------------")
        user = user.replace("@","%40")        
        location = location.replace("http://","http://"+user+":"+password+"@")
        logger.info("location="+location)

        # Averigua la redirección, para que funcione en Plex y WiiMC
        try:
            location2 = scrapertools.get_header_from_response(location,header_to_get="Location")
            logger.info("location2="+location2)
        except:
            location2=""

        logger.info("servers.filenium ----------------------------------------------------------------------------------------")

        if location2!="":
            location=location2

    return location

def get_file_extension(location):
    logger.info("servers.filenium get_file_extension("+location+")")

    try:
        content_disposition_header = scrapertools.get_header_from_response(location,header_to_get="Content-Disposition")
        logger.info("content_disposition="+content_disposition_header)
        partes=content_disposition_header.split("=")
        if len(partes)<=1:
            extension=""
        else:
            fichero = partes[1]
            fichero = fichero.replace("\\","")
            fichero = fichero.replace("'","")
            fichero = fichero.replace('"',"")
            extension = fichero[-4:]
    except:
        extension=""
    return extension

def extract_authorization_header(url):
    logger.info("servers.filenium extract_authorization_header")

    # Obtiene login y password, y lo añade como cabecera Authorization
    partes = url[7:].split("@")
    partes = partes[0].split(":")
    username = partes[0].replace("%40","@")
    password = partes[1]
    logger.info("servers.filenium username="+username)
    logger.info("servers.filenium password="+password)
    
    import base64
    base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
    logger.info("servers.filenium Authorization="+base64string)
    authorization_header = "Basic %s" % base64string
    
    # Ahora saca el login y password de la URL
    partes = url.split("@")
    url = "http://"+partes[1]
    logger.info("servers.filenium nueva url="+url)

    return url,authorization_header

def correct_url(url):
    if "userporn.com" in url:
        url = url.replace("/e/","/video/")
    
    if "putlocker" in url or "firedrive" in url:
        url = url.replace("/embed/","/file/")
    return url

def find_videos(data):
    return []
