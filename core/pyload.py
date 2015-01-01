# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Lista de vídeos descargados
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urllib
import os
from core import config
from core import logger
from core.item import Item
from urlparse import urlparse
import time
from lib.thriftbackend.ThriftClient import ThriftClient, WrongLogin
CHANNELNAME = "pyload"
DEBUG = True

pyload = config.get_setting("pyload")
ip_pto = urlparse(pyload)[1] 
SERVER = ip_pto.split(":")[0]
PORT = ip_pto.split(":")[1]


def isGeneric():
    return True

def mainlist(item):
    itemlist = []
    
    dir_descargas = config.get_setting("pyload_downloads")
    itemlist.append( Item( channel=CHANNELNAME, action="ver_activas", title="Descargas Activas"))
    itemlist.append( Item( channel=CHANNELNAME, action="ver_cola", title="Cola"))
    itemlist.append( Item( channel=CHANNELNAME, action="ver_descargados", title="Ver Descargados", url=dir_descargas))
    return itemlist

    
def ver_activas(item):
    itemlist = []
    try:
        client = ThriftClient(host=SERVER, port=PORT)
    except:
        itemlist.append( Item( title="Login incorrecto", channel=CHANNELNAME, action="mainlist" ) )
        return itemlist

    lista = client.statusDownloads()
    for p in lista:
        itemlist.append( Item( title=p.name.encode("iso-8859-15"), channel=CHANNELNAME, action="detalle_descarga",url="%s" % p.fid ) )
    if len(itemlist) == 0:
        itemlist.append( Item( title="Ninguna descarga activa", channel=CHANNELNAME, action="mainlist" ) )
   
    return itemlist
    
def detalle_descarga(item):
    itemlist = []
    try:
        client = ThriftClient(host=SERVER, port=PORT)
    except:
        itemlist.append( Item( title="Login incorrecto", channel=CHANNELNAME, action="mainlist" ) )
        return itemlist

    lista = client.statusDownloads()
    for p in lista:
        if p.fid == int(item.url):
            titulo =p.name.encode("iso-8859-15")
            detalles = "%s  %s@%skb/s  %s  %s%% / %s MB" % (p.statusmsg,p.format_eta,p.speed / 1000,p.format_size,p.percent, ((p.size - p.bleft)/1024)/1024)
            itemlist.append( Item( title=titulo, channel=CHANNELNAME, action="detalle_descarga",url="%s" % p.fid ) )
            itemlist.append( Item( title=detalles, channel=CHANNELNAME, action="detalle_descarga",url="%s" % p.fid ) )
    return itemlist
    if len(itemlist) == 0:
        itemlist.append( Item( title="Ninguna descarga activa", channel=CHANNELNAME, action="ver_activas" ) )
   

def ver_cola(item):
    itemlist = []
    try:
        client = ThriftClient(host=SERVER, port=PORT)
    except:
        itemlist.append( Item( title="Login incorrecto", channel=CHANNELNAME, action="mainlist" ) )
        return itemlist
    q = client.getQueue()
    for p in q:
        enlaces = len(p.links)
        if enlaces == 1: titulo = "%s (1 enlace)" % (p.name)
        else: titulo = "%s (%s enlaces)" % (p.name,enlaces)
        itemlist.append( Item( title=titulo, channel=CHANNELNAME, action="ver_paquete",url="%s" % p.pid ) )

    if len(itemlist) == 0:
        itemlist.append( Item( title="Ningún paquete en cola", channel=CHANNELNAME, action="mainlist" ) )

    itemlist.append( Item( title="Borrar terminados", channel=CHANNELNAME, action="borrar_terminados" ) )
    itemlist.append( Item( title="Reiniciar fallidos", channel=CHANNELNAME, action="reiniciar_fallidos" ) )
    return itemlist
    
def borrar_terminados(item):
    itemlist = []
    try:
        client = ThriftClient(host=SERVER, port=PORT)
    except:
        itemlist.append( Item( title="Login incorrecto", channel=CHANNELNAME, action="mainlist" ) )
        return itemlist

    client.deleteFinished()
    time.sleep(3)
    itemlist.append( Item( title="Paquetes terminados eliminados", channel=CHANNELNAME, action="ver_cola" ) )
    return itemlist
    
def reiniciar_fallidos(item):
    itemlist = []
    try:
        client = ThriftClient(host=SERVER, port=PORT)
    except:
        itemlist.append( Item( title="Login incorrecto", channel=CHANNELNAME, action="mainlist" ) )
        return itemlist

    client.restartFailed()
    time.sleep(3)
    itemlist.append( Item( title="Reiniciados los paquetes fallidos", channel=CHANNELNAME, action="ver_cola" ) )
    return itemlist

def ver_paquete(item):
    itemlist = []
    try:
        client = ThriftClient(host=SERVER, port=PORT)
    except:
        itemlist.append( Item( title="Login incorrecto", channel=CHANNELNAME, action="mainlist" ) )
        return itemlist

    data = client.getPackageData(int(item.url))
    for p in data.links:
       plot = "Estado = %s --> Progreso = %s%% de %s (URL: %s)" % (p.statusmsg, p.progress, p.format_size, p.url)
       itemlist.append( Item( title=p.name, plot=plot, channel=CHANNELNAME, action="detalle_fichero_cola",url="%s" % p.fid ) )
       itemlist.append( Item( title=plot, plot=plot, channel=CHANNELNAME, action="detalle_fichero_cola",url="%s" % p.fid ) )

    if len(itemlist) == 0:
        itemlist.append( Item( title="Ningún enlace", channel=CHANNELNAME, action="ver_cola" ) )
    else:
        itemlist.append( Item( title="ELIMINAR PAQUETE", channel=CHANNELNAME, action="eliminar_paquete", url=item.url ) )
        itemlist.append( Item( title="REINICIAR PAQUETE", channel=CHANNELNAME, action="reiniciar_paquete", url=item.url ) )
   
    return itemlist

