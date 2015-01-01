# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
import xbmc,time

from core import scrapertools
from core import config
from core import logger
from core.item import Item
from servers import servertools

logger.info("[library_service.py] Actualizando series...")
from platformcode.xbmc import library
from platformcode.xbmc import launcher
import xbmcgui

#Eliminar carpeta antes de actualizar
    
directorio = os.path.join(config.get_library_path(),"SERIES")
logger.info ("directorio="+directorio)
import shutil

#if os.path.exists(directorio):
#    shutil.rmtree(directorio)

if not os.path.exists(directorio):
    os.mkdir(directorio)

nombre_fichero_config_canal = os.path.join( config.get_library_path() , "series.xml" )
if not os.path.exists(nombre_fichero_config_canal):
    nombre_fichero_config_canal = os.path.join( config.get_data_path() , "series.xml" )

try:

    if config.get_setting("updatelibrary")=="true":
        config_canal = open( nombre_fichero_config_canal , "r" )
        
        for serie in config_canal.readlines():
            logger.info("[library_service.py] serie="+serie)
            serie = serie.split(",")
        
            ruta = os.path.join( config.get_library_path() , "SERIES" , serie[0] )
            logger.info("[library_service.py] ruta =#"+ruta+"#")
            if os.path.exists( ruta ):
                logger.info("[library_service.py] Actualizando "+serie[0])
                item = Item(url=serie[1], show=serie[0])
                try:
                    itemlist = []
                    if serie[2].strip()=='veranime':
                        from pelisalacarta.channels import veranime
                        itemlist = veranime.episodios(item)
                    if serie[2].strip()=='tumejortv':
                        from pelisalacarta.channels import tumejortv
                        itemlist = tumejortv.findepisodios(item)
                    if serie[2].strip()=='shurweb':
                        from pelisalacarta.channels import shurweb
                        itemlist = shurweb.episodios(item)
                    if serie[2].strip()=='seriespepito':
                        from pelisalacarta.channels import seriespepito
                        itemlist = seriespepito.episodios(item)
                    if serie[2].strip()=='seriesyonkis':
                        from pelisalacarta.channels import seriesyonkis
                        itemlist = seriesyonkis.episodios(item)
                    if serie[2].strip()=='seriesly':
                        from pelisalacarta.channels import seriesly
                        itemlist = seriesly.episodios(item)
                    if serie[2].strip()=='cuevana':
                        from pelisalacarta.channels import cuevana
                        itemlist = cuevana.episodios(item)
                    if serie[2].strip()=='animeflv':
                        from pelisalacarta.channels import animeflv
                        itemlist = animeflv.episodios(item)
                    if serie[2].strip()=='animeid':
                        from pelisalacarta.channels import animeid
                        itemlist = animeid.episodios(item)
                    if serie[2].strip()=='moviezet':
                        from pelisalacarta.channels import moviezet
                        itemlist = moviezet.serie(item)
                except:
                    import traceback
                    from pprint import pprint
                    exc_type, exc_value, exc_tb = sys.exc_info()
                    lines = traceback.format_exception(exc_type, exc_value, exc_tb)
                    for line in lines:
                        line_splits = line.split("\n")
                        for line_split in line_splits:
                            logger.error(line_split)
                    itemlist = []
            else:
                logger.info("[library_service.py] No actualiza "+serie[0]+" (no existe el directorio)")
                itemlist=[]

            for item in itemlist:
                #logger.info("item="+item.tostring())
                try:
                    item.show=serie[0].strip()
                    library.savelibrary( titulo=item.title , url=item.url , thumbnail=item.thumbnail , server=item.server , plot=item.plot , canal=item.channel , category="Series" , Serie=item.show , verbose=False, accion="play_from_library", pedirnombre=False, subtitle=item.subtitle )
                except:
                    logger.info("[library_service.py] Capitulo no valido")

        import xbmc
        xbmc.executebuiltin('UpdateLibrary(video)')
    else:
        logger.info("No actualiza la biblioteca, está desactivado en la configuración de pelisalacarta")

except:
    logger.info("[library_service.py] No hay series para actualizar")
