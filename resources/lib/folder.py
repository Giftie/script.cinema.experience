# -*- coding: utf-8 -*-

import sys, os, re
import xbmc
import utils
from json_utils import retrieve_json_dict

def dirEntries( dir_name, media_type="files", recursive="FALSE", contains="" ):
    '''Returns a list of valid XBMC files from a given directory(folder)

       Method to call:
       dirEntries( dir_name, media_type, recursive )
            dir_name   - the name of the directory to be searched
            media_type - valid types: video, music, pictures, files, programs
            recursive  - Setting to "TRUE" searches Parent and subdirectories, Setting to "FALSE" only search Parent Directory
    '''
    utils.log( "[folder.py] - dirEntries Activated" )
    fileList = []
    json_query = '{"jsonrpc": "2.0", "method": "Files.GetDirectory", "params": {"directory": "%s", "media": "%s"}, "id": 1}' % ( escapeDirJSON( dir_name ), media_type )
    json_folder_detail = retrieve_json_dict(json_query, items='files', force_log=True)
    if json_folder_detail:
        for f in json_folder_detail:
            try:
                if recursive == "TRUE" and f["filetype"] == "directory":
                    fileList.extend( dirEntries( f["file"], media_type, recursive, contains ) )
                elif not contains or ( contains and (contains in f["file"] ) ):
                    fileList.append( f["file"] )
                    #log( "[folder.py] - File Path: %s" % f["file"] ) 
                else:
                    continue
            except:
                continue
    return fileList

def getFolders( dir_name, recursive="FALSE" ):
    '''Returns a list of valid XBMC files from a given directory(folder)

       Method to call:
       getFolders( dir_name, , recursive )
            dir_name   - the name of the directory to be searched
            recursive  - Setting to "TRUE" searches Parent and subdirectories, Setting to "FALSE" only search Parent Directory
    '''
    utils.log( "[folder.py] - getFolders Activated" )
    folderList = []
    json_query = '{"jsonrpc": "2.0", "method": "Files.GetDirectory", "params": {"directory": "%s", "media": "files"}, "id": 1}' % ( escapeDirJSON( dir_name ) )
    json_folder_detail = retrieve_json_dict(json_query, items='files', force_log=True)
    if json_folder_detail:
        for f in json_folder_detail:
            if f["filetype"] == "directory":
                folderList.append( match.group(1) )
                #log( "[folder.py] - Folder Path: %s" % f["file"] )
                if recursive == "TRUE":
                    fileList.extend( getFolders( f["file"], recursive ) ) 
            else:
                continue
    return folderList

def escapeDirJSON ( dir_name ):
    ''' escapes characters in a directory path for use in JSON RPC calls

        Method to call:
        escapeDirJSON( dir_name )
            dir_name    - the name of the directory
    '''
    utils.log( "[folder.py] - escapeDirJSON Activated" )
    if dir_name.find(":"):
        dir_name = dir_name.replace("\\", "\\\\")
    return dir_name
