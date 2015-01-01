# -*- coding: utf-8 -*-

import os
import sys
import re
import xbmc
import xbmcgui
from xbmcaddon import Addon
from core import config
from core import logger
from core import scrapertools

import urllib2, urllib, httplib, time

__settings__ = Addon( "plugin.video.pelisalacarta" )
__addonDir__ = __settings__.getAddonInfo( "path" )

DEFAULT_CAPTCHA = os.path.join( __addonDir__, "resources","images","noimage.gif")

ACTION_PARENT_DIR     = 9
ACTION_PREVIOUS_MENU  = 10
ACTION_CONTEXT_MENU   = 117

CTRL_ID_BACK = 8
CTRL_ID_SPACE = 32
CTRL_ID_RETN = 300
CTRL_ID_MAYS = 302
CTRL_ID_CAPS = 303
CTRL_ID_SYMB = 304
CTRL_ID_IP = 307
CTRL_ID_TEXT = 310
CTRL_ID_HEAD = 311
CTRL_ID_HZLIST = 402

CTRL_ID_CAPTCHA = 4002

class InputWindow(xbmcgui.WindowXMLDialog):
    def __init__( self, *args, **kwargs ):
        self.totalpage = 1
        self.nowpage = 0
        self.words = ''
        self.inputString = kwargs.get( "default" ) or ""
        self.heading = kwargs.get( "heading" ) or ""
        self.captcha = kwargs.get( "captcha" ) or ""
        
        if(self.captcha==""):
            self.captcha=DEFAULT_CAPTCHA
        
        xbmcgui.WindowXMLDialog.__init__( self, *args, **kwargs )

    def onInit(self):
        self.setKeyOnKeyboard()
        self.getControl(CTRL_ID_HEAD).setLabel(self.heading)
        self.getControl(CTRL_ID_TEXT).setLabel(self.inputString)
        self.getControl(CTRL_ID_CAPTCHA).setImage(self.captcha)        
        self.confirmed = False

    def onFocus( self, controlId ):
        self.controlId = controlId
        

    def onClick( self, controlID ):   
        
        if controlID == CTRL_ID_CAPS:#big
            self.getControl(CTRL_ID_SYMB).setSelected(False)
            if self.getControl(CTRL_ID_CAPS).isSelected():
                self.getControl(CTRL_ID_MAYS).setSelected(False)
            self.setKeyOnKeyboard()
        elif controlID == CTRL_ID_IP:#ip
            dialog = xbmcgui.Dialog()
            value = dialog.numeric( 3, "Introduce la IP", '' )
            self.getControl(CTRL_ID_TEXT).setLabel(self.getControl(CTRL_ID_TEXT).getLabel()+value)
        elif controlID == CTRL_ID_SYMB:#num
            self.getControl(CTRL_ID_MAYS).setSelected(False)
            self.getControl(CTRL_ID_CAPS).setSelected(False)
            self.setKeyOnKeyboard()
        elif controlID == CTRL_ID_MAYS:
            self.getControl(CTRL_ID_SYMB).setSelected(False)
            if self.getControl(CTRL_ID_MAYS).isSelected():
                self.getControl(CTRL_ID_CAPS).setSelected(False)
            self.setKeyOnKeyboard()
        elif controlID == CTRL_ID_BACK:#back
            self.getControl(CTRL_ID_TEXT).setLabel(self.getControl(CTRL_ID_TEXT).getLabel().decode("utf-8")[0:-1])
        elif controlID == CTRL_ID_RETN:#enter
            newText = self.getControl(CTRL_ID_TEXT).getLabel()
            if not newText: return
            self.inputString = newText
            self.confirmed = True
            self.close()
        elif controlID == CTRL_ID_SPACE:#space
            self.getControl(CTRL_ID_TEXT).setLabel(self.getControl(CTRL_ID_TEXT).getLabel() + ' ')
            self.disableMayus()
        
        else:
            self.getControl(CTRL_ID_TEXT).setLabel(self.getControl(CTRL_ID_TEXT).getLabel()+self.getControl(controlID).getLabel().encode('utf-8'))
            self.disableMayus()        

    def onAction(self,action):
        #s1 = str(action.getId())
        #s2 = str(action.getButtonCode())
        #print "======="+s1+"========="+s2+"=========="
        
        if action == ACTION_PREVIOUS_MENU:
            self.close()
        else:
            id =   action.getId()                     
            keycode = action.getButtonCode()
            if keycode >= 61505 and keycode <= 61530:
                if self.getControl(CTRL_ID_CAPS).isSelected() or self.getControl(CTRL_ID_MAYS).isSelected():
                    keychar = chr(keycode - 61505 + ord('A'))
                else:
                    keychar = chr(keycode - 61505 + ord('a'))
                self.getControl(CTRL_ID_TEXT).setLabel(self.getControl(CTRL_ID_TEXT).getLabel()+keychar) 
                self.disableMayus()
        
            elif keycode >= 192577 and keycode <= 192602:
                if self.getControl(CTRL_ID_CAPS).isSelected() or self.getControl(CTRL_ID_MAYS).isSelected():
                    keychar = chr(keycode - 192577 + ord('a'))
                else:
                    keychar = chr(keycode - 192577 + ord('A'))                
                self.getControl(CTRL_ID_TEXT).setLabel(self.getControl(CTRL_ID_TEXT).getLabel()+keychar)  
                self.disableMayus()
          
            elif keycode >= 61536 and keycode <= 61545:
                self.onClick( keycode-61536+48 )
            elif keycode == 61472:
                self.onClick( CTRL_ID_SPACE )
            elif keycode == 61448:
                self.onClick( CTRL_ID_BACK )         
            elif(keycode!=0):
                s = "Unattended keycode: " + str(action.getButtonCode())
                logger.error( "%s" % s  ) 
       
    def disableMayus(self):
        if self.getControl(CTRL_ID_MAYS).isSelected():                
                self.getControl(CTRL_ID_MAYS).setSelected(False)
                self.setKeyOnKeyboard()     

    def setKeyOnKeyboard (self):
        if self.getControl(CTRL_ID_SYMB).isSelected():
            #if self.getControl(CTRL_ID_LANG).isSelected():
            #    pass
            #else:
                i = 48
                for c in ')!@#$%^&*(':
                    self.getControl(i).setLabel(c)
                    i+=1
                    if i > 57: break
                i = 65
                for c in '[]{}-_=+;:\'",.<>/?\\|`~':
                    self.getControl(i).setLabel(c)
                    i+=1
                    if i > 90: break
                for j in range(i,90+1):
                    self.getControl(j).setLabel('')
        else:
            for i in range(48, 57+1):
                keychar = chr(i - 48 + ord('0'))
                self.getControl(i).setLabel(keychar)
            if self.getControl(CTRL_ID_CAPS).isSelected() or self.getControl(CTRL_ID_MAYS).isSelected():
                for i in range(65, 90+1):
                    keychar = chr(i - 65 + ord('A'))                        
                    self.getControl(i).setLabel(keychar)
            else:
                for i in range(65, 90+1):
                    keychar = chr(i - 65 + ord('a'))
                    self.getControl(i).setLabel(keychar)


    def isConfirmed(self):
        return self.confirmed

    def getText(self):
        return self.inputString 

