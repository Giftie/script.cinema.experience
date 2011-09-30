# -*- coding: utf-8 -*-

__script__ = "Cinema Experience"
__scriptID__ = "script.cinema.experience"
# main imports
import os, sys, traceback
import xbmcgui
import xbmc
import xbmcaddon
import threading
import binascii
from random import shuffle, random
import re
import time

_A_ = xbmcaddon.Addon(__scriptID__)
_L_ = _A_.getLocalizedString
_S_ = _A_.getSetting

BASE_RESOURCE_PATH = os.path.join( xbmc.translatePath( _A_.getAddonInfo('path') ), 'resources' )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )
from music import parse_playlist
from folder import dirEntries
from ce_playlist import build_music_playlist

try:
    from pre_eden_code import _rebuild_playlist
    from xbmcvfs import delete as delete_file
    from xbmcvfs import exists as exists
    from xbmcvfs import copy as file_copy
    from folder import dirEntries
    volume_query = '{"jsonrpc": "2.0", "method": "Application.GetProperties", "params": { "properties": [ "volume" ] }, "id": 1}'
except:
    from dharma_code import _rebuild_playlist, dirEntries
    from os import remove as delete_file
    exists = os.path.exists
    from shutil import copy as file_copy
    volume_query = '{"jsonrpc": "2.0", "method": "XBMC.GetVolume", "id": 1}'

