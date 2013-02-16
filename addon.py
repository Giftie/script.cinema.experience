# -*- coding: utf-8 -*-

# constants
__script__ = "Cinema Experience"
__author__ = "nuka1195-giftie-ackbarr"
__url__ = "https://github.com/Giftie/script.cinema.experience"
__version__ = "3.0.0"
__scriptID__ = "script.cinema.experience"




import xbmcgui, xbmc, xbmcaddon, xbmcvfs
import os, re, sys, socket, traceback, time, __builtin__
from urllib import quote_plus
from threading import Thread
#from multiprocessing import Process as Thread

_A_ = xbmcaddon.Addon( __scriptID__ )
# language method
_L_ = _A_.getLocalizedString
# settings method
_S_ = _A_.getSetting

true = True
false = False
null = None

triggers                    = ( "Script Start", "Trivia Intro", "Trivia", "Trivia Outro", "Coming Attractions Intro", "Movie Trailer", 
                                "Coming Attractions Outro", "Movie Theater Intro", "Countdown", "Feature Presentation Intro", "Audio Format", 
                                "MPAA Rating", "Movie", "Feature Presentation Outro", "Movie Theatre Outro", "Intermission", "Script End", "Pause", "Resume" )

trivia_settings             = {        "trivia_mode": int( _S_( "trivia_mode" ) ),
                                 "trivia_total_time": int( float( _S_( "trivia_total_time" ) ) ),
                                     "trivia_folder": xbmc.translatePath( _S_( "trivia_folder" ) ),
                                 "trivia_slide_time": int( float( _S_( "trivia_slide_time" ) ) ),
                                      "trivia_intro": _S_( "trivia_intro" ),
                                      "trivia_music": _S_( "trivia_music" ),
                              "trivia_adjust_volume": eval( _S_( "trivia_adjust_volume" ) ),
                                "trivia_fade_volume": eval( _S_( "trivia_fade_volume" ) ),
                                  "trivia_fade_time": int( float( _S_( "trivia_fade_time" ) ) ),
                                 "trivia_music_file": xbmc.translatePath( _S_( "trivia_music_file" ) ),
                               "trivia_music_folder": xbmc.translatePath( _S_( "trivia_music_folder" ) ),
                               "trivia_music_volume": int( float( _S_( "trivia_music_volume" ) ) ),
                             "trivia_unwatched_only": eval( _S_( "trivia_unwatched_only" ) ), 
                                "trivia_limit_query": eval( _S_( "trivia_limit_query" ) )
                              }
                              
trailer_settings             = { "trailer_count": ( 0, 1, 2, 3, 4, 5, 10, )[int( float( _S_( "trailer_count" ) ) ) ],
                               "trailer_scraper": ( "amt_database", "amt_current", "local", "xbmc_library", )[int( float( _S_( "trailer_scraper" ) ) ) ],
                             "trailer_play_mode": int( float( _S_( "trailer_play_mode" ) ) ),
                       "trailer_download_folder": xbmc.translatePath( _S_( "trailer_download_folder" ) ),
                                "trailer_folder": xbmc.translatePath( _S_( "trailer_folder" ) ),
                           "trailer_amt_db_file": xbmc.translatePath( _S_( "trailer_amt_db_file" ) ),
                           "trailer_newest_only": eval( _S_( "trailer_newest_only" ) ),
                               "trailer_quality": ( "Standard", "480p", "720p", "1080p" )[ int( float( _S_( "trailer_quality" ) ) ) ],
                           "trailer_quality_url": ( "", "_480p", "_720p", "_720p", )[ int( float( _S_( "trailer_quality" ) ) ) ],
                               "trailer_hd_only": eval( _S_( "trailer_hd_only" ) ),
                            "trailer_limit_mpaa": eval( _S_( "trailer_limit_mpaa" ) ),
                           "trailer_limit_genre": eval( _S_( "trailer_limit_genre" ) ),
                                "trailer_rating": _S_( "trailer_rating" ),
                  "trailer_unwatched_movie_only": eval( _S_( "trailer_unwatched_movie_only" ) ),
                        "trailer_unwatched_only": eval( _S_( "trailer_unwatched_only" ) )
                               }

