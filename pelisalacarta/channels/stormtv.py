# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para stormtv 
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# Por JuRR
# v0.8
#------------------------------------------------------------
import urlparse,urllib2,urllib,re

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools
import xml.dom.minidom as minidom
import urllib,urllib2
import os,errno
from core import stormlib


__channel__ = "stormtv"
__category__ = "F,S,A"
__type__ = "generic"
__title__ = "stormtv2"
__language__ = "ES"
__server__ = "oc1.lopezepol.com"

DEBUG = config.get_setting("debug")
PREFERENCES  =stormlib.getpreferences()
LANG =stormlib.getlang()
SERVERS =stormlib.getservers()
SERVER = "https://"+__server__+"/stormtv/public/"
STATIC_SERVER= "http://"+__server__+"/stormtv/public/"
def isGeneric():
    return True

def searchtype(item):
	import socket
	socket.setdefaulttimeout(10) # timeout in seconds 
	itemlist = []
        itemlist.append( Item(channel=__channel__, action="search"    , thumbnail=STATIC_SERVER+"buscar.jpg", title="Buscar", url="",fanart=STATIC_SERVER+"logo.jpg"))
	itemlist.append( Item(channel=__channel__, action="nocatalogsearch"    , thumbnail=STATIC_SERVER+"buscar.jpg", title="Buscar sin catalogar", url="",fanart=STATIC_SERVER+"logo.jpg"))
	itemlist.append( Item(channel=__channel__,action="genresearch",thumbnail=STATIC_SERVER+"buscar.jpg",title="Buscar por Genero", url="",fanart=STATIC_SERVER+"logo.jpg"))
	itemlist.append( Item(channel=__channel__,action="yearsearch",thumbnail=STATIC_SERVER+"buscar.jpg",title="Buscar por AÃ±o", url="",fanart=STATIC_SERVER+"logo.jpg"))
	itemlist.append( Item(channel=__channel__,action="popular",thumbnail=STATIC_SERVER+"buscar.jpg",title="Series mas populares", url="",fanart=STATIC_SERVER+"logo.jpg"))
	path=config.get_data_path()+"stormtv/temp/"                                                                                                                                   
    	#itemlist=[]                                
	stormlib.getalltvslist()                                                                                                                                                
    	xml=path+"/"+"temp.xml"                                                                                                                                                       
    	doc = minidom.parse(xml)                                                                                                                                                      
    	node = doc.documentElement                                                                                                                                                    
    	series = doc.getElementsByTagName("serie")                                                                                                                                    
    	for serie in series:                                                                                                                                                          
        	name = serie.getElementsByTagName("name")[0].childNodes[0].data                                                                                                           
        	name = name.encode("utf-8")                                                                                                                                               
        	id = serie.getElementsByTagName("id")[0].childNodes[0].data                                                                                                               
        	fanart = serie.getElementsByTagName("fanart")[0].childNodes[0].data                                                                                                       
        	poster = serie.getElementsByTagName("poster")[0].childNodes[0].data                                                                                                       
        	type=serie.getElementsByTagName("type")[0].childNodes[0].data                                                                                                             
        	print "movies poster"+SERVER+fanart                                                                                                                                       
        	try:                                                                                                                                                                      
                        plot=serie.getElementsByTagName("plot")[0].childNodes[0].data                                                                                             
                        plot=plot.encode("utf-8")                                                                                                                                 
        	except:                                                                                                                                                                   
                        plot="" 
		itemlist.append( Item(channel=__channel__, action="listtvs" , title=name, fulltitle=name , url=id, thumbnail=STATIC_SERVER+poster, plot=plot, viewmode="movie", show=id, fanart=STATIC_SERVER+fanart))                                                                                                                                                  
	return itemlist


def search(item,texto, categoria="*"):
    import socket                                        
    socket.setdefaulttimeout(10) # timeout in seconds
    logger.info("[stormtv.py] search "+texto )
    itemlist = []
    #server= "https://"+__server__+"/stormtv/public/"
    path=config.get_data_path()+"stormtv/temp/"
    if not os.path.exists(path):                                                                                                     
       logger.info("[stormtv.py] search Creating data_path "+path)                                                                       
       try:                                                                                                                          
          os.mkdirs(path)                                                                                                      
       
       except:
       	  logger.info( "[stormtv.py] search fallo crear directorio" )                                                                                                                      
          pass                                           
    #urllib.urlretrieve (SERVER+"/tvseries/search/title/"+texto, path+"temp.xml")
    search = urllib2.urlopen(SERVER+"/tvseries/search/title/"+texto,timeout=30)
    output = open(path+"temp.xml",'wb')
    output.write(search.read())
    output.close()                             
    xml=path+"/"+"temp.xml"                                                                                                    
    doc = minidom.parse(xml)                                                                                                   
    node = doc.documentElement                                                                                                 
    series = doc.getElementsByTagName("serie")                                                                                 
    for serie in series:                                                                                                       
    	name = serie.getElementsByTagName("name")[0].childNodes[0].data
    	name = name.encode("utf-8")
    	id = serie.getElementsByTagName("id")[0].childNodes[0].data                                                    
        fanart = serie.getElementsByTagName("fanart")[0].childNodes[0].data                                                
        poster = serie.getElementsByTagName("poster")[0].childNodes[0].data
	type=serie.getElementsByTagName("type")[0].childNodes[0].data
	print "movies poster"+SERVER+fanart
	try:                                                                                                                                                              
                        plot=serie.getElementsByTagName("plot")[0].childNodes[0].data                                                                                             
                        plot=plot.encode("utf-8")                                                                                                                                 
        except:                                                                                                                                                           
                        plot=""                                               
    	if ((type=="0")or(type=="1")):
		itemlist.append( Item(channel=__channel__, action="channel" , title=name, fulltitle=name , url=id, thumbnail=STATIC_SERVER+poster, plot=plot, viewmode="movie", show=id,fanart=STATIC_SERVER+fanart))
	else:
		itemlist.append( Item(channel=__channel__, action="listtvs" , title=name, fulltitle=name , url=id, thumbnail=STATIC_SERVER+poster, plot=plot, viewmode="movie", show=id,fanart=STATIC_SERVER+fanart))
    itemlist.append( Item(channel=__channel__,action="nocatalogsearch",title="<Buscar en items sin catalogar>",fulltitle="",extra=texto))  
    return itemlist

