# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para ver un vídeo conociendo su URL
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys

from core import scrapertools
from core import config
from core import logger
from core.item import Item
from servers import servertools

__channel__ = "tengourl"
__category__ = "G"
__type__ = "generic"
__title__ = "tengourl"
__language__ = ""

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[tengourl.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="search", title="Entra aquí y teclea la URL"))

    return itemlist

# Al llamarse "search" la función, el launcher pide un texto a buscar y lo añade como parámetro
def search(item,texto):
    logger.info("[tengourl.py] search texto="+texto)
    
    if not texto.startswith("http://"):
        texto = "http://"+texto
    
    itemlist = []

    itemlist = servertools.find_video_items(data=texto)
    for item in itemlist:
        item.channel=__channel__
        item.action="play"

    if len(itemlist)==0:
        itemlist.append( Item(channel=__channel__, action="search", title="No hay ningún vídeo compatible en esa URL"))
    
    return itemlist

def test():
    return True