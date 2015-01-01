# -*- coding: utf-8 -*-                                                                                                                                                        
#------------------------------------------------------------                                                                                                                     
# pelisalacarta - XBMC Plugin                                                                                                                                                     
# libreria para stormtv
# v0.5.1                                                                                                                                                      
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/                                                                                                                          
#------------------------------------------------------------                                                                                                                     
import urlparse,urllib2,urllib,re
import xml.dom.minidom as minidom                                                                                                                                                 
import urllib                                                                                                                                                                     
import os
from core import config
from core import scrapertools                                                                                                                                                     
from core.item import Item                                                                                                                                                        
from servers import servertools
__server__ = "oc1.lopezepol.com"

SERVER="https://"+__server__+"/stormtv/public/"
PATH=config.get_data_path()+"stormtv/temp/"
def mkdir_p(path):       
    try:                     
      os.makedirs(path)
    except OSError as exc: # Python >2.5                             
           if exc.errno == errno.EEXIST and os.path.isdir(path):
              pass                                                              
           else: raise 

def getpreferences():
    print "[stormlib.py] getpreferences "                     
    user_id=config.get_setting("stormtvuser")                                   
    user_pass=config.get_setting("stormtvpassword")                             
    #server= "https://"+__server__+"/stormtv_v2/public/"                             
    #path=config.get_data_path()+"stormtv_v2/temp/"
    if not os.path.exists(PATH):                                                
       print "Creating data_path "+PATH                                         
       try:                                                                     
         mkdir_p(PATH)                                                       
       except:                                                                  
         pass
    urllib.urlretrieve (SERVER+"followers/preferences/user/"+user_id+"/pass/"+user_pass, PATH+"preferences.xml")
    #comprobar si hay error de usuario
    xml=PATH+"preferences.xml"
    if not os.path.exists(xml):                                                                                         
       status="1"                                                                                                     
       print "[stormlib.py] getpreferences "+status  
    else: 
	doc = minidom.parse(xml)                                                                                            
	node = doc.documentElement                                                                                          
	error = doc.getElementsByTagName("error")                                                                         
	if (len(error)>0):
		status="1"                                                                                                                  
		print "[stormlib.py] getpreferences "+status
	else:
		status="0"                                                                                                                  
		print "[stormlib.py] getpreferences "+status     	
    return status   
def addfollow(tvs_id):
    print "[stormlib.py] addfollow "+config.get_data_path()
    user_id=config.get_setting("stormtvuser")
    user_pass=config.get_setting("stormtvpassword")
    #server= "https://"+__server__+"/stormtv_v2/public/"
    #path=config.get_data_path()+"stormtv/temp/"                                
    urllib.urlretrieve (SERVER+"tvseries/addfollow/user/"+user_id+"/pass/"+user_pass+"/tvs/"+tvs_id, PATH+"temp.xml")
    print "[stormlib.py] addfollow"

def removefollow(tvs_id):
    user_id=config.get_setting("stormtvuser")
    user_pass=config.get_setting("stormtvpassword")
    #server= "https://"+__server__+"/stormtv/public/"
    #path=config.get_data_path()+"stormtv/temp/"
    urllib.urlretrieve (SERVER+"tvseries/removefollow/user/"+user_id+"/pass/"+user_pass+"/tvs/"+tvs_id, PATH+"temp.xml")
    print "[stormlib.py] Remove follow"

def iswatched(title,chap_dictionary):
    watched=False
    patronchap="([0-9](x|X)[0-9]*)"                                                                                                                                                 
    matcheschap= re.compile(patronchap,re.DOTALL).findall(title)                                                                                                              
    if (len(matcheschap)>0):
    	print matcheschap[0][0]                                                                                                                                                     
    	if (matcheschap[0][0].lower() in chap_dictionary):                                                                                                                                   
       		status=chap_dictionary[matcheschap[0][0].lower()].encode("utf-8")                                                                                                                    
       		#print status                                                                                                                                                      
       		title=title+" ["+status+"]"                                                                                                                                               
       		watched=True
		#print chap_dictionary[matcheschap[0]]+"#"
	matches=matcheschap[0][0].lower()
    else:
	matches="false"
	watched=False
    return title, matches, watched