video_settings             = { "mte_intro": ( 0, 1, 1, 2, 3, 4, 5, )[ int( float( _S_( "mte_intro" ) ) ) ],
                          "mte_intro_type": ( "file", "folder" )[ int( float( _S_( "mte_intro" ) ) ) > 1 ],
                          "mte_intro_file": xbmc.translatePath( _S_( "mte_intro_file" ) ).decode('utf-8'),
                        "mte_intro_folder": xbmc.translatePath( _S_( "mte_intro_folder" ) ).decode('utf-8'),
                               "mte_outro": ( 0, 1, 1, 2, 3, 4, 5, )[ int( float( _S_( "mte_outro" ) ) ) ],
                          "mte_outro_type": ( "file", "folder" )[ int( float( _S_( "mte_outro" ) ) ) > 1 ],
                          "mte_outro_file": xbmc.translatePath( _S_( "mte_outro_file" ) ).decode('utf-8'),
                        "mte_outro_folder": xbmc.translatePath( _S_( "mte_outro_folder" ) ).decode('utf-8'),
                               "fpv_intro": ( 0, 1, 1, 2, 3, 4, 5, )[ int( float( _S_( "fpv_intro" ) ) ) ],
                          "fpv_intro_type": ( "file", "folder" )[ int( float( _S_( "fpv_intro" ) ) ) > 1 ],
                          "fpv_intro_file": xbmc.translatePath( _S_( "fpv_intro_file" ) ).decode('utf-8'),
                        "fpv_intro_folder": xbmc.translatePath( _S_( "fpv_intro_folder" ) ).decode('utf-8'),
                               "fpv_outro": ( 0, 1, 1, 2, 3, 4, 5, )[ int( float( _S_( "fpv_outro" ) ) ) ],
                          "fpv_outro_type": ( "file", "folder" )[ int( float( _S_( "fpv_outro" ) ) ) > 1 ],
                          "fpv_outro_file": xbmc.translatePath( _S_( "fpv_outro_file" ) ).decode('utf-8'),
                        "fpv_outro_folder": xbmc.translatePath( _S_( "fpv_outro_folder" ) ).decode('utf-8'),
                          "enable_ratings": eval( _S_( "enable_ratings" ) ),
                    "rating_videos_folder": xbmc.translatePath( _S_( "rating_videos_folder" ) ).decode('utf-8'),
                            "enable_audio": eval( _S_( "enable_audio" ) ),
                     "audio_videos_folder": xbmc.translatePath( _S_( "audio_videos_folder" ) ).decode('utf-8'),
                         "countdown_video": ( 0, 1, 1, 2, 3, 4, 5, )[ int( float( _S_( "countdown_video" ) ) ) ],
                    "countdown_video_type": ( "file", "folder" )[ int( float( _S_( "countdown_video" ) ) ) > 1 ],
                    "countdown_video_file": xbmc.translatePath( _S_( "countdown_video_file" ) ).decode('utf-8'),
                  "countdown_video_folder": xbmc.translatePath( _S_( "countdown_video_folder" ) ).decode('utf-8'),
                               "cav_intro": ( 0, 1, 1, 2, 3, 4, 5, )[ int( float( _S_( "cav_outro" ) ) ) ],
                          "cav_intro_type": ( "file", "folder" )[ int( float( _S_( "cav_intro" ) ) ) > 1 ],
                          "cav_intro_file": xbmc.translatePath( _S_( "cav_intro_file" ) ).decode('utf-8'),
                        "cav_intro_folder": xbmc.translatePath( _S_( "cav_intro_folder" ) ).decode('utf-8'),
                               "cav_outro": ( 0, 1, 1, 2, 3, 4, 5, )[ int( float( _S_( "cav_outro" ) ) ) ],
                          "cav_outro_type": ( "file", "folder" )[ int( float( _S_( "cav_outro" ) ) ) > 1 ],
                          "cav_outro_file": xbmc.translatePath( _S_( "cav_outro_file" ) ).decode('utf-8'),
                        "cav_outro_folder": xbmc.translatePath( _S_( "cav_outro_folder" ) ).decode('utf-8'),
                            "trivia_intro": ( 0, 1, 1, 2, 3, 4, 5, )[ int( float( _S_( "trivia_intro" ) ) ) ],
                       "trivia_intro_type": ( "file", "folder" )[ int( float( _S_( "trivia_intro" ) ) ) > 1 ],
                       "trivia_intro_file": xbmc.translatePath( _S_( "trivia_intro_file" ) ).decode('utf-8'),
                     "trivia_intro_folder": xbmc.translatePath( _S_( "trivia_intro_folder" ) ).decode('utf-8'),
                            "trivia_outro": ( 0, 1, 1, 2, 3, 4, 5, )[ int( float( _S_( "trivia_outro" ) ) ) ],
                       "trivia_outro_type": ( "file", "folder" )[ int( float( _S_( "trivia_outro" ) ) ) > 1 ],
                       "trivia_outro_file": xbmc.translatePath( _S_( "trivia_outro_file" ) ).decode('utf-8'),
                     "trivia_outro_folder": xbmc.translatePath( _S_( "trivia_outro_folder" ) ).decode('utf-8')
                               }