def listtvs(item):
    path=config.get_data_path()+"stormtv/temp/"
    itemlist=[]
    stormlib.gettvslist(item.show)
    xml=path+"/"+"temp.xml"                                                                                                                                                       
    doc = minidom.parse(xml)                                                                                                                                                      
    node = doc.documentElement                                                                                                                                                    
    series = doc.getElementsByTagName("serie")                                                                                                                                    
    for serie in series:                                                                                                                                                          
        name = serie.getElementsByTagName("name")[0].childNodes[0].data                                                                                                           
        name = name.encode("utf-8")                                                                                                                                               
        id = serie.getElementsByTagName("id")[0].childNodes[0].data                                                                                                               
        fanart = serie.getElementsByTagName("fanart")[0].childNodes[0].data                                                                                                       
        poster = serie.getElementsByTagName("poster")[0].childNodes[0].data                                                                                                       
        type=serie.getElementsByTagName("type")[0].childNodes[0].data                                                                                                             
        print "movies poster"+SERVER+fanart                                                                                                                                       
        try:                                                                                                                                                                      
                        plot=serie.getElementsByTagName("plot")[0].childNodes[0].data                                                                                             
                        plot=plot.encode("utf-8")                                                                                                                                 
        except:                                                                                                                                                                   
                        plot=""                                                                                                                                                   
        itemlist.append( Item(channel=__channel__, action="channel" , title=name, fulltitle=name , url=id, thumbnail=STATIC_SERVER+poster, plot=plot, viewmode="movie", show=id,fanart=STATIC_SERVER+fanart))
    return itemlist
def popular(item):
    path=config.get_data_path()+"stormtv/temp/"                                                                                                                                   
    itemlist=[]                                                                                                                                                                   
    stormlib.getpopular()                                                                                                                                                
    xml=path+"/"+"temp.xml"                                                                                                                                                       
    doc = minidom.parse(xml)                                                                                                                                                      
    node = doc.documentElement                                                                                                                                                    
    series = doc.getElementsByTagName("serie")                                                                                                                                    
    for serie in series:                                                                                                                                                          
        name = serie.getElementsByTagName("name")[0].childNodes[0].data                                                                                                           
        name = name.encode("utf-8")                                                                                                                                               
        id = serie.getElementsByTagName("id")[0].childNodes[0].data                                                                                                               
        fanart = serie.getElementsByTagName("fanart")[0].childNodes[0].data                                                                                                       
        poster = serie.getElementsByTagName("poster")[0].childNodes[0].data                                                                                                       
        type=serie.getElementsByTagName("type")[0].childNodes[0].data                                                                                                             
        print "movies poster"+SERVER+fanart                                                                                                                                       
        try:                                                                                                                                                                      
                        plot=serie.getElementsByTagName("plot")[0].childNodes[0].data                                                                                             
                        plot=plot.encode("utf-8")                                                                                                                                 
        except:                                                                                                                                                                   
                        plot=""                                                                                                                                                   
        itemlist.append( Item(channel=__channel__, action="channel" , title=name, fulltitle=name , url=id, thumbnail=SERVER+poster, plot=plot, viewmode="movie", show=id,fanart=SERVER+fanart))
    return itemlist
def mkdir_p(path):
    try:
           os.makedirs(path)
    except OSError , exc: 
           if exc.errno == errno.EEXIST and os.path.isdir(path):
              pass
           else: raise    

def mainlist(item):
    import xbmc,sys                                                                                                                                                           
    print "vista "+item.extra                                                                                                                                                 
    #xbmc.executebuiltin("XBMC.Container.Update(%s?channel=%s&action=%s&extra=%s)" % ( sys.argv[ 0 ] , "stormtv" , "mainlist" , urllib.quote_plus( item.extra )))
    if (DEBUG): logger.info("[stormtv.py] Mainlist"+PREFERENCES)
    if (PREFERENCES=="0"):
    	user_id = config.get_setting("stormtvuser")                                                                                                                                   
    	user_pass = config.get_setting("stormtvpassword")                                                                                                                             
    	path=config.get_data_path()+"stormtv/temp/"
    	if not os.path.exists(path): 
       		logger.info ("[stormtv.py]Creating data_path "+path)
       		try:            
          		mkdir_p(path) 
       		except:            
          		logger.info("[stormtv.py] Mainlist  Fallo crear directorio")
          		pass            

    	itemlist = []
	itemlist.append( Item(channel=__channel__,action="searchtype",thumbnail=STATIC_SERVER+"buscar.jpg",title="Buscar", url="",fanart=STATIC_SERVER+"logo.jpg"))
	try:
		view=item.extra
	except:
		view="Mixed"
	itemlist.append( Item(channel=__channel__,action="change_view",thumbnail=STATIC_SERVER+"vista.jpg",title="Cambiar vista",url="",fanart=STATIC_SERVER+"logo.jpg"))
    	urllib.urlretrieve (SERVER+"tvseries/following/user/"+user_id+"/pass/"+user_pass+"/view/"+view, path+"temp.xml")                             
    	xml=path+"/"+"temp.xml"                                                                                                    
    	doc = minidom.parse(xml)                                                                                                   
    	node = doc.documentElement                                                                                                 
    	series = doc.getElementsByTagName("serie")                                                                                 
    	for serie in series:                                                                                                       
    		name = serie.getElementsByTagName("name")[0].childNodes[0].data
    		name = name.encode("utf-8")
    		id = serie.getElementsByTagName("id")[0].childNodes[0].data                                                    
        	fanart = serie.getElementsByTagName("fanart")[0].childNodes[0].data
        	poster = serie.getElementsByTagName("poster")[0].childNodes[0].data
		#type = serie.getElementsByTagName("type")[0].childNodes[0].data
		print "movies fanart"+SERVER+fanart                                                
    		try:
			plot=serie.getElementsByTagName("plot")[0].childNodes[0].data
			plot=plot.encode("utf-8")
		except:
			plot=""
    		art=SERVER+fanart      

        	# Depuracion
        	#if (DEBUG): logger.info("title=["+name+"], url=["+id+"], thumbnail=["+art+"]")            
    		itemlist.append( Item(channel=__channel__, action="channel" , title=name, fulltitle=name , url=id, thumbnail=STATIC_SERVER+poster, plot=plot, viewmode="movie", show=id ,fanart=art))

    else:
    	itemlist=[]
    	itemlist.append( Item(channel=__channel__, action="channel" , title="Usuario o contraseña incorrectas", fulltitle="" , url="", thumbnail="", plot="", viewmode="movie", show="" ,fanart=""))
    return itemlist
def change_view(item):
    import xbmcgui                                                                                                                                 
    #filters=get_default_filters()
    filters=[]                                                                                                                          
    dialog=xbmcgui.Dialog()                                                                                                                                
    orden=["Peliculas","Series","Todas"]
    order=["Movies","Tvseries","Mixed"]                                                                         
    view=order[dialog.select("Selecciona la vista preferida",orden)]
    print view
    return mainlist(Item(channel=__channel__, title="stormtv", action="mainlist", extra=view ))
