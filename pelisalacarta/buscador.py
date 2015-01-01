# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import sys

from core import config
from core import logger
from core.item import Item
from core import scrapertools

CHANNELNAME = "buscador"

logger.info("[buscador.py] init")

DEBUG = True

def mainlist(params,url="",category=""):
    logger.info("[buscador.py] mainlist")

    listar_busquedas(params,url,category)

def searchresults(params,url="",category=""):
    import xbmc
    import xbmcgui
    import xbmcplugin
    from platformcode.xbmc import xbmctools

    logger.info("[buscador.py] searchresults")
    salvar_busquedas(params,url,category)
    if url == "" and category == "":
        tecleado = params.url
    else:
        tecleado = url
    tecleado = tecleado.replace(" ", "+")
    
    # Lanza las búsquedas
    matches = []
    itemlist = do_search_results(tecleado)
    for item in itemlist:
        targetchannel = item.channel
        action = item.action
        category = category
        scrapedtitle = item.title+" ["+item.channel+"]"
        scrapedurl = item.url
        scrapedthumbnail = item.thumbnail
        scrapedplot = item.plot
        
        xbmctools.addnewfolder( targetchannel , action , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot, show=item.show )
    
    # Cierra el directorio
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_TITLE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def do_search_results(tecleado):

    itemlist = []

    #from pelisalacarta.channels import animeflv
    #itemlist.extend( animeflv.search( Item() , tecleado) )

    from pelisalacarta.channels import animeid
    itemlist.extend( animeid.search( Item() , tecleado) )

    from pelisalacarta.channels import bajui
    itemlist.extend( bajui.search( Item() , tecleado) )

    from pelisalacarta.channels import filmpertutti
    itemlist.extend( filmpertutti.search( Item() , tecleado) )

    from pelisalacarta.channels import filmsenzalimiti
    itemlist.extend( filmsenzalimiti.search( Item() , tecleado) )

    #from pelisalacarta.channels import cineblog01
    #itemlist.extend( cineblog01.search( Item() , tecleado) )
    #itemlist.extend( cineblog01.searchserie( Item() , tecleado) )

    from pelisalacarta.channels import cinetube
    itemlist.extend( cinetube.search( Item() , tecleado, "F") )

    from pelisalacarta.channels import cineonlineeu
    itemlist.extend( cineonlineeu.search( Item() , tecleado) )

    #from pelisalacarta.channels import cuevana
    #itemlist.extend( cuevana.search( Item() , tecleado) )

    #from pelisalacarta.channels import cinevos
    #itemlist.extend( cinevos.search( Item() , tecleado) )

    #from pelisalacarta.channels import cinegratis
    #itemlist.extend( cinegratis.search( Item() , tecleado) )

    #from pelisalacarta.channels import cuevana
    #itemlist.extend( cuevana.search( Item() , tecleado) )

    from pelisalacarta.channels import divxatope
    itemlist.extend( divxatope.search( Item() , tecleado) )

    #from pelisalacarta.channels import divxonline
    #itemlist.extend( divxonline.search( Item() , tecleado) )

    from pelisalacarta.channels import documaniatv
    itemlist.extend( documaniatv.search( Item() , tecleado) )

    #from pelisalacarta.channels import gnula
    #itemlist.extend( gnula.search( Item() , tecleado) )

    from pelisalacarta.channels import jkanime
    itemlist.extend( jkanime.search( Item() , tecleado) )

    #from pelisalacarta.channels import newdivx
    #itemlist.extend( newdivx.search( Item() , tecleado) )

    #from pelisalacarta.channels import newhd
    #itemlist.extend( newhd.search( Item() , tecleado) )

    from pelisalacarta.channels import peliculasaudiolatino
    itemlist.extend( peliculasaudiolatino.search( Item() , tecleado) )

    #from pelisalacarta.channels import peliculasflv
    #itemlist.extend( peliculasflv.search( Item() , tecleado) )

    from pelisalacarta.channels import peliculasyonkis_generico
    itemlist.extend( peliculasyonkis_generico.search( Item() , tecleado) )

    from pelisalacarta.channels import seriesyonkis
    itemlist.extend( seriesyonkis.search( Item() , tecleado) )

    from pelisalacarta.channels import serieonline
    itemlist.extend( serieonline.search( Item() , tecleado) )

    from pelisalacarta.channels import shurweb
    itemlist.extend( shurweb.search( Item() , tecleado) )

    from pelisalacarta.channels import tumejortv
    itemlist.extend( tumejortv.search( Item() , tecleado) )

    if config.get_setting("serieslyaccount")=="true":
        from pelisalacarta.channels import seriesly
        itemlist.extend( seriesly.search( Item() , tecleado) )

    #from pelisalacarta.channels import seriesdanko
    #itemlist.extend( seriesdanko.search( Item() , tecleado) )

    from pelisalacarta.channels import veranime
    itemlist.extend( veranime.search( Item() , tecleado) )

    itemlist.sort(key=lambda item: item.title.lower().strip())
    return itemlist