feature_settings             = { "enable_notification": eval( _S_( "enable_notification" ) ),
                                  "number_of_features": int( float( _S_( "number_of_features" ) ) ),
                                  "intermission_video": ( 0, 1, 1, 2, 3, 4, 5, )[ int( float( _S_( "intermission_video" ) ) ) ],
                             "intermission_video_type": ( "file", "folder" )[ int( _S_( "intermission_video" ) ) > 1 ],
                             "intermission_video_file": xbmc.translatePath( _S_( "intermission_video_file" ) ).decode('utf-8'),
                           "intermission_video_folder": xbmc.translatePath( _S_( "intermission_video_folder" ) ).decode('utf-8'),
                                  "intermission_audio": eval( _S_( "intermission_audio" ) ),
                                "intermission_ratings": eval( _S_( "intermission_ratings" ) )
                               }

ha_settings             = {       "ha_enable": eval( _S_( "ha_enable" ) ),
                           "ha_multi_trigger": eval( _S_( "ha_multi_trigger" ) ),
                            "ha_script_start": eval( _S_( "ha_script_start" ) ),
                            "ha_trivia_intro": eval( _S_( "ha_trivia_intro" ) ),
                            "ha_trivia_start": eval( _S_( "ha_trivia_start" ) ),
                            "ha_trivia_outro": eval( _S_( "ha_trivia_outro" ) ),
                               "ha_mte_intro": eval( _S_( "ha_mte_intro" ) ),
                               "ha_cav_intro": eval( _S_( "ha_cav_intro" ) ),
                           "ha_trailer_start": eval( _S_( "ha_trailer_start" ) ),
                               "ha_cav_outro": eval( _S_( "ha_cav_outro" ) ),
                               "ha_fpv_intro": eval( _S_( "ha_fpv_intro" ) ),
                             "ha_mpaa_rating": eval( _S_( "ha_mpaa_rating" ) ),
                         "ha_countdown_video": eval( _S_( "ha_countdown_video" ) ),
                            "ha_audio_format": eval( _S_( "ha_audio_format" ) ),
                                   "ha_movie": eval( _S_( "ha_movie" ) ),
                               "ha_fpv_outro": eval( _S_( "ha_fpv_outro" ) ),
                               "ha_mte_outro": eval( _S_( "ha_mte_outro" ) ),
                            "ha_intermission": eval( _S_( "ha_intermission" ) ),
                              "ha_script_end": eval( _S_( "ha_script_end" ) ),
                                  "ha_paused": eval( _S_( "ha_paused" ) ),
                                 "ha_resumed": eval( _S_( "ha_resumed" ) )
                          }

number_of_features = feature_settings[ "number_of_features" ] + 1
playback = ""
BASE_CACHE_PATH = os.path.join( xbmc.translatePath( "special://profile" ).decode('utf-8'), "Thumbnails", "Video" )
BASE_CURRENT_SOURCE_PATH = os.path.join( xbmc.translatePath( "special://profile/addon_data/" ).decode('utf-8'), os.path.basename( _A_.getAddonInfo('path') ) )
BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join( _A_.getAddonInfo('path').decode('utf-8'), 'resources' ) )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )
headings = ( _L_(32600), _L_(32601), _L_(32602), _L_(32603), _L_(32604), _L_(32605), _L_(32606), _L_(32607), _L_(32608), _L_(32609), _L_(32610), _L_(32611), _L_(32612) )
header = "Cinema Experience"
time_delay = 200
image = xbmc.translatePath( os.path.join( _A_.getAddonInfo("path"), "icon.png") ).decode('utf-8')
playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
is_paused = False
prev_trigger = ""
script_header = "[ %s ]" % __scriptID__

