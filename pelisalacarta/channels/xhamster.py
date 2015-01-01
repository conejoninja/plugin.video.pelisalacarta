# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para xhamster
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# Por boludiko
#------------------------------------------------------------
import cookielib
import urlparse,urllib2,urllib,re
import os
import sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "xhamster"
__category__ = "F"
__type__ = "generic"
__title__ = "xHamster"
__language__ = "ES"
__adult__ = "true"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[xhamster.py] mainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="videos"      , title="Útimos videos" , url="http://www.xhamster.com/"))
    itemlist.append( Item(channel=__channel__, action="listcategorias"    , title="Listado Categorias"))
    itemlist.append( Item(channel=__channel__, action="search"    , title="Buscar", url="http://xhamster.com/search.php?q=%s&qcat=video"))
    return itemlist

# REALMENTE PASA LA DIRECCION DE BUSQUEDA

def search(item,texto):
    logger.info("[xhamster.py] search")
    tecleado = texto.replace( " ", "+" )
    item.url = item.url % tecleado
    return videos(item)

# SECCION ENCARGADA DE BUSCAR

def videos(item):
    logger.info("[xhamster.py] videos")
    data = scrapertools.downloadpageWithoutCookies(item.url)
    #data = scrapertools.get_match(data,'<td valign="top" id="video_title">(.*?)<div id="footer">')
    itemlist = []

    '''
    <a href="/movies/1280051/pussy_pump_002.html?s=10" class='hRotator' >
    <img src='http://et1.xhamster.com/t/051/10_1280051.jpg' width='160' height='120' alt="pussy pump 002"/>
    <img class='hSprite' src="http://eu-st.xhamster.com/images/spacer.gif" width='160' height='120' sprite='http://et1.xhamster.com/t/051/s_1280051.jpg' id="1280051" onmouseover="hRotator.start2(this);">
    '''
    '''
    <a href='http://xhamster.com/movies/1627978/its_so_big_its_stretching_my_insides.html'  class='hRotator' >
    <img src='http://et18.xhamster.com/t/978/4_1627978.jpg' width='160' height='120' class='thumb' alt="Its So Big its Stretching My Insides"/><img class='hSprite' src='http://eu-st.xhamster.com/images/spacer.gif' width='160' height='120' sprite='http://et18.xhamster.com/t/978/s_1627978.jpg' id='1627978' onmouseover='hRotator.start2(this);'><b>12:13</b><u title="Its So Big its Stretching My Insides">Its So Big its Stretching My Insides</u></a><div class='hRate'><div class='fr'>94%</div>Views: 168,430</div></div><div class='video'><a href='http://xhamster.com/movies/1445375/busty_preggo_mom_dp_fuck.html'  class='hRotator' ><img src='http://et15.xhamster.com/t/375/3_1445375.jpg' width='160' height='120' class='thumb' alt="Busty preggo mom dp fuck"/><img class='hSprite' src='http://eu-st.xhamster.com/images/spacer.gif' width='160' height='120' sprite='http://et15.xhamster.com/t/375/s_1445375.jpg' id='1445375' onmouseover='hRotator.start2(this);'><b>13:38</b><u title="Busty preggo mom dp fuck">Busty preggo mom dp fuck</u></a><div class='hRate'><div class='fr'>93%</div>Views: 246,305</div></div><div class='video'><a href='http://xhamster.com/movies/745518/lauren_calendar_audition_netvideogirls.html'  class='hRotator' ><img src='http://et18.xhamster.com/t/518/2_745518.jpg' width='160' height='120' class='thumb' alt="Lauren Calendar Audition - netvideogirls"/><img class='hSprite' src='http://eu-st.xhamster.com/images/spacer.gif' width='160' height='120' sprite='http://et18.xhamster.com/t/518/s_745518.jpg' id='745518' onmouseover='hRotator.start2(this);'><b>46:25</b><u title="Lauren Calendar Audition - netvideogirls">Lauren Calendar Audition - netvideogirls</u></a><div class='hRate'><div class='fr'>95%</div>Views: 691,072</div></div><div class='clear' /></div><div class='video'><a href='http://xhamster.com/movies/1609732/pantyhose_hooker_nylon_prostitute_fetish_sex.html'  class='hRotator' ><img src='http://et12.xhamster.com/t/732/5_1609732.jpg' width='160' height='120' class='thumb' alt="pantyhose hooker nylon prostitute fetish sex"/><img class='hSprite' src='http://eu-st.xhamster.com/images/spacer.gif' width='160' height='120' sprite='http://et12.xhamster.com/t/732/s_1609732.jpg' id='1609732' onmouseover='hRotator.start2(this);'><b>13:02</b><u title="pantyhose hooker nylon prostitute fetish sex">pantyhose hooker nylon prostitute fetish sex</u><div class="hSpriteHD"></div></a><div class='hRate'><div class='fr'>95%</div>Views: 232,148</div></div><div class='video'><a href='http://xhamster.com/movies/1670755/tattooed_and_pierced_lesbians_licking_pussies.html'  class='hRotator' ><img src='http://et15.xhamster.com/t/755/7_1670755.jpg' width='160' height='120' class='thumb' alt="tattooed and pierced lesbians licking pussies"/><img class='hSprite' src='http://eu-st.xhamster.com/images/spacer.gif' width='160' height='120' sprite='http://et15.xhamster.com/t/755/s_1670755.jpg' id='1670755' onmouseover='hRotator.start2(this);'><b>13:32</b><u title="tattooed and pierced lesbians licking pussies">tattooed and pierced lesbians licking pussies</u></a><div class='hRate'><div class='fr'>92%</div>Views: 68,202</div></div><div class='video'><a href='http://xhamster.com/movies/1460297/brunette_en_jupe_jaune_baise_dehors.html'  class='hRotator' ><img src='http://et17.xhamster.com/t/297/6_1460297.jpg' width='160' height='120' class='thumb' alt="Brunette en jupe jaune baise dehors"/><img class='hSprite' src='http://eu-st.xhamster.com/images/spacer.gif' width='160' height='120' sprite='http://et17.xhamster.com/t/297/s_1460297.jpg' id='1460297' onmouseover='hRotator.start2(this);'><b>13:31</b><u title="Brunette en jupe jaune baise dehors">Brunette en jupe jaune baise dehors</u></a><div class='hRate'><div class='fr'>91%</div>Views: 64,222</div></div><div class='clear' /></div><div class="loader"></div>
    '''
    patron = "<a href='([^']+)'[^<]+<img src='([^']+)' width='[^']+' height='[^']+' class='[^']+' alt=\"([^\"]+)\""
    matches = re.compile(patron,re.DOTALL).findall(data)
    for url,thumbnail,title in matches:
        try:
            scrapedtitle = unicode( title, "utf-8" ).encode("iso-8859-1")
        except:
            scrapedtitle = title
        scrapedurl = urlparse.urljoin( "http://www.xhamster.com" , url )
        scrapedthumbnail = thumbnail
        scrapedplot = ""
        # Depuracion
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")            
        itemlist.append( Item(channel=__channel__, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle, folder=False))
        
    # EXTRAE EL PAGINADOR
    #<a href='search.php?q=sexo&qcat=video&page=3' class='last'>Next</a></td></tr></table></div></td>
    patronvideos  = '<a href=\'([^\']+)\' class=\'last\'>Next</a></td></tr></table></div></td>'
    siguiente = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(siguiente)
    if len(siguiente)>0:
        itemlist.append( Item(channel=__channel__, action='videos' , title=">> Pagina siguiente" , url=urlparse.urljoin( "http://www.xhamster.com" , siguiente[0] ), thumbnail="", plot="", show="!Página siguiente") )
    else:
        paginador = None

    return itemlist

