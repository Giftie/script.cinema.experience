# -*- coding: utf-8 -*-

import xbmcgui, xbmc, xbmcaddon, xbmcvfs
import os, re, sys, socket, traceback, time, __builtin__
from urllib import quote_plus
from threading import Thread

__addon__                = xbmcaddon.Addon()
__version__              = __addon__.getAddonInfo('version')
__scriptID__             = __addon__.getAddonInfo('id')
__script__               = __addon__.getAddonInfo('name')
__addonname__            = __script__
# language method
__language__             = __addon__.getLocalizedString
# settings method
__setting__              = __addon__.getSetting
BASE_CACHE_PATH          = os.path.join( xbmc.translatePath( "special://profile" ).decode('utf-8'), "Thumbnails", "Video" )
BASE_CURRENT_SOURCE_PATH = os.path.join( xbmc.translatePath( "special://profile/addon_data/" ).decode('utf-8'), os.path.basename( __addon__.getAddonInfo('path') ) )
BASE_RESOURCE_PATH       = xbmc.translatePath( os.path.join( __addon__.getAddonInfo('path').decode('utf-8'), 'resources' ) )
home_automation_folder   = os.path.join( BASE_CURRENT_SOURCE_PATH, "ha_scripts" )
home_automation_module   = os.path.join( home_automation_folder, "home_automation.py" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

playback = ""
header = "Cinema Experience"
time_delay = 200
image = xbmc.translatePath( os.path.join( __addon__.getAddonInfo("path"), "icon.png") ).decode('utf-8')
playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
is_paused = False
prev_trigger = ""
script_header = "[ %s ]" % __scriptID__

from ce_playlist import _get_special_items, build_music_playlist, _rebuild_playlist, _store_playlist, _get_queued_video_info, _clear_playlists
from slides import _fetch_slides
import utils
from launch_automation import Launch_automation
from settings import *

trivia_settings  = settings.trivia_settings
trailer_settings = settings.trailer_settings
ha_settings      = settings.ha_settings
video_settings   = settings.video_settings
extra_settings   = settings.extra_settings
audio_formats    = settings.audio_formats
triggers         = settings.triggers

number_of_features = extra_settings[ "number_of_features" ] + 1

#Check to see if module is moved to /userdata/addon_data/script.cinema.experience
if not xbmcvfs.exists( os.path.join( BASE_CURRENT_SOURCE_PATH, "ha_scripts", "home_automation.py" ) ):
    source = os.path.join( BASE_RESOURCE_PATH, "ha_scripts", "home_automation.py" )
    destination = os.path.join( BASE_CURRENT_SOURCE_PATH, "ha_scripts", "home_automation.py" )
    xbmcvfs.mkdir( os.path.join( BASE_CURRENT_SOURCE_PATH, "ha_scripts" ) )        
    xbmcvfs.copy( source, destination )
    utils.log( "home_automation.py copied", xbmc.LOGNOTICE )

def footprints():
    utils.log( "Script Name: %s" % __script__, xbmc.LOGNOTICE )
    utils.log( "Script ID: %s" % __scriptID__, xbmc.LOGNOTICE )
    utils.log( "Script Version: %s" % __version__, xbmc.LOGNOTICE )
    utils.log( "Starting Window ID: %s" % xbmcgui.getCurrentWindowId(), xbmc.LOGNOTICE )

def _clear_watched_items( clear_type ):
    utils.log( "_clear_watched_items( %s )" % ( clear_type ), xbmc.LOGNOTICE )
    # initialize base_path
    base_paths = []
    # clear trivia or trailers
    if ( clear_type == "ClearWatchedTrailers" ):
        # handle AMT db special
        sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib", "scrapers") )
        from amt_database import scraper as scraper
        Scraper = scraper.Main()
        # update trailers
        Scraper.clear_watched()
        # set base watched file path
        base_paths += [ os.path.join( BASE_CURRENT_SOURCE_PATH, "amt_current_watched.txt" ) ]
        base_paths += [ os.path.join( BASE_CURRENT_SOURCE_PATH, "local_watched.txt" ) ]
    else:
        # set base watched file path
        base_paths = [ os.path.join( BASE_CURRENT_SOURCE_PATH, "trivia_watched.txt" ) ]
    try:
        # set proper message
        message = ( 32531, 32541, )[ sys.argv[ 1 ] == "ClearWatchedTrailers" ]
        # remove watched status file(s)
        for base_path in base_paths:
            # remove file if it exists
            if ( xbmcvfs.exists( base_path ) ):
                xbmcvfs.delete( base_path )
    except:
        # set proper message
        message = ( 32532, 32542, )[ sys.argv[ 1 ] == "ClearWatchedTrailers" ]
    # inform user of result
    ok = xbmcgui.Dialog().ok( __language__( 32000 ), __language__( message ) )

def _build_playlist( movies, mode = "movie_titles" ):
    if mode == "movie_titles":
        utils.log( "Movie Title Mode", xbmc.LOGNOTICE )
        for movie in movies:
            utils.log( "Movie Title: %s" % movie, xbmc.LOGNOTICE )
            xbmc.executehttpapi( "SetResponseFormat()" )
            xbmc.executehttpapi( "SetResponseFormat(OpenField,)" )
            # select Movie path from movieview Limit 1
            sql = "SELECT movieview.idMovie, movieview.c00, movieview.strPath, movieview.strFileName, movieview.c08, movieview.c14 FROM movieview WHERE c00 LIKE '%s' LIMIT 1" % ( movie.replace( "'", "''", ), )
            utils.log( "SQL: %s" % ( sql, ) )
            # query database for info dummy is needed as there are two </field> formatters
            try:
                movie_id, movie_title, movie_path, movie_filename, thumb, genre, dummy = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % quote_plus( sql ), ).split( "</field>" )
                movie_id = int( movie_id )
            except:
                traceback.print_exc()
                utils.log( "Unable to match movie", level=xbmc.LOGERROR )
                movie_id = 0
                movie_title = movie_path = movie_filename = thumb = genre = dummy = ""
            movie_full_path = os.path.join(movie_path, movie_filename).replace("\\\\" , "\\")
            utils.log( "Movie Title: %s" % movie_title, xbmc.LOGNOTICE )
            utils.log( "Movie Path: %s" % movie_path, xbmc.LOGNOTICE )
            utils.log( "Movie Filename: %s" % movie_filename, xbmc.LOGNOTICE )
            utils.log( "Full Movie Path: %s" % movie_full_path, xbmc.LOGNOTICE )
            if not movie_id == 0:
                json_command = '{"jsonrpc": "2.0", "method": "Playlist.Add", "params": {"playlistid": 1, "item": {"movieid": %d} }, "id": 1}' % int( movie_id )
                json_response = xbmc.executeJSONRPC(json_command)
                utils.log( "JSONRPC Response: \n%s" % json_response )
                xbmc.sleep( 50 )
    elif mode == "movie_ids":
        utils.log( "Movie ID Mode", xbmc.LOGNOTICE )
        for movie_id in movies:
            utils.log( "Movie ID: %s" % movie_id, xbmc.LOGNOTICE )
            json_command = '{"jsonrpc": "2.0", "method": "Playlist.Add", "params": {"playlistid": 1, "item": {"movieid": %d} }, "id": 1}' % int( movie_id )
            json_response = xbmc.executeJSONRPC( json_command )
            utils.log( "JSONRPC Response: \n%s" % json_response )
            xbmc.sleep( 50 )

