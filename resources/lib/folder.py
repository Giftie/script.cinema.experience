# -*- coding: utf-8 -*-

import sys, os, re
import xbmc

def dirEntries( dir_name, media_type="files", recursive="FALSE", contains="" ):
    '''Returns a list of valid XBMC files from a given directory(folder)

       Method to call:
       dirEntries( dir_name, media_type, recursive )
            dir_name   - the name of the directory to be searched
            media_type - valid types: video, music, pictures, files, programs
            recursive  - Setting to "TRUE" searches Parent and subdirectories, Setting to "FALSE" only search Parent Directory
    '''
    xbmc.log( "[folder.py] - dirEntries Activated", level=xbmc.LOGDEBUG )
    fileList = []
    json_query = '{"jsonrpc": "2.0", "method": "Files.GetDirectory", "params": {"directory": "%s", "media": "%s"}, "id": 1}' % ( escapeDirJSON( dir_name ), media_type )
    json_folder_detail = xbmc.executeJSONRPC(json_query)
    xbmc.log( "[folder.py] - json_folder_detail -\n%s" % json_folder_detail, level=xbmc.LOGDEBUG )
    file_detail = re.compile( "{(.*?)}", re.DOTALL ).findall(json_folder_detail)
    for f in file_detail:
        match = re.search( '"file" : "(.*?)",', f )
        if not match:
            match = re.search( '"file":"(.*?)",', f )
        if match:
            if match.group(1).endswith( "/" ) or match.group(1).endswith( "\\" ):
                if recursive == "TRUE":
                    fileList.extend( dirEntries( match.group(1), media_type, recursive, contains ) )
            elif not contains or ( contains and (contains in match.group(1) ) ):
                fileList.append( match.group(1) )
            xbmc.log( "[folder.py] - File Path: %s" % match.group(1), level=xbmc.LOGDEBUG ) 
        else:
            continue
    return fileList

def getFolders( dir_name, recursive="FALSE" ):
    '''Returns a list of valid XBMC files from a given directory(folder)

       Method to call:
       getFolders( dir_name, , recursive )
            dir_name   - the name of the directory to be searched
            recursive  - Setting to "TRUE" searches Parent and subdirectories, Setting to "FALSE" only search Parent Directory
    '''
    xbmc.log( "[folder.py] - getFolders Activated", level=xbmc.LOGDEBUG )
    folderList = []
    json_query = '{"jsonrpc": "2.0", "method": "Files.GetDirectory", "params": {"directory": "%s", "media": "files"}, "id": 1}' % ( escapeDirJSON( dir_name ) )
    json_folder_detail = xbmc.executeJSONRPC(json_query)
    xbmc.log( "[folder.py] - json_folder_detail -\n%s" % json_folder_detail, level=xbmc.LOGDEBUG )
    file_detail = re.compile( "{(.*?)}", re.DOTALL ).findall(json_folder_detail)
    for f in file_detail:
        match = re.search( '"file" : "(.*?)",', f )
        if not match:
            match = re.search( '"file":"(.*?)",', f )
        if match:
            if match.group(1).endswith( "/" ) or match.group(1).endswith( "\\" ):
                folderList.append( match.group(1) )
                xbmc.log( "[folder.py] - Folder Path: %s" % match.group(1), level=xbmc.LOGDEBUG )
                if recursive == "TRUE":
                    fileList.extend( dirEntries( match.group(1), media_type, recursive, contains ) ) 
        else:
            continue
    return folderList

def escapeDirJSON ( dir_name ):
    ''' escapes characters in a directory path for use in JSON RPC calls

        Method to call:
        escapeDirJSON( dir_name )
            dir_name    - the name of the directory
    '''
    xbmc.log( "[folder.py] - escapeDirJSON Activated", level=xbmc.LOGDEBUG )
    if dir_name.find(":"):
        dir_name = dir_name.replace("\\", "\\\\")
    return dir_name
