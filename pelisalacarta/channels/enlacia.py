# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para enlacia
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os,sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "enlacia"
__category__ = "F,S,D"
__type__ = "generic"
__title__ = "enlacia"
__language__ = "ES"

DEBUG = config.get_setting("debug")

SITE = "http://www.enlacia.com"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[enlacia.py] mainlist")
    itemlist = []

    data = scrapertools.cache_page(SITE)
    data = scrapertools.get_match(data,'<div class="submenu wrap">(.*?)<a href="http://www.tripledeseo.com"')
    patron = '<a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for path,title in matches:
        itemlist.append( Item(channel=__channel__, title=title , action="categorias", url=SITE+path ,fanart="http://pelisalacarta.mimediacenter.info/fanart/enlacia.jpg"))

    itemlist.append( Item(channel=__channel__, title="Fichas: Todas las fichas" ,action="listadofichas", url=SITE+"/fichas" ,fanart="http://pelisalacarta.mimediacenter.info/fanart/enlacia.jpg", extra="ver etiquetas") )

    itemlist.append( Item(channel=__channel__, title="Etiquetas: Todas las categorías" ,action="etiquetas", url=SITE+"/tag/" ,fanart="http://pelisalacarta.mimediacenter.info/fanart/enlacia.jpg") )

    itemlist.append( Item(channel=__channel__, title="Buscar: Todas las categorías" ,action="search" ,fanart="http://pelisalacarta.mimediacenter.info/fanart/enlacia.jpg") )

    return itemlist

def categorias(item):
    logger.info("[enlacia.py] categorias")
    itemlist = []

    itemlist.append( Item(channel=__channel__, title=item.title+" - Nuevo-antiguo" ,action="listadofichas" ,url=item.url ,fanart="http://pelisalacarta.mimediacenter.info/fanart/enlacia.jpg") )
    itemlist.append( Item(channel=__channel__, title=item.title+" - A-Z" ,action="listadofichas" ,url=item.url+"/orden:nombre" ,fanart="http://pelisalacarta.mimediacenter.info/fanart/enlacia.jpg") )
    itemlist.append( Item(channel=__channel__, title=item.title+" - Nuevo-antiguo [Completo]" ,action="completo" ,url=item.url ,fanart="http://pelisalacarta.mimediacenter.info/fanart/enlacia.jpg") )
    itemlist.append( Item(channel=__channel__, title=item.title+" - A-Z [Completo]" ,action="completo" ,url=item.url+"/orden:nombre" ,fanart="http://pelisalacarta.mimediacenter.info/fanart/enlacia.jpg") )

    return itemlist

def etiquetas(item):
    logger.info("[enlacia.py] etiquetas")
    itemlist = []

    data = scrapertools.cache_page(item.url)
    patron = '<a href="(/tag/[^"]+)">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for path,title in matches:
        itemlist.append( Item(channel=__channel__, title=title+" - Nuevo-antiguo" ,action="listadofichas" ,url=SITE+path ,fanart="http://pelisalacarta.mimediacenter.info/fanart/enlacia.jpg", extra="ver etiquetas") )
        itemlist.append( Item(channel=__channel__, title=title+" - A-Z" ,action="listadofichas" ,url=SITE+path+"/orden:nombre" ,fanart="http://pelisalacarta.mimediacenter.info/fanart/enlacia.jpg", extra="ver etiquetas") )

    return itemlist

# Al llamarse "search" la función, el launcher pide un texto a buscar y lo añade como parámetro
def search(item,texto,categoria=""):
    logger.info("[enlacia.py] "+item.url+" search "+texto)
    itemlist = []
    url = item.url
    texto = texto.replace(" ","+")
    logger.info("categoria: "+categoria+" url: "+url)
    try:
        item.url = "http://www.enlacia.com/busqueda/%s"
        item.url = item.url % texto
        item.extra = "ver etiquetas"
        itemlist.extend(completo(item))
        return itemlist
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def listadofichas(item):
    logger.info("[enlacia.py] listadofichas")
    itemlist = []

    ### Listado ###
    data = scrapertools.cache_page(item.url)
    listado = scrapertools.get_match(data,'<h2>Listado de fichas</h2>(.*?)</div></div></div>')

    patron = '<a href="([^"]+)" class="ficha ficha2"><img src="([^"]+)" border="0" alt="([^"]+)"/>'
    patron+= '.*?<span class="categoria">([^<]+)</span>'
    matches = re.compile(patron,re.DOTALL).findall(listado)

    for path,thumbnail,title,categoria in matches:
        item_extra = item.extra
        if item.extra == "ver etiquetas": title = "[COLOR blue]"+categoria+":[/COLOR] "+title
        itemlist.append( Item(channel=__channel__, title=title , action="temporadas", url=SITE+path, thumbnail=SITE+"/"+thumbnail.replace('.jpg','_g.jpg'), fanart="http://pelisalacarta.mimediacenter.info/fanart/enlacia.jpg", show=title, extra=item_extra) )

    ### Paginación ###
    try:
        pagina_actual = scrapertools.get_match(data, '<span class="pagina pag_actual">([^<]+)</span>')
        pagina_siguiente = scrapertools.get_match(data, '<a href="([^"]+)" class="pagina pag_sig">[^<]+</a>')
        pagina_final = scrapertools.get_match(data, 'class="pagina">([^<]+)</a><a href="[^"]+" class="pagina pag_sig">')

        print "### pagina_siguiente: %s" % pagina_siguiente

        #if pagina_actual != pagina_final:
        if pagina_siguiente != "":
            if "tag/" in pagina_siguiente: pagina_siguiente = "/"+pagina_siguiente
            itemlist.append( Item(channel=__channel__, title=">> Página siguiente", action="listadofichas", url=SITE+pagina_siguiente, fanart="http://pelisalacarta.mimediacenter.info/fanart/enlacia.jpg", extra=item_extra) )
    except: pass

    return itemlist