if __name__ == "__main__" :
    #xbmc.sleep( 2000 )
    footprints()
    prev_trigger = ""
    utils.settings_to_log( BASE_CURRENT_SOURCE_PATH, script_header )
    # check to see if an argv has been passed to script
    xbmcgui.Window( 10001 ).setProperty( "CinemaExperienceRunning", "True" )
    from ce_player import Script
    try:
        try:
            if sys.argv[ 1 ]:
                utils.log( "Script Started With: %s" % sys.argv[ 1 ], xbmc.LOGNOTICE )
                try:
                    _command = ""
                    titles = ""
                    if sys.argv[ 1 ] == "ClearWatchedTrivia" or sys.argv[ 1 ] == "ClearWatchedTrailers":
                        _clear_watched_items( sys.argv[ 1 ] )
                        exit = True
                    elif sys.argv[ 1 ] == "oldway":
                        __addon__.setSetting( id='number_of_features', value='0' ) # set number of features to 1
                        _clear_playlists()
                        xbmc.sleep( 250 )
                        xbmc.executebuiltin( "Action(Queue,%d)" % ( xbmcgui.getCurrentWindowId() - 10000, ) )
                        utils.log( "Action(Queue,%d)" % ( xbmcgui.getCurrentWindowId() - 10000, ), xbmc.LOGNOTICE )
                        # we need to sleep so the video gets queued properly
                        xbmc.sleep( 250 )
                        exit = Script().start_script( "oldway" )
                    elif sys.argv[ 1 ] == "fromplay":
                        xbmc.sleep( 250 )
                        exit = Script().start_script( "oldway" )
                    elif sys.argv[ 1 ].startswith( "command" ):   # Command Arguments
                        _sys_arg = sys.argv[ 1 ].replace("<li>",";")
                        _command = re.split(";", _sys_arg, maxsplit=1)[1]
                        utils.log( "Command Call: %s" % _command, xbmc.LOGNOTICE )
                        if _command.startswith( "movie_title" ):   # Movie Title
                            _clear_playlists()
                            if _command.startswith( "movie_title;" ):
                                titles = re.split(";", _command, maxsplit=1)[1]
                            elif _command.startswith( "movie_title=" ):
                                titles = re.split("=", _command, maxsplit=1)[1]
                            movie_titles = titles.split( ";" )
                            if not movie_titles == "":
                                _build_playlist( movie_titles )
                                exit = Script().start_script( "oldway" )
                            else:
                                exit = False
                        elif _command.startswith( "sqlquery" ):    # SQL Query
                            _clear_playlists()
                            sqlquery = re.split(";", _command, maxsplit=1)[1]
                            movie_titles = _sqlquery( sqlquery )
                            if not movie_titles == "":
                                _build_playlist( movie_titles )
                                exit = Script().start_script( "oldway" )
                            else:
                                exit = False
                        elif _command.startswith( "open_settings" ):    # Open Settings
                            __addon__.openSettings()
                            exit = False
                    elif sys.argv[ 1 ].startswith( "movieid=" ):
                        _clear_playlists()
                        movie_id = sys.argv[ 1 ].split("=")[ 1 ]
                        movie_ids = movie_id.split( ";" )
                        if movie_ids:
                            _build_playlist( movie_ids, mode="movie_ids" )
                            exit = Script().start_script( "oldway" )
                        else:
                            exit = False
                    else:
                        _clear_playlists()
                        exit = Script().start_script( sys.argv[ 1 ].lower() )
                except:
                    traceback.print_exc()
        except:
            if not int( xbmcgui.getCurrentWindowId() ) == 10001: # Not Started from Addon/Programs window
                #start script in 'Old Way' if the script is called with out argv... queue the movie the old way
                __addon__.setSetting( id='number_of_features', value='0' ) # set number of features to 1
                _clear_playlists()
                xbmc.executebuiltin( "Action(Queue,%d)" % ( xbmcgui.getCurrentWindowId() - 10000, ) )
                utils.log( "Action(Queue,%d)" % ( xbmcgui.getCurrentWindowId() - 10000, ), xbmc.LOGNOTICE )
                # we need to sleep so the video gets queued properly
                xbmc.sleep( 500 )
                exit = Script().start_script( "oldway" )
            else:
                __addon__.openSettings()
                exit = True
        #xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % (header, __language__( 32545 ), time_delay, image) )
        utils.log( "messy_exit: %s" % exit, xbmc.LOGNOTICE )
        if exit:
            prev_trigger = Launch_automation().launch_automation( triggers[16], None ) # Script End
            __addon__.setSetting( id='number_of_features', value='%d' % (number_of_features - 1) )
            xbmcgui.Window( 10001 ).setProperty( "CinemaExperienceRunning", "False" )
            xbmcgui.Window( 10001 ).setProperty( "CinemaExperienceTriggered", "False" )
        else:
            _clear_playlists()
            prev_trigger = Launch_automation().launch_automation( triggers[16], None ) # Script End
            __addon__.setSetting( id='number_of_features', value='%d' % (number_of_features - 1) )
            xbmcgui.Window( 10001 ).setProperty( "CinemaExperienceRunning", "False" )
            xbmcgui.Window( 10001 ).setProperty( "CinemaExperienceTriggered", "False" )
    except:
        traceback.print_exc()
        # if script fails, changes settings back
        __addon__.setSetting( id='number_of_features', value='%d' % (number_of_features - 1) )
        prev_trigger = Launch_automation().launch_automation( triggers[16], None ) # Script End
        xbmcgui.Window( 10001 ).setProperty( "CinemaExperienceRunning", "False" )
        xbmcgui.Window( 10001 ).setProperty( "CinemaExperienceTriggered", "False" )
