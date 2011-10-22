# -*- coding: utf-8 -*-

# constants
__script__ = "Cinema Experience"
__author__ = "nuka1195-giftie-ackbarr"
__url__ = "http://code.google.com/p/xbmc-addons/"
__version__ = "1.0.53"
__scriptID__ = "script.cinema.experience"

import xbmcgui, xbmc, xbmcaddon, os, re, sys
import traceback
import time
from urllib import quote_plus
from threading import Thread
from shutil import copy2

_A_ = xbmcaddon.Addon( __scriptID__ )
# language method
_L_ = _A_.getLocalizedString
# settings method
_S_ = _A_.getSetting

number_of_features = int( _S_( "number_of_features" ) ) + 1
playback = ""
BASE_CACHE_PATH = os.path.join( xbmc.translatePath( "special://profile" ), "Thumbnails", "Video" )
BASE_CURRENT_SOURCE_PATH = os.path.join( xbmc.translatePath( "special://profile/addon_data/" ), os.path.basename( _A_.getAddonInfo('path') ) )
BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join( _A_.getAddonInfo('path'), 'resources' ) )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )
headings = ( _L_(32600), _L_(32601), _L_(32602), _L_(32603), _L_(32604), _L_(32605), _L_(32606), _L_(32607), _L_(32608), _L_(32609), _L_(32610), _L_(32611), _L_(32612) )
header = "Cinema Experience"
time_delay = 200
image = xbmc.translatePath( os.path.join( _A_.getAddonInfo("path"), "icon.png") )
autorefresh = xbmc.executehttpapi( "GetGuiSetting(1; videoplayer.adjustrefreshrate)" ).replace( "<li>", "" )
screensaver = xbmc.executehttpapi( "GetGUISetting(3;screensaver.mode)" ).replace( "<li>", "" )
playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
prev_trigger = ""
script_header = "[ %s ]" % __scriptID__

from ce_playlist import _get_special_items, _wait_until_end, build_music_playlist,  _rebuild_playlist
from slides import _fetch_slides
from trailer_downloader import downloader
from utils import settings_to_log

from dharma_code import _store_playlist, _get_queued_video_info, _build_playlist
from os import remove as delete_file
exists = os.path.exists
from shutil import copy as file_copy

#TODO: Check to see if module is moved to /userdata/addon_data/script.cinema.experience
try:
    if not exists( os.path.join( BASE_CURRENT_SOURCE_PATH, "ha_scripts", "home_automation.py" ) ) and _S_( "ha_enable") == "true":
        source = os.path.join( BASE_RESOURCE_PATH, "ha_scripts", "home_automation.py" )
        destination = os.path.join( BASE_CURRENT_SOURCE_PATH, "ha_scripts", "home_automation.py" )
        os.mkdir( os.path.join( BASE_CURRENT_SOURCE_PATH, "ha_scripts" ) )        
        file_copy( source, destination )
        xbmc.log( "[ script.cinema.experience ] - home_automation.py copied", level=xbmc.LOGNOTICE )
    sys.path.append( os.path.join( BASE_CURRENT_SOURCE_PATH, "ha_scripts" ) )
    from home_automation import activate_on
    # Import HA module set ha_imported to True if successful
    ha_imported = True
except ImportError:
    # or ha_imported to False if unsuccessful
    ha_imported = False
   
def footprints():
    xbmc.log( "[ script.cinema.experience ] - Script Name: %s" % __script__, level=xbmc.LOGNOTICE )
    xbmc.log( "[ script.cinema.experience ] - Script ID: %s" % __scriptID__, level=xbmc.LOGNOTICE )
    xbmc.log( "[ script.cinema.experience ] - Script Version: %s" % __version__, level=xbmc.LOGNOTICE )
    xbmc.log( "[ script.cinema.experience ] - Autorefresh - Before Script: %s" % autorefresh, level=xbmc.LOGNOTICE )
    xbmc.log( "[ script.cinema.experience ] - Starting Window ID: %s" % xbmcgui.getCurrentWindowId(), level=xbmc.LOGNOTICE )

