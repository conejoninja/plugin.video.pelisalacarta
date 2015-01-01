# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para Libreria XBMC
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

import os.path
import fnmatch
from core import DecryptYonkis as Yonkis
import sqlite3

from core import scrapertools
from core import logger
from core import config
from core.item import Item

CHANNELNAME = "LibreriaXBMC"
DEBUG = True
DIRNAME = config.get_setting("LIBRARY_PATH")
BD = config.get_setting("LIBRARY_BD")

conn = sqlite3.connect(BD)

def isGeneric():
   return True

def mainlist(item):
   logger.info("[libreriaXBMC.py] mainlist")
   
   itemlist = []
   # Listar entradas y meterlas en "files"
   c = conn.cursor()

   c.execute("""select sh.idShow, sh.c00 as title,
             sh.c06 as thumb, max(ep.c12)
            from tvshow sh, episode ep, TVSHOWLINKEPISODE rel
            where sh.idShow = rel.idShow 
            and      ep.idEpisode = rel.idEpisode
            group by sh.idShow""")

   for row in c:
       urlR= 'idshow='+str(row[0])+'&temps='+str(row[3])
       thumb= getThumb(row[2])
       titulo =  row[1].encode("iso-8859-1")
       itemlist.append( Item(channel=CHANNELNAME, title=titulo, action="listseries", url=urlR, thumbnail=thumb, folder=True) )
      
   #conn.close()
   return itemlist
   

def sortedlistdir(d, cmpfunc=cmp):
    l = os.listdir(d)
    l.sort(cmpfunc)
    return l

def getThumb(contenido):
     #<thumb ???></thumb>
     contenido = contenido.split("</thumb>")
     thumb = contenido[0].split(">")
     return thumb[1].encode("iso-8859-1")

def getParam(contenido,param):
    try:
        contenido = contenido.split(param + "=")
        contenido = contenido[1].split("&")
        result = contenido[0]
    except:
        result = ""
    return result

def listseries(item):
    logger.info("[libreriaXBMC.py] listseries")
    
    itemlist = []
    
    params = item.url
    
    
    # ------------------------------------------------------
    # Calculo de las temporadas
    # ------------------------------------------------------
    c = conn.cursor()
    
    idSerie = getParam(params,'idshow')
    tempActual = getParam(params,'temp')
    temps      = int(getParam(params,'temps'))
    if tempActual == "" :
        #lista temporadas
        if temps > 1 :

            #Mostramos lista de temporadas
            c.execute("""select  ep.c12
               from tvshow sh, episode ep, TVSHOWLINKEPISODE rel
               where sh.idShow = rel.idShow
               and     ep.idEpisode = rel.idEpisode
               and     sh.idShow = ?
               group by ep.c12
               order by ep.c12""", idSerie)

            for row in c:
                urlR= 'idshow='+idSerie+'&temps='+str(temps)+'&temp='+str(row[0])
                titulo =  'Temporada '+ str(row[0]) .encode("iso-8859-1")
                itemlist.append( Item(channel=CHANNELNAME, title=titulo, action="listseries", url=urlR,  folder=True) )
            return itemlist 
        else:
            tempActual = 1

   
    # ------------------------------------------------------
    # Extrae las entradas
    # ------------------------------------------------------
    
    c.execute("""select  ep.idFile
       from tvshow sh, episode ep, TVSHOWLINKEPISODE rel
       where sh.idShow = rel.idShow
       and     ep.idEpisode = rel.idEpisode
       and     sh.idShow = ?
       and     ep.c12 = ? """, [idSerie, tempActual])
      
    for row in c:
        #urlR= 'idshow='+idSerie+'&temps='+str(temps)+'&temp='+str(tempActual)
        contenido =  getContentFile(row[0])
        urlR= str(contenido['url']) + '&idFile=' +str(row[0])
        itemlist.append( Item(channel=CHANNELNAME, title=contenido['title'], action=contenido['action'], url=urlR, server=contenido['server'], thumbnail=contenido['thumbnail'], folder=True) )
   
    #conn.close()    
    return itemlist

def getContentFile(idFile):
     
    #print 'Entramos con ' + str(idFile)
    c = conn.cursor()
    
    c.execute(""" select  ep.c12||'x'||ep.c13||' - '||ep.c00 as title,
     ep.c06 as thumb,
     f.strFilename as file,
     p.strPath as path,   
     f.playCount as visto
    from episode ep,  files f,
      tvshowlinkpath relPa,
      tvshowlinkepisode relEp,
      path p
    where     ep.idFile = f.idFile
    and      relPa.idShow = relEp.idShow
    and      relEp.idEpisode = ep.idEpisode
    and      relPa.idPath = p.idPath
    and      ep.idFile = ?
    """, [idFile])

    for row in c:
        #special://home/userdata/addon_data/plugin.video.pelisalacarta/library/SERIES/titulo/
        path = row[3].split("library/")
        archivo = row[2]
        path = path[1] + archivo
        seriepath = os.path.join(DIRNAME,path)
        #print str(row[4]) + ' archivo ' + seriepath
        fileHandle = open ( seriepath )
        contenido = fileHandle.readline()
        fileHandle.close()
        #Arreglamos la url
        contenido = urllib.unquote(contenido)
        canal = getParam(contenido,"channel")
        urlFile = getParam(contenido,"url")
        servidor = getParam(contenido,"server")
      
    if ( row[4] > 0 ):
        visto = "X - "
    else:
        visto = ""
   
    titulo = visto+row[0].encode("iso-8859-1")
    thumb = getThumb(row[1])
    return {'title':titulo, 'action':canal, 'url':urlFile, 'server':servidor, 'thumbnail':thumb}

def marcarVisto(idFile):
    c = conn.cursor()
    c.execute("""update files
         set playCount = 1,
        lastPlayed = DATETIME('NOW') 
         where idFile = ?  """, [idFile])
          
    conn.commit()
    print 'Marcando como visto el ' + idFile