def getwatched(tvs_id):
    print "[stormlib.py] getwatched"+tvs_id
    user_id=config.get_setting("stormtvuser")
    user_pass=config.get_setting("stormtvpassword")
    chap_dictionary = {}                                                                                                                                                          
    #server= "https://"+__server__+"/stormtv/public/"                                                                                                                               
    #path=config.get_data_path()+"stormtv/temp/"                                                                                            
    urllib.urlretrieve (SERVER+"chapters/getstatus/user/"+user_id+"/pass/"+user_pass+"/tvs/"+tvs_id, PATH+"temp.xml")                                                              
    xml=PATH+"/"+"temp.xml"                                                                                                                                                       
    doc = minidom.parse(xml)                                                                                                                                                      
    node = doc.documentElement                                                                                                                                                    
    chapters = doc.getElementsByTagName("chapter")                                                                                                                                
    for chapter in chapters:                                                                                                                                                      
        number = chapter.getElementsByTagName("number")[0].childNodes[0].data                                                                                                 
        status = chapter.getElementsByTagName("status")[0].childNodes[0].data                                                                                                 
        chap_dictionary[number]=status                                                                                                                                        
        print number+chap_dictionary[number]+"#"
    return chap_dictionary

def getlang():
    print "[stormlib.py] getlang"
    #path=config.get_data_path()+"stormtv/temp/"
    xml=PATH+"/"+"preferences.xml"
    if not os.path.exists(xml):                                                                                         
        status="0"                                                                                                      
    else:                                                                                              
    	doc = minidom.parse(xml)                                                                                            
    	node = doc.documentElement
    	error = doc.getElementsByTagName("error")                                                                                  
    	if (len(error)>0):
    		status="0"                                                                                                         
    	else:                                                                                                                      
    		lang = doc.getElementsByTagName("Lang") 
    		status = lang[0].childNodes[0].data                                                                     
    print "[stormlib.py] getlang"+status
    return status  

def getservers():
    print "[stormlib.py] getlang"                                                                                                   
    #path=config.get_data_path()+"stormtv/temp/"                                                                                     
    xml=PATH+"/"+"preferences.xml"
    if not os.path.exists(xml):
    	status="0"
    else:                                                                                                          
    	doc = minidom.parse(xml)                                                                                                        
    	node = doc.documentElement
    	error = doc.getElementsByTagName("error")                                                                                  
    	if (len(error)>0):                                                                                                         
    	       	status="0"                                                                                                         
        else:                                                                                                      
    		servers = doc.getElementsByTagName("Servers")                                                                                         
    		status = servers[0].childNodes[0].data                                                                                             
    print "[stormlib.py] getservers"+status
    return status

def setwatched (tvs_id,chap_number):
    print"[stormlib.py] setwatched"+tvs_id+" "+chap_number
    user_id=config.get_setting("stormtvuser")
    user_pass=config.get_setting("stormtvpassword")
    #server= "https://"+__server__+"/stormtv/public/"                                                                                                                               
    #path=config.get_data_path()+"stormtv/temp/"
    print"[stormlib.py] setwatched "+SERVER+"chapters/add/tvs/"+tvs_id+"/user/"+user_id+"/pass/"+user_pass+"/chap/"+chap_number
    urllib.urlretrieve (SERVER+"chapters/add/tvs/"+tvs_id+"/user/"+user_id+"/pass/"+user_pass+"/chap/"+chap_number, PATH+"temp.xml")

def gettvslist (tvsl_id):
    print "[stormlib.py] gettvslist"+tvsl_id
    user_id=config.get_setting("stormtvuser")                                                                                                                                     
    user_pass=config.get_setting("stormtvpassword")                                                                                                                               
    #server= "https://"+__server__+"/stormtv/public/"                                                                                                                             
    #path=config.get_data_path()+"stormtv/temp/"                                                                                                                                  
    print"[stormlib.py] setwatched "+SERVER+"tvseries/tvslist/user/"+user_id+"/pass/"+user_pass+"/id/"+tvsl_id                                                  
    urllib.urlretrieve (SERVER+"tvseries/tvslist/user/"+user_id+"/pass/"+user_pass+"/id/"+tvsl_id, PATH+"temp.xml")
def getalltvslist():
    print "[stormlib.py] getalltvslist"                                                                                        
    user_id=config.get_setting("stormtvuser")                                                                                       
    user_pass=config.get_setting("stormtvpassword")                                                                                 
    #server= "https://"+__server__+"/stormtv/public/"                                                                               
    #path=config.get_data_path()+"stormtv/temp/"                                                                                    
    print"[stormlib.py] getalltvslist "+SERVER+"tvseries/alltvslist/user/"+user_id+"/pass/"+user_pass                     
    urllib.urlretrieve (SERVER+"tvseries/alltvslist/user/"+user_id+"/pass/"+user_pass, PATH+"temp.xml")    