def _load_trigger_list():
    xbmc.log( "[script.cinema.experience] - Loading Trigger List", level=xbmc.LOGNOTICE)
    try:
        # set base watched file path
        base_path = os.path.join( BASE_CURRENT_SOURCE_PATH, "trigger_list.txt" )
        # open path
        usock = open( base_path, "r" )
        # read source
        trigger_list = eval( usock.read() )
        # close socket
        usock.close()
    except:
        xbmc.log( "[script.cinema.experience] - Loading Trigger List", level=xbmc.LOGNOTICE)
        traceback.print_exc()
        trigger_list = []
    return trigger_list
            
def _clear_watched_items( clear_type ):
    xbmc.log( "[ script.cinema.experience ] - _clear_watched_items( %s )" % ( clear_type ), level=xbmc.LOGNOTICE )
    # initialize base_path
    base_paths = []
    # clear trivia or trailers
    if ( clear_type == "ClearWatchedTrailers" ):
        # trailer settings, grab them here so we don't need another _S_() object
        settings = { "trailer_amt_db_file":  xbmc.translatePath( _S_( "trailer_amt_db_file" ) ) }
        # handle AMT db special
        sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib", "scrapers") )
        from amt_database import scraper as scraper
        Scraper = scraper.Main( settings=settings )
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
            if ( exists( base_path ) ):
                delete_file( base_path )
    except:
        # set proper message
        message = ( 32532, 32542, )[ sys.argv[ 1 ] == "ClearWatchedTrailers" ]
    # inform user of result
    ok = xbmcgui.Dialog().ok( _L_( 32000 ), _L_( message ) )

def _view_changelog( ):
    xbmc.log( "[ script.cinema.experience ] - _view_changelog()", level=xbmc.LOGNOTICE )

def _view_readme( ):
    xbmc.log( "[ script.cinema.experience ] - _view_readme()", level=xbmc.LOGNOTICE )

def _check_compatible():
    try:
        # spam plugin statistics to log
        xbmc.log( "[ script.cinema.experience ] - Version - %s-r%s' initialized!" % ( __version__, __svn_revision__.replace( "$", "" ).replace( "Revision", "" ).replace( ":", "" ).strip() ), level=xbmc.LOGNOTICE )
        # get xbmc revision
        xbmc_rev = int( xbmc.getInfoLabel( "System.BuildVersion" ).split( " r" )[ -1 ][ : 5 ] )
        # compatible?
        ok = xbmc_rev >= int( __XBMC_Revision__ )
    except:
        # error, so unknown, allow to run
        xbmc_rev = 0
        ok = 2
    # spam revision info
    xbmc.log( "[ script.cinema.experience ] -     ** Required XBMC Revision: r%s **" % ( __XBMC_Revision__, ), level=xbmc.LOGNOTICE )
    xbmc.log( "[ script.cinema.experience ] -     ** Found XBMC Revision: r%d [%s] **" % ( xbmc_rev, ( "Not Compatible", "Compatible", "Unknown", )[ ok ], ), level=xbmc.LOGNOTICE )
    return ok

def _clear_playlists( mode="both" ):
    # clear playlists
    if mode=="video" or mode=="both":
        vplaylist = playlist
        vplaylist.clear()
        xbmc.log( "[ script.cinema.experience ] - Video Playlist Cleared", level=xbmc.LOGNOTICE )
    if mode=="music" or mode=="both":
        mplaylist = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
        mplaylist.clear()
        xbmc.log( "[ script.cinema.experience ] - Music Playlist Cleared", level=xbmc.LOGNOTICE )