def genresearch(item):
	user_id = config.get_setting("stormtvuser")                                                                                                                               
        user_pass = config.get_setting("stormtvpassword")                                                                                                                         
        path=config.get_data_path()+"stormtv/temp/"
        urllib.urlretrieve (SERVER+"tvseries/genres", path+"temp.xml")                                                                        
        xml=path+"/"+"temp.xml"                                                                                                                                                   
        doc = minidom.parse(xml)                                                                                                                                                  
        node = doc.documentElement                                                                                                                                                
        genres = doc.getElementsByTagName("genre")
	if (DEBUG): print len(genres)
	itemlist=[]
	for genre in genres:
		name2= genre.getElementsByTagName("name")[0].childNodes[0].data
		name = name2.decode("utf-8")
		if (DEBUG): logger.info("###"+name+"$$")
		id = genre.getElementsByTagName("id")[0].childNodes[0].data
		itemlist.append( Item(channel=__channel__, action="genretvs" , title=name, fulltitle=name , url=id, thumbnail=STATIC_SERVER+"logo.jpg", plot="", viewmode="movie", show=id ,fanart=STATIC_SERVER+"logo.jpg"))
	return itemlist
def nocatalogsearch(item):
    if (item.extra==""):
    	import xbmc                        
    	keyboard = xbmc.Keyboard("")       
    	keyboard.doModal()                 
    	if (keyboard.isConfirmed()):       
       		texto = keyboard.getText()
    	else:
		texto=""
    else:
	texto=item.extra
    logger.info("[stormtv.py] search "+texto )                                                                                                                                    
    itemlist = []                                                                                                                                                                 
    #server= "https://"+__server__+"/stormtv/public/"                                                                                                                             
    path=config.get_data_path()+"stormtv/temp/"                                                                                                                                   
    if not os.path.exists(path):                                                                                                                                                  
       logger.info("[stormtv.py] search Creating data_path "+path)                                                                                                                
       try:                                                                                                                                                                       
          os.mkdirs(path)                                                                                                                                                         
                                                                                                                                                                                  
       except:                                                                                                                                                                    
          logger.info( "[stormtv.py] search fallo crear directorio" )                                                                                                             
          pass                                                                                                                                                                    
    #urllib.urlretrieve (SERVER+"/tvseries/search/title/"+texto, path+"temp.xml")                                                                                                 
    search = urllib2.urlopen(SERVER+"/tvseries/searchnocatalog/title/"+texto,timeout=30)                                                                                                   
    output = open(path+"temp.xml",'wb')                                                                                                                                           
    output.write(search.read())                                                                                                                                                   
    output.close()                                                                                                                                                                
    xml=path+"/"+"temp.xml"                                                                                                                                                       
    doc = minidom.parse(xml)                                                                                                                                                      
    node = doc.documentElement                                                                                                                                                    
    series = doc.getElementsByTagName("serie")                                                                                                                                    
    for serie in series:                                                                                                                                                          
        name = serie.getElementsByTagName("name")[0].childNodes[0].data                                                                                                           
        #name = name.encode("utf-8")                                                                                                                                               
        id = serie.getElementsByTagName("id")[0].childNodes[0].data                                                                                                               
        fanart = serie.getElementsByTagName("fanart")[0].childNodes[0].data                                                                                                       
        poster = serie.getElementsByTagName("poster")[0].childNodes[0].data                                                                                                       
        type=serie.getElementsByTagName("type")[0].childNodes[0].data 
	channel=serie.getElementsByTagName("channel")[0].childNodes[0].data
	if (channel=="peliculasyonkis"):
		channel="peliculasyonkis_generico"
	name=name+"-"+channel
	name = name.encode("utf-8")                                                                                                         
        print "movies poster"+SERVER+fanart                                                                                                                                       
        try:                                                                                                                                                                      
                        plot=serie.getElementsByTagName("plot")[0].childNodes[0].data                                                                                             
                        plot=plot.encode("utf-8")                                                                                                                                 
        except:                                                                                                                                                                   
                        plot=""                                                                                                                                                   
        if (type=="5"):
		itemlist.append( Item(channel=__channel__, action="channeltvs" , title=name, fulltitle=channel , url=id, thumbnail=STATIC_SERVER+poster, plot=plot, viewmode="movie", show=id,fanart=STATIC_SERVER+fanart))
        else:                                                                                                                                                                     
                itemlist.append( Item(channel=__channel__, action="findvideos" , title=name, fulltitle=channel , url=id, thumbnail=STATIC_SERVER+poster, plot=plot, viewmode="movie", show="0",fanart=STATIC_SERVER+fanart))
    return itemlist


def yearsearch(item):                                                                                                                                                            
        user_id = config.get_setting("stormtvuser")                                                                                                                               
        user_pass = config.get_setting("stormtvpassword")                                                                                                                         
        path=config.get_data_path()+"stormtv/temp/"                                                                                                                               
        urllib.urlretrieve (SERVER+"tvseries/years", path+"temp.xml")                                                                                                            
        xml=path+"/"+"temp.xml"                                                                                                                                                   
        doc = minidom.parse(xml)                                                                                                                                                  
        node = doc.documentElement                                                                                                                                                
        years = doc.getElementsByTagName("year")                                                                                                                                
        if (DEBUG): print len(years)                                                                                                                                                         
        itemlist=[]                                                                                                                                                               
        for year in years:                                                                                                                                                      
                name = year.getElementsByTagName("name")[0].childNodes[0].data                                                                                                   
                if (DEBUG): logger.info("[stormtv.py] yearsearch ###"+name+"$$")                                                                                                                                             
                id = year.getElementsByTagName("id")[0].childNodes[0].data                                                                                                       
                itemlist.append( Item(channel=__channel__, action="yeartvs" , title=name, fulltitle=name , url=id, thumbnail=STATIC_SERVER+"logo.jpg", plot="", viewmode="movie_with_plot", show=id ,fanart=STATIC_SERVER+"logo.jpg"))
        return itemlist
def yeartvs(item):
	user_id = config.get_setting("stormtvuser")                                                                                                                               
        user_pass = config.get_setting("stormtvpassword")                                                                                                                         
        path=config.get_data_path()+"stormtv/temp/"                                                                                                                               
        urllib.urlretrieve (SERVER+"tvseries/yeartvs/year/"+item.url, path+"temp.xml")                                                                                          
        xml=path+"/"+"temp.xml"                                                                                                                                                   
        doc = minidom.parse(xml)                                                                                                                                                  
        node = doc.documentElement                                                                                                                                                
        series = doc.getElementsByTagName("serie")                                                                                                                                
        itemlist=[]                                                                                                                                                               
        for serie in series:                                                                                                                                                      
                name = serie.getElementsByTagName("name")[0].childNodes[0].data                                                                                                   
                name = name.encode("utf-8")                                                                                                                                       
                id = serie.getElementsByTagName("id")[0].childNodes[0].data                                                                                                       
                fanart = serie.getElementsByTagName("fanart")[0].childNodes[0].data                                                                                               
                poster = serie.getElementsByTagName("poster")[0].childNodes[0].data                                                                                               
                try:                                                                                                                                                              
                        plot=serie.getElementsByTagName("plot")[0].childNodes[0].data                                                                                             
                        plot=plot.encode("utf-8")                                                                                                                                 
                except:                                                                                                                                                           
                        plot=""                                                                                                                                                   
                art=SERVER+fanart                                                                                                                                                 
                                                                                                                                                                                  
                # Depuracion                                                                                                                                                      
                #if (DEBUG): logger.info("title=["+name+"], url=["+id+"], thumbnail=["+art+"]")                                                                                   
                itemlist.append( Item(channel=__channel__, action="channel" , title=name, fulltitle=name , url=id, thumbnail=STATIC_SERVER+poster, plot=plot, viewmode="movie_with_plot", show=id ,fanart=art))
        return itemlist 