# Pone el listado de todas las páginas juntas
def completo(item):
    logger.info("[enlacia.py] completo")
    itemlist = []

    # Guarda el valor por si son etquitas para que lo vea 'listadofichas'
    item_extra = item.extra

    # Lee las entradas
    items_programas = listadofichas(item)

    salir = False
    while not salir:

        # Saca la URL de la siguiente página
        ultimo_item = items_programas[ len(items_programas)-1 ]

        # Páginas intermedias
        if ultimo_item.action=="listadofichas":
            # Quita el elemento de "Página siguiente" 
            ultimo_item = items_programas.pop()

            # Añade las entradas de la página a la lista completa
            itemlist.extend( items_programas )
    
            # Carga la sigiuente página
            ultimo_item.extra = item_extra
            items_programas = listadofichas(ultimo_item)

        # Última página
        else:
            # Añade a la lista completa y sale
            itemlist.extend( items_programas )
            salir = True

    return itemlist

def play(item):
    logger.info("[enlacia.py] play")
    itemlist=[]
    
    # Busca el vídeo
    #data = scrapertools.cache_page(item.url)
    #videoitemlist = servertools.find_video_items(data=data)
    videoitemlist = servertools.find_video_items(data=item.url)
    i=1
    for videoitem in videoitemlist:
        if not "favicon" in videoitem.url:
            videoitem.title = "Mirror %d%s" % (i,videoitem.title)
            videoitem.fulltitle = item.fulltitle
            videoitem.channel=channel=__channel__
            videoitem.show = item.show
            itemlist.append(videoitem)
            i=i+1

    return itemlist

def temporadas(item):
    logger.info("[enlacia.py] temporadas")
    itemlist = []

    # Carga la página
    data = scrapertools.cache_page(item.url)

    if '<div class="mensaje error">No hay vídeos disponibles</div>' in data:
        itemlist.append( Item(channel=__channel__, title="No hay vídeos disponibles", folder=False) )

    elif '<div class="fficha-temporadas">' not in data:
        ### paso 1: mostrar_temporada.php ###
        id = scrapertools.get_match(data, "<script type=.text/javascript.>mostrar_temporada.'([^']+)'.;</script>")
        path = "/ajax/mostrar_temporada.php?id="+id
        data = scrapertools.cache_page(SITE+path)

        ### paso 2: mostrar_capitulo.php ###
        id = scrapertools.get_match(data, '<div id="item-([^"]+)" class="item  ">')
        path = "/ajax/mostrar_capitulo.php?id="+id
        item.url = SITE+path
        itemlist.extend( findvideos(item))

    elif '<span class="temporadas">Temporadas:</span>' not in data:
        ### paso 1: mostrar_temporada.php ###
        id = scrapertools.get_match(data, "<script type=.text/javascript.>mostrar_temporada.'([^']+)'.;</script>")
        temporada = scrapertools.get_match(data, '<span class="temporadas">([^<]+)</span>')
        path = "/ajax/mostrar_temporada.php?id="+id
        item.title = "Temporada: "+temporada
        item.url = SITE+path
        itemlist.extend( episodios(item))
    else:
        ### paso 1: mostrar_temporada.php ###
        patron = '<a id="temp-([^"]+)" class="temp" href="[^"]+">([^<]+)</a>'
        matches = re.compile(patron,re.DOTALL).findall(data)
        for id,temporada in matches:
            path = "/ajax/mostrar_temporada.php?id="+id
            if temporada == "Extra": temporada = "Temporada: 0"
            item.title = "Temporada: "+temporada
            item.url = SITE+path
            itemlist.extend( episodios(item))

    return itemlist

