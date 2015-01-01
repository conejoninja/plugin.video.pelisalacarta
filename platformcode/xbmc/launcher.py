# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta
# XBMC Launcher (xbmc / xbmc-dharma / boxee)
# http://blog.tvalacarta.info/plugin-xbmc/
#------------------------------------------------------------

import urllib, urllib2
import os,sys

from core import logger
from core import config
from core import scrapertools

PLUGIN_NAME = "pelisalacarta"

def run():
    logger.info("[launcher.py] run")
    
    # Test if all the required directories are created
    config.verify_directories_created()
    
    # Extract parameters from sys.argv
    params, fanart, channel_name, title, fulltitle, url, thumbnail, plot, action, server, extra, subtitle, viewmode, category, show, password = extract_parameters()
    logger.info("[launcher.py] fanart=%s, channel_name=%s, title=%s, fulltitle=%s, url=%s, thumbnail=%s, plot=%s, action=%s, server=%s, extra=%s, subtitle=%s, category=%s, show=%s, password=%s" % (fanart, channel_name, title, fulltitle, url, thumbnail, plot, action, server, extra, subtitle, category, show, password))

    try:
        # Accion por defecto - elegir canal
        if ( action=="selectchannel" ):
            # Borra el fichero de las cookies para evitar problemas con MV
            #ficherocookies = os.path.join( config.get_data_path(), 'cookies.lwp' )
            #if os.path.exists(ficherocookies):
            #    os.remove(ficherocookies)
            
            if config.get_setting("updatechannels")=="true":
                try:
                    from core import updater
                    actualizado = updater.updatechannel("channelselector")

                    if actualizado:
                        import xbmcgui
                        advertencia = xbmcgui.Dialog()
                        advertencia.ok("tvalacarta",config.get_localized_string(30064))
                except:
                    pass

            import channelselector as plugin
            plugin.mainlist(params, url, category)

        # Actualizar version
        elif ( action=="update" ):
            try:
                from core import updater
                updater.update(params)
            except ImportError:
                logger.info("[launcher.py] Actualizacion automática desactivada")

            #import channelselector as plugin
            #plugin.listchannels(params, url, category)
            if config.get_system_platform()!="xbox":
                import xbmc
                xbmc.executebuiltin( "Container.Refresh" )

        elif (action=="channeltypes"):
            import channelselector as plugin
            plugin.channeltypes(params,url,category)

        elif (action=="listchannels"):
            import channelselector as plugin
            plugin.listchannels(params,url,category)

        # El resto de acciones vienen en el parámetro "action", y el canal en el parámetro "channel"
        else:
            if action=="mainlist" and config.get_setting("updatechannels")=="true":
                try:
                    from core import updater
                    actualizado = updater.updatechannel(channel_name)

                    if actualizado:
                        import xbmcgui
                        advertencia = xbmcgui.Dialog()
                        advertencia.ok("plugin",channel_name,config.get_localized_string(30063))
                except:
                    pass

            # La acción puede estar en el core, o ser un canal regular. El buscador es un canal especial que está en pelisalacarta
            regular_channel_path = os.path.join( config.get_runtime_path(), PLUGIN_NAME , 'channels' , channel_name+".py" )
            core_channel_path = os.path.join( config.get_runtime_path(), 'core' , channel_name+".py" )
            logger.info("[launcher.py] regular_channel_path=%s" % regular_channel_path)
            logger.info("[launcher.py] core_channel_path=%s" % core_channel_path)

            if channel_name=="buscador":
                import pelisalacarta.buscador as channel
            if channel_name=="personal" or channel_name=="personal2" or channel_name=="personal3" or channel_name=="personal4" or channel_name=="personal5":
                import pelisalacarta.channels.personal as channel
            elif os.path.exists( regular_channel_path ):
                exec "import pelisalacarta.channels."+channel_name+" as channel"
            elif os.path.exists( regular_channel_path ):
                exec "import tvalacarta.channels."+channel_name+" as channel"
            elif os.path.exists( core_channel_path ):
                exec "from core import "+channel_name+" as channel"

            logger.info("[launcher.py] running channel %s %s" % (channel.__name__ , channel.__file__))

            generico = False
            # Esto lo he puesto asi porque el buscador puede ser generico o normal, esto estará asi hasta que todos los canales sean genericos 
            if category == "Buscador_Generico":
                generico = True
            else:
                try:
                    generico = channel.isGeneric()
                except:
                    generico = False

            if not generico:
                logger.info("[launcher.py] xbmc native channel")
                if (action=="strm"):
                    from platformcode.xbmc import xbmctools
                    xbmctools.playstrm(params, url, category)
                else:
                    exec "channel."+action+"(params, url, category)"
            else:            
                logger.info("[launcher.py] multiplatform channel")
                from core.item import Item
                item = Item(channel=channel_name, title=title , fulltitle=fulltitle, url=url, thumbnail=thumbnail , plot=plot , server=server, category=category, extra=extra, subtitle=subtitle, viewmode=viewmode, show=show, password=password, fanart=fanart)
                
                '''
                if item.subtitle!="":
                    logger.info("[launcher.py] Downloading subtitle file "+item.subtitle)
                    from core import downloadtools
                    
                    ficherosubtitulo = os.path.join( config.get_data_path() , "subtitulo.srt" )
                    if os.path.exists(ficherosubtitulo):
                        os.remove(ficherosubtitulo)

                    downloadtools.downloadfile(item.subtitle, ficherosubtitulo )
                    config.set_setting("subtitulo","true")
                else:
                    logger.info("[launcher.py] No subtitle")
                '''
                from platformcode.xbmc import xbmctools

                if action=="play":
                    logger.info("[launcher.py] play")
                    # Si el canal tiene una acción "play" tiene prioridad
                    if hasattr(channel, 'play'):
                        logger.info("[launcher.py] executing channel 'play' method")
                        itemlist = channel.play(item)
                        if len(itemlist)>0:
                            item = itemlist[0]
                            xbmctools.play_video(channel=channel_name, server=item.server, url=item.url, category=item.category, title=item.title, thumbnail=item.thumbnail, plot=item.plot, extra=item.extra, subtitle=item.subtitle, video_password = item.password, fulltitle=item.fulltitle, Serie=item.show)
                        else:
                            import xbmcgui
                            ventana_error = xbmcgui.Dialog()
                            ok = ventana_error.ok ("plugin", "No hay nada para reproducir")
                    else:
                        logger.info("[launcher.py] no channel 'play' method, executing core method")
                        xbmctools.play_video(channel=channel_name, server=item.server, url=item.url, category=item.category, title=item.title, thumbnail=item.thumbnail, plot=item.plot, extra=item.extra, subtitle=item.subtitle, video_password = item.password, fulltitle=item.fulltitle, Serie=item.show)

                elif action=="strm_detail" or action=="play_from_library":
                    logger.info("[launcher.py] play_from_library")

                    fulltitle = item.show + " " + item.title
                    elegido = Item(url="")                    

                    logger.info("item.server=#"+item.server+"#")
                    # Ejecuta find_videos, del canal o común
                    try:
                        itemlist = channel.findvideos(item)
                    except:
                        from servers import servertools
                        itemlist = servertools.find_video_items(item)

                    if len(itemlist)>0:
                        #for item2 in itemlist:
                        #    logger.info(item2.title+" "+item2.subtitle)
    
                        # El usuario elige el mirror
                        opciones = []
                        for item in itemlist:
                            opciones.append(item.title)
                    
                        import xbmcgui
                        dia = xbmcgui.Dialog()
                        seleccion = dia.select(config.get_localized_string(30163), opciones)
                        elegido = itemlist[seleccion]
    
                        if seleccion==-1:
                            return
                    else:
                        elegido = item
                
                    # Ejecuta el método play del canal, si lo hay
                    try:
                        itemlist = channel.play(elegido)
                        item = itemlist[0]
                    except:
                        item = elegido
                    logger.info("Elegido %s (sub %s)" % (item.title,item.subtitle))
                    
                    from platformcode.xbmc import xbmctools
                    logger.info("subtitle="+item.subtitle)
                    xbmctools.play_video(strmfile=True, channel=item.channel, server=item.server, url=item.url, category=item.category, title=item.title, thumbnail=item.thumbnail, plot=item.plot, extra=item.extra, subtitle=item.subtitle, video_password = item.password, fulltitle=fulltitle)

                elif action=="add_pelicula_to_library":
                    logger.info("[launcher.py] add_pelicula_to_library")
                    from platformcode.xbmc import library
                    # Obtiene el listado desde el que se llamó
                    library.savelibrary( titulo=item.fulltitle , url=item.url , thumbnail=item.thumbnail , server=item.server , plot=item.plot , canal=item.channel , category="Cine" , Serie=item.show.strip() , verbose=False, accion="play_from_library", pedirnombre=False, subtitle=item.subtitle )

                elif action=="add_serie_to_library":
                    logger.info("[launcher.py] add_serie_to_library, show=#"+item.show+"#")
                    from platformcode.xbmc import library
                    import xbmcgui
                
                    # Obtiene el listado desde el que se llamó
                    action = item.extra
                    
                    # Esta marca es porque el item tiene algo más aparte en el atributo "extra"
                    if "###" in item.extra:
                        action = item.extra.split("###")[0]
                        item.extra = item.extra.split("###")[1]

                    exec "itemlist = channel."+action+"(item)"

                    # Progreso
                    pDialog = xbmcgui.DialogProgress()
                    ret = pDialog.create('pelisalacarta', 'Añadiendo episodios...')
                    pDialog.update(0, 'Añadiendo episodio...')
                    totalepisodes = len(itemlist)
                    logger.info ("[launcher.py] Total Episodios:"+str(totalepisodes))
                    i = 0
                    errores = 0
                    nuevos = 0
                    for item in itemlist:
                        i = i + 1
                        pDialog.update(i*100/totalepisodes, 'Añadiendo episodio...',item.title)
                        logger.info("[launcher.py] add_serie_to_library, title="+item.title)
                        if (pDialog.iscanceled()):
                            return
                
                        try:
                            #(titulo="",url="",thumbnail="",server="",plot="",canal="",category="Cine",Serie="",verbose=True,accion="strm",pedirnombre=True):
                            # Añade todos menos el que dice "Añadir esta serie..." o "Descargar esta serie..."
                            if item.action!="add_serie_to_library" and item.action!="download_all_episodes":
                                nuevos = nuevos + library.savelibrary( titulo=item.title , url=item.url , thumbnail=item.thumbnail , server=item.server , plot=item.plot , canal=item.channel , category="Series" , Serie=item.show.strip() , verbose=False, accion="play_from_library", pedirnombre=False, subtitle=item.subtitle, extra=item.extra )
                        except IOError:
                            import sys
                            for line in sys.exc_info():
                                logger.error( "%s" % line )
                            logger.info("[launcher.py]Error al grabar el archivo "+item.title)
                            errores = errores + 1
                        
                    pDialog.close()
                    
                    # Actualizacion de la biblioteca
                    itemlist=[]
                    if errores > 0:
                        itemlist.append(Item(title="ERROR, la serie NO se ha añadido a la biblioteca o lo ha hecho incompleta"))
                        logger.info ("[launcher.py] No se pudo añadir "+str(errores)+" episodios")
                    else:
                        itemlist.append(Item(title="La serie se ha añadido a la biblioteca"))
                        logger.info ("[launcher.py] Ningún error al añadir "+str(errores)+" episodios")
                    
                    # FIXME:jesus Comentado porque no funciona bien en todas las versiones de XBMC
                    #library.update(totalepisodes,errores,nuevos)
                    xbmctools.renderItems(itemlist, params, url, category)
                    
                    #Lista con series para actualizar
                    nombre_fichero_config_canal = os.path.join( config.get_library_path() , "series.xml" )
                    if not os.path.exists(nombre_fichero_config_canal):
                        nombre_fichero_config_canal = os.path.join( config.get_data_path() , "series.xml" )

                    logger.info("nombre_fichero_config_canal="+nombre_fichero_config_canal)
                    if not os.path.exists(nombre_fichero_config_canal):
                        f = open( nombre_fichero_config_canal , "w" )
                    else:
                        f = open( nombre_fichero_config_canal , "r" )
                        contenido = f.read()
                        f.close()
                        f = open( nombre_fichero_config_canal , "w" )
                        f.write(contenido)
                    from platformcode.xbmc import library
                    f.write( library.title_to_folder_name(item.show)+","+item.url+","+item.channel+"\n")
                    f.close();

                elif action=="download_all_episodes":
                    download_all_episodes(item,channel)

                elif action=="search":
                    logger.info("[launcher.py] search")
                    import xbmc
                    keyboard = xbmc.Keyboard("")
                    keyboard.doModal()
                    if (keyboard.isConfirmed()):
                        tecleado = keyboard.getText()
                        tecleado = tecleado.replace(" ", "+")
                        itemlist = channel.search(item,tecleado)
                    else:
                        itemlist = []
                    xbmctools.renderItems(itemlist, params, url, category)

                else:
                    logger.info("[launcher.py] executing channel '"+action+"' method")
                    if action!="findvideos":
                        exec "itemlist = channel."+action+"(item)"
                            
                        #for item in itemlist:
                        #    logger.info("viemode="+item.viewmode)
                    else:

                        # Intenta ejecutar una posible funcion "findvideos" del canal
                        if hasattr(channel, 'findvideos'):
                            exec "itemlist = channel."+action+"(item)"
                        # Si no funciona, lanza el método genérico para detectar vídeos
                        else:
                            logger.info("[launcher.py] no channel 'findvideos' method, executing core method")
                            from servers import servertools
                            itemlist = servertools.find_video_items(item)

                        from core import subtitletools
                        subtitletools.saveSubtitleName(item)

                    # Activa el modo biblioteca para todos los canales genéricos, para que se vea el argumento
                    import xbmcplugin
                    import sys
                    handle = sys.argv[1]
                    xbmcplugin.setContent(int( handle ),"movies")
                    
                    # Añade los items a la lista de XBMC
                    xbmctools.renderItems(itemlist, params, url, category)

    except urllib2.URLError,e:
        import traceback,sys
        from pprint import pprint
        exc_type, exc_value, exc_tb = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_tb)
        for line in lines:
            line_splits = line.split("\n")
            for line_split in line_splits:
                logger.error(line_split)

        import xbmcgui
        ventana_error = xbmcgui.Dialog()
        # Agarra los errores surgidos localmente enviados por las librerias internas
        if hasattr(e, 'reason'):
            logger.info("Razon del error, codigo: %d , Razon: %s" %(e.reason[0],e.reason[1]))
            texto = config.get_localized_string(30050) # "No se puede conectar con el sitio web"
            ok = ventana_error.ok ("plugin", texto)
        # Agarra los errores con codigo de respuesta del servidor externo solicitado     
        elif hasattr(e,'code'):
            logger.info("codigo de error HTTP : %d" %e.code)
            texto = (config.get_localized_string(30051) % e.code) # "El sitio web no funciona correctamente (error http %d)"
            ok = ventana_error.ok ("plugin", texto)    

