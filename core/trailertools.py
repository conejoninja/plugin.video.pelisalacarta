# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Buscador de Trailers en youtube
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import sys
import xbmc
import string
import xbmcgui
import xbmcplugin

import gdata.youtube
import gdata.youtube.service
from servers import youtube

from platformcode.xbmc import xbmctools
from core import scrapertools
from core import logger
from core import config

import os
CHANNELNAME = "trailertools"

DEBUG = True
IMAGES_PATH = xbmc.translatePath( os.path.join( config.get_data_path(), 'resources' , 'images'  ) )

def mainlist(params,url,category):
    logger.info("[trailertools.py] mainlist")
    titulo = ""
    listavideos = GetTrailerbyKeyboard(titulo,category)
    if len(listavideos)>0:
        for video in listavideos:
            titulo = video[1]
            url        = video[0]
            thumbnail  = video[2]
            xbmctools.addnewvideo( "trailertools" , "youtubeplay" , category , "Directo" ,  titulo , url , thumbnail , "Ver Video" )
            
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )        
    
def buscartrailer(params,url,category):
    print "[trailertools.py] Modulo: buscartrailer()"
    thumbnail = ""
    solo = "false"
    videotitle = title = urllib.unquote_plus( params.get("title") ).strip()
    if ":]" in videotitle:
        solo = "true"
        videotitle = re.sub("\[[^\]]+\]","",videotitle).strip()
    if config.get_localized_string(30110) in videotitle: #"Buscar trailer para"
        videotitle = videotitle.replace(config.get_localized_string(30110),"").strip()
    if config.get_localized_string(30111) in videotitle: #"Insatisfecho?, busca otra vez : "
        videotitle = videotitle.replace(config.get_localized_string(30111),"").strip()
    
        listavideos = GetTrailerbyKeyboard(videotitle.strip(),category)
    else:
        listavideos = gettrailer(videotitle.strip().strip(),category,solo)
    
    if len(listavideos)>0:
        for video in listavideos:
            titulo = video[1]
            url        = video[0]
            thumbnail  = video[2]
            duracion = video[3]
            xbmctools.addnewvideo( "trailertools" , "youtubeplay" , category , "youtube" ,  titulo , url , thumbnail , "Ver Video","",duracion )
    
    xbmctools.addnewfolder( CHANNELNAME , "buscartrailer" , category , config.get_localized_string(30111)+" "+videotitle , url , os.path.join(IMAGES_PATH, 'trailertools.png'), "" ) #"Insatisfecho?, busca otra vez : "        
    # Propiedades
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
    
    
def GetFrom_Trailersdepeliculas(titulovideo):
    print "[trailertools.py] Modulo: GetFrom_Trailersdepeliculas(titulo = %s)"  % titulovideo
    devuelve = []

    titulo = LimpiarTitulo(titulovideo)
    # ---------------------------------------
    #  Busca el video en la pagina de www.trailerdepeliculas.org,
    #  la busqueda en esta pagina es porque a veces tiene los
    #  trailers en ingles y que no existen en español
    # ----------------------------------------
    c = 0
    url1 ="http://www.trailersdepeliculas.org/"
    url  ="http://www.trailersdepeliculas.org/buscar.html"
    urldata=getpost(url,{'busqueda': titulo})
    #logger.info("post url  :  "+urldata)
    patronvideos = "<td><h2><a href='([^']+)'>(.*?)<.*?src='([^']+)'.*?"
    matches  = re.compile(patronvideos,re.DOTALL).findall(urldata)
    if len(matches)>0:
        patronvideos = 'movie" value="http://www.youtube.com([^"]+)"'
        for match in matches:
            logger.info("Trailers encontrados en www.trailerdepeliculas.org :  "+match[1])
            if titulo in (string.lower(LimpiarTitulo(match[1]))):
                urlpage = urlparse.urljoin(url1,match[0])
                thumbnail = urlparse.urljoin(url1,match[2])
                data     = scrapertools.cachePage(urlpage)
                logger.info("Trailer elegido :  "+match[1])
                matches2 = re.compile(patronvideos,re.DOTALL).findall(data)
                for match2 in matches2:
                    logger.info("link yt del Trailer encontrado :  "+match2)
                    c=c+1
                    devuelve.append( [match2, match[1] , thumbnail,""] )
                    #scrapedthumbnail = match[2]
                    #scrapedtitle     = match[1]
                    #scrapedurl       = match[0]
            
            
        logger.info(" lista de links encontrados U "+str(len(match)))
    print '%s Trailers encontrados en Modulo: GetFrom_Trailersdepeliculas()' % str(c)
    return devuelve