from ce_playlist import _get_special_items, build_music_playlist,  _rebuild_playlist
from slides import _fetch_slides
from new_trailer_downloader import downloader
from utils import settings_to_log

from pre_eden_code import _store_playlist, _get_queued_video_info

#Check to see if module is moved to /userdata/addon_data/script.cinema.experience
try:
    if not xbmcvfs.exists( os.path.join( BASE_CURRENT_SOURCE_PATH, "ha_scripts", "home_automation.py" ) ) and ha_settings[ "ha_enable" ]:
        source = os.path.join( BASE_RESOURCE_PATH, "ha_scripts", "home_automation.py" )
        destination = os.path.join( BASE_CURRENT_SOURCE_PATH, "ha_scripts", "home_automation.py" )
        xbmcvfs.mkdir( os.path.join( BASE_CURRENT_SOURCE_PATH, "ha_scripts" ) )        
        xbmcvfs.copy( source, destination )
        xbmc.log( "[ script.cinema.experience ] - home_automation.py copied", level=xbmc.LOGNOTICE )
    sys.path.append( os.path.join( BASE_CURRENT_SOURCE_PATH, "ha_scripts" ) )
    from home_automation import Automate
    # Import HA module set ha_imported to True if successful
    ha_imported = True
except ImportError:
    # or ha_imported to False if unsuccessful
    xbmc.log( "[ script.cinema.experience ] - Failed to import Automate", level=xbmc.LOGNOTICE )
    ha_imported = False
except:
    traceback.print_exc()
    ha_imported = False

ce_pause_time = int( float( _S_("ha_pause_time") ) )

class CE_Player( xbmc.Player ):
    def __init__(self, *args, **kwargs):
        xbmc.Player.__init__( self )

    def onPlayBackPaused( self ):
        Launch_automation().launch_automation( trigger = "Pause", prev_trigger = None )
        is_paused = True

    def onPlayBackResumed( self ):
        Launch_automation().launch_automation( trigger = "Resumed", prev_trigger = None )
        is_paused = False

class Launch_automation():
    def __init__(self, *args, **kwargs):
        pass

    def launch_automation( self, trigger = None, prev_trigger = None, mode="normal" ):
        if _S_( "ha_enable" ) == "true":
            prev_trigger = Automate().activate_ha( trigger, prev_trigger, mode )
        return prev_trigger

def footprints():
    xbmc.log( "[ script.cinema.experience ] - Script Name: %s" % __script__, level=xbmc.LOGNOTICE )
    xbmc.log( "[ script.cinema.experience ] - Script ID: %s" % __scriptID__, level=xbmc.LOGNOTICE )
    xbmc.log( "[ script.cinema.experience ] - Script Version: %s" % __version__, level=xbmc.LOGNOTICE )
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
        xbmc.log( "[script.cinema.experience] - Error Loading Trigger List", level=xbmc.LOGNOTICE)
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
    ok = xbmcgui.Dialog().ok( _L_( 32000 ), _L_( message ) )

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

