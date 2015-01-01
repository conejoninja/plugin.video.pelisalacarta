# -*- coding: utf-8 -*-
#:-----------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para enlaces a torrent y magnet
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
from core import logger
import urllib

# Returns an array of possible video url's from the page_url
def get_video_url( page_url , premium = False , user="" , password="" , video_password="" ):
    logger.info("[torrent.py] server=torrent, la url es la buena")

    name = page_url[page_url.rfind("/") + 1:page_url.rfind(".")]

    if page_url.startswith('magnet:'):
        link = page_url
    else:
        link = from_torrent_url(page_url)

    media_url_xbmctorrent = "plugin://plugin.video.xbmctorrent/play/%s" % urllib.quote_plus(link)
    media_url_pulsar = "plugin://plugin.video.pulsar/play?uri=%s" % urllib.quote_plus(link)

    video_urls = [
         [ "[xbmctorrent] %s" % (name), media_url_xbmctorrent ],
         [ "[pulsar] %s" % (name), media_url_pulsar ]
     ]

    return video_urls

def from_torrent_url(url):
    import base64
    import bencode
    import hashlib
    print "#### url: %s" % (url)
    torrent_data = url_get(url)
    metadata = bencode.bdecode(torrent_data)
    hashcontents = bencode.bencode(metadata['info'])
    digest = hashlib.sha1(hashcontents).digest()
    b32hash = base64.b32encode(digest)
    params = {
        'dn': metadata['info']['name'],
        'tr': metadata['announce'],
    }
    logger.info(params)
    paramstr = urllib.urlencode(params)
    return 'magnet:?%s&%s' % ('xt=urn:btih:%s' % b32hash, paramstr)

def url_get(url, params={}, headers={}):
    import urllib2
    from contextlib import closing

    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:20.0) Gecko/20100101 Firefox/20.0"

    if params:
        import urllib
        url = "%s?%s" % (url, urllib.urlencode(params))

    req = urllib2.Request(url)
    req.add_header("User-Agent", USER_AGENT)
    for k, v in headers.items():
        req.add_header(k, v)

    try:
        with closing(urllib2.urlopen(req)) as response:
            data = response.read()
            if response.headers.get("Content-Encoding", "") == "gzip":
                import zlib
                return zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(data)
            return data
    except urllib2.HTTPError:
        return None