def GetFromYoutubePlaylist(titulovideo):
    print "[trailertools.py] Modulo: GetFromYoutubePlaylist(titulo = %s)"  % titulovideo
    devuelve = []    
    #
    # ---------------------------------------
    #  Busca el video en las listas de youtube
    # ---------------------------------------
    c = 0
    #http://www.youtube.com/results?search_type=search_playlists&search_query=luna+nueva+trailer&uni=1
    for i in ["+trailer+espa%C3%B1ol","+trailer"]:
        listyoutubeurl  = "http://www.youtube.com/results?search_type=search_playlists&search_query="
        listyoutubeurl += titulovideo.replace(" ","+")+i+"&uni=1"
        listyoutubeurl = listyoutubeurl.replace(" ","")
        logger.info("Youtube url parametros de busqueda  :"+listyoutubeurl)
        data = scrapertools.cachePage(listyoutubeurl)

        thumbnail=""
        patronyoutube  = '<span><a class="hLink" title="(.*?)" href="(.*?)">.*?'
        #patronyoutube += '<span class="playlist-video-duration">(.*?)</span>'
        matches  = re.compile(patronyoutube,re.DOTALL).findall(data)
        if len(matches)>0:
            for match in matches:
                logger.info("Trailer Titulo encontrado :"+match[0])
                logger.info("Trailer Url    encontrado :"+match[1])
                logger.info("Trailer Titulo Recortado  :"+string.lower(LimpiarTitulo(match[0])))
                if (titulovideo) in (string.lower(LimpiarTitulo(match[0]))):
                    campo = match[1]
                    longitud = len(campo)
                    campo = campo[-11:]
                    logger.info("codigo del video :  "+campo)
                    scrapedurl = "http://www.youtube.com/watch?v="+campo
                    patron    = "(http\:\/\/i[^/]+/vi/"+campo+"/default.jpg)"
                    matches2  = re.compile(patron,re.DOTALL).findall(data)
                    if len(matches2)>0:
                        thumbnail = matches2[0]
                    c = c + 1
                    logger.info("Trailer elegido :  "+match[1])
                    devuelve.append( [scrapedurl, match[0] , thumbnail,""] )
                    #scrapedthumbnail = thumbnail
                    #scrapedtitle     = match[0]
                    #scrapedurl       = match[1]
                    if c == 6 :
                        break
            #logger.info(" Total de links encontrados U "+str(len(match)))
        if c == 6:break
    print '%s Trailers encontrados en Modulo: GetFromYoutubePlaylist()' % str(c)
    return devuelve

def gettrailer(titulovideo,category,solo="false"):

    print "[trailertools.py] Modulo: gettrailer(titulo = %s , category = %s)"  % (titulovideo,category)

    if not solo=="true":
        titulo = re.sub('\([^\)]+\)','',titulovideo)
        titulo = title = re.sub('\[[^\]]+\]','',titulo)

        sopa_palabras_invalidas = ("dvdrip" ,  "dvdscreener2" ,"tsscreener" , "latino" ,     # Esto es para peliculasyonkis o parecidos
                                   "dvdrip1",  "dvdscreener"  ,"tsscreener1", "latino1",
                                   "latino2",  "dvdscreener1" ,"screener"    ,
                                   "mirror" ,  "megavideo"    ,"vose"        , "subtitulada"
                                   )
                                   
        titulo = LimpiarTitulo(titulo)
        print "el tituloooo es :%s" %titulo
        
        trozeado = titulo.split()
        for trozo in trozeado:
            if trozo in sopa_palabras_invalidas:
                titulo = titulo.replace(trozo ,"")
        titulo = re.sub(' $','',titulo)
        titulo = titulo.replace("ver pelicula online vos","").strip()
        titulo = titulo.replace("ver pelicula online","").strip()
        titulo = titulo.replace("mirror 1","").strip()
        titulo = titulo.replace("parte 1","").strip()
        titulo = titulo.replace("part 1","").strip()
        titulo = titulo.replace("pt 1","").strip()        
        titulo = titulo.replace("peliculas online","").strip()
        encontrados = []
        if len(titulo)==0:
            titulo = "El_video_no_tiene_titulo"

        encontrados = GetFrom_Trailersdepeliculas(titulo)      # Primero busca en www.trailerdepeliculas.org
        encontrados  = encontrados + GetVideoFeed(titulo)      # luego busca con el API de youtube 
    else:
        titulo = titulovideo
        encontrados = []
        if len(titulo)==0:
            titulo = "El_video_no_tiene_titulo"
        encontrados  = encontrados + GetVideoFeed(titulo,"true")
    if len(encontrados)>0:                                   # si encuentra algo, termina
        return encontrados
    else:
        encontrados = GetFromYoutubePlaylist(titulo)       # si no encuentra, busca en las listas de la web de youtube
        if len(encontrados)>0:
            return encontrados
        else:
            respuesta = alertnoencontrado(titulo)          # si aun no encuentra,lanza mensaje de alerta y pregunta si quiere 
            if respuesta:                                  # buscar, modificando el titulo, con el teclado 
                encontrados = GetTrailerbyKeyboard(titulo,category) # si respuesta es afirmativa este entrara en un bucle 
                if len(encontrados)>0:                       # de autollamadas hasta encontrar el trailer o la respuesta 
                    return encontrados                       # del mensaje alerta sea negativo.
                else:return []
            else:
                xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
                xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
    
    return encontrados

