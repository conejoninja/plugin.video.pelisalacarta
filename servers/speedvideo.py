# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para speedvideo
# by be4t5
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def test_video_exists( page_url ):
    logger.info("[speedvideo.py] test_video_exists(page_url='%s')" % page_url)

    

    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[speedvideo.py] url="+page_url)
    video_urls = []
    import time
    opener = urllib2.build_opener()
    req = urllib2.Request(page_url, None, {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'})
    page = urllib2.urlopen(req)
    page = page.read()
    hash1 = scrapertools.find_single_match(page,'name="hash" value="([^<]+)"')
    idd = scrapertools.find_single_match(page,'name="id" value="([^<]+)"')
    params = {'op': 'download1', 'usr_login': '', 'id': idd, 'fname': '', 'referer': '', 'hash': hash1}
    data = urllib.urlencode(params)
    res = urllib2.Request(page_url, data, {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'})
    response =opener.open(res) 
    page = response.read()
    codif = scrapertools.find_single_match(page,'var [a-z]+ = ([0-9]+);')
    link = scrapertools.find_single_match(page,'linkfile ="([^"]+)"')

    numero = int(codif)

    #Decrypt link base64 // python version of speedvideo's base64_decode() [javascript] 
    
    link1= link[0:numero]
    link2= link[numero+10:]
    link= link1+link2

    alfabeto="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="

    if (not link):
        return link
    link+=""
    
    i=0
    k=0
    array = [""]*1000
    out= ""
    while True:
        a= alfabeto.index(link[i])
        i=i+1
        b= alfabeto.index(link[i])
        i=i+1
        c= alfabeto.index(link[i])
        i=i+1
        d= alfabeto.index(link[i])
        i=i+1
        e= a << 18 | b << 12 | c << 6 | d
        e7 = e >> 16&0xff
        e8 = e >> 8&0xff
        e9 = e&0xff
        uno= [e7,e8]
        due = [e7]
        tre = [e7,e8,e9]
        if(c==64):
            array[k] = ''.join(map(unichr, due))
            k=k+1
        else:
            if (d==64):
               array[k] = ''.join(map(unichr, uno))
               k=k+1
            else:
               array[k] = ''.join(map(unichr, tre))
               k=k+1
        if(i>= len(link)):
            break

    link= "".join(array)
    

    video_urls.append(['[speedvideo]',link])
    
    return video_urls

# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    #http://speedvideo.net/embed-fmbvopi1381q-530x302.html
    patronvideos  = 'speedvideo.net/embed-([A-Z0-9a-z]+)-'
    logger.info("[speedvideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[speedvideo]"
        url = "http://speedvideo.net/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'speedvideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
	
    #http://speedvideo.net/hs7djap7jwrw/Tekken.Kazuyas.Revenge.2014.iTALiAN.Subbed.DVDRiP.XViD.NeWZoNe.avi.html
    patronvideos  = 'speedvideo.net/([A-Z0-9a-z]+)'
    logger.info("[speedvideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[speedvideo]"
        url = "http://speedvideo.net/"+match
        if url not in encontrados and url != "http://speedvideo.net/embed":
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'speedvideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

#Cineblog by be4t5
    patronvideos  = 'cineblog01.../HR/go.php\?id\=([0-9]+)'
    logger.info("[nowvideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)
    page = scrapertools.find_single_match(text,'rel="canonical" href="([^"]+)"')
    from lib import mechanize
    br = mechanize.Browser()
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.set_handle_robots(False)

    for match in matches:
        
        titulo = "[speedvideo]"
        url = "http://cineblog01.pw/HR/go.php?id="+match
        r = br.open(page)
        req = br.click_link(url=url)
        data = br.open(req)
        data= data.read()
        data = scrapertools.find_single_match(data,'speedvideo.net/([^"]+)"?')
        if data=="":
            continue
        d = data.split('-')
        if len(d)>1:
            data = d[1]
            
        url = "http://speedvideo.net/"+data
        d = scrapertools.cache_page(url)
        ma = scrapertools.find_single_match(d,'<title>Watch ([^<]+)</title>')
        ma=titulo+" "+ma

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ ma , url , 'speedvideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

					
    
    return devuelve

def test():

    video_urls = get_video_url("http://www.firedrive.com/embed/E89565C3A0C6183E")

    return len(video_urls)>0