def genretvs(item):
	user_id = config.get_setting("stormtvuser")                                                                                                                               
        user_pass = config.get_setting("stormtvpassword")                                                                                                                         
        path=config.get_data_path()+"stormtv/temp/"                                                                                                                               
        urllib.urlretrieve (SERVER+"tvseries/genretvs/genre/"+item.url, path+"temp.xml")                                                                                                            
        xml=path+"/"+"temp.xml"                                                                                                                                                   
        doc = minidom.parse(xml)                                                                                                                                                  
        node = doc.documentElement                                                                                                                                                
        series = doc.getElementsByTagName("serie")
	itemlist=[]                                                                                                                                
        for serie in series:                                                                                                                                                      
                name = serie.getElementsByTagName("name")[0].childNodes[0].data                                                                                                   
                name = name.encode("utf-8")                                                                                                                                       
                id = serie.getElementsByTagName("id")[0].childNodes[0].data                                                                                                       
                fanart = serie.getElementsByTagName("fanart")[0].childNodes[0].data                                                                                               
                poster = serie.getElementsByTagName("poster")[0].childNodes[0].data                                                                                               
                try:                                                                                                                                                              
                        plot=serie.getElementsByTagName("plot")[0].childNodes[0].data                                                                                             
                        plot=plot.encode("utf-8")                                                                                                                                 
                except:                                                                                                                                                           
                        plot=""
                art=SERVER+fanart                                                                                                                                                 
                                                                                                                                                                                  
                # Depuracion                                                                                                                                                      
                #if (DEBUG): logger.info("title=["+name+"], url=["+id+"], thumbnail=["+art+"]")                                                                                   
                itemlist.append( Item(channel=__channel__, action="channel" , title=name, fulltitle=name , url=id, thumbnail=STATIC_SERVER+poster, plot=plot, viewmode="movie_with_plot", show=id ,fanart=art))
	return itemlist 

def channel(item):
	##################Test###################                                                                                                                                     
        #path=config.get_data_path()+"stormtv/temp/"                                                                                                                                   
        #from xml.dom.minidom import Document                                                                                                                                          
        #doc = Document()                                                                                                                                                              
        #base= doc.createElement('tvseries')                                                                                                                                           
        #doc.appendChild(base)                                                                                                                                                         
                                                                                                                                                                                  
        #name=doc.createElement('name')                                                                                                                                                
        #base.appendChild(name)                                                                                                                                                        
        #name_content = doc.createTextNode(item.fulltitle)                                                                                                                          
        #name.appendChild(name_content)                                                                                                                                                
        #year=doc.createElement('year')                                                                                                                                                
        #base.appendChild(year)                                                                                                                                                        
        #year_content = doc.createTextNode("2012")                                                                                                                                     
        #year.appendChild(year_content)                                                                                                                                                
                                                                                                                                                                                  
        #f = open(path+"tvserie.xml", 'w')                                                                                                                                                
        #doc.writexml(f)                                                                                                                                                               
        #f.close()                                                                                                                                                                     
        ###########################################
	stormlib.get_filenium_status()
	logger.info("[stormtv.py] Channel")
	logger.info("[stormtv.py]"+item.fulltitle+" "+item.title)
	storm_show=item.show
	storm_thumbnail=item.thumbnail
	storm_plot=item.plot
	storm_name=item.title
	storm_fanart=item.fanart
	name = ""
	url = ""
	action=""
	path=config.get_data_path()+"stormtv/temp/"                                   
	urllib.urlretrieve (SERVER+"tvseries/getchannelsxml/id/"+storm_show, path+"temp.xml")            
        xml=path+"temp.xml"                                                                                              
        doc = minidom.parse(xml)                                                                                             
        node = doc.documentElement                                                                                           
        series = doc.getElementsByTagName("channel")  
        itemlist = []  
        for serie in series:                                                                                                 
	        name=serie.getElementsByTagName("name")[0].childNodes[0].data
		type=serie.getElementsByTagName("type")[0].childNodes[0].data                                                 
                url=serie.getElementsByTagName("url")[0].childNodes[0].data
		if (type=="1"):
                	itemlist.append( Item(channel=__channel__, action="channeltvs" , title=name, fulltitle=name , url=url, thumbnail=storm_thumbnail, plot=storm_plot, viewmode="movie", show=storm_show, fanart=storm_fanart, extra=action))
		#elif (type=="2"):
		#	itemlist.append( Item(channel=__channel__, action="listtvs" , title=name, fulltitle=name , url=url, thumbnail=storm_thumbnail, plot=storm_plot, viewmode="movie", show=storm_show, fanart=storm_fanart, extra=action))                                                     
		else:
			#Si es una pelicula u otra cosa
			if (name=="peliculasyonkis"):
				fulltitle="peliculasyonkis_generico"
			else:
				fulltitle=name
			itemlist.append( Item(channel=__channel__, action="findvideos" , title=name, fulltitle=fulltitle , url=url, thumbnail=storm_thumbnail, plot=storm_plot, viewmode="movie", show=storm_show, fanart=storm_fanart, extra=action))	
	#ver trailer
	if (type!="1"):
		itemlist.append( Item(channel=__channel__, action="trailer" , title="<Ver trailer>", fulltitle=name , url=url, thumbnail=storm_thumbnail, plot=storm_plot, viewmode="movie", show=storm_show, fanart=storm_fanart, extra=storm_name))
	# Si no es una serie favorita añade el item para añadirla o para quitarla en caso de que este añadida como favorita	
	if (stormlib.isfollow(item.show)=='0'):	
		itemlist.append( Item(channel=__channel__, action="addfollow" , title="<AÃ±adir a Favoritas>", show=item.show,fanart=item.fanart,folder=False))
	else:
		itemlist.append( Item(channel=__channel__, action="removefollow" , title="<Quitar de Favoritas>", show=item.show,fanart=item.fanart,folder=False))
	itemlist.append( Item(channel=__channel__,action="nocatalogsearch",title="<Buscar en items sin catalogar>",fulltitle="",extra=storm_name))
	return itemlist
def trailer(item):
    from core import trailertools
    resultlist=trailertools.youtube_search(item.extra+" trailer")
    itemlist=[]
    for result in resultlist:
	name=result[0]
	url=result[2]
	thumbnail=result[1]
	itemlist.append(Item(channel=__channel__, action="playtrailer" , title=name, fulltitle=name , url=url, thumbnail=thumbnail, plot=item.plot, viewmode="movie",folder=False,server="youtube",fanart=item.fanart))
    return itemlist