def getpopular():
    print "[stormlib.py] getpopular"                                                                                             
    user_id=config.get_setting("stormtvuser")                                                                                       
    user_pass=config.get_setting("stormtvpassword")                                                                                 
    #server= "https://"+__server__+"/stormtv/public/"                                                                               
    #path=config.get_data_path()+"stormtv/temp/"                                                                                    
    print"[stormlib.py] getpopular "+SERVER+"tvseries/alltvslist/user/"+user_id+"/pass/"+user_pass                               
    urllib.urlretrieve (SERVER+"tvseries/popular/user/"+user_id+"/pass/"+user_pass, PATH+"temp.xml") 
def isfollow (tvs_id):
    print "[stormlib.py] isfollow"+ tvs_id
    user_id=config.get_setting("stormtvuser")                                                                                                   
    user_pass=config.get_setting("stormtvpassword")
    #server= "https://"+__server__+"/stormtv/public/"
    # Create data_path if not exists
    #path=config.get_data_path()+"stormtv/temp/"                                
    if not os.path.exists(PATH):                         
       print "Creating data_path "+PATH                                                             
       try:                                                        
           os.mkdir(PATH)                               
       except:                                            
           pass                                                                                                                                
    urllib.urlretrieve (SERVER+"tvseries/isfollow/user/"+user_id+"/pass/"+user_pass+"/tvs/"+tvs_id, PATH+"temp.xml")
    xml=PATH+"/"+"temp.xml"                                                                                                                        
    doc = minidom.parse(xml)                                                                                                                       
    node = doc.documentElement                                                                                                                 
    follow = doc.getElementsByTagName("follow")
    status = follow[0].childNodes[0].data
    print status
    return status

def audio_serieonline(title):
    print "[stormlib.py]audio_serionline "+title
    patron_vo="(audio Ingl�s, subtitulos no)"
    patron_vos="(audio Versi�n Original (V.O), subtitulos Espa�ol)"
    patron_vos2="(audio Ingl�s, subtitulos Espa�ol)"
    patron_spa="(audio Espa�ol, subtitulos no)"
    '''
    matches_vos = re.compile(patron_vos,re.DOTALL).findall(title)
    matches_vo = re.compile(patron_vo,re.DOTALL).findall(title)
    matches_spa = re.compile(patron_spa,re.DOTALL).findall(title)
    '''
    n_title=title.replace(patron_vo,"(VO)")
    n_title=n_title.replace(patron_vos,"(VOS)")
    n_title=n_title.replace(patron_vos2,"(VOS)")
    n_title=n_title.replace(patron_spa,"(Español)")
    return n_title
def combined(seasonepisode):
	print "[stormlib.py]combined "+seasonepisode
	patron = "(.*)x(.*)"
	matches = re.compile(patron,re.DOTALL).findall(seasonepisode)
	for season,episode in matches:
		sea=season
		epi=episode
	print "Season "+sea+" Episode "+epi
	return season,episode

def audio_seriesyonkis(title):
	print "[stormlib.py]audio_seriesyonkis "+title
    	patron_vo="[Audio:eng Subs:no]"           
        patron_vos="[Audio:eng Subs:eng]"
        patron_vos2="[Audio:eng Subs:spa]"
        patron_spa="[Audio:spa Subs:no]"
        '''      
        matches_vos = re.compile(patron_vos,re.DOTALL).findall(title)
        matches_vo = re.compile(patron_vo,re.DOTALL).findall(title)
        matches_spa = re.compile(patron_spa,re.DOTALL).findall(title)
        '''
        n_title=title.replace(patron_vo,"(VO)")
        n_title=n_title.replace(patron_vos,"(VOS)")
        n_title=n_title.replace(patron_vos2,"(VOS)")
        n_title=n_title.replace(patron_spa,"(Español)")
        return n_title
def servers_divxonline(title):
	print "[stormlib.py]servers_divxonline"+title
	patron_moe="moevideo"
	matches_moe= re.compile(patron_moe, re.DOTALL).findall(title)
	n_title= title.replace(patron_moe,"moevideos")
	n_title= title.replace("played","played.to")
	return n_title