# SECCION ENCARGADA DE VOLCAR EL LISTADO DE CATEGORIAS CON EL LINK CORRESPONDIENTE A CADA PAGINA
    
def listcategorias(item):
    logger.info("[xhamster.py] listcategorias")
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="videos" , title="Amateur", url="http://xhamster.com/channels/new-amateur-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Anal"  , url="http://xhamster.com/channels/new-anal-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Asian"  , url="http://xhamster.com/channels/new-asian-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="BBW"  , url="http://xhamster.com/channels/new-bbw-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="BDSM"  , url="http://xhamster.com/channels/new-bdsm-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Beach"  , url="http://xhamster.com/channels/new-beach-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Big Boobs"  , url="http://xhamster.com/channels/new-big_boobs-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Bisexuals"  , url="http://xhamster.com/channels/new-bisexuals-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Black and Ebony"  , url="http://xhamster.com/channels/new-ebony-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Blowjobs"  , url="http://xhamster.com/channels/new-blowjobs-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="British"  , url="http://xhamster.com/channels/new-british-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Cartoons"  , url="http://xhamster.com/channels/new-cartoons-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Celebrities"  , url="http://xhamster.com/channels/new-celebs-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Cream Pie"  , url="http://xhamster.com/channels/new-creampie-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Cuckold"  , url="http://xhamster.com/channels/new-cuckold-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Cumshots"  , url="http://xhamster.com/channels/new-cumshots-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Female"  , url="http://xhamster.com/channels/new-female_choice-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Femdom"  , url="http://xhamster.com/channels/new-femdom-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Flashing"  , url="http://xhamster.com/channels/new-flashing-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="French"  , url="http://xhamster.com/channels/new-french-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Gays"  , url="http://xhamster.com/channels/new-gays-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="German"  , url="http://xhamster.com/channels/new-german-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Grannies"  , url="http://xhamster.com/channels/new-grannies-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Group Sex"  , url="http://xhamster.com/channels/new-group-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Hairy"  , url="http://xhamster.com/channels/new-hairy-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Handjobs"  , url="http://xhamster.com/channels/new-handjobs-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Hidden Cam"  , url="http://xhamster.com/channels/new-hidden-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Interracial"  , url="http://xhamster.com/channels/new-interracial-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Japanese"  , url="http://xhamster.com/channels/new-japanese-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Latin"  , url="http://xhamster.com/channels/new-latin-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Lesbians"  , url="http://xhamster.com/channels/new-lesbians-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Massage"  , url="http://xhamster.com/channels/new-massage-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Men"  , url="http://xhamster.com/channels/new-men-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Masturbation"  , url="http://xhamster.com/channels/new-masturbation-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Matures"  , url="http://xhamster.com/channels/new-matures-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="MILFs"  , url="http://xhamster.com/channels/new-milfs-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Old and Young"  , url="http://xhamster.com/channels/new-old_young-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Public Nudity"  , url="http://xhamster.com/channels/new-public-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Sex Toys"  , url="http://xhamster.com/channels/new-toys-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Shemales"  , url="http://xhamster.com/channels/new-shemales-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Stockings"  , url="http://xhamster.com/channels/new-stockings-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Squirting"  , url="http://xhamster.com/channels/new-squirting-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Swingers"  , url="http://xhamster.com/channels/new-swingers-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Teens"  , url="http://xhamster.com/channels/new-teens-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Upskirts"  , url="http://xhamster.com/channels/new-upskirts-1.htm"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Vintage"  , url="http://xhamster.com/channels/new-vintage-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Voyeur"  , url="http://xhamster.com/channels/new-voyeur-1.html"))
    itemlist.append( Item(channel=__channel__, action="videos" , title="Webcams"  , url="http://xhamster.com/channels/new-webcams-1.html"))
    return itemlist
    

# OBTIENE LOS ENLACES SEGUN LOS PATRONES DEL VIDEO Y LOS UNE CON EL SERVIDOR
def play(item):
    logger.info("[xhamster.py] play")
    itemlist = []

    data = scrapertools.cachePage(item.url)
    #logger.debug(data)

    url = scrapertools.get_match(data,'<video poster="[^"]+" controls type=\'video/mp4\' file="([^"]+)"')
    logger.debug("url="+url)
    itemlist.append( Item(channel=__channel__, action="play" , title=item.title, fulltitle=item.fulltitle , url=url, thumbnail=item.thumbnail, plot=item.plot, show=item.title, server="directo", folder=False))
    return itemlist


# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True

    # mainlist
    mainlist_itemlist = mainlist(Item())
    video_itemlist = videos(mainlist_itemlist[0])
    
    # Si algún video es reproducible, el canal funciona
    for video_item in video_itemlist:
        play_itemlist = play(video_item)

        if len(play_itemlist)>0:
            return True

    return False