def playtrailer(item):
   from platformcode.xbmc import xbmctools
   xbmctools.play_video("Trailer",item.server,item.url,"category",item.title,item.thumbnail,item.plot)

def addfollow(item):
    logger.info("[stormtv.py] Addfollow "+item.show)
    from core import stormlib
    stormlib.addfollow(item.show)
    import xbmcgui                                    
    advertencia = xbmcgui.Dialog()                    
    advertencia.ok("Stormtv","Se ha aÃ±adido el elemento de favoritos")
def removefollow(item):
    logger.info("[stormtv.py] Removefollow "+item.show)	
    from core import stormlib                                                                                                                                                     
    stormlib.removefollow(item.show)  
    import xbmcgui                                                                                                                                                                
    advertencia = xbmcgui.Dialog()                                                                                                                                                
    advertencia.ok("Stormtv","Se ha quitado el elemento de favoritos")
def channeltvs(item):
	logger.info("[stormtv.py] Channeltvs")
	storm_fanart=item.fanart
	storm_plot=item.plot
	storm_thumbnail=item.thumbnail
	storm_show=item.show	
	storm_channel_name=item.fulltitle
	storm_title=item.title
        action="episodios"	
	item=Item(channel=__channel__,url=item.url)
	exec "import pelisalacarta.channels."+storm_channel_name+" as channel"
	# El action nos devolvera el listado de capitulos (episodelist o episodios)
	exec "itemlist_p = channel."+action+"(item)"
	# le quitamos el ultimo elemento que es añadir a la biblioteca de xbmc solo si es seriespepito o seriesyonkis
	patternbiblio="esta serie a la biblioteca"
	patterndescarga="Descargar todos los episodios de la serie"
	#si el ultimo elemento de la lista es descargar la serie completa lo quitamos
	if (len(re.compile(patterndescarga,re.DOTALL).findall(itemlist_p[len(itemlist_p)-1].title))>0):
	   itemlist_p = itemlist_p[0:len(itemlist_p)-1] 

	#Si el ultimo elemento de la lista es añadir a la biblioteca lo quitamos	
	if (len(re.compile(patternbiblio,re.DOTALL).findall(itemlist_p[len(itemlist_p)-1].title))>0):                                                                                    
           itemlist_p = itemlist_p[0:len(itemlist_p)-1]
	itemlist=itemlist_p
	storm_itemlist=[]
	if (config.get_setting("stormtvaccount")=="true"):
	        from core import stormlib
	        chap_dictionary=stormlib.getwatched(storm_show)
	                
	for item in itemlist:
		# comprobar si esta visto y añadir visto.
		if (config.get_setting("stormtvaccount")=="true"):    
	                from core import stormlib                     
	                title, extra, watched = stormlib.iswatched(item.title,chap_dictionary)
	                #hace falta saber cuantos hemos visto para dejar los n ultimos vistos
	        else:                                                           
	                extra=""                                                
	        logger.info("[stormtv.py] extra="+extra)  	
		storm_itemlist.append( Item(channel=__channel__,action="findvideos", server=item.server,fulltitle=storm_channel_name, title=title, url=item.url,thumbnail=storm_thumbnail, plot=storm_plot, viewmode="movie", show=storm_show,fanart=storm_fanart, extra=extra))
	return storm_itemlist