def verify(itemlist):
	print "[stormlib.py] verify"		
	strue=1                                                                                                                                                           
	ltrue=1                                                                                                                                                           
        excluded=[]                                                                                                                                                       
        excluded.append("letitbit")
	storm_itemlist=[]
	verified=[]
	from core import scrapertools                                                                                                                                     
        from core.item import Item
	for item in itemlist:
		channel=item.fulltitle                                                                                                                                          
                print "[verify]channel:"+channel
		vserver=item.server                                                                                                                                       
                print "Server="+vserver+" URL="+item.url
		if (channel<>"seriesyonkis"):                                                                                                                  
                   if ((vserver not in verified)&(vserver not in excluded)):                                                                                                 
                	   try:                                                                                                                                                   
                              exec "import servers."+vserver+" as tserver"                                                                                                        
                           except:                                                                                                                                                
                                print "[stormtv.py] Verified no existe el servidor"                                                                                               
                           try:                                                                                                                                                   
                              data =scrapertools.cache_page(item.url)                                                                                                             
                           except:                                                                                                                                                
                                print "[stormtv.py] Verified no se puede descargar la pagina"
			   if (channel<>"shurweb"):                                                                                     
                           	print "dentro del if<>shurweb"
				try:                                                                                                                                                   
                              		resultado = tserver.find_videos(data)                                                                                                               
                           	except:                                                                                                                                                
                                	print "[stormtv.py] Verified no find_videos"                                                                                                       
                           	try:                                                                                                                                                   
                              		res,test= tserver.test_video_exists(resultado[0][1])                                                                                                
                           	except:                                                                                                                                                
                              		print "[stormtv.py] Verified fallo test_video_exist "+vserver                                                                                       
                              		res=False
			   else:
				print "dentro del else<>shurweb"
				try:
					res,test= tserver.test_video_exists(data)
				except:
					print "[stormtv.py] Verified fallo test_video_exist "+vserver                                                                             
                                        res=False                                                                                                                                           
                           if (res):                                                                                                                                              
                              print("[stormtv.py] findvideos"+"True#"+test)                                                                                                       
                              item.title="[Verificado]"+item.title                                                                                                                
                              verified.append(vserver)                                                                                                                            
                              strue=1                                                                                                                                             
                           else:                                                                                                                                                  
                              print("[stormtv.py] findvideos false")                                                                                                              
                              strue=0                                                                                                                                             
		if ((strue==1)&(ltrue==1)):                                                                                                                               
                	storm_itemlist.append( Item(channel=item.channel, action="play" , title=item.title, fulltitle=item.fulltitle , url=item.url, thumbnail=item.thumbnail, plot= item.plot, folder=False,fanart= item.fanart,show = item.show,extra=item.extra, server=item.server))  
	return storm_itemlist

def find_video_storm(item=None, data=None, channel=""):                                                                                                                           
    #logger.info("[launcher.py] findvideos")                                                                                                                                       
                                                                                                                                                                                  
    # Descarga la página                                                                                                                                                         
    if data is None:                                                                                                                                                              
        from core import scrapertools                                                                                                                                             
        data = scrapertools.cache_page(item.url)                                                                                                                                  
        #logger.info(data)                                                                                                                                                        
                                                                                                                                                                                  
    # Busca los enlaces a los videos                                                                                                                                              
    from core.item import Item                                                                                                                                                    
    from servers import servertools                                                                                                                                               
    listavideos = servertools.findvideosbyserver(data,item.server)                                                                                                                                    
    print "[find_video_storm] Server"+item.server                                                                                                                                                                             
    if item is None:                                                                                                                                                              
        item = Item()                                                                                                                                                             
                                                                                                                                                                                  
    itemlist = []                                                                                                                                                                 
    for video in listavideos:                                                                                                                                                     
        scrapedtitle = item.title.strip() + " - " + video[0].strip()                                                                                                              
        scrapedurl = video[1]                                                                                                                                                     
        server = video[2]                                                                                                                                                         
                                                                                                                                                                                  
        itemlist.append( Item(channel=item.channel, title=scrapedtitle , action="play" , server=item.server, page=item.page, url=scrapedurl, thumbnail=item.thumbnail, show=item.show , plot=item.plot , folder=False) )
                                                                                                                                                                                  
    return itemlist 
