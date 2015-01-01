# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para safelinking (ocultador de url)
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def get_long_url( short_url ):
    logger.info("[safelinking.py] get_long_url(short_url='%s')" % short_url)
    
    location = scrapertools.get_header_from_response(short_url,header_to_get="location")
    logger.info("location="+location)

    return location

def test():
    
    location = get_long_url("https://safelinking.net/d/b038a2ed6e")
    ok = ("http://played.to" in location)

    return ok