# Parse XBMC params - based on script.module.parsedom addon    
def get_params():
    logger.info("get_params")
    
    param_string = sys.argv[2]
    
    logger.info("get_params "+str(param_string))
    
    commands = {}

    if param_string:
        split_commands = param_string[param_string.find('?') + 1:].split('&')
    
        for command in split_commands:
            logger.info("get_params command="+str(command))
            if len(command) > 0:
                if "=" in command:
                    split_command = command.split('=')
                    key = split_command[0]
                    value = split_command[1] #urllib.unquote_plus()
                    commands[key] = value
                else:
                    commands[command] = ""
    
    logger.info("get_params "+repr(commands))
    return commands

# Extract parameters from sys.argv
def extract_parameters():
    logger.info("[launcher.py] extract_parameters")
    #Imprime en el log los parámetros de entrada
    logger.info("[launcher.py] sys.argv=%s" % str(sys.argv))
    
    # Crea el diccionario de parametros
    #params = dict()
    #if len(sys.argv)>=2 and len(sys.argv[2])>0:
    #    params = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
    params = get_params()
    logger.info("[launcher.py] params=%s" % str(params))

    if (params.has_key("channel")):
        channel = urllib.unquote_plus( params.get("channel") )
    else:
        channel=''
    
    # Extrae la url de la página
    if (params.has_key("url")):
        url = urllib.unquote_plus( params.get("url") )
    else:
        url=''

    # Extrae la accion
    if (params.has_key("action")):
        action = params.get("action")
    else:
        action = "selectchannel"

    # Extrae el server
    if (params.has_key("server")):
        server = params.get("server")
    else:
        server = ""

    # Extrae la categoria
    if (params.has_key("category")):
        category = urllib.unquote_plus( params.get("category") )
    else:
        if params.has_key("channel"):
            category = params.get("channel")
        else:
            category = ""
            
    # Extrae el título de la serie
    if (params.has_key("show")):
        show = params.get("show")
    else:
        show = ""

    # Extrae el título del video
    if params.has_key("title"):
        title = urllib.unquote_plus( params.get("title") )
    else:
        title = ""

    # Extrae el título del video
    if params.has_key("fulltitle"):
        fulltitle = urllib.unquote_plus( params.get("fulltitle") )
    else:
        fulltitle = ""

    if params.has_key("thumbnail"):
        thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    else:
        thumbnail = ""

    if params.has_key("fanart"):                                                                                                                                                
        fanart = urllib.unquote_plus( params.get("fanart") )                                                                                                                  
    else:                                                                                                                                                                         
        fanart = ""  

    if params.has_key("plot"):
        plot = urllib.unquote_plus( params.get("plot") )
    else:
        plot = ""

    if params.has_key("extradata"):
        extra = urllib.unquote_plus( params.get("extradata") )
    else:
        extra = ""

    if params.has_key("subtitle"):
        subtitle = urllib.unquote_plus( params.get("subtitle") )
    else:
        subtitle = ""

    if params.has_key("viewmode"):
        viewmode = urllib.unquote_plus( params.get("viewmode") )
    else:
        viewmode = ""

    if params.has_key("password"):
        password = urllib.unquote_plus( params.get("password") )
    else:
        password = ""

    if params.has_key("show"):
        show = urllib.unquote_plus( params.get("show") )
    else:
        if params.has_key("Serie"):
            show = urllib.unquote_plus( params.get("Serie") )
        else:
            show = ""

    return params, fanart, channel, title, fulltitle, url, thumbnail, plot, action, server, extra, subtitle, viewmode, category, show, password