def findvideos(item):
	##############################################
	#sea,epi = stormlib.combined(item.extra)
	#path=config.get_data_path()+"stormtv/temp/"
        #xml=path+"tvserie.xml"
        #doc = minidom.parse(xml)
        #base = doc.documentElement 
	#season=doc.createElement('season')                                                                                                                                        
        #base.appendChild(season)                                                                                                                                                  
        #season_content = doc.createTextNode(str(sea))                                                                                                                                  
        #season.appendChild(season_content)                                                                                                                                        
                                                                                                                                                                                  
        #episode=doc.createElement('episode')                                                                                                                                      
        #base.appendChild(episode)                                                                                                                                                 
        #episode_content = doc.createTextNode(str(epi))                                                                                                                                 
        #episode.appendChild(episode_content)
	#f = open(path+"info.xml", 'w')                                                                                                                                         
        #doc.writexml(f)                                                                                                                                                           
        #f.close()
	#################################################### 
	logger.info("[stormtv.py] Findvideos - Filtro Idioma:"+LANG+" Filtro Servers:"+SERVERS)
        storm_fanart=item.fanart
        storm_plot=item.plot                                                                                                                                                            
        storm_thumbnail=item.thumbnail                                                                                                                                                  
        storm_chapter=item.extra                                                                                                                                                         
        storm_show=item.show                                                                                                                                                            
        storm_channel_name=item.fulltitle                                                                                                                                                   
        storm_title=item.title
        free_url=item.url
        action="findvideos"
        from servers import servertools                                                                                                                                                          
	itemn=Item(channel=__channel__,url=item.url)
	logger.info("[stormtv.py] Findvideons "+itemn.url+" "+storm_channel_name)
        exec "import pelisalacarta.channels."+storm_channel_name+" as channel"
        # El action nos devolvera el listado de posibles enlaces                                                                                             
        try:
        	exec "itemlist = channel."+action+"(itemn)"
        except:
        	#from servers import servertools
        	itemlist= servertools.find_video_items(itemn)                                                                                                                                
        storm_itemlist=[]
        #lang=LANG
       	#logger.info("[stormtv.py] Findvideos"+LANG) 
        # creamos la cadena de servidores free
        pat_free="("
        for fserver in servertools.FREE_SERVERS:
        	pat_free=pat_free+fserver+"|"
        pat_free=pat_free[:len(pat_free)-1]+")"
        
        # creamos la cadena de servidores filenium
        pat_filenium="("
        for filenium in servertools.FILENIUM_SERVERS:
        	pat_filenium=pat_filenium+filenium+"|"
        pat_filenium=pat_filenium[:len(pat_filenium)-1]+")"
        
        #creamos la cadena de servidores alldebrid
        pat_all="(" 
        for all in servertools.ALLDEBRID_SERVERS:
        	pat_all=pat_all+all+"|"
        pat_all=pat_all[:len(pat_all)-1]+")"
        
        #creamos la cadena de servidores real
        pat_real="("
        for real in servertools.REALDEBRID_SERVERS:
        	pat_real=pat_real+real+"|"
        pat_real=pat_real[:len(pat_real)-1]+")"
        pat_all_servers="("
	for all_server in servertools.ALL_SERVERS:
		pat_all_servers=pat_all_servers+all_server+"|"
	pat_all_servers=pat_all_servers[:len(pat_all_servers)-1]+")" 
        #logger.info("pat_free"+pat_free)
        #server=SERVERS
	dictionary=stormlib.filenium()
	####################
	#from xml.dom.minidom import Document
	#doc = Document()                                                           
	#base= doc.createElement('Vos')                                
	#doc.appendChild(base)
	####################
        strue=0
        ltrue=0
        verified=[]
        vserver=""
  	excluded=[]
	excluded.append("letitbit")
	for item in itemlist:
		#Si el canal es shurweb le añadimos (spa)
		if (storm_channel_name=="shurweb"):                                                                                                                               
                        item.title=item.title+" (spa)"
		fserver=item.server
		logger.info("[stormtv.py] title"+item.title)
		title=item.title.lower()
		if (storm_channel_name=="divxonline"):
			title=stormlib.servers_divxonline(title)
		if (SERVERS!="0"):
			if (SERVERS=="1"):
				#seriesdanko no tiene el nombre del server en el titulo, sino en el thumbnail
				if (storm_channel_name=="seriesdanko"):
					matches_free=re.compile(pat_free,re.DOTALL).findall(item.thumbnail)
					#logger.info("matches[0]"+matches_free[0])
					if (len(matches_free)>0):
					   item.title=item.title+" ("+matches_free[0]+")"
					
				else:
					matches_free= re.compile(pat_free,re.DOTALL).findall(title)
				if (len(matches_free)>0):
					vserver=matches_free[0]
					if (DEBUG):logger.info("free"+title)
					strue=1
				else:
					strue=0
			elif (SERVERS=="2"):
				if (config.get_setting("fileniumpremium")=="true"):
					if (storm_channel_name=="seriesdanko"):                                                                                                            
					   matches_filenium=re.compile(pat_filenium,re.DOTALL).findall(item.thumbnail)
					   if (len(matches_filenium)>0):
						vserver=matches_filenium[0]
					   	item.title=item.title+" ("+matches_filenium[0]+")"
					   	#logger.info("matches[0]"+matches_filenium[0])                                                                       
					else:
						#if (storm_channel_name=="seriespepito"):
						#	matches_filenium= re.compile("Streamcloud",re.DOTALL).findall(item.title)
						#else:
						#titulo=item.title.lower()
					   	matches_filenium= re.compile(pat_filenium,re.DOTALL).findall(title)
					if (len(matches_filenium)>0):
						vserver=matches_filenium[0]
						if (DEBUG):logger.info("Filenium"+item.title)
						print ("[stormtv.py] findvideos"+matches_filenium[0])
						strue=1
					else:
						strue=0
				if (config.get_setting("alldebridpremium")=="true"):
					if (storm_channel_name=="seriesdanko"):                                                                                                    
					   matches_all=re.compile(pat_all,re.DOTALL).findall(item.thumbnail)
					   if (len(matches_all)>0):                                              
					          item.title=item.title+" ("+matches_all[0]+")"                                                                   
					else:
					   matches_all=re.compile(pat_all,re.DOTALL).findall(title)
					if (len(matches_all)>0):
						vserver=matches_all[0]
						if (DEBUG): logger.info("Alldebrid"+item.title)
						strue=1
					else:
						strue=0
				if (config.get_setting("realdebridpremium")=="true"):
					if (storm_channel_name=="seriesdanko"):                                                                                                    
					   matches_real=re.compile(pat_real,re.DOTALL).findall(item.thumbnail)                                                                    
					   if (len(matches_real)>0):                                              
					      item.title=item.title+" ("+matches_real[0]+")"	
					else:
					   matches_real=re.compile(pat_real,re.DOTALL).findall(title)
					if (len(matches_real)>0):
						vserver=matches_real[0]
						if (DEBUG):logger.info("Real"+item.title)
						strue=1
					else:
						strue=0
		else:
			if (DEBUG):logger.info("[stormtv.py] strue=1")
			if (storm_channel_name=="seriesdanko"):                                                                                                           
                                        matches_all_servers=re.compile(pat_all_servers,re.DOTALL).findall(item.thumbnail)                                                                       
                                        if (len(matches_all_servers)>0):                                                                                                   
                                           item.title=item.title+" ("+matches_all_servers[0]+")"                                                                           
                                                                                                                                                                    
                        else:                                                                                                                               
                                        matches_all_servers= re.compile(pat_all_servers,re.DOTALL).findall(title)                                                                 
                        if (len(matches_all_servers)>0):                                                                                                           
                                        vserver=matches_all_servers[0]                                                                                                     
                                        if (DEBUG):logger.info("all servers"+title)                                                                                        
                                        strue=1                                                                                                                     
                        else:                                                                                                                               
                                        strue=0
			#strue=1
		#Comprobamos si el enlace existe
		# de momento solo para filenium
		#if (config.get_setting("fileniumpremium")=="true"):
			#logger.info("[stormtv.py] findvideos"+matches_filenium[0])	
			#exec "import servers."+matches_filenium[0]+" as tserver" 
			#res,test= tserver.test_vide_exists(item.url)                                                                                                   
			#logger.info("[stormtv.py] findvideos"+res+"#"+test)
		#Comprobamos el idioma
		if ((LANG!="0")&(strue==1)):
			logger.info("lang="+item.title)
			if (storm_channel_name=="serieonline"):                                                                                                                           
			   item.title=stormlib.audio_serieonline(item.title)	
			elif ((storm_channel_name=="seriesyonkis")or (storm_channel_name=="peliculasyonkis_generico")):
			   item.title=stormlib.audio_seriesyonkis(item.title)
			patron_vos='VOS|Sub'                                                                                                                                              
			matches_vos = re.compile(patron_vos,re.DOTALL).findall(item.title)	
			patron_vo='VO(?!S)'                                                                                                                                               
			matches_vo = re.compile(patron_vo,re.DOTALL).findall(item.title)
			patron_spa='Espa|spa'                                                                                                                                               
			matches_spa = re.compile(patron_spa,re.DOTALL).findall(item.title) 	
			if (len(matches_vos)>0):
				if (LANG in ["2","4","6","0"]):
					if (DEBUG):logger.info("[stormlib.py] findvideos: encontrado match vos")
					ltrue=1
				else:
					ltrue=0
			elif (len(matches_vo)>0):
				if (LANG in ["3","5","6","0"]):
					if (DEBUG):logger.info("[stormlib.py] findvideos: encontrado match vo")
					ltrue=1                                                                                                                                   
				else:
					ltrue=0
			elif (len(matches_spa)>0):
				if (LANG in ["1","4","5","0"]):
					if(DEBUG):logger.info("[stormlib.py] findvideos: encontrado match spa")
					ltrue=1
				else:
					ltrue=0
			else:
				if (DEBUG):logger.info("[stormlib.py] findvideos: No se ha encontrado ningun tipo.")
				ltrue=1
		else:
			if (DEBUG):logger.info("[stormtv.py] ltrue=0")
			ltrue=1
		if ((strue==1)&(ltrue==1)):                                                                                                                                           
                #seriesyonkis es un poco distinto para comprobar, de momento hacemos bypass :)                                                                                    
                 if ((storm_channel_name<>"seriespepito")and(storm_channel_name<>"peliculaspepito")and(storm_channel_name<>"seriesflv") and (storm_channel_name<>"cinehanwer")): 
                   if ((vserver not in verified)&(vserver not in excluded)):                                                                                                      
                           try:                                                                                                                                                   
                              exec "import servers."+vserver+" as tserver"                                                                                                        
                           except:                                                                                                                                                
                                print "[stormtv.py] Free Verify no existe el servidor"                                                                                            
                           try:                                                                                                                                                   
                              data =scrapertools.cache_page(item.url)                                                                                                             
                           except:                                                                                                                                                
                                print "[stormtv.py] Free Verify no se puede descargar la pagina"                                                                                  
                           #Shurweb y otros canales que usan la funcion generica de findvideos tienen el enlace directamente, no hay que descargar la pagina.                     
                           if ((storm_channel_name<>"shurweb")&(storm_channel_name<>"animeflv")):                                                                                 
                                print "dentro del if<>shurweb"                                                                                                                   
                                try:                                                                                                                                              
                                        resultado = tserver.find_videos(data)                                                                                                     
                                except:                                                                                                                                           
                                        print "[stormtv.py] Free Verify no find_videos"                                                                                           
                                try:
					if (vserver=="torrent"):
						res=True
						test=""
					else:                                                                                                                                              
                                        	res,test= tserver.test_video_exists(resultado[0][1])                                                                                      
                                except:                                                                                                                                           
                                        print "[stormtv.py] Free Verified fallo test_video_exist "+vserver                                                                        
                                        res=False                                                                                                                                 
                           else:                                                                                                                                                  
                                print "dentro del else<>shurweb"                                                                                                                 
                                try:                                                                                                                                              
                                        res,test= tserver.test_video_exists(data)                                                                                                 
                                except:                                                                                                                                           
                                        print "[stormtv.py] Verified fallo test_video_exist "+vserver                                                                             
                                        res=False                                                                                                                                 
                           if (res):                                                                                                                                              
                              print("[stormtv.py] Free Verify"+"True#"+test)                                                                                                      
			      if (vserver.upper() in dictionary):
				   item.title="[Verificado]"+dictionary[vserver.upper()]+item.title
			      else:
			      	   item.title="[Verificado]"+item.title                                                                                                                
                              verified.append(vserver)                                                                                                                            
                              strue=1                                                                                                                                             
                           else:                                                                                                                                                  
                              print("[stormtv.py] findvideos false")                                                                                                              
                              strue=0             
		if ((strue==1)&(ltrue==1)):
			##############Anadido para guardar los enlaces en un fichero############
			#entry = doc.createElement('Link')                                 
			#base.appendChild(entry)                                             
			#name=doc.createElement('Name')                                      
			#entry.appendChild(name)                                          
			#name_content = doc.createTextNode(item.title)
			#name.appendChild(name_content)                                   
			#url=doc.createElement('Url')                                  
			#entry.appendChild(url)                                           
			#url_content = doc.createTextNode(item.url)                       
			#url.appendChild(url_content)
			###############################################
                        storm_itemlist.append( Item(channel=__channel__, action="play" , title=item.title, fulltitle=storm_channel_name , url=item.url, thumbnail=storm_thumbnail,  plot=storm_plot, folder=False, fanart=storm_fanart,show = storm_show,extra=storm_chapter, server=vserver)) 	 
	if (SERVERS=="2"):
		storm_itemlist.append( Item(channel=__channel__, action="free" , title="Buscar gratuitos", fulltitle=storm_channel_name , url=free_url, thumbnail=storm_thumbnail,plot=storm_plot, fanart=storm_fanart,show = storm_show,extra=storm_chapter))
	##################################
	#f = open("/storage/vos.xml", 'w')                                      
    	#doc.writexml(f)                                                         
    	#f.close()       
	################################
	return sorted(storm_itemlist, key=lambda item: item.title,  reverse=True) 

