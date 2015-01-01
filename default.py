# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta
# XBMC entry point
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

# Constants
__plugin__  = "pelisalacarta"
__author__  = "pelisalacarta"
__url__     = "http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/"
__date__ = "29/12/2014"
__version__ = "3.2.74"

import os
import sys
from core import config
from core import logger

logger.info("[default.py] pelisalacarta init...")

librerias = xbmc.translatePath( os.path.join( config.get_runtime_path(), 'lib' ) )
sys.path.append (librerias)

# Runs xbmc launcher
from platformcode.xbmc import launcher
launcher.run()