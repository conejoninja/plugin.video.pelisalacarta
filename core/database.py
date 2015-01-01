import sqlite3

import logging.config
import logging
logging.config.fileConfig("logging.conf")
logger=logging.getLogger("database")

def get_connection(database_name):
    logger.info("get_connection(database_name=%s)" , database_name)
    conn = sqlite3.connect(database_name)

    cursor = conn.cursor()
    cursor.execute('create table if not exists "show" ( "channel_id" TEXT NOT NULL , "show_id" TEXT NOT NULL , "title" TEXT, "thumbnail" TEXT, "plot" TEXT, "disponible" TEXT)')
    cursor.close()

    safe_database_change(cursor,conn,'alter table "show" add column "url" TEXT')
    safe_database_change(cursor,conn,'alter table "show" add column "created" TEXT')
    safe_database_change(cursor,conn,'alter table "show" add column "deleted" TEXT')

    return conn

def safe_database_change(cursor,conn,text):
    try:
        cursor.execute(text)
        conn.commit()
    except:
        pass
    
def query(conn,query_text):
    logger.debug("query(query_text='%s')" , query_text)
    cursor = conn.cursor()

    cursor.execute(query_text)
    devuelve = cursor.fetchall()
    cursor.close()

    logger.debug("...devuelve %d filas" , len(devuelve))

    return devuelve

def get_numeric_value(conn,query_text,when_null=0):
    logger.debug('get_numeric_value(query_text="%s")' , query_text)
    cursor = conn.cursor()

    cursor.execute(query_text)
    devuelve = cursor.fetchall()
    cursor.close()
    
    if devuelve[0][0]==None:
        numero = when_null
    else:
        numero = int(devuelve[0][0])

    logger.debug("...devuelve [%d]" , numero)
    return numero

def get_single_value(conn,query_text):
    logger.debug("get_single_value(query_text='%s')" , query_text)
    cursor = conn.cursor()

    cursor.execute(query_text)
    devuelve = cursor.fetchall()
    cursor.close()

    logger.debug("...devuelve [%s]" , str(devuelve[0][0]))

    return devuelve[0][0]

def execute(conn,query):
    logger.debug("execute(query='%s')" , query)
    cursor = conn.cursor()

    cursor.execute(query)
    conn.commit()
    cursor.close()

def execute_parameters(conn,query,parameters):
    logger.debug("execute_parameters(query='%s',parameters=%s)" , query , str(parameters))
    cursor = conn.cursor()
    cursor.execute(query,parameters)
    conn.commit()
    cursor.close()