def voxcommando():
    playlistsize = playlist.size()
    if playlistsize > 1:
        movie_titles = ""
        for feature_count in range (1, playlistsize + 1):
            movie_title = playlist[ feature_count - 1 ].getdescription()
            xbmc.log( "[ script.cinema.experience ] - Feature #%-2d - %s" % ( feature_count, movie_title ), level=xbmc.LOGNOTICE )
            movie_titles = movie_titles + movie_title + "<li>"
        movie_titles = movie_titles.rstrip("<li>")
        if _S_( "voxcommando" ) == "true":
            xbmc.executehttpapi( "Broadcast(<b>CElaunch." + str(playlistsize ) + "<li>" + movie_titles + "</b>;33000)" )
    else:
        # get the queued video info
        movie_title = playlist[ 0 ].getdescription()
        xbmc.log( "[ script.cinema.experience ] - Feature - %s" % movie_title, level=xbmc.LOGNOTICE )
        if _S_( "voxcommando" ) == "true":
            xbmc.executehttpapi( "Broadcast(<b>CElaunch<li>" + movie_title + "</b>;33000)" )

def _sqlquery( sqlquery ):
    movie_list = []
    movies = []
    xbmc.executehttpapi( "SetResponseFormat()" )
    xbmc.executehttpapi( "SetResponseFormat(OpenField,)" )
    #sqlquery = "SELECT movieview.c00 FROM movieview JOIN genrelinkmovie ON genrelinkmovie.idMovie=movieview.idMovie JOIN genre ON genrelinkmovie.idGenre=genre.idGenre WHERE strGenre='Action' ORDER BY RANDOM() LIMIT 4"
    xbmc.log( "[ script.cinema.experience ]  - SQL: %s" % ( sqlquery, ), level=xbmc.LOGDEBUG )
    try:
        sqlresult = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % quote_plus( sqlquery ), )
        xbmc.log( "[ script.cinema.experience ] - sqlresult: %s" % sqlresult, level=xbmc.LOGDEBUG )
        movies = sqlresult.split("</field>")
        movie_list = movies[ 0:len( movies ) -1 ]
    except:
        xbmc.log( "[ script.cinema.experience ] - Error searching database", level=xbmc.LOGNOTICE )
    return movie_list

def auto_refresh( before, mode ):
    xbmc.log( "[ script.cinema.experience ] - auto_refresh( %s, %s )" % ( before, mode ), level=xbmc.LOGNOTICE )
    # turn off autorefresh
    if _S_( "autorefresh" ) == "true" and before == "True" and mode=="disable":
        xbmc.executehttpapi( "SetGUISetting(1; videoplayer.adjustrefreshrate; False)" )
    # turn on autorefresh
    elif _S_( "autorefresh" ) == "true" and before == "True" and mode=="enable":
        xbmc.executehttpapi( "SetGUISetting(1; videoplayer.adjustrefreshrate; True)" )
    status = xbmc.executehttpapi( "GetGuiSetting(1; videoplayer.adjustrefreshrate)" ).strip("<li>")
    xbmc.log( "[ script.cinema.experience ] - Autorefresh Status: %s" % status, level=xbmc.LOGNOTICE )

def trivia_intro():
    xbmc.log( "[ script.cinema.experience ] - ## Intro ##", level=xbmc.LOGNOTICE)
    play_list = playlist
    play_list.clear()
    # initialize intro lists
    playlist_intro = []
    # get trivia intro videos
    _get_special_items( playlist=play_list,
                           items=( 0, 1, 1, 2, 3, 4, 5, )[ int( _S_( "trivia_intro" ) ) ],
                            path=( xbmc.translatePath( _S_( "trivia_intro_file" ) ), xbmc.translatePath( _S_( "trivia_intro_folder" ) ), )[ int( _S_( "trivia_intro" ) ) > 1 ],
                           genre=_L_( 32609 ),
                           index=0,
                      media_type="video"
                      )
    if not int( _S_( "trivia_intro" ) ) == 0:
        xbmc.Player().play( play_list )
        