def _build_playlist( movies, mode = "movie_titles" ):
    if mode == "movie_titles":
        xbmc.log( "[script.cinema.experience] - Movie Title Mode", level=xbmc.LOGNOTICE )
        for movie in movies:
            xbmc.log( "[script.cinema.experience] - Movie Title: %s" % movie, level=xbmc.LOGNOTICE )
            xbmc.executehttpapi( "SetResponseFormat()" )
            xbmc.executehttpapi( "SetResponseFormat(OpenField,)" )
            # select Movie path from movieview Limit 1
            sql = "SELECT movieview.idMovie, movieview.c00, movieview.strPath, movieview.strFileName, movieview.c08, movieview.c14 FROM movieview WHERE c00 LIKE '%s' LIMIT 1" % ( movie.replace( "'", "''", ), )
            xbmc.log( "[script.cinema.experience]  - SQL: %s" % ( sql, ), level=xbmc.LOGDEBUG )
            # query database for info dummy is needed as there are two </field> formatters
            try:
                movie_id, movie_title, movie_path, movie_filename, thumb, genre, dummy = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % quote_plus( sql ), ).split( "</field>" )
                movie_id = int( movie_id )
            except:
                traceback.print_exc()
                xbmc.log( "[script.cinema.experience] - Unable to match movie", level=xbmc.LOGERROR )
                movie_id = 0
                movie_title = movie_path = movie_filename = thumb = genre = dummy = ""
            movie_full_path = os.path.join(movie_path, movie_filename).replace("\\\\" , "\\")
            xbmc.log( "[script.cinema.experience] - Movie Title: %s" % movie_title, level=xbmc.LOGNOTICE )
            xbmc.log( "[script.cinema.experience] - Movie Path: %s" % movie_path, level=xbmc.LOGNOTICE )
            xbmc.log( "[script.cinema.experience] - Movie Filename: %s" % movie_filename, level=xbmc.LOGNOTICE )
            xbmc.log( "[script.cinema.experience] - Full Movie Path: %s" % movie_full_path, level=xbmc.LOGNOTICE )
            if not movie_id == 0:
                json_command = '{"jsonrpc": "2.0", "method": "Playlist.Add", "params": {"playlistid": 1, "item": {"movieid": %d} }, "id": 1}' % int( movie_id )
                json_response = xbmc.executeJSONRPC(json_command)
                xbmc.log( "[script.cinema.experience] - JSONRPC Response: \n%s" % json_response, level=xbmc.LOGDEBUG )
                xbmc.sleep( 50 )
    elif mode == "movie_ids":
        xbmc.log( "[script.cinema.experience] - Movie ID Mode", level=xbmc.LOGNOTICE )
        for movie_id in movies:
            xbmc.log( "[script.cinema.experience] - Movie ID: %s" % movie_id, level=xbmc.LOGNOTICE )
            json_command = '{"jsonrpc": "2.0", "method": "Playlist.Add", "params": {"playlistid": 1, "item": {"movieid": %d} }, "id": 1}' % int( movie_id )
            json_response = xbmc.executeJSONRPC( json_command )
            xbmc.log( "[script.cinema.experience] - JSONRPC Response: \n%s" % json_response, level=xbmc.LOGDEBUG )
            xbmc.sleep( 50 )

