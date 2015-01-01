# -*- coding: utf-8 -*-
import urllib

import scrapertools
import config
import logger
import urlparse

def login(username,password):
    logger.info("pyload_client.login")

    #url = config.get_setting("pyload")+"/api/login"
    api_url = urlparse.urljoin(config.get_setting("pyload"),"/api/login")
    logger.info("pyload_client.login api_url="+api_url)

    data = scrapertools.cache_page( api_url , post=urllib.urlencode( {"username":username,"password":password} ) )
    logger.info("pyload_client.login data="+data)
    return data

def download(url,package_name):
    logger.info("pyload_client.download url="+url+", package_name="+package_name)

    session = login(config.get_setting("pyload_user"),config.get_setting("pyload_password"))

    package_id = find_package_id(package_name)

    if package_id is None:
        api_url = urlparse.urljoin(config.get_setting("pyload"),"/api/addPackage")
        logger.info("pyload_client.download api_url="+api_url)

        data = scrapertools.cache_page( api_url , post=urllib.urlencode( {"name":"'"+package_name+"'","links":str([url])} ) )
        logger.info("pyload_client.download data="+data)
    else:
        api_url = urlparse.urljoin(config.get_setting("pyload"),"/api/addFiles")
        logger.info("pyload_client.download api_url="+api_url)

        data = scrapertools.cache_page( api_url , post=urllib.urlencode( {"pid":str(package_id),"links":str([url])} ) )
        logger.info("pyload_client.download data="+data)

    return

def find_package_id(package_name):
    logger.info("pyload_client.find_package_id package_name="+package_name)

    api_url = urlparse.urljoin(config.get_setting("pyload"),"/api/getQueue")
    logger.info("pyload_client.find_package_id api_url="+api_url)

    data = scrapertools.cache_page( api_url )
    logger.info("pyload_client.find_package_id data="+data)

    try:
        package_id = scrapertools.get_match(data,'"name"\s*:\s*"'+package_name+'".*?"pid"\s*\:\s*(\d+)')
    except:
        package_id = None

    return package_id
