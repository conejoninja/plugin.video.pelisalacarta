# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Utilidades para detectar vídeos de los diferentes conectores
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
#LvX Edited Patched
import re,sys

from core import scrapertools
from core import config
from core import logger

# Listas de servidores empleadas a la hora de reproducir para explicarle al usuario por qué no puede ver un vídeo

# Lista de los servidores que se pueden ver sin cuenta premium de ningún tipo
FREE_SERVERS = []
FREE_SERVERS.extend(['directo','allmyvideos','adnstream','bliptv','divxstage','facebook','fourshared', 'hulkshare', 'twitvid'])
FREE_SERVERS.extend(['googlevideo','gigabyteupload','mediafire','moevideos','movshare','novamov']) #,'putlocker'
FREE_SERVERS.extend(['royalvids','sockshare','stagevu','tutv','userporn','veoh','videobam'])
FREE_SERVERS.extend(['vidbux','videoweed','vimeo','vk','watchfreeinhd','youtube'])#,'videobeer','nowdownload'
FREE_SERVERS.extend(['jumbofiles','nowvideo','streamcloud', 'zinwa', 'dailymotion','justintv', 'vidbull'])
FREE_SERVERS.extend(['vureel','nosvideo','videopremium','movreel','flashx','upafile'])
FREE_SERVERS.extend(['fileflyer','playedto','tunepk','powvideo','videomega','mega','vidspot','netutv','rutube'])
FREE_SERVERS.extend(['videozed','documentary','hugefiles', 'firedrive','videott','tumitv','gamovideo'])
FREE_SERVERS.extend(['torrent','video4you','mailru','streaminto','backin','akstream', 'speedvideo', 'junkyvideo', 'rapidvideo'])

# Lista de TODOS los servidores que funcionan con cuenta premium individual
PREMIUM_SERVERS = ['uploadedto','nowvideo']

# Lista de TODOS los servidores soportados por Filenium
FILENIUM_SERVERS = []
FILENIUM_SERVERS.extend(['linkto','uploadedto','gigasize','youtube','filepost','hotfile','rapidshare','turbobit','mediafire','bitshare','depositfiles'])
FILENIUM_SERVERS.extend(['oron','allmyvideos','novamov','videoweed','movshare','letitbit','shareonline','shareflare','rapidgator'])
FILENIUM_SERVERS.extend(['filefactory','netload','nowdownload','filevelocity','freakshare','userporn','divxstage','putlocker','extabit','vidxden'])
FILENIUM_SERVERS.extend(['vimeo','dailymotion','jumbofiles','zippyshare','glumbouploads','bayfiles','twoshared', 'fourshared','crocko','fiberupload'])
FILENIUM_SERVERS.extend(['ifile','megashares','slingfile','uploading','vipfile','filenium','movreel','one80upload','flashx','nowvideo','vk','moevideos'])
FILENIUM_SERVERS.extend(['cloudzer','filecloudio','luckyshare','lumfile','playedto','ryushare','streamcloud','videozed','xenubox','filesmonster'])
#wupload,fileserve

# Lista de TODOS los servidores soportados por Real-Debrid
REALDEBRID_SERVERS = ['one80upload','tenupload','onefichier','onehostclick','twoshared','fourfastfile','fourshared','abc','asfile','badongo','bayfiles','bitshare','cbscom','cloudzer','cramit','crocko','cwtv','dailymotion','dateito',
                    'dengee','diglo','extabit','fiberupload','filedino','filefactory','fileflyer','filekeen','filemade','filemates','fileover','filepost',
                   'filesend','filesmonster','filevelocity','freakshare','free','furk','fyels','gigasize','gigaup','glumbouploads','goldfile','hitfile','hipfile','hostingbulk',
                   'hotfile','hulkshare','hulu','ifile','jakfile','jumbofiles','justintv','letitbit','loadto','mediafire','mega','megashare','megashares','mixturevideo','muchshare','netload',
                   'novafile','nowdownload','purevid','putbit','putlocker','redtube','rapidgator','rapidshare','rutube','ryushare','scribd','sendspace','sharebees','shareflare','shragle','slingfile','sockshare',
                   'soundcloud','speedyshare','turbobit','unibytes','uploadc','uploadedto','uploading','uploadspace','uptobox',
                   'userporn','veevr','vidbux','vidhog','vidxden','vimeo','vipfile','wattv','xfileshare','youporn','youtube','yunfile','zippyshare','justintv','nowvideo','ultramegabit','filesmonster','oboom']