def episodios(item):
    logger.info("[enlacia.py] episodios")
    itemlist = []

    ### paso 2: mostrar_capitulo.php ###
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    
    patron = '<a class="nombre " href="javascript:mostrar_capitulo.([^\)]+).;">([^<]+)</a>'
    #patron = '<div id="item-([^"]+)" class="item  ">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for id,capitulo in matches:
        path = "/ajax/mostrar_capitulo.php?id="+id
        #logger.info("title="+item.title+", capitulo="+capitulo)
        #title=Temporada: Temporada 1, capitulo=Capítulo: 1

        nombre_temporada = item.title.replace("Temporada: Temporada ","")
        nombre_episodio = capitulo.replace("Capítulo: ","")
        if len(nombre_episodio)==1:
            nombre_episodio="0"+nombre_episodio
        itemlist.append( Item(channel=__channel__, title=nombre_temporada+"x"+nombre_episodio , action="findvideos", url=SITE+path, thumbnail=item.thumbnail, fanart="http://pelisalacarta.mimediacenter.info/fanart/enlacia.jpg", show=item.show) )

    return itemlist

def findvideos(item):
    logger.info("[enlacia.py] findvideos")
    itemlist = []

    ### paso 3: ver_video.php ###
    data = scrapertools.cache_page(item.url)
    patron = '<div id="vitem-([^"]+)" class="vitem">.*?'
    #patron+= '<img src="..([^"]+)" alt="Tipo enlace"/>.*?'
    patron+= '<img src="..([^"]+)" alt="Servidor"/>.*?'
    patron+= '<div class="info-idioma"><img src="/images/idiomas/(.).png" />.*?'
    patron+= '<div class="info-calidad">([^<]+)</div>'

    #Listado de servidores
    matches = re.compile(patron,re.DOTALL).findall(data)
    #for id,tipo,thumbnail,idioma_id,calidad in matches:
    for id,thumbnail,idioma_id,calidad in matches:
        path = "/ajax/ver_video.php?id_video="+id
        #tipo_id = tipo.replace('/images/tipos/','').split('.')[0]
        servidor_id = thumbnail.replace('/images/servidores/','').split('.')[0]
        #if servidor_id != "999" and servidor_id != "0":
        title = servidores(servidor_id)+" ("+idiomas(idioma_id)+") ("+calidad+")"
        #title = tipos(tipo_id)+" en "+servidores(servidor_id)+" ("+idiomas(idioma_id)+") ("+calidad+")"
        if id != "0":
            # Partes
            data = scrapertools.cache_page(SITE+path)
            patron = '<a href="([^"]+)" target="_blank">'
            matches = re.compile(patron,re.DOTALL).findall(data)
            partes = len(matches)
            i = 1
            for url in matches:
                print "### url: "+url
                parte = ""
                if partes > 1: parte = " [partes: %s/%s]" %(i,partes)
                itemlist.append( Item(channel=item.channel, title=title+parte, action="play", url=url, thumbnail=SITE+thumbnail, show=item.show, fulltitle=item.show, folder=False) )
                i = i+1

    return itemlist

def tipos(id):
    lista = {'0':'tipo desconocido', '1':'Emule', '2':'uTorrent', '3':'Descargar', '4':'Ver'}
    return lista[id]

def idiomas(id):
    lista = {'0':'idioma desconocido', '1':'Español', '2':'Latino', '3':'VOS', '4':'VO', '5':'Catalán'}
    return lista[id]

def servidores(id):
    lista = {'/images/hdsponsor':'hd', '0':'servidor desconocido', '1':'emule', '2':'bittorrent', '3':'elitetorrent', '4':'youtube', '5':'mitele', '6':'lasextaon', '7':'antena3', '8':'rapidshare', '9':'fileserve', '10':'rtvees', '11':'uploaded', '12':'mediafire', '13':'mtv', '14':'letitbit', '15':'allmyvideos', '16':'vidxden', '17':'depositfiles', '18':'bitshare', '19':'filepost', '20':'turbobit', '21':'wupload', '22':'modovideo', '23':'divxstage', '24':'oneficher', '25':'zippyshare', '26':'fooget', '27':'vk', '28':'freakshare', '29':'filedino', '30':'shareonline', '31':'putlocker', '32':'filebox', '33':'jumbofiles', '34':'shragle', '35':'stagevu', '36':'easybytez', '37':'shareflare', '38':'bulletupload', '39':'filevelocity', '40':'videobam', '41':'uploadstation', '42':'uploaz', '43':'glumbo', '44':'rapidgator', '45':'fileserving', '46':'filefactory', '47':'gigasize', '48':'refile', '49':'vimple', '50':'videoweed', '51':'veevr', '52':'vipfile', '53':'crtvg', '54':'vimeo', '55':'fiberupload', '56':'moevideos', '57':'novamov', '58':'uploading', '59':'fileflyer', '60':'nowvideo', '61':'bayfiles', '62':'piratebay', '63':'movshare', '64':'bupload', '65':'sharpfile', '66':'uploadjet', '67':'henchfile', '68':'uloadto', '69':'z47upload', '70':'muchshare', '71':'magnovideo', '72':'streamcloud', '73':'cloudzer', '74':'playedto', '75':'allbox4', '76':'mega', '77':'videomega', '78':'vidspot', '79':'nowvideo', '80':'upfiles', '81':'uploadable', '82':'streaminto', '83':'nowdownload', '84':'filemonkey', '85':'uploadable', '86':'shockshare', '87':'oleup', '999':'servidor desconocido'}
    return lista[id]