class Script():
    def __init__(self, *args, **kwargs):
        self. init_var()
        
    def init_var( self ):
        self.player = CE_Player()
        
    def start_script( self, library_view = "oldway" ):
        messy_exit = False
        xbmc.log( "[ script.cinema.experience ] - Library_view: %s" % library_view, level=xbmc.LOGNOTICE )
        early_exit = False
        movie_next = False
        prev_trigger = None
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
            plist = _store_playlist() # need to store movie playlist
            self._play_trivia( mpaa, genre, plist, equivalent_mpaa )
            _clear_playlists( "music" )
            trigger_list = _load_trigger_list()
            count = -1
            stop_check = 0
            paused = False
            # prelim programming for adding - Activate script and other additions
            while not playlist.getposition() == ( playlist.size() - 1 ):
                if playlist.getposition() > count:
                    try:
                        xbmc.log( "[ script.cinema.experience ] - Item From Trigger List: %s" % trigger_list[ playlist.getposition() ], level=xbmc.LOGNOTICE )
                    except:
                        xbmc.log( "[ script.cinema.experience ] - Problem With Trigger List", level=xbmc.LOGNOTICE )
                    xbmc.log( "[ script.cinema.experience ] - Playlist Position: %s  Playlist Size: %s " % ( ( playlist.getposition() + 1 ), ( playlist.size() ) ), level=xbmc.LOGNOTICE )
                    if not playlist.getposition() == ( playlist.size() - 1 ):
                        prev_trigger = Launch_automation().launch_automation( trigger_list[ playlist.getposition() ], prev_trigger )
                        count = playlist.getposition()
                    else: 
                        break  # Reached the last item in the playlist
                try:
                    #if not self.player.isPlayingVideo() and not is_paused:
                    if not xbmc.getCondVisibility( "Window.IsActive(fullscreenvideo)" ):
                        xbmc.log( "[ script.cinema.experience ] - Video may have stopped", level=xbmc.LOGNOTICE )
                        messy_exit = True
                        break
                except:
                    if xbmc.getCondVisibility( "Container.Content(movies)" ):
                        xbmc.log( "[ script.cinema.experience ] - Video Definitely Stopped", level=xbmc.LOGNOTICE )
                        messy_exit = True
                        break
            if not playlist.size() < 1 and not messy_exit: # To catch an already running script when a new instance started
                xbmc.log( "[ script.cinema.experience ] - Playlist Position: %s  Playlist Size: %s " % ( playlist.getposition() + 1, ( playlist.size() ) ), level=xbmc.LOGNOTICE )
                prev_trigger = Launch_automation().launch_automation( trigger_list[ playlist.getposition() ], prev_trigger )
                if trigger_list[ playlist.getposition() ] == "Movie":
                    xbmc.log( "[ script.cinema.experience ] - Item From Trigger List: %s" % trigger_list[ playlist.getposition() ], level=xbmc.LOGNOTICE )
                else:
                    xbmc.log( "[ script.cinema.experience ] - Item From Trigger List: %s" % trigger_list[ playlist.getposition() ], level=xbmc.LOGNOTICE )
                messy_exit = False
                xbmc.sleep(1000)
                self._wait_until_end()
            else:
                xbmc.log( "[ script.cinema.experience ] - User might have pressed stop", level=xbmc.LOGNOTICE )
                xbmc.log( "[ script.cinema.experience ] - Stopping Script", level=xbmc.LOGNOTICE )
                messy_exit = False
        del self.player
        return messy_exit
    
    def broadcastUDP( self, data, port = 8278 ): # XBMC's former HTTP API output port is 8278
        IPADDR = '255.255.255.255'
        PORTNUM = port
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        if hasattr(socket,'SO_BROADCAST'):
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.connect((IPADDR, PORTNUM))
        s.send(data)
        s.close()
    
    def voxcommando():
        playlistsize = playlist.size()
        if playlistsize > 1:
            movie_titles = ""
            #for feature_count in range (1, playlistsize + 1):
            for feature_count in range (1, playlistsize):
                movie_title = playlist[ feature_count - 1 ].getdescription()
                xbmc.log( "[ script.cinema.experience ] - Feature #%-2d - %s" % ( feature_count, movie_title ), level=xbmc.LOGNOTICE )
                movie_titles = movie_titles + movie_title + "<li>"
            movie_titles = movie_titles.rstrip("<li>")
            if eval( _S_( "voxcommando" ) ):
                self.broadcastUDP( "<b>CElaunch." + str( playlistsize ) + "<li>" + movie_titles + "</b>", port = 33000 )
        else:
            # get the queued video info
            movie_title = playlist[ 0 ].getdescription()
            xbmc.log( "[ script.cinema.experience ] - Feature - %s" % movie_title, level=xbmc.LOGNOTICE )
            if eval( _S_( "voxcommando" ) ):
                self.broadcastUDP( "<b>CElaunch<li>" + movie_title + "</b>", port = 33000 )

    # No longer works in Frodo to be removed
    def _sqlquery( self, sqlquery ):
        movie_list = []
        movies = []
        xbmc.executehttpapi( "SetResponseFormat()" )
        xbmc.executehttpapi( "SetResponseFormat(OpenField,)" )
        sqlquery = "SELECT movieview.c00 FROM movieview JOIN genrelinkmovie ON genrelinkmovie.idMovie=movieview.idMovie JOIN genre ON genrelinkmovie.idGenre=genre.idGenre WHERE strGenre='Action' ORDER BY RANDOM() LIMIT 4"
        xbmc.log( "[ script.cinema.experience ]  - SQL: %s" % ( sqlquery, ), level=xbmc.LOGDEBUG )
        try:
            sqlresult = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % quote_plus( sqlquery ), )
            xbmc.log( "[ script.cinema.experience ] - sqlresult: %s" % sqlresult, level=xbmc.LOGDEBUG )
            movies = sqlresult.split("</field>")
            movie_list = movies[ 0:len( movies ) -1 ]
        except:
            xbmc.log( "[ script.cinema.experience ] - Error searching database", level=xbmc.LOGNOTICE )
        return movie_list

    def trivia_intro( self ):
        xbmc.log( "[ script.cinema.experience ] - ## Intro ##", level=xbmc.LOGNOTICE)
        play_list = playlist
        play_list.clear()
        # initialize intro lists
        playlist_intro = []
        # get trivia intro videos
        _get_special_items( playlist=play_list,
                               items=( 0, 1, 1, 2, 3, 4, 5, )[ int( _S_( "trivia_intro" ) ) ],
                                path=( xbmc.translatePath( _S_( "trivia_intro_file" ) ), xbmc.translatePath( _S_( "trivia_intro_folder" ) ), )[ int( _S_( "trivia_intro" ) ) > 1 ],
                               genre= "Trivia Intro",
                               index=0,
                          media_type="video"
                          )
        if not int( _S_( "trivia_intro" ) ) == 0:
            self.player.play( play_list )
            
    def start_downloader( self, mpaa, genre, equivalent_mpaa ):
        # start the downloader if Play Mode is set to stream and if scraper is not Local or XBMC_library
        if ( int( _S_( "trailer_play_mode" ) ) == 1 ) and ( not ( int( _S_( "trailer_scraper" ) ) in (2, 3) ) ):
            xbmc.log( "[ script.cinema.experience ] - Starting Downloader Thread", level=xbmc.LOGNOTICE )
            thread = Thread( target=downloader, args=( mpaa, genre, equivalent_mpaa ) )
            thread.start()
        else:
            pass
            
    def _wait_until_end( self ): # wait until the end of the playlist(for Trivia Intro)
        xbmc.log( "[ script.cinema.experience ] - Waiting Until End Of Video", level=xbmc.LOGNOTICE)
        try:
            self.psize = int( xbmc.PlayList( xbmc.PLAYLIST_VIDEO ).size() ) - 1
            xbmc.log( "[ script.cinema.experience ] - Playlist Size: %s" % ( self.psize + 1 ), level=xbmc.LOGDEBUG)
            while xbmc.PlayList( xbmc.PLAYLIST_VIDEO ).getposition() < self.psize:
                pass
            xbmc.log( "[ script.cinema.experience ] - Video TotalTime: %s" % self.player.getTotalTime(), level=xbmc.LOGDEBUG)
            while self.player.getTime() < ( self.player.getTotalTime() - 1 ):
                pass
            xbmc.log( "[ script.cinema.experience ] - Video getTime: %s"  % self.player.getTime(), level=xbmc.LOGDEBUG)
            #xbmc.sleep(400)
        except:
            traceback.print_exc()
            xbmc.log( "[ script.cinema.experience ] - Video either stopped or skipped, Continuing on...", level=xbmc.LOGDEBUG)

    def _play_trivia( self, mpaa, genre, plist, equivalent_mpaa ):
        Launch_automation().launch_automation( triggers[0] ) # Script Start - Or where it seems to be
        if int( _S_( "trivia_mode" ) ) == 2: # Start Movie Quiz Script
            xbmc.log( "[ script.cinema.experience ] - Starting script.moviequiz", level=xbmc.LOGNOTICE )
            self.start_downloader( mpaa, genre, equivalent_mpaa )
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
    #            pDialog.close()
                Launch_automation().launch_automation( triggers[0] ) # Script Start - Or where it seems to be
                self.trivia_intro()        
                if playlist.size() > 0:
                    self._wait_until_end()
                xbmc.sleep(500) # wait .5 seconds
                path = _MA_.getAddonInfo('path')
                question_type = 1
                mode = ( True, False )[ int( float( _S_( "trivia_moviequiz_mode" ) ) ) ]
                mpaa = (  _S_( "trivia_rating" ), equivalent_mpaa, )[ eval( _S_( "trivia_limit_query" ) ) ]
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
            #xbmc.sleep(500) # wait .5 seconds
            self.player.play( playlist )
        elif _S_( "trivia_folder" ) and int( _S_( "trivia_mode" ) ) == 1:  # Start Slide Show
            self.start_downloader( mpaa, genre, equivalent_mpaa )
            # trivia settings, grab them here so we don't need another _S_() object
            if not int( _S_( "trivia_music" ) )== 0:
                build_music_playlist()
            # set the proper mpaa rating user preference
            mpaa = (  _S_( "trivia_rating" ), equivalent_mpaa, )[ eval( _S_( "trivia_limit_query" ) ) ]
            xbmc.log( "[ script.cinema.experience ] - Slide MPAA Rating: %s" % equivalent_mpaa, level=xbmc.LOGNOTICE )
            # import trivia module and execute the gui
            slide_playlist = _fetch_slides( equivalent_mpaa )
            self.trivia_intro()
            if playlist.size() > 0:
                Launch_automation().launch_automation( triggers[1] ) # Trivia Intro
                xbmc.sleep(500) # wait .5 seconds 
                self._wait_until_end()
            #xbmc.sleep(500) # wait .5 seconds 
            __builtin__.plist = plist
            __builtin__.slide_playlist = slide_playlist
            __builtin__.movie_mpaa = mpaa
            __builtin__.movie_genre = genre
            from xbmcscript_trivia import Trivia
            xbmc.log( "[ script.cinema.experience ] - Starting Trivia script", level=xbmc.LOGNOTICE )
            Launch_automation().launch_automation( triggers[2] ) # Trivia Start
            ui = Trivia( "script-CExperience-trivia.xml", _A_.getAddonInfo('path'), "default", "720p" )
            ui.doModal()
            del ui
            # we need to activate the video window
            #xbmc.sleep(5) # wait .005 seconds
            xbmc.executebuiltin( "XBMC.ActivateWindow(2005)" )
            self.player.play( playlist )
        elif int( _S_( "trivia_mode" ) ) == 0: # No Trivia
            # no trivia slide show so play the video
            self.start_downloader( mpaa, genre, equivalent_mpaa )
            _rebuild_playlist( plist )
            # play the video playlist
            import xbmcscript_player as script
            script.Main()
            Launch_automation().launch_automation( triggers[0] ) # Script Start - Or where it seems to be
            xbmc.sleep(500) # wait .5 seconds
            self.player.play( playlist )
            