def start_downloader( mpaa, genre, equivalent_mpaa ):
    # start the downloader if Play Mode is set to stream and if scraper is not Local or XBMC_library
    if ( int( _S_( "trailer_play_mode" ) ) == 1 ) and ( not ( int( _S_( "trailer_scraper" ) ) in (2, 3) ) ):
        xbmc.log( "[ script.cinema.experience ] - Starting Downloader Thread", level=xbmc.LOGNOTICE )
        #thread = Thread( target=downloader, args=( mpaa, genre ) )
        #thread.start()
        _genre = genre.replace( " / ", "_" )
        downloader_path = os.path.join( BASE_RESOURCE_PATH, "lib", "new_trailer_downloader.py,mpaa=%s;genre=%s" % ( equivalent_mpaa, genre ) )
        #xbmc.executescript( downloader_path )
        xbmc.executebuiltin( "XBMC.RunScript(%s)" % downloader_path )
    else:
        pass
        
def activate_ha( trigger = None, prev_trigger = None, mode="thread" ):
    if _S_( "ha_enable" ) == "true" and ha_imported:
        if _S_( "ha_multi_trigger" ) == "true" and prev_trigger == trigger:
            pass
        elif mode != "thread":
            activate_on( trigger )
        else:
            thread = Thread( target=activate_on, args=( trigger, ) )
            thread.start()
        if not trigger in ( _L_( 32618 ), _L_( 32619 ) ):
            prev_trigger = trigger
    return prev_trigger
    