class Keyboard:
    def __init__( self, default='', heading='' , captcha=''):
        self.confirmed = False
        self.inputString = default
        self.heading = heading
        self.captcha = captcha
        
    def initializeImage(self):
        #EL captcha no lo recuoera, por lo que lo guardamos en fichero
        try:
            if(self.captcha==""):
                self.captcha = DEFAULT_CAPTCHA
            else:
                nombre_fichero_config_canal = os.path.join( config.get_data_path() , "captcha.img" )   
                webFile = urllib.urlopen(self.captcha)
                localFile = open(nombre_fichero_config_canal, "wb")
                localFile.write(webFile.read())
                webFile.close()
                localFile.close()   
                self.captcha = nombre_fichero_config_canal
        except:
            self.captcha = DEFAULT_CAPTCHA
            import sys
            for line in sys.exc_info():
                logger.error( "%s" % line )               
 
    def doModal (self):
        self.initializeImage()
        self.win = InputWindow("Captcha.xml", __addonDir__, "default", heading=self.heading, default=self.inputString, captcha=self.captcha )
        self.win.doModal()
        self.confirmed = self.win.isConfirmed()
        self.inputString = self.win.getText()
        del self.win

    def setHeading(self, heading):
        self.heading = heading

    def isConfirmed(self):
        return self.confirmed

    def getText(self):
        return self.inputString