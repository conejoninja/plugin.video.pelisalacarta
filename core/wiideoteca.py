# -*- coding: iso-8859-15 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Blibioteca para Wii por Dalim
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import re,urllib,urllib2,sys
import os
import downloadtools
import config
import logger
import samba
import scrapertools
from item import Item
from xml.dom import minidom
import scrapertools

CHANNELNAME = "wiideoteca"
DEBUG = True
XML = os.path.join( config.get_setting("bookmarkpath"),"series.xml")
if not os.path.exists(XML) and os.path.exists(config.get_setting("bookmarkpath")):
    import shutil
    shutil.copyfile( os.path.join(config.get_runtime_path(),"resources","wiideoteca.xml") , XML )

XML2 = XML.replace("series","pruebas")
title = []
fulltitle = []
thumbnail = []
channel = []
directory = []
idioma = []
plot = []
solonuevos = []
ultimo = []
url = []
borrar = []

def isGeneric():
    return True

def mainlist(item):
    logger.info("[wiideoteca.py] mainlist")
    leerXML()
    eliminarmarcadas()
    itemlist = []
    for i in range(len(title)):
        logger.info(str(i)+" Title: %s | Fulltitle: %s | Thumbnail: %s | Channel: %s | Url: %s" % (title[i],fulltitle[i],thumbnail[i],channel[i],url[i]))
        itemlist.append( Item(channel=CHANNELNAME, action="actualiza", title=title[i] , fulltitle=fulltitle[i] , url=url[i] , thumbnail=thumbnail[i] , plot=plot[i] , extra=str(i) ) )
    itemlist = sorted(itemlist, key=lambda Item: Item.title)  
    return itemlist

def GetXMLTag(archivo,etiqueta):
    logger.info("[wiideoteca.py] GetXMLTag "+etiqueta)
    returnlist = []
    dom = minidom.parse(archivo)
    elementos = dom.getElementsByTagName(etiqueta)
    if len(elementos) != 0:
        for i in range(0,len(elementos)):
            returnlist.extend([elementos[i].childNodes[0].nodeValue]) 
    else:
        logger.info('Error al cargar la etiqueta ' + etiqueta)
    dom.unlink()
    return returnlist

def leerXML():
    logger.info("[wiideoteca.py] leerXML")
    global title,fulltitle,thumbnail,channel,directory,idioma,plot,solonuevos,ultimo,url,borrar
    title = [];fulltitle = [];thumbnail = [];channel = [];directory = [];idioma = [];plot = [];solonuevos = [];ultimo = [];url = []; borrar = []
    title.extend (GetXMLTag(XML,"title"))
    fulltitle.extend (GetXMLTag(XML,"fulltitle"))
    thumbnail.extend (GetXMLTag(XML,"thumbnail"))
    channel.extend (GetXMLTag(XML,"channel"))
    directory.extend (GetXMLTag(XML,"directory"))
    idioma.extend (GetXMLTag(XML,"idioma"))
    plot.extend (GetXMLTag(XML,"plot"))
    solonuevos.extend (GetXMLTag(XML,"solonuevos"))
    ultimo.extend (GetXMLTag(XML,"ultimo"))
    url.extend (GetXMLTag(XML,"url"))
    borrar.extend (GetXMLTag(XML,"borrar"))
    for i in range(len(title)):
        title[i] = urllib.unquote_plus(title[i].strip().encode('utf-8'))
        fulltitle[i] = urllib.unquote_plus(fulltitle[i].strip().encode('utf-8'))
        thumbnail[i] = thumbnail[i].encode('utf-8')
        channel[i] = channel[i].encode('utf-8')
        directory[i] = directory[i].encode('utf-8')
        idioma[i] = urllib.unquote_plus(idioma[i].strip().encode('utf-8'))
        plot[i] = urllib.unquote_plus(plot[i].strip().encode('utf-8'))
        ultimo[i] = urllib.unquote_plus(ultimo[i].strip().encode('utf-8'))
        url[i] = url[i].encode('utf-8')
    