def free(item):
        logger.info("[stormtv.py] Free")                                                                                                                                    
        storm_fanart=item.fanart                                                                                                                                                  
        storm_plot=item.plot                                                                                                                                                      
        storm_thumbnail=item.thumbnail                                                                                                                                            
        storm_chapter=item.extra                                                                                                                                                  
        storm_show=item.show                                                                                                                                                      
        storm_channel_name=item.fulltitle                                                                                                                                         
        storm_title=item.title                                                                                                                                                    
        free_url=item.url                                                                                                                                                         
        action="findvideos"                                                                                                                                                       
        item=Item(channel=__channel__,url=item.url)                                                                                                                               
        exec "import pelisalacarta.channels."+storm_channel_name+" as channel"                                                                                                    
        # El action nos devolvera el listado de posibles enlaces                                                                                                                  
        exec "itemlist = channel."+action+"(item)"                                                                                                                                
        storm_itemlist=[]                                                                                                                                                         
        #lang=1              
	# creamos la cadena de servidores free                                                                                                                                    
	pat_free="("                                                                                                                                                              
	for fserver in servertools.FREE_SERVERS:                                                                                                                                  
	    pat_free=pat_free+fserver+"|"                                                                                                                                     
	pat_free=pat_free[:len(pat_free)-1]+")"
	strue=0                                                                                                                                                                   
	ltrue=0 
	#Verified contendrá la lista de servidores que hemos podido comprobar
	verified=[]
	#Excluded contendrá los servidores que no podemos verificar
	excluded=[]
	excluded.append("letitbit")                                                                                                                                                                  
	for item in itemlist:
	    #Si el canal es shurweb le añadimos (spa)                                                                                                                         
            if (storm_channel_name=="shurweb"):                                                                                                                               
                item.title=item.title+" (spa)"
	    title=item.title.lower()
	    if (storm_channel_name=="seriesdanko"):                                                                                                           
	       matches_free=re.compile(pat_free,re.DOTALL).findall(item.thumbnail)
	       if (len(matches_free)>0):                                                                  
	          item.title=item.title+" ("+matches_free[0]+")"                                                                      
	    else:                                                                                                                                                     
	       matches_free= re.compile(pat_free,re.DOTALL).findall(title)                                                                                  
	    if (len(matches_free)>0):                                                                                                                         
	        logger.info("[stormtv.py] Free :"+item.title) 
		vserver=matches_free[0]                                                                                                           
	        strue=1                                                                                                                                   
	    else:                                                                                                                                             
	        strue=0 
        #Comprobamos el idioma                                                                                                                                            
	    if (LANG!="0"):                                                                                                                                                     
	   	if (storm_channel_name=="serieonline"):                                                                                                                   
	      		item.title=stormlib.audio_serieonline(item.title)                                                                                                      
	   	elif ((storm_channel_name=="seriesyonkis")or(storm_channel_name=="peliculasyonkis_generico")):
	   	        item.title=stormlib.audio_seriesyonkis(item.title)	
	   	patron_vos='VOS|Sub'                                                                                                                                      
	   	matches_vos = re.compile(patron_vos,re.DOTALL).findall(item.title)                                                                                        
	   	patron_vo='VO(?!S)'                                                                                                                                       
	   	matches_vo = re.compile(patron_vo,re.DOTALL).findall(item.title)                                                                                          
	   	patron_spa='Espa'                                                                                                                                         
	   	matches_spa = re.compile(patron_spa,re.DOTALL).findall(item.title)                                                                                        
	   	if (len(matches_vos)>0):
			if (LANG in ["2","4","6","0"]):                                                                                                                           
		    		if (DEBUG): logger.info("[stormlib.py] findvideos: encontrado match vos")                                                                             
		    		ltrue=1                                                                                                                                   
			else:                                                                                                                                             
		    		ltrue=0                                                                                                                                   
	   	elif (len(matches_vo)>0):                                                                                                                                 
		  	if (LANG in ["3","5","6","0"]):                                                                                                                           
		     		if (DEBUG): logger.info("[stormlib.py] findvideos: encontrado match vo")                                                                              
		     		ltrue=1                                                                                                                                   
		  	else:                                                                                                                                             
		     		ltrue=0
	   	elif (len(matches_spa)>0):                                                                                                                                
	          	if (LANG in ["1","4","5","0"]):                                                                                                                           
	             		if (DEBUG): logger.info("[stormlib.py] findvideos: encontrado match spa")                                                                             
	             		ltrue=1                                                                                                                                   
	          	else:                                                                                                                                             
	             		ltrue=0                                                                                                                                   
	   	else:                                                                                                                                                     
	          	if (DEBUG): logger.info("[stormlib.py] findvideos: No se ha encontrado ningun tipo.")                                                                         
      	          	ltrue=1                                                                                                                                           
	    else:                                                                                                                                                             
	    	ltrue=1
	
	    if ((strue==1)&(ltrue==1)):
		#seriesyonkis es un poco distinto para comprobar, de momento hacemos bypass :)
	        if ((storm_channel_name<>"seriesyonkis")and (storm_channel_name<>"peliculasyonkis_generico")):                                                        
                   if ((vserver not in verified)&(vserver not in excluded)):                         
                           try:                                                                      
                              exec "import servers."+vserver+" as tserver"                           
                           except:                                                                   
                                print "[stormtv.py] Free Verify no existe el servidor"                  
                           try:                                                                      
                              data =scrapertools.cache_page(item.url)                                
                           except:                                                                   
                                print "[stormtv.py] Free Verify no se puede descargar la pagina" 
			   #Shurweb y otros canales que usan la funcion generica de findvideos tienen el enlace directamente, no hay que descargar la pagina.       
                           if ((storm_channel_name<>"shurweb")&(storm_channel_name<>"animeflv")):                                                  
                                #print "dentro del if<>shurweb"                                       
                                try:                                                                 
                                        resultado = tserver.find_videos(data)                        
                                except:                                                              
                                        print "[stormtv.py] Free Verify no find_videos"                 
                                try:                                                                 
                                        res,test= tserver.test_video_exists(resultado[0][1])                                                                                      
                                except:                                                                                                                                           
                                        print "[stormtv.py] Free Verified fallo test_video_exist "+vserver                                                                             
                                        res=False                                                                                                                                 
                           else:                                                                                                                                                  
                                #print "dentro del else<>shurweb"                                                                                                                  
                                try:                                                                                                                                              
                                        res,test= tserver.test_video_exists(data)                                                                                                 
                                except:                                                                                                                                           
                                        print "[stormtv.py] Verified fallo test_video_exist "+vserver                                                                             
                                        res=False                                                                                                                                 
                           if (res):                                                                                                                                              
                              print("[stormtv.py] Free Verify"+"True#"+test)                                                                                                       
                              item.title="[Verificado]"+item.title                                                                                                                
                              verified.append(vserver)                                                                                                                            
                              strue=1                                                                                                                                             
                           else:                                                                                                                                                  
                              print("[stormtv.py] findvideos false")                                                                                                              
                              strue=0
		if ((strue==1)&(ltrue==1)):
             		storm_itemlist.append( Item(channel=__channel__, action="play" , title=item.title, fulltitle=storm_channel_name , url=item.url, thumbnail=storm_thumbnail, plot=storm_plot, folder=False,fanart=storm_fanart,show = storm_show,extra=storm_chapter, server=vserver))	
	#return storm_itemlist
	return sorted(storm_itemlist, key=lambda item: item.title,  reverse=True)    	   