def eliminar_paquete(item):
    itemlist = []
    try:
        client = ThriftClient(host=SERVER, port=PORT)
    except:
        itemlist.append( Item( title="Login incorrecto", channel=CHANNELNAME, action="mainlist" ) )
        return itemlist

    client.deletePackages((int(item.url)))
    time.sleep(10)
    q = client.getQueue()
#    hallado = 0 --> El tiempo de respuesta de pyLoad es poco previsible
#    for p in q:
#        if p.pid == int(item.url): hallado = 1
#    if hallado == 1:
    itemlist.append( Item( title="Paquete eliminado", channel=CHANNELNAME, action="ver_cola" ) )
#    else:
#        itemlist.append( Item( title="Error al eliminar el paquete", channel=CHANNELNAME, action="ver_cola" ) )
    return itemlist

def reiniciar_paquete(item):
    itemlist = []
    try:
        client = ThriftClient(host=SERVER, port=PORT)
    except:
        itemlist.append( Item( title="Login incorrecto", channel=CHANNELNAME, action="mainlist" ) )
        return itemlist

    client.restartPackage(int(item.url))
    time.sleep(15)
    lista = client.statusDownloads()
#    hallado = 0
#    for p in lista:
#        if p.pid == int(item.url): hallado = 1
#    if hallado == 1:
    itemlist.append( Item( title="Paquete reiniciado", channel=CHANNELNAME, action="ver_cola" ) )
#    else:
#        itemlist.append( Item( title="Error al reiniciar el paquete", channel=CHANNELNAME, action="ver_cola" ) )
    return itemlist

def detalle_fichero_cola(item):
    itemlist = []
    try:
        client = ThriftClient(host=SERVER, port=PORT)
    except:
        itemlist.append( Item( title="Login incorrecto", channel=CHANNELNAME, action="mainlist" ) )
        return itemlist

    p = client.getFileData(int(item.url))
    plot = "Fichero = %s: Estado = %s --> Progreso = %s%% de %s (URL: %s)" % (p.name, p.statusmsg, p.progress, p.format_size, p.url)
    if len(p.error) > 0: plot = plot+" ERROR: "+p.error 
    itemlist.append( Item( title=p.name, fulltitle=p.name, plot=plot, channel=CHANNELNAME, action="detalle_fichero_cola",url="%s" % p.fid ) )
    itemlist.append( Item( title=plot, fulltitle=p.name, plot=plot, channel=CHANNELNAME, action="detalle_fichero_cola",url="%s" % p.fid ) )
    itemlist.append( Item( title="Borrar fichero", fulltitle=p.name, plot=plot, channel=CHANNELNAME, action="borrar_fichero",url="%s" % p.fid ) )
    itemlist.append( Item( title="Reintentar", fulltitle=p.name, plot=plot, channel=CHANNELNAME, action="reintentar_fichero",url="%s" % p.fid ) )
    itemlist.append( Item( title="Volver", fulltitle=p.name, plot=plot, channel=CHANNELNAME, action="ver_paquete",url="%s" % p.packageID ) )

    return itemlist

def borrar_fichero(item):
    itemlist = []
    try:
        client = ThriftClient(host=SERVER, port=PORT)
    except:
        itemlist.append( Item( title="Login incorrecto", channel=CHANNELNAME, action="mainlist" ) )
        return itemlist

    client.deleteFiles((int(item.url)))
    time.sleep(10)
    itemlist.append( Item( title="Paquete eliminado", channel=CHANNELNAME, action="ver_cola" ) )
    return itemlist

def reintentar_fichero(item):
    itemlist = []
    try:
        client = ThriftClient(host=SERVER, port=PORT)
    except:
        itemlist.append( Item( title="Login incorrecto", channel=CHANNELNAME, action="mainlist" ) )
        return itemlist

    client.restartFile(int(item.url))
    time.sleep(10)
    itemlist.append( Item( title="Paquete reiniciado", channel=CHANNELNAME, action="ver_cola" ) )
    return itemlist

def descargar(item):
    itemlist = []
    try:
        client = ThriftClient(host=SERVER, port=PORT)
    except:
        item.title = "Error al conectar con el servidor pyLoad"
        itemlist.append( item )
        return itemlist
  
    try: 
        packid = client.addPackage(item.fulltitle, [item.url],0)
        item.title = "Fichero pedido a pyLoad"
    except:
        item.title = "Error al encolar el fichero"
    
    itemlist.append( item )
    time.sleep(5)
    return itemlist

def ver_descargados(item):
    itemlist=[]
    # Lee la ruta de descargas
    dir_descargas = item.url
    raiz = config.get_setting("pyload_downloads")
    print "raiz = %s, dir_descargas = %s" % (raiz, dir_descargas)
    if os.path.normpath(raiz) != os.path.normpath(dir_descargas):
        itemlist.append( Item( channel=CHANNELNAME, action="ver_descargados", title=". .", url=os.path.dirname(dir_descargas)))
        
    ficheros = os.listdir(dir_descargas)
        
    for fichero in ficheros:
        url = os.path.join(dir_descargas, fichero) 
        if os.path.isdir(url):
            itemlist.append( Item( channel=CHANNELNAME, action="ver_descargados", title="DIR "+fichero, url=url))
        else: 
            itemlist.append( Item( channel=CHANNELNAME, action="play", title=fichero, url=url, server="local", folder=False))
    return itemlist