def actualiza(item):
    logger.info("[wiideoteca.py] actualiza")
    from pelisalacarta.channels import cinetube
    returnlist = []
    itemlist = []
    i=int(item.extra)
    leerXML()
    if solonuevos[i]=="True":
        logger.info("Ultimo episodio visto: %s" %ultimo[i])
        if channel[i]=="cinetube":
            itemlist.extend( cinetube.temporadas(item))
            for temporada in itemlist:
                if int(directory[i].rsplit(" ")[1])<int(temporada.title.split(" ")[1]):
                    itemlist2 = []
                    itemlist2.extend( cinetube.episodios(temporada))
                    for capitulo in itemlist2:
                        returnlist.append( Item(channel=capitulo.channel, action=capitulo.action, title=capitulo.title , fulltitle=capitulo.title , url=capitulo.url , thumbnail=thumbnail[i] , plot=plot[i] , extra=temporada.extra , category="wiideoteca") )
                elif int(directory[i].rsplit(" ")[1])==int(temporada.title.split(" ")[1]):
                    itemlist2 = []
                    itemlist2.extend( cinetube.episodios(temporada))
                    for capitulo in itemlist2:
                        if str(ultimo[i])<capitulo.title and str(ultimo[i])not in capitulo.title:
                            returnlist.append( Item(channel=capitulo.channel, action=capitulo.action, title=capitulo.title , fulltitle=capitulo.title , url=capitulo.url , thumbnail=thumbnail[i] , plot=plot[i] , extra=temporada.extra , category="wiideoteca") )
            if returnlist==[]:
                returnlist.append( Item(title="No hay nuevos episodios desde "+str(ultimo[i])) )
            else:
                returnlist.append( Item(channel=CHANNELNAME, action="MarcarVisto", title=">> Marcar todos como vistos <<", url=temporada.extra , fulltitle=capitulo.title, extra=str(i)))
        else:
            returnlist.append( Item(title="Error al actualizar serie") )
    else:
        item.channel=CHANNELNAME;item.action="temporadas";item.category="wiideoteca"
        returnlist.extend( cinetube.temporadas(item))
    returnlist.append( Item(channel=CHANNELNAME, action="configurarSerie", title=">> Configurar Serie <<", fulltitle=item.fulltitle, extra=str(i)))
        
    return returnlist


def configurarSerie(item):
    logger.info("[wiideoteca.py] configurarSerie")
    itemlist = []
    i=int(item.extra)
    leerXML()
    if solonuevos[i]=="True":
        itemlist.append( Item(channel=CHANNELNAME, action="CambiarModo", title="Mostrar todos los episodios", fulltitle=item.fulltitle, extra=str(i)))
    else:
        itemlist.append( Item(channel=CHANNELNAME, action="CambiarModo", title="Mostrar solo los episodios no vistos", fulltitle=item.fulltitle, extra=str(i)))
    itemlist.append( Item(channel=CHANNELNAME, action="ListarEpisodios", title="Seleccionar ultimo episodio visto", fulltitle=item.fulltitle , url=url[i] , thumbnail=thumbnail[i] , plot=plot[i] , extra=str(i)))
    if borrar[i]=="False":
        itemlist.append( Item(channel=CHANNELNAME, action="QuitarSerie", title="Quitar Serie de "+CHANNELNAME, fulltitle=item.fulltitle, extra=str(i)))
    else:
        itemlist.append( Item(channel=CHANNELNAME, action="QuitarSerie", title="Recuperar Serie para "+CHANNELNAME, fulltitle=item.fulltitle, extra=str(i)))
    itemlist.append( Item(channel=CHANNELNAME, action="actualiza", title="Volver" , fulltitle=fulltitle[i] , url=url[i] , thumbnail=thumbnail[i] , plot=plot[i] , extra=str(i)))
#wiideoteca/actualiza/http%3A%2F%2Fwww.cinetube.es%2Fseries%2Flos-misterios-de-laura%2F/directo/Los%20misterios%20de%20Laura/0/none/Los+misterios+de+Laura/playlist.rss
    return itemlist

