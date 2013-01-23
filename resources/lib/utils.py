# -*- coding: utf-8 -*-

# a collection of useful utilities

import re, os, sys, traceback
import xbmc

def list_to_string( item ):
    list_to_string = ""
    if not ( type( item ) is list ):
        list_to_string = item
    else:
        if len( item ) > 1:
            list_to_string = " / ".join( item )
        else:
            list_to_string = "".join( item )
    return list_to_string

def settings_to_log( settings_path, script_heading="[utils.py]" ):
    try:
        xbmc.log( "%s - Settings\n" % script_heading, level=xbmc.LOGDEBUG)
        # set base watched file path
        base_path = os.path.join( settings_path, "settings.xml" )
        # open path
        usock = open( base_path, "r" )
        u_read = usock.read()
        settings_list = u_read.replace("<settings>\n","").replace("</settings>\n","").split("/>\n")
        # close socket
        usock.close()
        for set in settings_list:
            match = re.search('    <setting id="(.*?)" value="(.*?)"', set)
            if match:
                xbmc.log( "%s - %30s: %s" % ( script_heading, match.group(1), match.group(2) ), level=xbmc.LOGDEBUG)
    except:
        traceback.print_exc()