def _play_trivia( mpaa, genre, plist, equivalent_mpaa ):
    activate_ha( _L_( 32613 ) ) # Script Start - Or where it seems to be
    # if trivia path and time to play the trivia slides
    pDialog = xbmcgui.DialogProgress()
    pDialog.create( __script__, _L_( 32520 )  )
    pDialog.update( 0 )
    if int( _S_( "trivia_mode" ) ) == 2: # Start Movie Quiz Script
        xbmc.log( "[ script.cinema.experience ] - Starting script.moviequiz", level=xbmc.LOGNOTICE )
        start_downloader( mpaa, genre, equivalent_mpaa )
        try:
            _MA_= xbmcaddon.Addon( "script.moviequiz" )
            BASE_MOVIEQUIZ_PATH = xbmc.translatePath( _MA_.getAddonInfo('path') )
            sys.path.append( BASE_MOVIEQUIZ_PATH )
            try:
                import quizlib.question as question
                xbmc.log( "[ script.cinema.experience ] - Loaded question module", level=xbmc.LOGNOTICE )
            except ImportError:
                traceback.print_exc()
                xbmc.log( "[ script.cinema.experience ] - Failed to Load question module", level=xbmc.LOGNOTICE )
            except:
                traceback.print_exc()
            try:
                import quizlib.mq_ce_play as moviequiz
                xbmc.log( "[ script.cinema.experience ] - Loaded mq_ce_play module", level=xbmc.LOGNOTICE )
            except ImportError:
                traceback.print_exc()
                xbmc.log( "[ script.cinema.experience ] - Failed to Load mq_ce_play module", level=xbmc.LOGNOTICE )
            except:
                traceback.print_exc()
            pDialog.close()
            activate_ha( _L_( 32613 ) ) # Script Start - Or where it seems to be
            trivia_intro()
        
            if playlist.size() > 0:
                _wait_until_end()
            xbmc.sleep(1500) # wait 1.5 seconds
            path = _MA_.getAddonInfo('path')
            question_type = question.TYPE_MOVIE
            mode = ( True, False )[int( _S_( "trivia_moviequiz_mode" ) ) ]
            mpaa = (  _S_( "trivia_rating" ), equivalent_mpaa, )[ _S_( "trivia_limit_query" ) == "true" ]
            question_limit = int( float( _S_( "trivia_moviequiz_qlimit" ) ) )
            completion = moviequiz.runCinemaExperience( question_type, mode, mpaa, genre, question_limit )
            if completion:
                xbmc.log( "[ script.cinema.experience ] - Completed script.moviequiz", level=xbmc.LOGNOTICE )
            else:
                xbmc.log( "[ script.cinema.experience ] - Failed in script.moviequiz", level=xbmc.LOGNOTICE )
        except:
            traceback.print_exc()
            xbmc.log( "[ script.cinema.experience ] - Failed to start script.moviequiz", level=xbmc.LOGNOTICE )
        _rebuild_playlist( plist )
        import xbmcscript_player as script
        script.Main()
        xbmc.Player().play( playlist )
    elif _S_( "trivia_folder" ) and int( _S_( "trivia_mode" ) ) == 1:  # Start Slide Show
        start_downloader( mpaa, genre, equivalent_mpaa )
        ## update dialog with new message
        #pDialog.update( -1, _L_( 32510 ) )
        
        # trivia settings, grab them here so we don't need another _S_() object
        settings = {  "trivia_total_time": int( float( _S_( "trivia_total_time" ) ) ),
                          "trivia_folder": xbmc.translatePath( _S_( "trivia_folder" ) ),
                      "trivia_slide_time": int( float( _S_( "trivia_slide_time" ) ) ),
                           "trivia_intro": _S_( "trivia_intro" ),
                           "trivia_music": _S_( "trivia_music" ),
                   "trivia_adjust_volume": _S_( "trivia_adjust_volume" ),
                     "trivia_fade_volume": _S_( "trivia_fade_volume" ),
                       "trivia_fade_time": int( float( _S_( "trivia_fade_time" ) ) ),
                      "trivia_music_file": xbmc.translatePath( _S_( "trivia_music_file" ) ),
                    "trivia_music_folder": xbmc.translatePath( _S_( "trivia_music_folder" ) ),
                    "trivia_music_volume": int( float( _S_( "trivia_music_volume" ) ) ),
                  "trivia_unwatched_only": _S_( "trivia_unwatched_only" ) == "true"
                            }

        if not int( _S_( "trivia_music" ) )== 0:
            pDialog.update( -1, _L_( 32511 )  )
            build_music_playlist()
        # set the proper mpaa rating user preference
        mpaa = (  _S_( "trivia_rating" ), equivalent_mpaa, )[ _S_( "trivia_limit_query" ) == "true" ]
        xbmc.log( "[ script.cinema.experience ] - Slide MPAA Rating: %s" % equivalent_mpaa, level=xbmc.LOGNOTICE )
        # import trivia module and execute the gui
        pDialog.update( 50 )
        slide_playlist = _fetch_slides( equivalent_mpaa )
        pDialog.close()
        trivia_intro()
        if playlist.size() > 0:
            activate_ha( _L_( 32609 ) ) # Trivia Intro
            _wait_until_end()
        xbmc.sleep(1500) # wait 1.5 seconds 
        from xbmcscript_trivia import Trivia
        xbmc.log( "[ script.cinema.experience ] - Starting Trivia script", level=xbmc.LOGNOTICE )
        activate_ha( _L_( 32615 ) ) # Trivia Start
        ui = Trivia( "script-CExperience-trivia.xml", _A_.getAddonInfo('path'), "default", "720p", settings=settings, mpaa=mpaa, genre=genre, plist=plist, slide_playlist=slide_playlist )
        #ui.doModal()
        del ui
        # we need to activate the video window
        xbmc.executebuiltin( "XBMC.ActivateWindow(2005)" )
        xbmc.Player().play( playlist )
    elif int( _S_( "trivia_mode" ) ) == 0: # No Trivia
        # no trivia slide show so play the video
        pDialog.close()
        start_downloader( mpaa, genre, equivalent_mpaa )
        _rebuild_playlist( plist )
        # play the video playlist
        import xbmcscript_player as script
        script.Main()
        activate_ha( _L_( 32613 ) ) # Script Start - Or where it seems to be
        xbmc.Player().play( playlist )
    