def CambiarModo(item):
    logger.info("[wiideoteca.py] CambiarModo")
    itemlist = []
    i=int(item.extra)
    dom = minidom.parse(XML)
    elementos = dom.getElementsByTagName("series")
    for elemento in elementos:
        if item.title=="Mostrar todos los episodios":
            elemento.getElementsByTagName('solonuevos')[i].childNodes[0].nodeValue="False"
        elif item.title=="Mostrar solo los episodios no vistos":
            elemento.getElementsByTagName('solonuevos')[i].childNodes[0].nodeValue="True"        
    f = open(XML, "w")
    dom.writexml(f, indent="", addindent="", newl="", encoding='utf-8')
    f.close()
    dom.unlink()

    itemlist.append( Item(title="Se ha cambiado el metodo de visualizacion", action="configurarSerie",fulltitle=item.fulltitle,extra=item.extra) )
    return itemlist

def ListarEpisodios(item):
    logger.info("[wiideoteca.py] ListarEpisodios")
    from pelisalacarta.channels import cinetube
    returnlist = []
    itemlist = []
    i=int(item.extra)
    item.title=item.fulltitle
    leerXML()
    logger.info("Ultimo episodio visto: %s" %ultimo[i])
    if channel[i]=="cinetube":
        itemlist.extend( cinetube.temporadas(item))
        returnlist.append( Item(channel=CHANNELNAME, action="UltimoVisto", title="Ninguno" , fulltitle="0x00" , url="Temporada 0" , thumbnail=thumbnail[i] , extra=str(i) ) )
        for temporada in itemlist:
            itemlist2 = []
            itemlist2.extend( cinetube.episodios(temporada))
            for capitulo in itemlist2:
                returnlist.append( Item(channel=CHANNELNAME, action="MarcarVisto", title=capitulo.title , fulltitle=capitulo.title , url=temporada.extra , thumbnail=thumbnail[i] , extra=str(i) ) )
        if returnlist==[]:
            returnlist.append( Item(title="Error al abrir serie", action="mainlist") )
        else:
            returnlist.append( Item(channel=CHANNELNAME, action="MarcarVisto", title=">> Marcar todos como vistos <<", url=temporada.extra , fulltitle=capitulo.title, extra=str(i)))
    else:
        returnlist.append( Item(title="Error al abrir serie", action="mainlist") )
        
    return returnlist

def UltimoVisto(item):
    logger.info("[wiideoteca.py] UltimoVisto")
    itemlist = []
    leerXML()
    for i in range(len(title)):
        if title[i] in item.fulltitle:
            item.extra=str(i)
            itemlist = MarcarVisto(item)
    return itemlist

def MarcarVisto(item):
    logger.info("[wiideoteca.py] MarcarVisto")
    itemlist = []
    i=int(item.extra)
    dom = minidom.parse(XML)
    elementos = dom.getElementsByTagName("series")
    for elemento in elementos:
        elemento.getElementsByTagName('ultimo')[i].childNodes[0].nodeValue=urllib.quote_plus(item.fulltitle)
        elemento.getElementsByTagName('directory')[i].childNodes[0].nodeValue=str(item.url)
    f = open(XML, "w")
    dom.writexml(f, indent="", addindent="", newl="", encoding='utf-8')
    f.close()
    dom.unlink()
    if item.title==">> Marcar todos como vistos <<":
        itemlist.append( Item(title="Todos los episodios han sido marcados como vistos", action="configurarSerie",fulltitle=item.fulltitle,extra=item.extra) )
    else:
        itemlist.append( Item(title="Seleccionado %s como ultimo episodio visto" % item.fulltitle, action="configurarSerie",fulltitle=item.fulltitle,extra=item.extra) )
    return itemlist

def QuitarSerie(item):
    logger.info("[wiideoteca.py] QuitarSerie")
    itemlist = []
    i=int(item.extra)
    dom = minidom.parse(XML)
    elementos = dom.getElementsByTagName("series")
    for elemento in elementos:
        if "Quitar Serie de " in item.title:
            elemento.getElementsByTagName('borrar')[i].childNodes[0].nodeValue="True"
            itemlist.append( Item(title="La serie "+str(item.fulltitle)+" se ha quitado de "+CHANNELNAME, action="mainlist") )
        elif "Recuperar Serie para " in item.title:
            elemento.getElementsByTagName('borrar')[i].childNodes[0].nodeValue="False"
            itemlist.append( Item(title="La serie "+str(item.fulltitle)+" se ha recuperado para "+CHANNELNAME, action="mainlist") )            
    f = open(XML, "w")
    dom.writexml(f, indent="", addindent="", newl="", encoding='utf-8')
    f.close()
    dom.unlink()
    return itemlist
    
