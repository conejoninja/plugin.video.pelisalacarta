# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para streaminto
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[streaminto.py] url="+page_url)

    logger.info("### page_url-streaminto-find_videos : "+page_url)
    # Normaliza la URL
    try:
        if not page_url.startswith("http://streamin.to/embed-"):
            videoid = scrapertools.get_match(page_url,"streamin.to/([a-z0-9A-Z]+)")
            page_url = "http://streamin.to/embed-"+videoid+".html"
    except:
        import traceback
        logger.info(traceback.format_exc())
    
    # Lo pide una vez
    headers = [['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14']]
    data = scrapertools.cache_page( page_url , headers=headers )
    #logger.info("data="+data)
    
    #file: "37/2640690613_n.flv?h=2ki7efbuztuzcg3h5gecfdpdy3es3m7wc5423nwgzsxybtapha4sna47txdq",
    #streamer: "rtmp://95.211.184.228:1935/vod?h=2ki7efbuztuzcg3h5gecfdpdy3es3m7wc5423nwgzsxybtapha4sna47txdq"
    #image: "http://95.211.184.228:8777/i/03/00130/p0uqfu1iecak.jpg"

    #http://95.211.184.228:8777/15/4045655336_n.flv?h=2ki7efbuztuzcg3h5gecfdpdy3es3m7wc5423nwgzsxybtapha447fe7txcq
    #15/4045655336_n.flv?h=
    #patron = ',\{file\: "([^"]+)"'
    patron_flv = 'file: "([^"]+)"'
    #patron_rtmp = 'streamer: "([^"]+)"'
    patron_jpg = 'image: "(http://[^/]+/)'

    #media_url = []
    try:
        host = scrapertools.get_match(data, patron_jpg)
        logger.info("[streaminto.py] host="+host)
        flv_url = scrapertools.get_match(data, patron_flv)
        logger.info("[streaminto.py] flv_url="+flv_url)
        flv = host+flv_url.split("=")[1]+"/v.flv"
        logger.info("[streaminto.py] flv="+flv)
        #rtmp = scrapertools.get_match(data, patron_rtmp)
    except:
        logger.info("[streaminto.py] opcion 2")
        op = scrapertools.get_match(data,'<input type="hidden" name="op" value="([^"]+)"')
        logger.info("[streaminto.py] op="+op)
        usr_login = ""
        id = scrapertools.get_match(data,'<input type="hidden" name="id" value="([^"]+)"')
        logger.info("[streaminto.py] id="+id)
        fname = scrapertools.get_match(data,'<input type="hidden" name="fname" value="([^"]+)"')
        logger.info("[streaminto.py] fname="+fname)
        referer = scrapertools.get_match(data,'<input type="hidden" name="referer" value="([^"]*)"')
        logger.info("[streaminto.py] referer="+referer)
        hashstring = scrapertools.get_match(data,'<input type="hidden" name="hash" value="([^"]*)"')
        logger.info("[streaminto.py] hashstring="+hashstring)
        imhuman = scrapertools.get_match(data,'<input type="submit" name="imhuman".*?value="([^"]+)"').replace(" ","+")
        logger.info("[streaminto.py] imhuman="+imhuman)
        
        import time
        time.sleep(10)
        
        # Lo pide una segunda vez, como si hubieras hecho click en el banner
        #op=download1&usr_login=&id=z3nnqbspjyne&fname=Coriolanus_DVDrip_Castellano_by_ARKONADA.avi&referer=&hash=nmnt74bh4dihf4zzkxfmw3ztykyfxb24&imhuman=Continue+to+Video
        post = "op="+op+"&usr_login="+usr_login+"&id="+id+"&fname="+fname+"&referer="+referer+"&hash="+hashstring+"&imhuman="+imhuman
        headers.append(["Referer",page_url])
        data = scrapertools.cache_page( page_url , post=post, headers=headers )
        logger.info("data="+data)
    
        # Extrae la URL
        host = scrapertools.get_match(data, patron_jpg)
        flv = host+scrapertools.get_match(data, patron_flv).split("=")[1]+"/v.flv"
        #rtmp = scrapertools.get_match(data, patron_rtmp)
        

    video_urls = []
    video_urls.append( [ scrapertools.get_filename_from_url(flv)[-4:]+" [streaminto]",flv])
    #video_urls.append( [ scrapertools.get_filename_from_url(rtmp)[-4:]+" [streaminto]",rtmp])

    for video_url in video_urls:
        logger.info("[streaminto.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    # Añade manualmente algunos erróneos para evitarlos
    encontrados = set()
    encontrados.add("http://streamin.to/embed-theme.html")
    encontrados.add("http://streamin.to/embed-jquery.html")
    encontrados.add("http://streamin.to/embed-s.html")
    encontrados.add("http://streamin.to/embed-images.html")
    encontrados.add("http://streamin.to/embed-faq.html")
    encontrados.add("http://streamin.to/embed-embed.html")
    encontrados.add("http://streamin.to/embed-ri.html")
    encontrados.add("http://streamin.to/embed-d.html")
    encontrados.add("http://streamin.to/embed-css.html")
    encontrados.add("http://streamin.to/embed-js.html")
    encontrados.add("http://streamin.to/embed-player.html")
    encontrados.add("http://streamin.to/embed-cgi.html")
    devuelve = []

    #http://streamin.to/z3nnqbspjyne
    patronvideos  = 'streamin.to/([a-z0-9A-Z]+)'
    logger.info("[streaminto.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[streaminto]"
        url = "http://streamin.to/embed-"+match+".html"
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'streaminto' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://streamin.to/embed-z3nnqbspjyne.html
    patronvideos  = 'streamin.to/embed-([a-z0-9A-Z]+)'
    logger.info("[streaminto.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[streaminto]"
        url = "http://streamin.to/embed-"+match+".html"
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'streaminto' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve

def test():

    video_urls = get_video_url("http://streamin.to/embed-olnmqfuh1bml.html")

    return len(video_urls)>0