def start_script( library_view = "oldway" ):
    messy_exit = False
    xbmc.log( "[ script.cinema.experience ] - Library_view: %s" % library_view, level=xbmc.LOGNOTICE )
    # turn off autorefresh
    early_exit = False
    autorefresh_movie = False
    movie_next = False
    prev_trigger = None
    auto_refresh( autorefresh, "disable" )
    if library_view != "oldway":
        xbmc.executebuiltin( "ActivateWindow(videolibrary,%s,return)" % library_view )
        # wait until Video Library shows
        while not xbmc.getCondVisibility( "Container.Content(movies)" ):
            pass
        if _S_( "enable_notification" ) == "true":
            xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % (header, _L_( 32546 ), 300000, image) )
        # wait until playlist is full to the required number of features
        xbmc.log( "[ script.cinema.experience ] - Waiting for queue to be filled with %s Feature films" % number_of_features, level=xbmc.LOGNOTICE )
        count = 0
        while playlist.size() < number_of_features:
            if playlist.size() > count:
                xbmc.log( "[ script.cinema.experience ] - User queued %s of %s Feature films" % (playlist.size(), number_of_features), level=xbmc.LOGNOTICE )
                header1 = header + " - Feature " + "%d" % playlist.size()
                message = _L_( 32543 ) + playlist[playlist.size() -1].getdescription()
                if _S_( "enable_notification" ) == "true":
                    xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % (header1, message, time_delay, image) )
                count = playlist.size()
                xbmc.sleep(time_delay*2)
            if not xbmc.getCondVisibility( "Container.Content(movies)" ):
                early_exit = True
                break
        xbmc.log( "[ script.cinema.experience ] - User queued %s Feature films" % playlist.size(), level=xbmc.LOGNOTICE )
        if not early_exit:
            header1 = header + " - Feature " + "%d" % playlist.size()
            message = _L_( 32543 ) + playlist[playlist.size() -1].getdescription()
            if _S_( "enable_notification" ) == "true":
                xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % (header1, message, time_delay, image) )
            early_exit = False
        # If for some reason the limit does not get reached and the window changed, cancel script
    if playlist.size() < number_of_features and library_view != "oldway":
        if _S_( "enable_notification" ) == "true":
            xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % (header, _L_( 32544 ), time_delay, image) )
        _clear_playlists()
    else:
        mpaa, audio, genre, movie, equivalent_mpaa = _get_queued_video_info( feature = 0 )
        voxcommando()
        plist = _store_playlist() # need to store movie playlist
        _play_trivia( mpaa, genre, plist, equivalent_mpaa )
        _clear_playlists( "music" )
        trigger_list = _load_trigger_list()
        count = -1
        stop_check = 0
        paused = False
        # prelim programming for adding - Activate script and other additions
        while not playlist.getposition() == ( playlist.size() - 1 ):
            try:
                pauseCheck = xbmc.Player().getTime()
                time.sleep( 1 )
                if xbmc.Player().isPlayingVideo():
                    stop_check = 0
                    if (xbmc.Player().getTime() == pauseCheck) and not paused:
                        prev_trigger = activate_ha( _L_( 32618 ), prev_trigger )
                        paused = True
                    elif not (xbmc.Player().getTime() == pauseCheck) and paused:
                        prev_trigger = activate_ha( _L_( 32619 ), prev_trigger )
                        paused = False
                    else: 
                        pass
                elif not xbmc.Player().isPlayingVideo():
                    xbmc.log( "[ script.cinema.experience ] - Video may have stopped", level=xbmc.LOGNOTICE )
            except:
                if stop_check == 50000:
                	xbmc.log( "[ script.cinema.experience ] - Video Definitely Stopped", level=xbmc.LOGNOTICE )
                	messy_exit = True
                	break
                else:
                     stop_check += 1 
            if playlist.getposition() > count:
                try:
                    xbmc.log( "[ script.cinema.experience ] - Item From Trigger List: %s" % trigger_list[ playlist.getposition() ], level=xbmc.LOGNOTICE )
                except:
                    xbmc.log( "[ script.cinema.experience ] - Problem With Trigger List", level=xbmc.LOGNOTICE )
                xbmc.log( "[ script.cinema.experience ] - Playlist Position: %s  Playlist Size: %s " % ( ( playlist.getposition() + 1 ), ( playlist.size() ) ), level=xbmc.LOGNOTICE )
                if not playlist.getposition() == ( playlist.size() - 1 ):
                    prev_trigger = activate_ha( trigger_list[ playlist.getposition() ], prev_trigger )
                    if trigger_list[ playlist.getposition() ] == "Movie":
                        if _S_( "autorefresh" ) == "true" and _S_( "autorefresh_movie" ) == "true":
                            auto_refresh( autorefresh, "enable" )
                            autorefresh_movie = True
                    else:
                        if autorefresh_movie:
                            auto_refresh( autorefresh, "disable" )
                            autorefresh_movie = False
                    xbmc.log( "[ script.cinema.experience ] - autorefresh_movie: %s" % autorefresh_movie, level=xbmc.LOGNOTICE )
                    count = playlist.getposition()
                else: 
                    break  # Reached the last item in the playlist
        if not playlist.size() < 1 and not messy_exit: # To catch an already running script when a new instance started
            xbmc.log( "[ script.cinema.experience ] - Playlist Position: %s  Playlist Size: %s " % ( playlist.getposition() + 1, ( playlist.size() ) ), level=xbmc.LOGNOTICE )
            prev_trigger = activate_ha( trigger_list[ playlist.getposition() ], prev_trigger, "normal" )
            if trigger_list[ playlist.getposition() ] == "Movies":
                xbmc.log( "[ script.cinema.experience ] - Item From Trigger List: %s" % trigger_list[ playlist.getposition() ], level=xbmc.LOGNOTICE )
                if _S_( "autorefresh" ) == "true" and _S_( "autorefresh_movie" ) == "true":
                    auto_refresh( autorefresh, "enable" )
                    autorefresh_movie = True
            else:
                xbmc.log( "[ script.cinema.experience ] - Item From Trigger List: %s" % trigger_list[ playlist.getposition() ], level=xbmc.LOGNOTICE )
                if autorefresh_movie:
                    auto_refresh( autorefresh, "disable" )
                    autorefresh_movie == False
            messy_exit = False
            _wait_until_end()
        else:
            xbmc.log( "[ script.cinema.experience ] - User might have pressed stop", level=xbmc.LOGNOTICE )
            xbmc.log( "[ script.cinema.experience ] - Stopping Script", level=xbmc.LOGNOTICE )
            messy_exit = False
    return messy_exit