def AgregarSerie (item):
    logger.info("[wiideoteca.py] AgregarSerie")
    itemlist = []
    leerXML()
    seguir = True
    for x in range(0,len(fulltitle)):
        if fulltitle[x]==item.fulltitle.strip(): seguir = False
    if seguir==True:
        i=len(title)
        if item.thumbnail=="": item.thumbnail="Vacio"
        item.fulltitle = urllib.quote_plus(item.fulltitle.strip())
        dom = minidom.parse(XML)

        titulo = dom.createElement("title")
        titulo.appendChild(dom.createTextNode(item.fulltitle))
        
        fulltitulo = dom.createElement("fulltitle")
        titulo.appendChild(fulltitulo)
        fulltitulo.appendChild(dom.createTextNode(item.fulltitle))
        
        caratula = dom.createElement("thumbnail")
        titulo.appendChild(caratula)
        caratula.appendChild(dom.createTextNode(item.thumbnail))

        
        canal = dom.createElement("channel")
        titulo.appendChild(canal)
        canal.appendChild(dom.createTextNode(item.channel))

        
        directorio = dom.createElement("directory")
        titulo.appendChild(directorio)
        directorio.appendChild(dom.createTextNode(item.extra))

            
        lenguaje = dom.createElement("idioma")
        titulo.appendChild(lenguaje)
        lenguaje.appendChild(dom.createTextNode("Vacio"))

            
        sinopsis = dom.createElement("plot")
        titulo.appendChild(sinopsis)
        sinopsis.appendChild(dom.createTextNode("Vacio"))

            
        nuevo = dom.createElement("solonuevos")
        titulo.appendChild(nuevo)
        nuevo.appendChild(dom.createTextNode("False"))

            
        episodio = dom.createElement("ultimo")
        titulo.appendChild(episodio)
        episodio.appendChild(dom.createTextNode("0x00"))

        web = dom.createElement("url")
        titulo.appendChild(web)
        web.appendChild(dom.createTextNode(item.url))
            
        marcar = dom.createElement("borrar")
        titulo.appendChild(marcar)
        marcar.appendChild(dom.createTextNode("False"))
        
        dom.childNodes[0].appendChild(titulo)
        
        f = open(XML, "w")
        dom.writexml(f, indent="", addindent="", newl="", encoding='utf-8')
        f.close()
        dom.unlink()
        
        logger.info("Numero para la serie nueva: "+str(i))
        logger.info("Titulo: "+item.fulltitle)
        logger.info("Web: "+item.url)
        logger.info("Caratula: "+item.thumbnail)
        logger.info("Canal: "+item.channel)
        logger.info("Temporada: "+item.extra)
        
        itemlist.append( Item(title="Se ha añadido la serie a "+CHANNELNAME) )
    else:
        itemlist.append( Item(title="La serie ya esta en la "+CHANNELNAME) )
    return itemlist

def eliminarmarcadas():
    logger.info("[wiideoteca.py] eliminarmarcadas")
    limpiar=False
    dom = minidom.parse(XML)
    elementos = dom.getElementsByTagName("borrar")
    if len(borrar) != 0:
        for i in range(0,len(borrar)):
            if elementos[i].childNodes[0].nodeValue=="True":
                limpiar=True
                elementos = dom.getElementsByTagName("title")
                logger.info("Eliminada serie: %s" % elementos[i].childNodes[0].nodeValue)
                elementos[i].parentNode.removeChild(elementos[i])
        if limpiar==True:
            f = open(XML, "w")
            dom.normalize()
            dom.writexml(f, indent="", addindent="", newl="", encoding='utf-8')
            f.close()
            leerXML()
    dom.unlink()
                