def GetTrailerbyKeyboard(titulo,category,solo="false"):
    print "[trailertools.py] Modulo: GetTrailerbyKeyboard(titulo = %s , category = %s)"  % (titulo,category)
    devuelve = []
    keyboard = xbmc.Keyboard('default','heading')
    keyboard.setDefault(titulo)
    if titulo == "":
        keyboard.setHeading(config.get_localized_string(30112)) #"Introduce el Titulo a buscar"
    else:
        keyboard.setHeading(config.get_localized_string(30113)) #'Puedes recortar el titulo ó bien cambiar a otro idioma'
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        tecleado = keyboard.getText()
        if len(tecleado)>0:
            devuelve = gettrailer(tecleado,category,solo)
            return devuelve
        else:return []
    else:return []    

def alertnoencontrado(titulo):
    advertencia = xbmcgui.Dialog()
    #'Trailer no encontrado'
    #'El Trailer para "%s"'
    #'no se ha podido localizar.'
    #'¿Deseas seguir buscando con el teclado?'
    tituloq = '"'+titulo+'"'
    resultado = advertencia.yesno(config.get_localized_string(30114), config.get_localized_string(30115) % tituloq, config.get_localized_string(30116),config.get_localized_string(30117))
    return(resultado)
def LimpiarTitulo(title):
        title = string.lower(title)
        #title = re.sub('\([^\)]+\)','',title)
        title = re.sub(' $','',title)
        title = title.replace("Ã‚Â", "")
        title = title.replace("ÃƒÂ©","e")
        title = title.replace("ÃƒÂ¡","a")
        title = title.replace("ÃƒÂ³","o")
        title = title.replace("ÃƒÂº","u")
        title = title.replace("ÃƒÂ­","i")
        title = title.replace("ÃƒÂ±","ñ")
        title = title.replace("Ã¢â‚¬Â", "")
        title = title.replace("Ã¢â‚¬Å“Ã‚Â", "")
        title = title.replace("Ã¢â‚¬Å“","")
        title = title.replace("Ã©","e")
        title = title.replace("Ã¡","a")
        title = title.replace("Ã³","o")
        title = title.replace("Ãº","u")
        title = title.replace("Ã­","i")
        title = title.replace("Ã±","ñ")
        title = title.replace("Ãƒâ€œ","O")
        title = title.replace("@","")
        title = title.replace("é","e")
        title = title.replace("á","a")
        title = title.replace("ó","o")
        title = title.replace("ú","u")
        title = title.replace("í","i")
        title = title.replace('ñ','n')
        title = title.replace('Á','a')
        title = title.replace('É','e')
        title = title.replace('Í','i')
        title = title.replace('Ó','o')
        title = title.replace('Ú','u')
        title = title.replace('Ñ','n')
        title = title.replace(":"," ")
        title = title.replace("&","")
        title = title.replace('#','')
        title = title.replace('-','')
        title = title.replace('?','')
        title = title.replace('¿','')
        title = title.replace(",","")
        title = title.replace("*","")
        title = title.replace("\\","")
        title = title.replace("/","")
        title = title.replace("'","")
        title = title.replace('"','')
        title = title.replace("<","")
        title = title.replace(">","")
        title = title.replace(".","")
        title = title.replace("_"," ")
        title = title.replace("\("," ")
        title = title.replace("\)"," ")
        title = title.replace('|','')
        title = title.replace('!','')
        title = title.replace('¡','')
        title = title.replace("  "," ")
        title = title.replace("\Z  ","")
        return(title)