class Trivia( xbmcgui.WindowXML ):
    # base paths
    BASE_CURRENT_SOURCE_PATH = os.path.join( xbmc.translatePath( "special://profile/addon_data/" ), os.path.basename( _A_.getAddonInfo('path') ) )
    # special action codes
    ACTION_NEXT_SLIDE = ( 2, 3, 7, )
    ACTION_PREV_SLIDE = ( 1, 4, )
    ACTION_EXIT_SCRIPT = ( 9, 10, 92)

    def __init__( self, *args, **kwargs ):
        xbmcgui.WindowXML.__init__( self, *args, **kwargs )
        # update dialog
        self.settings = kwargs[ "settings" ]
        self.playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
        self.mpaa = kwargs[ "mpaa" ]
        self.genre = kwargs[ "genre" ]
        # initialize our class variable
        self.plist = kwargs[ "plist" ]
        self.slide_playlist = kwargs[ "slide_playlist" ]
        self.music_playlist = xbmc.PlayList( xbmc.PLAYLIST_MUSIC )
        self._init_variables()
        # turn screensaver off
        xbmc.executehttpapi( "SetGUISetting(3,screensaver.mode,None)" )
        self._get_global_timer( (self.settings[ "trivia_total_time" ] * 60 ) , self._exit_trivia )
        #display slideshow
        self.doModal()

    def onInit( self ):
        self._load_watched_trivia_file()
        # start music
        self._start_slideshow_music()
        # Build Video Playlist
        _rebuild_playlist( self.plist )
        # start slideshow
        self._next_slide( 0 )

    def _init_variables( self ):
        self.global_timer = None
        self.slide_timer = None
        self.exiting = False
        # get current screensaver
        self.screensaver = xbmc.executehttpapi( "GetGUISetting(3;screensaver.mode)" ).replace( "<li>", "" )
        self.xbmc_volume = self._get_current_volume()
        self.image_count = 0

    def _get_current_volume( self ):
        # get the current volume
        result = xbmc.executeJSONRPC( volume_query )
        if volume_query == '{"jsonrpc": "2.0", "method": "XBMC.GetVolume", "id": 1}':
            match = re.search( '"result" : ([0-9]{1,3})', result )
            if not match:
                match = re.search( '"result":([0-9]{1,3})', result )
                if not match:
                    match = re.search( '"result": ([0-9]{1,3})', result )
        else:
            match = re.search( '"volume" : ([0-9]{1,3})', result )
            if not match:
                match = re.search( '"volume":([0-9]{1,3})', result )
                if not match:
                    match = re.search( '"volume": ([0-9]{1,3})', result )
        volume = int(match.group(1))
        xbmc.log( "[script.cinema.experience] - Current Volume: %d" % volume, level=xbmc.LOGDEBUG)
        return volume

    def _start_slideshow_music( self ):
        xbmc.log( "[script.cinema.experience] - Starting Tivia Music", level=xbmc.LOGNOTICE)
        # did user set this preference
        #xbmc.log( "[script.cinema.experience] - Setting - trivia_music: %s"  % self.settings[ "trivia_music" ], level=xbmc.LOGNOTICE)
        if int(self.settings[ "trivia_music" ]) > 0:
            # check to see if script is to adjust the volume
            if self.settings[ "trivia_adjust_volume" ] == "true":
                xbmc.log( "[script.cinema.experience] - Adjusting Volume to %s" % self.settings[ "trivia_music_volume" ], level=xbmc.LOGNOTICE)
                # calculate the new volume
                volume = self.settings[ "trivia_music_volume" ]
                # set the volume percent of current volume
                xbmc.executebuiltin( "XBMC.SetVolume(%d)" % ( volume, ) )
            # play music
            #if self.settings[ "trivia_music_file" ].endswith(".m3u"):
            #    xbmc.Player().play( self.music_playlist )
            xbmc.sleep( 200 )
            xbmc.Player().play( self.music_playlist )


    def _next_slide( self, slide=1, final_slide=False ):
        # cancel timer if it's running
        if self.slide_timer is not None:
            self.slide_timer.cancel()
        # increment/decrement count
        self.image_count += slide
        # check for invalid count, TODO: make sure you don't want to reset timer
        # check to see if playlist has come to an end
        if not xbmc.Player().isPlayingAudio() and int(self.settings[ "trivia_music" ]) > 0:
                #build_music_playlist()
                xbmc.Player().play( self.music_playlist )
        else:
            pass
        if self.image_count < 0:
            self.image_count = 0
        # if no more slides, exit
        if self.image_count > len( self.slide_playlist ) -1:
            self._exit_trivia()
        else:     
            # set the property the image control uses
            xbmcgui.Window( xbmcgui.getCurrentWindowId() ).setProperty( "Slide", self.slide_playlist[ self.image_count ] )
            # add id to watched file TODO: maybe don't add if not user preference
            self.watched += [ xbmc.getCacheThumbName( self.slide_playlist[ self.image_count ] ) ]
            # start slide timer
            self._get_slide_timer()
        

    def _load_watched_trivia_file( self ):
        xbmc.log( "[script.cinema.experience] - Loading Watch Slide List", level=xbmc.LOGNOTICE)
        try:
            # set base watched file path
            base_path = os.path.join( self.BASE_CURRENT_SOURCE_PATH, "trivia_watched.txt" )
            # open path
            usock = open( base_path, "r" )
            # read source
            self.watched = eval( usock.read() )
            # close socket
            usock.close()
        except:
            self.watched = []

    def _save_watched_trivia_file( self ):
        xbmc.log( "[script.cinema.experience] - Saving Watch Slide List", level=xbmc.LOGNOTICE)
        try:
            # base path to watched file
            base_path = os.path.join( self.BASE_CURRENT_SOURCE_PATH, "trivia_watched.txt" )
            # if the path to the source file does not exist create it
            if not os.path.isdir( os.path.dirname( base_path ) ):
                os.makedirs( os.path.dirname( base_path ) )
            # open source path for writing
            file_object = open( base_path, "w" )
            # write xmlSource
            file_object.write( repr( self.watched ) )
            # close file object
            file_object.close()
        except:
            traceback.print_exc()

    def _reset_watched( self ):
        base_path = os.path.join( self.BASE_CURRENT_SOURCE_PATH, "trivia_watched.txt" )
        if exists( base_path ):
            delete_file( base_path )
            self.watched = []

    def _get_slide_timer( self ):
        self.slide_timer = threading.Timer( self.settings[ "trivia_slide_time" ], self._next_slide,() )
        self.slide_timer.start()

    def _get_global_timer( self, time, function ):
        self.global_timer = threading.Timer( time, function,() )
        self.global_timer.start()

    def _exit_trivia( self ):
        import xbmcscript_player as script
        script.Main()
        # notify we are exiting
        self.exiting = True
        # cancel timers
        self._cancel_timers()
        # save watched slides
        self._save_watched_trivia_file()
        # set the volume back to original
        # show an end image
        self._show_intro_outro( "outro" )

    def _show_intro_outro( self, type="intro" ):
        is_playing = "True"
        if type == "outro":
            xbmc.log( "[script.cinema.experience] - ## Outro ##", level=xbmc.LOGNOTICE)
            if self.settings[ "trivia_fade_volume" ] == "true" and self.settings[ "trivia_adjust_volume"] == "true":
                self._fade_volume()
            self._play_video_playlist()
        else:
            pass

    def _play_video_playlist( self ):
        # set this to -1 as True and False are taken
        self.exiting = -1
        # cancel timers
        self._cancel_timers()
        xbmc.Player().stop()
        time.sleep( 1 )
        if (self.settings[ "trivia_fade_volume" ] == "true" and self.settings[ "trivia_adjust_volume"] == "true" ):
            self._fade_volume( False )
        elif (self.settings[ "trivia_fade_volume" ] == "false" and self.settings[ "trivia_adjust_volume"] == "true" ):
            xbmc.executebuiltin( "XBMC.SetVolume(%d)" % ( self.xbmc_volume ) )
        # turn screensaver back on
        xbmc.executehttpapi( "SetGUISetting(3,screensaver.mode,%s)" % self.screensaver )
        # we play the video playlist here so the screen does not flash
        xbmc.Player().play( self.playlist )
        # close trivia slide show
        self.close()

    def _cancel_timers( self ):
        # cancel all timers
        if self.slide_timer is not None:
            self.slide_timer.cancel()
            self.slide_timer = None
        if self.global_timer is not None:
            self.global_timer.cancel()
            self.global_timer = None

    def _fade_volume( self, out=True ):
        # set initial start/end values
        volumes = range( 1, self.xbmc_volume + 1 )
        # calc sleep time, 0.5 second for rise time
        sleep_time = 0.5 / len( volumes )
        # if fading out reverse order
        if out:
            xbmc.log( "[script.cinema.experience] - Fading Volume", level=xbmc.LOGNOTICE)
            volumes = range( 1, self.settings[ "trivia_music_volume" ] )
            volumes.reverse()
            # calc sleep time, for fade time
            sleep_time = ( self.settings[ "trivia_fade_time" ] * 1.0 ) / len( volumes )
        else:
            xbmc.log( "[script.cinema.experience] - Raising Volume", level=xbmc.LOGNOTICE)
        # loop thru and set volume
        xbmc.log( "[script.cinema.experience] - Start Volume: %d " % ( self._get_current_volume() ), level=xbmc.LOGNOTICE)
        for volume in volumes:
            xbmc.executebuiltin( "XBMC.SetVolume(%d)" % volume  )
            # sleep
            #time.sleep( sleep_time )
            xbmc.sleep( int( sleep_time * 1000 ) )
        xbmc.log( "[script.cinema.experience] - Finish Volume: %d " % ( self._get_current_volume() ), level=xbmc.LOGNOTICE)

    def onClick( self, controlId ):
        pass

    def onFocus( self, controlId ):
        pass

    def onAction( self, action ):
        if action in self.ACTION_EXIT_SCRIPT and self.exiting is False:
            print action
            self._exit_trivia()
        elif action in self.ACTION_EXIT_SCRIPT and self.exiting is True:
            print action
            self._play_video_playlist()
        elif action in self.ACTION_NEXT_SLIDE and not self.exiting:
            self._next_slide()
        elif action in self.ACTION_PREV_SLIDE and not self.exiting:
            self._next_slide( -1 )