def play_yonkis(item):                                                                                                                                                                   
    print "[seriesyonkis.py] play"                                                                                                                                         
    itemlist = []                                                                                                                                                                 
                                                                                                                                                                                  
    # Descarga la página de reproducción de este episodio y server                                                                                                              
    #<a href="/s/y/597157/0/s/1244" target="_blank">Reproducir ahora</a>                                                                                                          
    #logger.info("[seriesyonkis.py] play url="+item.url)                                                                                                                           
    data = scrapertools.cache_page(item.url)                                                                                                                                      
    patron = '<a href="([^"]+)" target="_blank">\s*Reproducir ahora\s*</a>'                                                                                                       
    matches = re.compile(patron,re.DOTALL).findall(data)                                                                                                                          
    if len(matches)==0:                                                                                                                                                           
        patron = '<a href="([^"]+)" target="_blank">\s*Descargar ahora\s*</a>'                                                                                                    
        matches = re.compile(patron,re.DOTALL).findall(data)                                                                                                                      
                                                                                                                                                                                  
    if len(matches)==0:                                                                                                                                                           
        #logger.info("[seriesyonkis.py] play ERROR, no encuentro el enlace 'Reproducir ahora' o 'Descargar ahora'")                                                                
        return []                                                                                                                                                                 
                                                                                                                                                                                  
    playurl = urlparse.urljoin(item.url,matches[0])                                                                                                                               
    #logger.info("[seriesyonkis.py] play url="+playurl)                                                                                                                            
                                                                                                                                                                                  
    try:                                                                                                                                                                          
        location = scrapertools.getLocationHeaderFromResponse(playurl)                                                                                                            
        #logger.info("[seriesyonkis.py] play location="+location)                                                                                                                  
                                                                                                                                                                                  
        if location<>"":                                                                                                                                                          
            #logger.info("[seriesyonkis.py] Busca videos conocidos en la url")                                                                                                     
            videos = servertools.findvideosbyserver(location,item.server)                                                                                                                             
                                                                                                                                                                                  
            if len(videos)==0:                                                                                                                                                    
                location = scrapertools.getLocationHeaderFromResponse(location)                                                                                                   
                #logger.info("[seriesyonkis.py] play location="+location)                                                                                                          
                                                                                                                                                                                  
                if location<>"":                                                                                                                                                  
                    #logger.info("[seriesyonkis.py] Busca videos conocidos en la url")                                                                                             
                    videos = servertools.findvideosbyserver(location,item.server)                                                                                                                     
                                                                                                                                                                                  
                    if len(videos)==0:
                        #logger.info("[seriesyonkis.py] play downloading location")                                                                                                
                        data = scrapertools.cache_page(location)                                                                                                                  
                        #logger.info("------------------------------------------------------------")                                                                               
                        #logger.info(data)                                                                                                                                        
                        #logger.info("------------------------------------------------------------")                                                                               
                        videos = servertools.findvideosbyserver(data,item.server)                                                                                                                     
                        #logger.info(str(videos))                                                                                                                                  
                        #logger.info("------------------------------------------------------------")                                                                               
        else:                                                                                                                                                                     
            #logger.info("[seriesyonkis.py] play location vacía")                                                                                                                 
            videos=[]                                                                                                                                                             
                                                                                                                                                                                  
        if(len(videos)>0):                                                                                                                                                        
            url = videos[0][1]                                                                                                                                                    
            server=videos[0][2]                                                                                                                                                   
            itemlist.append( Item(channel=item.channel, action="play" , title=item.title, fulltitle=item.fulltitle , url=url, thumbnail=item.thumbnail, plot=item.plot, server=item.server, extra=item.extra, folder=False)) 
        else:                                                                                                                                                                     
            data = scrapertools.cache_page(playurl)                                                                                                                               
            patron='<ul class="form-login">(.*?)</ul'                                                                                                                             
            matches = re.compile(patron, re.S).findall(data)                                                                                                                      
            if(len(matches)>0):                                                                                                                                                   
                if "xbmc" in config.get_platform():                                                                                                                               
                    data = matches[0]                                                                                                                                             
                    #buscamos la public key                                                                                                                                       
                    patron='src="http://www.google.com/recaptcha/api/noscript\?k=([^"]+)"'                                                                                        
                    pkeys = re.compile(patron, re.S).findall(data)                                                                                                                
                    if(len(pkeys)>0):                                                                                                                                             
                        pkey=pkeys[0]                                                                                                                                             
                        #buscamos el id de challenge                                                                                                                              
                        data = scrapertools.cache_page("http://www.google.com/recaptcha/api/challenge?k="+pkey)                                                                   
                        patron="challenge.*?'([^']+)'"                                                                                                                            
                        challenges = re.compile(patron, re.S).findall(data)                                                                                                       
                        if(len(challenges)>0):                                                                                                                                    
                            challenge = challenges[0]                                                                                                                             
                            image = "http://www.google.com/recaptcha/api/image?c="+challenge                                                                                      
                                                                                                                                                                                  
                            #CAPTCHA                                                                                                                                              
                            exec "import pelisalacarta.captcha as plugin"                                                                                                         
                            tbd = plugin.Keyboard("","",image)
                            tbd.doModal()                                                                                                                                         
                            confirmed = tbd.isConfirmed()                                                                                                                         
                            if (confirmed):                                                                                                                                       
                                tecleado = tbd.getText()                                                                                                                          
                                #logger.info("tecleado="+tecleado)                                                                                                                 
                                sendcaptcha(playurl,challenge,tecleado)                                                                                                           
                            del tbd                                                                                                                                               
                            #tbd ya no existe                                                                                                                                     
                            if(confirmed and tecleado != ""):                                                                                                                     
                                itemlist = play(item)                                                                                                                             
                else:                                                                                                                                                             
                    itemlist.append( Item(channel=item.channel, action="error", title="El sitio web te requiere un captcha") )                                                    
                                                                                                                                                                                  
    except: 
	pass                                                                                                                                                                      
        #import sys                                                                                                                                                                
        #for line in sys.exc_info():                                                                                                                                               
        #    logger.error( "%s" % line )                                                                                                                                           
    #logger.info("len(itemlist)=%s" % len(itemlist))                                                                                                                               
    return itemlist