def play(item):
	serverlist=["animeflv","shurweb","divxatope"]	
	logger.info("[stormtv.py] Play")
	storm_fanart=item.fanart
	storm_plot=item.plot
	storm_thumbnail=item.thumbnail
	storm_chapter=item.extra
	storm_show=item.show
	storm_channel_name=item.fulltitle
	storm_title=item.title
	action="play"
	if (config.get_setting("stormtvaccount")=="true"):                                                                                                                        
	   from core import stormlib                                                                                                                                        
	   stormlib.setwatched(storm_show,storm_chapter)
	   logger.info("[stormtv.py] Play"+storm_show+"mm"+storm_chapter)
	   if ((storm_channel_name =='peliculasyonkis_generico') or (storm_channel_name=='seriesyonkis')):
		item_storm=Item(channel=__channel__,url=item.url,server=item.server,title=item.title, thumbnail=item.thumbnail, plot=item.plot)
		itemlist=stormlib.play_yonkis(item_storm)
	   elif ((storm_channel_name=="seriesflv")or (storm_channel_name=="seriespepito") or (storm_channel_name=="peliculaspepito") or (storm_channel_name=="cinehanwer")):
		itemlist=[]
		exec "import pelisalacarta.channels."+storm_channel_name+" as channel"
		try:
			exec "itemlist = channel."+action+"(item)"
			return itemlist
		except: pass
	   elif (storm_channel_name not in serverlist):
		item_storm=Item(channel=__channel__,url=item.url,server=item.server,title=item.title, thumbnail=item.thumbnail, plot=item.plot)
		itemlist=stormlib.find_video_storm(item_storm)
	#print itemlist[0].title
	#exec "import pelisalacarta.channels."+storm_channel_name+" as channel"                                                                                                          
	# El action nos devolvera el enlace que se reproducira
	#try:                                                                                                                  
	#	exec "itemlist = channel."+action+"(item_storm)"
	#	#return itemlist
	   else:
		#from platformcode.xbmc import xbmctools
		itemlist=[]	
		itemlist.append(Item(channel="shurweb", server=item.server, url=item.url, category=item.category, title=item.title, thumbnail=item.thumbnail, plot=item.plot,  extra=item.extra, subtitle=item.subtitle,  fulltitle=item.fulltitle)) 
	return itemlist
	                 	
# VerificaciÃ³n automÃ¡tica de canales: Esta funciÃ³n debe devolver "True" si estÃ¡ ok el canal.
def test():
    from servers import servertools
    
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vÃ­deos de "Novedades" devuelve mirrors
    episode_items = lastepisodes(mainlist_items[0])
    bien = False
    for episode_item in episode_items:
        mediaurls = findvideos( episode_item )
        if len(mediaurls)>0:
            return True

    return False