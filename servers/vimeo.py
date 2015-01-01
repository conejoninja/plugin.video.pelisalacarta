# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para Vimeo
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os
import socket
from xml.dom.minidom import parseString

from core import scrapertools
from core import logger
from core import config
from core import jsontools

# Returns an array of possible video url's from the page_url
def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("servers.vimeo get_video_url(page_url='%s')" % page_url)

    video_urls = []

    headers = []
    headers.append( ['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'] )
    data = scrapertools.cache_page(page_url, headers=headers)

    '''
    <div class="player" style="background-image: url(http://b.vimeocdn.com/ts/433/562/433562952_960.jpg);" id="player_1_53086fb0f413f" data-config-url="http://player.vimeo.com/v2/video/63073570/config?autoplay=0&amp;byline=0&amp;bypass_privacy=1&amp;context=clip.main&amp;default_to_hd=1&amp;portrait=0&amp;title=0&amp;s=4268c7772994be693b480b75b5d84452f3e81f96" data-fallback-url="//player.vimeo.com/v2/video/63073570/fallback?js"
    '''
    url = scrapertools.find_single_match(data,'<div class="player" style="[^"]+" id="[^"]+" data-config-url="([^"]+)"')
    url = url.replace("&amp;","&")
    headers.append( ['Referer',page_url] )
    data = scrapertools.cache_page(url, headers=headers)
    json_object = jsontools.load_json(data)
    '''
    http://player.vimeo.com/v2/video/63073570/config?autoplay=0&byline=0&bypass_privacy=1&context=clip.main&default_to_hd=1&portrait=0&title=0&s=4268c7772994be693b480b75b5d84452f3e81f96

    > GET /v2/video/63073570/config?autoplay=0&byline=0&bypass_privacy=1&context=clip.main&default_to_hd=1&portrait=0&title=0&s=4268c7772994be693b480b75b5d84452f3e81f96 HTTP/1.1
    > User-Agent: curl/7.24.0 (x86_64-apple-darwin12.0) libcurl/7.24.0 OpenSSL/0.9.8y zlib/1.2.5
    > Host: player.vimeo.com
    > Accept: */*
    > 
    < HTTP/1.1 200 OK
    < Expires: Sun, 23 02 2014 09:39:32 GMT
    < Vary: Origin, Accept-Encoding
    < Etag: "009d88dc9b151e402faf10efb7ba4cabe0412385"
    < P3p: CP="This is not a P3P policy! See http://vimeo.com/privacy"
    < Content-Type: application/json
    < Transfer-Encoding: chunked
    < Date: Sat, 22 Feb 2014 09:39:32 GMT
    < X-Varnish: 1162931632
    < Age: 0
    < Via: 1.1 varnish
    < Cache-Control: no-store, no-cache, must-revalidate, post-check=0, pre-check=0
    < X-Player2: 1
    < X-Varnish-Cache: 0
    < nnCoection: close
    < X-VServer: 10.90.128.193
    < 
    * Connection #0 to host player.vimeo.com left intact
    {"cdn_url":"http://a.vimeocdn.com","view":1,"request":{"files":{"h264":{"hd":{"profile":113,"origin":"ns3.pdl","url":"http://pdl.vimeocdn.com/72437/773/155150233.mp4?token2=1393065072_197f0ca458049c7217e9e8969c373af1&aksessionid=358994b3a75767bb","height":720,"width":1280,"id":155150233,"bitrate":2658,"availability":60},"sd":{"profile":112,"origin":"ns3.pdl","url":"http://pdl.vimeocdn.com/44925/440/155100150.mp4?token2=1393065072_cd5b62387758a46798e02dbd0b19bd3e&aksessionid=56c93283ac081129","height":360,"width":640,"id":155100150,"bitrate":860,"availability":60}},"hls":{"all":"http://av70.hls.vimeocdn.com/i/,44925/440/155100150,72437/773/155150233,.mp4.csmil/master.m3u8?primaryToken=1393065072_fe1a557fd7460bc8409bf09960614694","hd":"http://av70.hls.vimeocdn.com/i/,72437/773/155150233,.mp4.csmil/master.m3u8?primaryToken=1393065072_8ba190ee7643f318c75dc265a14b750d"},"codecs":["h264"]},"ga_account":"UA-76641-35","timestamp":1393061972,"expires":3100,"prefix":"/v2","session":"9d8f0ce5a2de113df027f1f1d2428648","cookie":{"scaling":1,"volume":1.0,"hd":null,"captions":null},"cookie_domain":".vimeo.com","referrer":null,"conviva_account":"c3.Vimeo","flags":{"login":1,"preload_video":1,"plays":1,"partials":1,"conviva":1},"build":{"player":"d854ba1a","js":"2.3.7"},"urls":{"zeroclip_swf":"http://a.vimeocdn.com/p/external/zeroclipboard/ZeroClipboard.swf","js":"http://a.vimeocdn.com/p/2.3.7/js/player.js","proxy":"https://secure-a.vimeocdn.com/p/2.3.7/proxy.html","conviva":"http://livepassdl.conviva.com/ver/2.72.0.13589/LivePass.js","flideo":"http://a.vimeocdn.com/p/flash/flideo/1.0.3b10/flideo.swf","canvas_js":"http://a.vimeocdn.com/p/2.3.7/js/player.canvas.js","moog":"http://a.vimeocdn.com/p/flash/moogaloop/6.0.7/moogaloop.swf?clip_id=63073570","conviva_service":"http://livepass.conviva.com","moog_js":"http://a.vimeocdn.com/p/2.3.7/js/moogaloop.js","zeroclip_js":"http://a.vimeocdn.com/p/external/zeroclipboard/ZeroClipboard-patch.js","css":"http://a.vimeocdn.com/p/2.3.7/css/player.css"},"signature":"67ef54c1e894448dd7c38e7da8a3bdba"},"player_url":"player.vimeo.com","video":{"allow_hd":1,"height":720,"owner":{"account_type":"basic","name":"Menna Fit\u00e9","img":"http://b.vimeocdn.com/ps/446/326/4463264_75.jpg","url":"http://vimeo.com/user10601457","img_2x":"http://b.vimeocdn.com/ps/446/326/4463264_300.jpg","id":10601457},"thumbs":{"1280":"http://b.vimeocdn.com/ts/433/562/433562952_1280.jpg","960":"http://b.vimeocdn.com/ts/433/562/433562952_960.jpg","640":"http://b.vimeocdn.com/ts/433/562/433562952_640.jpg"},"duration":2200,"id":63073570,"hd":1,"embed_code":"<iframe src=\"//player.vimeo.com/video/63073570\" width=\"500\" height=\"281\" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>","default_to_hd":1,"title":"No le digas a la Mama que me he ido a Mongolia en Moto","url":"http://vimeo.com/63073570","privacy":"anybody","share_url":"http://vimeo.com/63073570","width":1280,"embed_permission":"public","fps":25.0},"build":{"player":"d854ba1a","rpc":"dev"},"embed":{"player_id":null,"outro":"nothing","api":2,"context":"clip.main","time":0,"color":"00adef","settings":{"fullscreen":1,"instant_sidedock":1,"byline":0,"like":1,"playbar":1,"title":0,"color":1,"branding":0,"share":1,"scaling":1,"logo":0,"info_on_pause":0,"watch_later":1,"portrait":0,"embed":1,"badge":0,"volume":1},"on_site":1,"loop":0,"autoplay":0},"vimeo_url":"vimeo.com","user":{"liked":0,"account_type":"none","logged_in":0,"owner":0,"watch_later":0,"id":0,"mod":0}}* Closing connection #0
    '''

    media_url = json_object['request']['files']['h264']['hd']['url']
    video_urls.append( [ "HD [vimeo]",media_url ] )    
    media_url = json_object['request']['files']['h264']['sd']['url']
    video_urls.append( [ "SD [vimeo]",media_url ] )    

    for video_url in video_urls:
        logger.info("servers.vimeo %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    #"http://player.vimeo.com/video/17555432?title=0&amp;byline=0&amp;portrait=0
    patronvideos  = 'player.vimeo.com/video/([0-9]+)'
    logger.info("servers.vimeo find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[vimeo]"
        url = "http://vimeo.com/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'vimeo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            

    #"http://vimeo.com/17555432
    patronvideos  = 'vimeo.com/([0-9]+)'
    logger.info("servers.vimeo find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[vimeo]"
        url = "http://vimeo.com/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'vimeo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
    return devuelve