if __name__ == "__main__" :
    footprints()
    prev_trigger = ""
    loglevel = int(xbmc.executehttpapi( "GetLogLevel" ).replace( "<li>", "" ) )
    xbmc.log( "[ script.cinema.experience ] - Log Level: %s" % loglevel, level=xbmc.LOGNOTICE )
    settings_to_log( BASE_CURRENT_SOURCE_PATH, script_header )
    # check to see if an argv has been passed to script
    xbmcgui.Window(10025).setProperty( "CinemaExperienceRunning", "True" )
    try:
        try:
            if sys.argv[ 1 ]:
                xbmc.log( "[ script.cinema.experience ] - Script Started With: %s" % sys.argv[ 1 ], level=xbmc.LOGNOTICE )
                try:
                    _command = ""
                    titles = ""
                    if sys.argv[ 1 ] == "ClearWatchedTrivia" or sys.argv[ 1 ] == "ClearWatchedTrailers":
                        _clear_watched_items( sys.argv[ 1 ] )
                        exit = True
                    elif sys.argv[ 1 ] == "ViewChangelog":
                        _view_changelog()
                        exit = True
                    elif sys.argv[ 1 ] == "ViewReadme":
                        _view_readme()
                        exit = True
                    elif sys.argv[ 1 ] == "oldway":
                        _A_.setSetting( id='number_of_features', value='0' ) # set number of features to 1
                        _clear_playlists()
                        xbmc.sleep( 250 )
                        xbmc.executebuiltin( "Action(Queue,%d)" % ( xbmcgui.getCurrentWindowId() - 10000, ) )
                        xbmc.log( "[ script.cinema.experience ] - Action(Queue,%d)" % ( xbmcgui.getCurrentWindowId() - 10000, ), level=xbmc.LOGNOTICE )
                        # we need to sleep so the video gets queued properly
                        xbmc.sleep( 250 )
                        autorefresh_movie = False
                        exit = start_script( "oldway" )
                    elif sys.argv[ 1 ].startswith( "command" ):   # Command Arguments
                        _sys_arg = sys.argv[ 1 ].replace("<li>",";")
                        _command = re.split(";", _sys_arg, maxsplit=1)[1]
                        xbmc.log( "[ script.cinema.experience ] - Command Call: %s" % _command, level=xbmc.LOGNOTICE )
                        if _command.startswith( "movie_title" ):   # Movie Title
                            _clear_playlists()
                            if _command.startswith( "movie_title;" ):
                                titles = re.split(";", _command, maxsplit=1)[1]
                            elif _command.startswith( "movie_title=" ):
                                titles = re.split("=", _command, maxsplit=1)[1]
                            movie_titles = titles.split( ";" )
                            if not movie_titles == "":
                                _build_playlist( movie_titles )
                                autorefresh_movie = False
                                exit = start_script( "oldway" )
                            else:
                                exit = False
                        elif _command.startswith( "sqlquery" ):    # SQL Query
                            _clear_playlists()
                            sqlquery = re.split(";", _command, maxsplit=1)[1]
                            movie_titles = _sqlquery( sqlquery )
                            if not movie_titles == "":
                                _build_playlist( movie_titles )
                                autorefresh_movie = False
                                exit = start_script( "oldway" )
                            else:
                                exit = False
                        elif _command.startswith( "open_settings" ):    # Open Settings
                            _A_.openSettings()
                            exit = False
                    else:
                        _clear_playlists()
                        exit = start_script( sys.argv[ 1 ].lower() )
                except:
                    traceback.print_exc()
        except:
            if not int( xbmcgui.getCurrentWindowId() ) == 10001: # Not Started from Addon/Programs window
                #start script in 'Old Way' if the script is called with out argv... queue the movie the old way
                _A_.setSetting( id='number_of_features', value='0' ) # set number of features to 1
                _clear_playlists()
                xbmc.executebuiltin( "Action(Queue,%d)" % ( xbmcgui.getCurrentWindowId() - 10000, ) )
                xbmc.log( "[ script.cinema.experience ] - Action(Queue,%d)" % ( xbmcgui.getCurrentWindowId() - 10000, ), level=xbmc.LOGNOTICE )
                # we need to sleep so the video gets queued properly
                xbmc.sleep( 500 )
                autorefresh_movie = False
                exit = start_script( "oldway" )
            else:
                _A_.openSettings()
                exit = True
        # turn on autorefresh if script turned it off
        #xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % (header, _L_( 32545 ), time_delay, image) )
        xbmc.log( "[ script.cinema.experience ] - messy_exit: %s" % exit, level=xbmc.LOGNOTICE )
        if exit:
            pass
        else:
            _clear_playlists()
            if _S_( "autorefresh" ) == "true":
                auto_refresh( autorefresh, "enable" )
            prev_trigger = activate_ha( _L_( 32614 ), None, "normal" ) # Script End
            _A_.setSetting( id='number_of_features', value='%d' % (number_of_features - 1) )
            xbmc.executehttpapi( "SetGUISetting(3,screensaver.mode,%s)" % screensaver )
            xbmcgui.Window(10025).setProperty( "CinemaExperienceRunning", "False" )
    except:
        traceback.print_exc()
        # if script fails, changes settings back
        if _S_( "autorefresh" ) == "true":
            auto_refresh( autorefresh, "enable" )
        _A_.setSetting( id='number_of_features', value='%d' % (number_of_features - 1) )
        xbmc.executehttpapi( "SetGUISetting(3,screensaver.mode,%s)" % screensaver )
        prev_trigger = activate_ha( _L_( 32614 ), None, "normal" ) # Script End
        xbmcgui.Window(10025).setProperty( "CinemaExperienceRunning", "False" )
    #sys.modules.clear()