def salvar_busquedas(params,url="",category=""):
    if url == "" and category == "":
        channel = params.channel
        url = params.url
    else:
        channel = params.get("channel")
    limite_busquedas = ( 10, 20, 30, 40, )[ int( config.get_setting( "limite_busquedas" ) ) ]
    matches = []
    try:
        presets = config.get_setting("presets_buscados")
        if "|" in presets:
            presets = matches = presets.split("|")            
            for count, preset in enumerate( presets ):
                if url in preset:
                    del presets[ count ]
                    break
        
        if len( presets ) >= limite_busquedas:
            presets = presets[ : limite_busquedas - 1 ]
    except:
        presets = ""
    presets2 = ""
    if len(matches)>0:
        for preset in presets:
            presets2 = presets2 + "|" + preset 
        presets = url + presets2
    elif presets != "":
        presets = url + "|" + presets
    else:
        presets = url
    config.set_setting("presets_buscados",presets)
    # refresh container so items is changed
    #xbmc.executebuiltin( "Container.Refresh" )
        
def listar_busquedas(params,url="",category=""):
    import xbmc
    import xbmcgui
    import xbmcplugin
    
    from platformcode.xbmc import xbmctools
    #print "category :" +category
    if url == "" and category == "":
        channel_preset = params.channel
        accion = params.action
        category = "Buscador_Generico"
    else:
        channel_preset = params.get("channel")
        accion = params.get("action")
        category = "Buscador_Normal"
    #print "listar_busquedas()"
    channel2 = ""
    itemlist=[]
    # Despliega las busquedas anteriormente guardadas
    try:
        presets = config.get_setting("presets_buscados")
        
        if channel_preset != CHANNELNAME:
            channel2 = channel_preset
        logger.info("channel_preset :%s" %channel_preset)
        
        matches = ""
        if "|" in presets:
            matches = presets.split("|")
            itemlist.append( Item(channel="buscador" , action="por_teclado"  , title=config.get_localized_string(30103)+"..."  , url=matches[0] ,thumbnail="" , plot=channel2, category = category , context = 1 ))
            #addfolder( "buscador"   , config.get_localized_string(30103)+"..." , matches[0] , "por_teclado", channel2 ) # Buscar
        else:
            itemlist.append( Item(channel="buscador" , action="por_teclado"  ,  title=config.get_localized_string(30103)+"..." ,   url="" ,thumbnail="" , plot=channel2 , category = category , context = 0 ))
            #addfolder( "buscador"   , config.get_localized_string(30103)+"..." , "" , "por_teclado", channel2 )
        if len(matches)>0:    
            for match in matches:
                
                title=scrapedurl = match
                itemlist.append( Item(channel=channel_preset , action="searchresults"  , title=title ,  url=scrapedurl, thumbnail="" , plot="" , category = category ,  context=1 ))
                #addfolder( channel_preset , title , scrapedurl , "searchresults" )
        elif presets != "":
        
            title = scrapedurl = presets
            itemlist.append( Item(channel=channel_preset , action="searchresults"  , title=title ,  url=scrapedurl, thumbnail= "" , plot="" , category = category , context = 1 ))
            #addfolder( channel_preset , title , scrapedurl , "searchresults" )
    except:
         itemlist.append( Item(channel="buscador" , action="por_teclado"  , title=config.get_localized_string(30103)+"..." ,  url="", thumbnail="" , plot=channel2 , category = category ,  context = 0  ))
        #addfolder( "buscador"   , config.get_localized_string(30103)+"..." , "" , "por_teclado" , channel2 )
    
    if url=="" and category=="Buscador_Generico":

        return itemlist
    else:
        for item in itemlist:
            channel = item.channel
            action = item.action
            category = category
            scrapedtitle = item.title
            scrapedurl = item.url
            scrapedthumbnail = item.thumbnail
            scrapedplot = item.plot
            extra=item.extra
            context = item.context
            xbmctools.addnewfolderextra( channel , action , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot , extradata = extra , context = context)
            
        # Cierra el directorio
        xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
    
