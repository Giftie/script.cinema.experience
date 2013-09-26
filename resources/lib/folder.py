# -*- coding: utf-8 -*-

import sys, os, re
import xbmc, xbmcvfs
import utils

def absolute_listdir( path, media_type = "files", recursive = False, contains = "" ):
    absolute_files = []
    absolute_folders = []
    folders, files = xbmcvfs.listdir( path )
    for f in files:
        f = utils.smart_unicode( f )
        if media_type == "files":
            if not contains or ( contains and ( contains in f ) ):
                absolute_files.append( os.path.join( path, f ) )
        else:
            if os.path.splitext( f )[ 1 ] in xbmc.getSupportedMedia( media_type ):
                if not contains or ( contains and ( contains in f ) ):
                    absolute_files.append( os.path.join( path, f ) )
    if folders:
        absolute_folders = absolute_folder_paths( folders, path )
        if recursive:
            for folder in absolute_folders:
                absolute_files.extend( absolute_listdir( folder, recursive = recursive, contains = contains ) )
    return absolute_files

def absolute_folder_paths( folders, root_path ):
    actual_folders = []
    for folder in folders:
        folder = utils.smart_unicode( folder )
        actual_folders.append( os.path.join( root_path, folder ).replace("\\\\","\\") )
    return actual_folders
        