#wupload,fileserve

ALLDEBRID_SERVERS = ['one80upload','onefichier','twoshared','fourfastfile','fourshared','albafile','bayfiles','bitshare','cloudzer','cramit','crocko','cyberlocker','dailymotion','dengee',
                   'depfile','dlfree','extabit','extmatrix','filefactory','fileflyer','filegag','filehost','fileover','filepost','filerio','filesabc',
                   'filesend','filesmonster','filestay','freakshare','gigasize','hotfile','hulkshare','jumbofiles','letitbit','loadto','mediafire','megashares','mixturevideo','netload',
                   'nitrobits','oteupload','purevid','putlocker','rapidgator','rapidshare','redtube','scribd','secureupload','sharebees','shareflare','slingfile','sockshare',
                   'soundcloud','speedload','speedyshare','turbobit', 'uloadto', 'uploadc','uploadedto','uploading','uptobox',
                   'userporn','vimeo','vipfile','youporn','youtube','yunfile','zippyshare','lumfile','ultramegabit','filesmonster']
    
# Lista completa de todos los servidores soportados por pelisalacarta, usada para buscar patrones
ALL_SERVERS = list( set(FREE_SERVERS) | set(FILENIUM_SERVERS) | set(REALDEBRID_SERVERS) | set(ALLDEBRID_SERVERS) )
ALL_SERVERS.sort()

# Función genérica para encontrar vídeos en una página
def find_video_items(item=None, data=None, channel=""):
    logger.info("[launcher.py] findvideos")

    # Descarga la página
    if data is None:
        from core import scrapertools
        data = scrapertools.cache_page(item.url)
        #logger.info(data)
    
    # Busca los enlaces a los videos
    from core.item import Item
    from servers import servertools
    listavideos = servertools.findvideos(data)

    if item is None:
        item = Item()

    itemlist = []
    for video in listavideos:
        scrapedtitle = item.title.strip() + " - " + video[0].strip()
        scrapedurl = video[1]
        server = video[2]
        
        itemlist.append( Item(channel=item.channel, title=scrapedtitle , action="play" , server=server, page=item.page, url=scrapedurl, thumbnail=item.thumbnail, show=item.show , plot=item.plot , folder=False) )

    return itemlist

def findvideosbyserver(data, serverid):
    logger.info("[servertools.py] findvideos")
    encontrados = set()
    devuelve = []
    try:
        exec "from servers import "+serverid
        exec "devuelve.extend("+serverid+".find_videos(data))"
    except ImportError:
        logger.info("No existe conector para "+serverid)
    except:
        logger.info("Error en el conector "+serverid)
        import traceback,sys
        from pprint import pprint
        exc_type, exc_value, exc_tb = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_tb)
        for line in lines:
            line_splits = line.split("\n")
            for line_split in line_splits:
                logger.error(line_split)

    return devuelve

def findvideos(data):
    logger.info("[servertools.py] findvideos")
    encontrados = set()
    devuelve = []

    # Ejecuta el findvideos en cada servidor
    for serverid in ALL_SERVERS:
        try:
            # Sustituye el código por otro "Plex compatible"
            #exec "from servers import "+serverid
            #exec "devuelve.extend("+serverid+".find_videos(data))"
            servers_module = __import__("servers."+serverid)
            server_module = getattr(servers_module,serverid)
            devuelve.extend( server_module.find_videos(data) )
        except ImportError:
            logger.info("No existe conector para "+serverid)
        except:
            logger.info("Error en el conector "+serverid)
            import traceback,sys
            from pprint import pprint
            exc_type, exc_value, exc_tb = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_tb)
            for line in lines:
                line_splits = line.split("\n")
                for line_split in line_splits:
                    logger.error(line_split)

    return devuelve