def borrar_busqueda(params,url="",category=""):
    import xbmc
    import xbmcgui
    import xbmcplugin
    
    from platformcode.xbmc import xbmctools
    if url == "" and category == "":
        channel = params.channel
        url = params.url
    else:
        channel = params.get("channel")
    
    matches = []
    try:
        presets = config.get_setting("presets_buscados")
        if "|" in presets:
            presets = matches = presets.split("|")
            for count, preset in enumerate( presets ):
                if url in preset:
                    del presets[ count ]
                    break
        elif presets == url:
            presets = ""
            
    except:
        presets = ""
    if len(matches)>1:
        presets2 = ""
        c = 0
        barra = ""
        for preset in presets:
            if c>0:
                barra = "|"
            presets2 =  presets2 + barra + preset 
            c +=1
        presets = presets2
    elif len(matches) == 1:
        presets = presets[0]
    config.set_setting("presets_buscados",presets)
    # refresh container so item is removed
    xbmc.executebuiltin( "Container.Refresh" )

def teclado(default="", heading="", hidden=False):
    import xbmc
    import xbmcgui
    import xbmcplugin
    
    from platformcode.xbmc import xbmctools
    logger.info("[buscador.py] teclado")
    tecleado = ""
    keyboard = xbmc.Keyboard(default)
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        tecleado = keyboard.getText()
        if len(tecleado)<=0:
            return
    
    return tecleado
    
def por_teclado(params,url="",category=""):
    logger.info("[buscador.py] por_teclado")
    logger.info("category :"+category+" url :"+url)
    if category == "" or category == "Buscador_Generico":

        channel  = params.channel
        tecleado = teclado(params.url)
        if len(tecleado)<=0:
            return
        if params.plot:
            channel = params.plot
            exec "import pelisalacarta.channels."+channel+" as plugin"
        else:
            exec "import pelisalacarta."+channel+" as plugin"


        params.url = tecleado
        itemlist = plugin.searchresults(params)
        return itemlist
    else:
        channel  = params.get("channel")
        tecleado = teclado(url)
        if len(tecleado)<=0:
            return
        if params.get("plot"):
            channel = params.get("plot")
            exec "import pelisalacarta.channels."+channel+" as plugin"
        else:
            exec "import pelisalacarta."+channel+" as plugin"

        url = tecleado
        plugin.searchresults(params, url, category)

def addfolder( canal , nombre , url , accion , channel2 = "" ):
    import xbmc
    import xbmcgui
    import xbmcplugin
    
    from platformcode.xbmc import xbmctools
    logger.info('[buscador.py] addfolder( "'+nombre+'" , "' + url + '" , "'+accion+'")"')
    listitem = xbmcgui.ListItem( nombre , iconImage="DefaultFolder.png")
    itemurl = '%s?channel=%s&action=%s&category=%s&url=%s&channel2=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus(nombre) , urllib.quote_plus(url),channel2 )
    
    
    if accion != "por_teclado":
        contextCommands = []
        DeleteCommand = "XBMC.RunPlugin(%s?channel=buscador&action=borrar_busqueda&title=%s&url=%s)" % ( sys.argv[ 0 ]  ,  urllib.quote_plus( nombre ) , urllib.quote_plus( url ) )
        contextCommands.append((config.get_localized_string( 30300 ),DeleteCommand))
        listitem.addContextMenuItems ( contextCommands, replaceItems=False)
        
    xbmcplugin.addDirectoryItem( handle = int( sys.argv[ 1 ] ), url = itemurl , listitem=listitem, isFolder=True)
