# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para rapidvideo
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config


USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:18.0) Gecko/20100101 Firefox/18.0"

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[rapidvideo.py] url="+page_url)
    video_urls=[]
    from lib import mechanize
    br = mechanize.Browser()
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.set_handle_robots(False)
    res = br.open(page_url)
    print res.read()
    for form in br.forms():
        br.form = form    
    res = br.submit(name='imhuman')
    page = res.read()
    page = page.split('mp4|')
    idLink = page[1].split('|')
    ip2 = idLink[2]
    ip3 = idLink[3]

    video_urls.append(["[rapidvideo]","http://50.7."+ip3+"."+ip2+":8777/"+idLink[0]+"/v.mp4"])
    
    return video_urls

# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []
            
    #http://www.rapidvideo.com/view/YK7A0L7FU3A
    patronvideos  = 'rapidvideo.org/([A-Za-z0-9]+)/'
    logger.info("[rapidvideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[rapidvideo]"
        url = "http://www.rapidvideo.org/"+match
        d = scrapertools.cache_page(url)
        ma = scrapertools.find_single_match(d,'"fname" value="([^<]+)"')
        ma=titulo+" "+ma
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ ma , url , 'rapidvideo' ] )

            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)


    return devuelve

def test():

    video_urls = get_video_url("http://www.rapidvideo.com/embed/sy6wen17")

    return len(video_urls)>0