def get_filenium_status():                                                                                                                                                                 
    from xml.dom.minidom import Document                                            
    print "[Filenium.py] get_status"                                                                                                                                       
    url = "http://www.filenium.com"                                                                                                                                               
    # Descarga la página                                                                                                                                                         
    data = scrapertools.cachePage(url)                                                                                                                                            
    # Extrae las entradas                                                                                                                                                         
    patronvideos = '<p class="([^"]+)">([^"]+)</p>'                                                                                                                               
    matches = re.compile(patronvideos,re.DOTALL).findall(data)                                                                                                                    
    #if DEBUG: scrapertools.printMatches(matches)                                                                                                                                 
    itemlist = []                                                                                                                                                                 
    doc = Document()                                                                
    base= doc.createElement('Filenium')                                             
    doc.appendChild(base)

    for match in matches:                                                                                                                                                         
        #print match[0]+" "+match[1]
	entry = doc.createElement('Server')
	base.appendChild(entry)
	name=doc.createElement('Name')
	entry.appendChild(name)
	name_content = doc.createTextNode(match[1])
	name.appendChild(name_content)
	status=doc.createElement('Status')
	entry.appendChild(status)
	status_content = doc.createTextNode(match[0])
	status.appendChild(status_content)
    f = open(PATH+"filenium.xml", 'w')
    doc.writexml(f)
    f.close() 
#with codecs.open(PATH+"filenium.xml", "w", "utf-8") as out:
#    doc.writexml(out)
def filenium():
    print "[stormlib.py] filenium dictionary"                                                                                                                                       
    filenium_dictionary = {}                                                                                                                                                          
    #server= "https://"+__server__+"/stormtv/public/"                                                                                                                             
    #path=config.get_data_path()+"stormtv/temp/"                                                                                                                                  
    xml=PATH+"filenium.xml"                                                                                                                                                       
    doc = minidom.parse(xml)                                                                                                                                                      
    node = doc.documentElement                                                                                                                                                    
    servers = doc.getElementsByTagName("Server")                                                                                                                                
    for server in servers:                                                                                                                                                      
        name= server.getElementsByTagName("Name")[0].childNodes[0].data
	if (name=="Uploaded"):
		name="uploadedto"
	if (name=="Nowvideo.eu"):
		name="nowvideo"
        status = server.getElementsByTagName("Status")[0].childNodes[0].data
	if (status=="activehost"):
            stat="[A]"
	elif (status=="problemshost"):
	    stat="[P]"
	else:
	    stat="[I]"                                                                                         
        filenium_dictionary[name.upper()]=stat                                                                                                                                            
        print name+filenium_dictionary[name.upper()]+"#"                                                                                                                                  
    return  filenium_dictionary               