def getpost(url,values): # Descarga la pagina con envio de un Form
    
    #url=url
    try:
        data = urllib.urlencode(values)          
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        the_page = response.read() 
        return the_page 
    except Exception: 
        return "Err " 
####################################################################################################
# Buscador de Trailer : mediante el servicio de Apis de Google y Youtube                           #
####################################################################################################

# Show first 50 videos from YouTube that matches a search string
def youtube_search(texto):
    devuelve = []

    # Fetch video list from YouTube feed
    data = scrapertools.cache_page( "https://gdata.youtube.com/feeds/api/videos?q="+texto.replace(" ","+")+"&orderby=published&start-index=1&max-results=50&v=2&lr=es" )
    
    # Extract items from feed
    matches = re.compile("<entry(.*?)</entry>",re.DOTALL).findall(data)

    for entry in matches:
        logger.info("entry="+entry)
        # Not the better way to parse XML, but clean and easy
        title = scrapertools.get_match(entry,"<titl[^>]+>([^<]+)</title>")
        thumbnail = scrapertools.get_match(entry,"<media\:thumbnail url='([^']+)'")
        try:
            url = scrapertools.get_match(entry,"http\://www.youtube.com/watch\?v\=([0-9A-Za-z_-]{11})")
        except:
            url = scrapertools.get_match(entry,"https\://www.youtube.com/watch\?v\=([0-9A-Za-z_-]{11})")

        devuelve.append( [ title,thumbnail,url ] )

    return devuelve

def GetVideoFeed(titulo,solo="false"):
    print "[trailertools.py] Modulo: GetVideoFeed(titulo = %s)"  % titulo
    if solo=="true":
        esp   = ""
        noesp = ""
    else:
        esp   = " trailer espanol"
        noesp = " trailer"
    devuelve = []
    encontrados = set()
    c = 0
    entries = youtube_search(titulo+esp)
    
    for title,thumbnail,url in entries:
        print 'Video title: %s' % title
        titulo2 = title
        url = url
        duracion = ""
        if titulo in (string.lower(LimpiarTitulo(titulo2))): 
            if url not in encontrados:
                devuelve.append([url,titulo2,thumbnail,""])
                encontrados.add(url)
                c = c + 1
            if c > 10:
                return (devuelve)

    if c < 6:
        entries = youtube_search(titulo+esp)
        for title,thumbnail,url in entries:
            print 'Video title: %s' % title
            titulo2 = title
            url = url
            duracion = ""
            if titulo in (string.lower(LimpiarTitulo(titulo2))): 
                if url not in encontrados:
                    devuelve.append([url,titulo2,thumbnail,""])
                    encontrados.add(url)
                    c = c + 1
                if c > 10:
                    return (devuelve)
    if c < 6:
        entries = youtube_search(titulo)
        for title,thumbnail,url in entries:
            print 'Video title: %s' % title
            titulo2 = title
            url = url
            duracion = ""
            if titulo in (string.lower(LimpiarTitulo(titulo2))): 
                if url not in encontrados:
                    devuelve.append([url,titulo2,thumbnail,""])
                    encontrados.add(url)
                    c = c + 1
                if c > 10:
                    return (devuelve)

    print '%s Trailers encontrados en Modulo: GetVideoFeed()' % str(c)
    return (devuelve)
    
def youtubeplay(params,url,category):
    logger.info("[trailertools.py] youtubeplay")
    #http://www.youtube.com/watch?v=byvXidWNf2A&feature=youtube_gdata
    title = urllib.unquote_plus( params.get("title") )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    plot = "Ver Video"
    server = "youtube"
    #id = youtube.Extract_id(url)
    #videourl = youtube.geturl(id)

    xbmctools.play_video("Trailer",server,url,category,title,thumbnail,plot)

    
def alertaerror():
    ventana = xbmcgui.Dialog()
    ok= ventana.ok ("Plugin Pelisalacarta", "Uuppss...la calidad elegida en configuracion",'no esta disponible o es muy baja',"elijá otra calidad distinta y vuelva a probar")