def episodio_ya_descargado(show_title,episode_title):

    ficheros = os.listdir( "." )

    for fichero in ficheros:
        #logger.info("fichero="+fichero)
        if fichero.lower().startswith(show_title.lower()) and scrapertools.find_single_match(fichero,"(\d+x\d+)")==episode_title:
            logger.info("encontrado!")
            return True

    return False

def download_all_episodes(item,channel,first_episode="",preferred_server="vidspot",filter_language=""):
    logger.info("[launcher.py] download_all_episodes, show="+item.show)
    show_title = item.show

    # Obtiene el listado desde el que se llamó
    action = item.extra

    # Esta marca es porque el item tiene algo más aparte en el atributo "extra"
    if "###" in item.extra:
        action = item.extra.split("###")[0]
        item.extra = item.extra.split("###")[1]

    exec "episode_itemlist = channel."+action+"(item)"

    # Ordena los episodios para que funcione el filtro de first_episode
    episode_itemlist = sorted(episode_itemlist, key=lambda Item: Item.title) 

    from servers import servertools
    from core import downloadtools
    from core import scrapertools

    best_server = preferred_server
    worst_server = "moevideos"

    # Para cada episodio
    if first_episode=="":
        empezar = True
    else:
        empezar = False

    for episode_item in episode_itemlist:
        try:
            logger.info("[launcher.py] download_all_episodes, episode="+episode_item.title)
            episode_title = scrapertools.get_match(episode_item.title,"(\d+x\d+)")
            logger.info("[launcher.py] download_all_episodes, episode="+episode_title)
        except:
            import traceback
            logger.info(traceback.format_exc())
            continue

        if first_episode!="" and episode_title==first_episode:
            empezar = True

        if episodio_ya_descargado(show_title,episode_title):
            continue

        if not empezar:
            continue

        # Extrae los mirrors
        try:
            mirrors_itemlist = channel.findvideos(episode_item)
        except:
            mirrors_itemlist = servertools.find_video_items(episode_item)
        print mirrors_itemlist

        descargado = False

        new_mirror_itemlist_1 = []
        new_mirror_itemlist_2 = []
        new_mirror_itemlist_3 = []
        new_mirror_itemlist_4 = []
        new_mirror_itemlist_5 = []
        new_mirror_itemlist_6 = []

        for mirror_item in mirrors_itemlist:
            
            # Si está en español va al principio, si no va al final
            if "(Español)" in mirror_item.title:
                if best_server in mirror_item.title.lower():
                    new_mirror_itemlist_1.append(mirror_item)
                else:
                    new_mirror_itemlist_2.append(mirror_item)
            elif "(Latino)" in mirror_item.title:
                if best_server in mirror_item.title.lower():
                    new_mirror_itemlist_3.append(mirror_item)
                else:
                    new_mirror_itemlist_4.append(mirror_item)
            elif "(VOS)" in mirror_item.title:
                if best_server in mirror_item.title.lower():
                    new_mirror_itemlist_3.append(mirror_item)
                else:
                    new_mirror_itemlist_4.append(mirror_item)
            else:
                if best_server in mirror_item.title.lower():
                    new_mirror_itemlist_5.append(mirror_item)
                else:
                    new_mirror_itemlist_6.append(mirror_item)

        mirrors_itemlist = new_mirror_itemlist_1 + new_mirror_itemlist_2 + new_mirror_itemlist_3 + new_mirror_itemlist_4 + new_mirror_itemlist_5 + new_mirror_itemlist_6

        for mirror_item in mirrors_itemlist:
            logger.info("[launcher.py] download_all_episodes, mirror="+mirror_item.title)

            if "(Español)" in mirror_item.title:
                idioma="(Español)"
                codigo_idioma="es"
            elif "(Latino)" in mirror_item.title:
                idioma="(Latino)"
                codigo_idioma="lat"
            elif "(VOS)" in mirror_item.title:
                idioma="(VOS)"
                codigo_idioma="vos"
            elif "(VO)" in mirror_item.title:
                idioma="(VO)"
                codigo_idioma="vo"
            else:
                idioma="(Desconocido)"
                codigo_idioma="desconocido"

            logger.info("[launcher.py] filter_language=#"+filter_language+"#, codigo_idioma=#"+codigo_idioma+"#")
            if filter_language=="" or (filter_language!="" and filter_language==codigo_idioma):
                logger.info("[launcher.py] download_all_episodes, downloading mirror")
            else:
                logger.info("[launcher.py] language "+codigo_idioma+" filtered, skipping")
                continue

            if hasattr(channel, 'play'):
                video_items = channel.play(mirror_item)
            else:
                video_items = [mirror_item]

            if len(video_items)>0:
                video_item = video_items[0]

                # Comprueba que esté disponible
                video_urls, puedes, motivo = servertools.resolve_video_urls_for_playing( video_item.server , video_item.url , video_password="" , muestra_dialogo=False)

                # Lo añade a la lista de descargas
                if puedes:
                    logger.info("[launcher.py] download_all_episodes, downloading mirror started...")
                    # El vídeo de más calidad es el último
                    mediaurl = video_urls[len(video_urls)-1][1]
                    devuelve = downloadtools.downloadbest(video_urls,show_title+" "+episode_title+" "+idioma+" ["+video_item.server+"]",continuar=False)

                    if devuelve==0:
                        logger.info("[launcher.py] download_all_episodes, download ok")
                        descargado = True
                        break
                    elif devuelve==-1:
                        try:
                            import xbmcgui
                            advertencia = xbmcgui.Dialog()
                            resultado = advertencia.ok("plugin" , "Descarga abortada")
                        except:
                            pass
                        return
                    else:
                        logger.info("[launcher.py] download_all_episodes, download error, try another mirror")
                        continue

                else:
                    logger.info("[launcher.py] download_all_episodes, downloading mirror not available... trying next")

        if not descargado:
            logger.info("[launcher.py] download_all_episodes, EPISODIO NO DESCARGADO "+episode_title)