def get_video_urls(server,url):
    '''
    servers_module = __import__("servers."+server)
    server_module = getattr(servers_module,server)
    return server_module.get_video_url( page_url=url)
    '''

    video_urls,puede,motivo = resolve_video_urls_for_playing(server,url)
    return video_urls

def get_channel_module(channel_name):
    channels_module = __import__("channels."+channel_name)
    channel_module = getattr(channels_module,channel_name)
    return channel_module

def get_server_from_url(url):
    encontrado = findvideos(url)
    if len(encontrado)>0:
        devuelve = encontrado[0][2]
    else:
        devuelve = "directo"

    return devuelve

def resolve_video_urls_for_playing(server,url,video_password="",muestra_dialogo=False):
    logger.info("[servertools.py] resolve_video_urls_for_playing, server="+server+", url="+url)
    video_urls = []
    torrent = False
    
    server = server.lower()

    # Si el vídeo es "directo", no hay que buscar más
    if server=="directo" or server=="local":
        logger.info("[servertools.py] server=directo, la url es la buena")
        
        try:
            import urlparse
            parsed_url = urlparse.urlparse(url)
            logger.info("parsed_url="+str(parsed_url))
            extension = parsed_url.path[-4:]
        except:
            extension = url[-4:]

        video_urls = [[ "%s [%s]" % (extension,server) , url ]]
        return video_urls,True,""

    # Averigua las URL de los vídeos
    else:
        
        #if server=="torrent":
        #    server="filenium"
        #    torrent = True

        # Carga el conector
        try:
            # Muestra un diálogo de progreso
            if muestra_dialogo:
                import xbmcgui
                progreso = xbmcgui.DialogProgress()
                progreso.create( "pelisalacarta" , "Conectando con "+server)

            # Sustituye el código por otro "Plex compatible"
            #exec "from servers import "+server+" as server_connector"
            servers_module = __import__("servers."+server)
            server_connector = getattr(servers_module,server)

            logger.info("[servertools.py] servidor de "+server+" importado")
            if muestra_dialogo:
                progreso.update( 20 , "Conectando con "+server)

            # Si tiene una función para ver si el vídeo existe, lo comprueba ahora
            if hasattr(server_connector, 'test_video_exists'):
                logger.info("[servertools.py] invocando a "+server+".test_video_exists")
                puedes,motivo = server_connector.test_video_exists( page_url=url )

                # Si la funcion dice que no existe, fin
                if not puedes:
                    logger.info("[servertools.py] test_video_exists dice que el video no existe")
                    if muestra_dialogo: progreso.close()
                    return video_urls,puedes,motivo
                else:
                    logger.info("[servertools.py] test_video_exists dice que el video SI existe")

            # Obtiene enlaces free
            if server in FREE_SERVERS:
                logger.info("[servertools.py] invocando a "+server+".get_video_url")
                video_urls = server_connector.get_video_url( page_url=url , video_password=video_password )
                
                # Si no se encuentran vídeos en modo free, es porque el vídeo no existe
                if len(video_urls)==0:
                    if muestra_dialogo: progreso.close()
                    return video_urls,False,"No se puede encontrar el vídeo en "+server

            # Obtiene enlaces premium si tienes cuenta en el server
            if server in PREMIUM_SERVERS and config.get_setting(server+"premium")=="true":
                video_urls = server_connector.get_video_url( page_url=url , premium=(config.get_setting(server+"premium")=="true") , user=config.get_setting(server+"user") , password=config.get_setting(server+"password"), video_password=video_password )
                
                # Si no se encuentran vídeos en modo premium directo, es porque el vídeo no existe
                if len(video_urls)==0:
                    if muestra_dialogo: progreso.close()
                    return video_urls,False,"No se puede encontrar el vídeo en "+server
    
            # Obtiene enlaces filenium si tienes cuenta
            if server in FILENIUM_SERVERS and config.get_setting("fileniumpremium")=="true":
    
                # Muestra un diálogo de progreso
                if muestra_dialogo:
                    progreso.update( 40 , "Conectando con Filenium")
    
                from servers import filenium as gen_conector
                
                video_gen = gen_conector.get_video_url( page_url=url , premium=(config.get_setting("fileniumpremium")=="true") , user=config.get_setting("fileniumuser") , password=config.get_setting("fileniumpassword"), video_password=video_password )
                extension = gen_conector.get_file_extension(video_gen)
                logger.info("[xbmctools.py] filenium url="+video_gen)
                video_urls.append( [ extension+" ["+server+"][filenium]", video_gen ] )

            # Obtiene enlaces realdebrid si tienes cuenta
            if server in REALDEBRID_SERVERS and config.get_setting("realdebridpremium")=="true":
    
                # Muestra un diálogo de progreso
                if muestra_dialogo:
                    progreso.update( 60 , "Conectando con Real-Debrid")

                from servers import realdebrid as gen_conector
                video_gen = gen_conector.get_video_url( page_url=url , premium=(config.get_setting("realdebridpremium")=="true") , user=config.get_setting("realdebriduser") , password=config.get_setting("realdebridpassword"), video_password=video_password )
                logger.info("[xbmctools.py] realdebrid url="+video_gen)
                if not "REAL-DEBRID" in video_gen:
                    video_urls.append( [ "."+video_gen.rsplit('.',1)[1]+" [realdebrid]", video_gen ] )
                else:
                    if muestra_dialogo: progreso.close()
                    # Si RealDebrid da error pero tienes un enlace válido, no te dice nada
                    if len(video_urls)==0:
                        return video_urls,False,video_gen
                  
            # Obtiene enlaces alldebrid si tienes cuenta
            if server in ALLDEBRID_SERVERS and config.get_setting("alldebridpremium")=="true":
    
                # Muestra un diálogo de progreso
                if muestra_dialogo:
                    progreso.update( 80 , "Conectando con All-Debrid")

                from servers import alldebrid as gen_conector
                video_gen = gen_conector.get_video_url( page_url=url , premium=(config.get_setting("alldebridpremium")=="true") , user=config.get_setting("alldebriduser") , password=config.get_setting("alldebridpassword"), video_password=video_password )
                logger.info("[xbmctools.py] alldebrid url="+video_gen)
                if video_gen.startswith("http"):
                    video_urls.append( [ "."+video_gen.rsplit('.',1)[1]+" [alldebrid]", video_gen ] )
                else:
                    # Si Alldebrid da error pero tienes un enlace válido, no te dice nada
                    if len(video_urls)==0:
                        return [],False,video_gen.strip()

            
            if muestra_dialogo:
                progreso.update( 100 , "Proceso finalizado")

            # Cierra el diálogo de progreso
            if muestra_dialogo: progreso.close()

            # Llegas hasta aquí y no tienes ningún enlace para ver, así que no vas a poder ver el vídeo
            if len(video_urls)==0:
                # ¿Cual es el motivo?
                
                # 1) No existe -> Ya está controlado
                # 2) No tienes alguna de las cuentas premium compatibles

                # Lista de las cuentas que soportan este servidor
                listapremium = ""
                if server in ALLDEBRID_SERVERS: listapremium+="All-Debrid o "            
                if server in FILENIUM_SERVERS: listapremium+="Filenium o "
                if server in REALDEBRID_SERVERS: listapremium+="Real-Debrid o "
                if server in PREMIUM_SERVERS: listapremium+=server+" o "
                listapremium = listapremium[:-3]
    
                return video_urls,False,"Para ver un vídeo en "+server+" necesitas<br/>una cuenta en "+listapremium

        except:
            if muestra_dialogo: progreso.close()
            import traceback
            from pprint import pprint
            exc_type, exc_value, exc_tb = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_tb)
            for line in lines:
                line_splits = line.split("\n")
                for line_split in line_splits:
                    logger.error(line_split)

            return video_urls,False,"Se ha producido un error en<br/>el conector con "+server

    return video_urls,True,""