if __name__ == "__main__" :
    #xbmc.sleep( 2000 )
    footprints()
    prev_trigger = ""
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
                    elif sys.argv[ 1 ] == "oldway":                       
                        _A_.setSetting( id='number_of_features', value='0' ) # set number of features to 1
                        _clear_playlists()
                        xbmc.sleep( 250 )
                        xbmc.executebuiltin( "Action(Queue,%d)" % ( xbmcgui.getCurrentWindowId() - 10000, ) )
                        xbmc.log( "[ script.cinema.experience ] - Action(Queue,%d)" % ( xbmcgui.getCurrentWindowId() - 10000, ), level=xbmc.LOGNOTICE )
                        # we need to sleep so the video gets queued properly
                        xbmc.sleep( 250 )
                        exit = Script().start_script( "oldway" )
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
                            _A_.openSettings()
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
                _A_.setSetting( id='number_of_features', value='0' ) # set number of features to 1
                _clear_playlists()
                xbmc.executebuiltin( "Action(Queue,%d)" % ( xbmcgui.getCurrentWindowId() - 10000, ) )
                xbmc.log( "[ script.cinema.experience ] - Action(Queue,%d)" % ( xbmcgui.getCurrentWindowId() - 10000, ), level=xbmc.LOGNOTICE )
                # we need to sleep so the video gets queued properly
                xbmc.sleep( 500 )
                exit = Script().start_script( "oldway" )
            else:
                _A_.openSettings()
                exit = True
        #xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % (header, _L_( 32545 ), time_delay, image) )
        xbmc.log( "[ script.cinema.experience ] - messy_exit: %s" % exit, level=xbmc.LOGNOTICE )
        if exit:
            pass
        else:
            _clear_playlists()
            prev_trigger = Launch_automation().launch_automation( triggers[16], None ) # Script End
            _A_.setSetting( id='number_of_features', value='%d' % (number_of_features - 1) )
            xbmcgui.Window(10025).setProperty( "CinemaExperienceRunning", "False" )
    except:
        traceback.print_exc()
        # if script fails, changes settings back
        _A_.setSetting( id='number_of_features', value='%d' % (number_of_features - 1) )
        prev_trigger = Launch_automation().launch_automation( triggers[16], None ) # Script End
        xbmcgui.Window(10025).setProperty( "CinemaExperienceRunning", "False" )
