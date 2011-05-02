# -*- coding: utf-8 -*-

__script__ = "Cinema Experience"
__scriptID__ = "script.cinema.experience"
###########################################################
"""
    Video Playlist Module:
    - Assembles Video Playlist based on user settings
"""
############################################################
# main imports
import sys
import os
import xbmcgui
import xbmc
import xbmcaddon
import traceback, threading, re

_A_ = xbmcaddon.Addon( __scriptID__ )
# language method
_L_ = _A_.getLocalizedString
# settings method
_S_ = _A_.getSetting


# set proper message
message = 32520

#pDialog = xbmcgui.DialogProgress()
#pDialog.create( __script__, _L_( message )  )
#pDialog.update( 0 )

from urllib import quote_plus
from random import shuffle, random

log_sep = "-"*70

BASE_CACHE_PATH = os.path.join( xbmc.translatePath( "special://profile" ), "Thumbnails", "Video" )
BASE_CURRENT_SOURCE_PATH = os.path.join( xbmc.translatePath( "special://profile/addon_data/" ), os.path.basename( _A_.getAddonInfo('path') ) )
BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join( _A_.getAddonInfo('path'), 'resources' ) )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )
from ce_playlist import _get_special_items, _get_trailers, _set_trailer_info
if _S_("pre_eden") == "true":
    from pre_eden_code import _get_queued_video_info
    from json_utils import retrieve_movie_db
    movie_db = retrieve_movie_db()
else:
    from dharma_code import _get_queued_video_info
    movie_db = None

class Main:
    def __init__( self ):
        self.trigger_list = []
        self.downloaded_trailers = []
        self._play_mode = _S_( "trailer_play_mode" )
        self.number_of_features = int( _S_( "number_of_features") ) + 1
        self.playlistsize = xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size()
        self._build_trigger_list()
        self._start()
        self._save_trigger_list()
        # Set play mode back to the original setting
        _A_.setSetting( id='trailer_play_mode', value='%d' % int( self._play_mode ) )        

    def _save_trigger_list( self ):
        xbmc.log( "[script.cinema.experience] - Saving trigger List", level=xbmc.LOGNOTICE)
        try:
            # base path to watched file
            base_path = os.path.join( BASE_CURRENT_SOURCE_PATH, "trigger_list.txt" )
            # if the path to the source file does not exist create it
            if os.path.isfile( base_path ):
                os.remove( base_path )
            if not os.path.isdir( os.path.dirname( base_path ) ):
                os.makedirs( os.path.dirname( base_path ) )
            # open source path for writing
            file_object = open( base_path, "w" )
            # write xmlSource
            file_object.write( repr( self.trigger_list ) )
            # close file object
            file_object.close()
        except:
            xbmc.log( "[script.cinema.experience] - Error saving trigger List", level=xbmc.LOGNOTICE)
            traceback.print_exc()       
    
    def _build_trigger_list( self ):
        if self.playlistsize == 1:
            self.trigger_list.append( _L_( 32616 ) )
        else:
            for count in range( 0, self.playlistsize - 1 ):
                self.trigger_list.append( _L_( 32616 ) )
            self.trigger_list.append( _L_( 32616 ) )
    
    def _check_trailers( self ):
        if int( _S_( "trailer_play_mode" ) ) == 1:
            path = os.path.join( BASE_CURRENT_SOURCE_PATH, "downloaded_trailers.txt" )
            if xbmc.executehttpapi( "FileExists(%s)" % ( path, ) )== "<li>True":
                xbmc.log( "[script.cinema.experience] - File Exists: downloaded_trailers.txt", level=xbmc.LOGDEBUG )
                trailer_list = self._load_trailer_list()
                if trailer_list:
                    for trailer in trailer_list:
                        trailer_detail = _set_trailer_info( trailer )
                        self.downloaded_trailers += trailer_detail
                else:
                    # Change trailer play mode to stream if no download 
                    xbmc.log( "[script.cinema.experience] - Empty File: downloaded_trailers.txt", level=xbmc.LOGDEBUG )
                    _A_.setSetting( id='trailer_play_mode', value='%d' % 0 )
            else:
                # Change trailer play mode to stream if no download 
                xbmc.log( "[script.cinema.experience] - File Does Not Exists: downloaded_trailers.txt", level=xbmc.LOGDEBUG )
                _A_.setSetting( id='trailer_play_mode', value='%d' % 0 )
        else:
            pass
                    
    def _load_trailer_list( self ):
        xbmc.log( "[script.cinema.experience] - Loading Downloaded Trailer List", level=xbmc.LOGNOTICE)
        try:
            # set base watched file path
            base_path = os.path.join( BASE_CURRENT_SOURCE_PATH, "downloaded_trailers.txt" )
            # open path
            usock = open( base_path, "r" )
            # read source
            trailer_list = eval( usock.read() )
            # close socket
            usock.close()
        except:
            trailer_list = []
        return trailer_list
        
    def _start( self ):
        mpaa = audio = genre = movie = equivalent_mpaa = ""
        try:
            # create the playlist
            self.playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
            # Check to see if multiple features have been set in settings
            # if multiple features is greater than 1(not a single feature)
            # add the intermission videos and audio files for the 2, third, etc movies
            if self.playlistsize > 1:
                if int( _S_( "intermission_video") ) > 0 or _S_( "intermission_audio") or _S_( "intermission_ratings"):
                    mpaa, audio, genre, movie, equivalent_mpaa = self._add_intermission_videos()
            # otherwise just build for a single video
            else:
                mpaa, audio, genre, movie, equivalent_mpaa = _get_queued_video_info( movie_db=None, feature = 0 )
            self._create_playlist( mpaa, audio, genre, movie, equivalent_mpaa )
            # play the trivia slide show
        except:
            traceback.print_exc()

    def _add_intermission_videos( self ):
        xbmc.log( "[script.cinema.experience] - Adding intermission Video(s)", level=xbmc.LOGNOTICE )
        count = 0
        index_count = 1
        for feature in range( 1, self.playlistsize ):
            mpaa, audio, genre, movie, equivalent_mpaa = _get_queued_video_info( movie_db=None, feature = index_count )
            #count = index_count
            # add intermission video
            if int( _S_( "intermission_video") ) > 0:
                xbmc.log( "[script.cinema.experience] - Inserting intermission Video(s): %s" % (0, 1, 1, 2, 3, 4, 5,)[ int( _S_( "intermission_video" ) ) ], level=xbmc.LOGNOTICE )
                xbmc.log( "[script.cinema.experience] -     playlist Position: %d" % index_count, level=xbmc.LOGDEBUG )
                p_size = xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size()
                xbmc.log( "[script.cinema.experience] -     p_size: %d" % p_size, level=xbmc.LOGDEBUG )
                _get_special_items(    playlist=self.playlist,
                                          items=( 0, 1, 1, 2, 3, 4, 5, )[ int( _S_( "intermission_video" ) ) ],
                                           path=( xbmc.translatePath( _S_( "intermission_video_file" ) ), xbmc.translatePath( _S_( "intermission_video_folder" ) ), )[ int( _S_( "intermission_video" ) ) > 1 ],
                                          genre=_L_( 32612 ),
                                         writer=_L_( 32612 ),
                                          index=index_count
                                   )
                for count in range( 0, ( xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() - p_size ) ):
                    # Insert Intermission Label into Trigger List
                    self.trigger_list.insert( index_count, _L_( 32612 ) ) 
                if xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() > p_size and int( _S_( "intermission_video" ) ) > 1:
                    index_count += int( _S_( "intermission_video" ) ) - 1
                elif xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() > p_size and int( _S_( "intermission_video" ) ) == 1:
                    index_count += int( _S_( "intermission_video" ) )                 
            # get rating video
            if ( _S_( "enable_ratings" ) ) == "true"  and (_S_( "intermission_ratings") ) == "true":
                xbmc.log( "[script.cinema.experience] - Inserting Intermission Rating Video",level=xbmc.LOGNOTICE )
                xbmc.log( "[script.cinema.experience] -     playlist Position: %d" % index_count, level=xbmc.LOGDEBUG )
                p_size = xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size()
                xbmc.log( "[script.cinema.experience] -     p_size: %d" % p_size, level=xbmc.LOGDEBUG )
                _get_special_items(    playlist=self.playlist,
                                          items=1 * ( _S_( "rating_videos_folder" ) != "" ),
                                           path=xbmc.translatePath( _S_( "rating_videos_folder" ) ) + mpaa + ".avi",
                                          genre=_L_( 32603 ),
                                         writer=_L_( 32603 ),
                                         index = index_count
                                   )
                for count in range( 0, ( xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() - p_size ) ):
                    # Insert Rating Label into Trigger List
                    self.trigger_list.insert( index_count, _L_( 32603 ) )
                if xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() > p_size:
                    index_count += 1
            # get Dolby/DTS videos
            if ( _S_( "enable_audio" ) ) == "true"  and (_S_( "intermission_audio") ) == "true":
                xbmc.log( "[script.cinema.experience] - Inserting Intermission Audio Format Video",level=xbmc.LOGNOTICE )
                xbmc.log( "[script.cinema.experience] -     playlist Position: %d" % index_count, level=xbmc.LOGDEBUG )
                p_size = xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size()
                xbmc.log( "[script.cinema.experience] -     p_size: %d" % p_size, level=xbmc.LOGDEBUG )
                _get_special_items(    playlist=self.playlist,
                                          items=1 * ( _S_( "audio_videos_folder" ) != "" ),
                                          path = xbmc.translatePath( _S_( "audio_videos_folder" ) ) + { "dca": "DTS", "ac3": "Dolby", "dtsma": "DTSHD-MA", "dtshd_ma": "DTSHD-MA", "a_truehd": "Dolby TrueHD", "truehd": "Dolby TrueHD" }.get( audio, "Other" ) + xbmc.translatePath( _S_( "audio_videos_folder" ) )[ -1 ],
                                          genre=_L_( 32606 ),
                                         writer=_L_( 32606 ),
                                         index = index_count
                                   )
                for count in range( 0, ( xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() - p_size ) ):
                    # Insert Audio Format Label into Trigger List
                    self.trigger_list.insert( index_count, _L_( 32606 ) )
                if xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() > p_size:
                    index_count += 1
            index_count += 1
        # return info from first movie in playlist
        mpaa, audio, genre, movie, equivalent_mpaa = _get_queued_video_info( 0 )
        return mpaa, audio, genre, movie, equivalent_mpaa

    def _create_playlist( self, mpaa, audio, genre, movie, equivalent_mpaa ):
        # TODO: try to get a local thumb for special videos?
        xbmc.log( "[script.cinema.experience] - Building Cinema Experience Playlist",level=xbmc.LOGNOTICE )
        # get Dolby/DTS videos
        xbmc.log( "[script.cinema.experience] - Adding Audio Format Video",level=xbmc.LOGNOTICE )
        if ( _S_( "enable_audio" ) ) == "true" and ( _S_( "audio_videos_folder" ) ):
            p_size = xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size()
            _get_special_items(    playlist=self.playlist,
                                      items=1 * ( _S_( "audio_videos_folder" ) != "" ),
                                       path=xbmc.translatePath( _S_( "audio_videos_folder" ) ) + { "dca": "DTS", "ac3": "Dolby", "dtsma": "DTSHD-MA", "dtshd_ma": "DTSHD-MA", "a_truehd": "Dolby TrueHD", "truehd": "Dolby TrueHD"  }.get( audio, "Other" ) + xbmc.translatePath( _S_( "audio_videos_folder" ) )[ -1 ],
                                      genre=_L_( 32606 ),
                                     writer=_L_( 32606 ),
                                      index=0
                               )
            for count in range( 0, ( xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() - p_size ) ):
                # Insert Audio Format Label into Trigger List
                self.trigger_list.insert( 0, _L_( 32606 ) )
        # Add Countdown video
        xbmc.log( "[script.cinema.experience] - Adding Countdown Videos: %s Video(s)" % (0, 1, 1, 2, 3, 4, 5,)[ int( _S_( "countdown_video" ) ) ], level=xbmc.LOGNOTICE )
        p_size = xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size()
        _get_special_items(    playlist=self.playlist,
                                  items=( 0, 1, 1, 2, 3, 4, 5, )[ int( _S_( "countdown_video" ) ) ],
                                   path=( xbmc.translatePath( _S_( "countdown_video_file" ) ), xbmc.translatePath( _S_( "countdown_video_folder" ) ), )[ int( _S_( "countdown_video" ) ) > 1 ],
                                  genre=_L_( 32611 ),
                                 writer=_L_( 32611 ),
                                  index=0
                           )
        for count in range( 0, ( xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() - p_size ) ):
            # Insert Countdown Label into Trigger List
            self.trigger_list.insert( 0, _L_( 32611 ) )
        # get rating video
        xbmc.log( "[script.cinema.experience] - Adding Ratings Video",level=xbmc.LOGNOTICE )
        if ( _S_( "enable_ratings" ) ) == "true" :
            p_size = xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size()
            _get_special_items(    playlist=self.playlist,
                                      items=1 * ( _S_( "rating_videos_folder" ) != "" ),
                                       path=xbmc.translatePath( _S_( "rating_videos_folder" ) ) + mpaa + ".avi",
                                      genre=_L_( 32603 ),
                                     writer=_L_( 32603 ),
                                      index=0
                              )
        for count in range( 0, ( xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() - p_size ) ):
            # Insert Rating Label into Trigger List
            self.trigger_list.insert( 0, _L_( 32603 ) )
        # get feature presentation intro videos
        xbmc.log( "[script.cinema.experience] - Adding Feature Presentation Intro Videos: %s Videos" % (0, 1, 1, 2, 3, 4, 5,)[ int( _S_( "fpv_intro" ) ) ], level=xbmc.LOGNOTICE )
        p_size = xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size()
        _get_special_items(    playlist=self.playlist,
                                  items=( 0, 1, 1, 2, 3, 4, 5, )[ int( _S_( "fpv_intro" ) ) ],
                                   path=( xbmc.translatePath( _S_( "fpv_intro_file" ) ), xbmc.translatePath( _S_( "fpv_intro_folder" ) ), )[ int( _S_( "fpv_intro" ) ) > 1 ],
                                  genre=_L_( 32601 ),
                                 writer=_L_( 32601 ),
                                  index=0
                           )
        for count in range( 0, ( xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() - p_size ) ):
            # Insert Feature Presentation Label into Trigger List
            self.trigger_list.insert( 0, _L_( 32601 ) )
        # get trailers
        xbmc.log( "[script.cinema.experience] - Retriving Trailers: %s Trailers" % (0, 1, 2, 3, 4, 5, 10,)[ int( _S_( "trailer_count" ) ) ],level=xbmc.LOGNOTICE )
        trailers = _get_trailers(  items=( 0, 1, 2, 3, 4, 5, 10, )[ int( _S_( "trailer_count" ) ) ],
                                        mpaa=equivalent_mpaa,
                                       genre=genre,
                                       movie=movie,
                                       mode = "playlist"
                                )
        # get coming attractions outro videos
        xbmc.log( "[script.cinema.experience] - Adding Coming Attraction Outro Video: %s Videos" % ( 0, 1, 1, 2, 3, 4, 5, )[ int( _S_( "cav_outro" ) ) ], level=xbmc.LOGNOTICE )
        p_size = xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size()
        _get_special_items(    playlist=self.playlist,
                                  items=( 0, 1, 1, 2, 3, 4, 5, )[ int( _S_( "cav_outro" ) ) ] * ( len( trailers ) > 0 ),
                                   path=( xbmc.translatePath( _S_( "cav_outro_file" ) ), xbmc.translatePath( _S_( "cav_outro_folder" ) ), )[ int( _S_( "cav_outro" ) ) > 1 ],
                                  genre=_L_( 32608 ),
                                 writer=_L_( 32608 ),
                                  index=0
                           )
        for count in range( 0, ( xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() - p_size ) ):
            # Insert Coming Attraction Outro Label into Trigger List
            self.trigger_list.insert( 0, _L_( 32608 ) )
        # enumerate through our list of trailers and add them to our playlist
        xbmc.log( "[script.cinema.experience] - Adding Trailers: %s Trailers" % len( trailers ),level=xbmc.LOGNOTICE )
        p_size = xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size()
        for trailer in trailers:
            # get trailers
            _get_special_items(    playlist=self.playlist,
                                       items=1,
                                        path=trailer[ 2 ],
                                       genre=trailer[ 9 ] or _L_( 32605 ),
                                       title=trailer[ 1 ],
                                   thumbnail=trailer[ 3 ],
                                        plot=trailer[ 4 ],
                                     runtime=trailer[ 5 ],
                                        mpaa=trailer[ 6 ],
                                release_date=trailer[ 7 ],
                                      studio=trailer[ 8 ] or _L_( 32605 ),
                                      writer= _L_( 32605 ),
                                    director=trailer[ 11 ],
                                       index=0
                              )
        for count in range( 0, ( xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() - p_size ) ):
            # Insert Trailer Label into Trigger List
            self.trigger_list.insert( 0, _L_( 32605 ) )
        # get coming attractions intro videos
        xbmc.log( "[script.cinema.experience] - Adding Coming Attraction Intro Videos: %s Videos" % ( 0, 1, 1, 2, 3, 4, 5, )[ int( _S_( "cav_intro" ) ) ], level=xbmc.LOGNOTICE )
        p_size = xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size()
        _get_special_items(    playlist=self.playlist,
                                  items=( 0, 1, 1, 2, 3, 4, 5, )[ int( _S_( "cav_intro" ) ) ] * ( len( trailers ) > 0 ),
                                   path=( xbmc.translatePath( _S_( "cav_intro_file" ) ), xbmc.translatePath( _S_( "cav_intro_folder" ) ), )[ int( _S_( "cav_intro" ) ) > 1 ],
                                  genre=_L_( 32600 ),
                                 writer=_L_( 32600 ),
                                  index=0
                           )
        for count in range( 0, ( xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() - p_size ) ):
            # Insert Coming Attraction Intro Label into Trigger List
            self.trigger_list.insert( 0, _L_( 32600 ) )
        # get movie theater experience intro videos
        xbmc.log( "[script.cinema.experience] - Adding Movie Theatre Intro Videos: %s Videos" % ( 0, 1, 1, 2, 3, 4, 5, )[ int( _S_( "mte_intro" ) ) ], level=xbmc.LOGNOTICE )
        p_size = xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size()
        _get_special_items(    playlist=self.playlist,
                                  items=( 0, 1, 1, 2, 3, 4, 5, )[ int( _S_( "mte_intro" ) ) ],
                                   path=( xbmc.translatePath( _S_( "mte_intro_file" ) ), xbmc.translatePath( _S_( "mte_intro_folder" ) ), )[ int( _S_( "mte_intro" ) ) > 1 ],
                                  genre=_L_( 32607 ),
                                 writer=_L_( 32607 ),
                                  index=0
                          )
        for count in range( 0, ( xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() - p_size ) ):
            # Insert Movie Theatre Intro Label into Trigger List
            self.trigger_list.insert( 0, _L_( 32607 ) )
        # get trivia outro video(s)
        print _S_( "trivia_mode" )
        if int( _S_( "trivia_mode" ) ) != 0:
            xbmc.log( "[script.cinema.experience] - Adding Trivia Outro Videos: %s Videos" % ( 0, 1, 1, 2, 3, 4, 5, )[ int( _S_( "trivia_outro" ) ) ], level=xbmc.LOGNOTICE )
            p_size = xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size()
            _get_special_items(    playlist=self.playlist,
                                      items=( 0, 1, 1, 2, 3, 4, 5, )[ int( _S_( "trivia_outro" ) ) ],
                                       path=( xbmc.translatePath( _S_( "trivia_outro_file" ) ), xbmc.translatePath( _S_( "trivia_outro_folder" ) ), )[ int( _S_( "trivia_outro" ) ) > 1 ],
                                      genre=_L_( 32610 ),
                                     writer=_L_( 32610 ),
                                      index=0
                                #media_type="video/picture"
                               )
            for count in range( 0, ( xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() - p_size ) ):
                # Insert Trivia Outro Label into Trigger List
                self.trigger_list.insert( 0, _L_( 32610) )
        # get feature presentation outro videos
        xbmc.log( "[script.cinema.experience] - Adding Feature Presentation Outro Videos: %s Videos" % ( 0, 1, 1, 2, 3, 4, 5, )[ int( _S_( "fpv_outro" ) ) ], level=xbmc.LOGNOTICE )
        p_size = xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size()
        _get_special_items(    playlist=self.playlist,
                                  items=( 0, 1, 1, 2, 3, 4, 5, )[ int( _S_( "fpv_outro" ) ) ],
                                   path=( xbmc.translatePath( _S_( "fpv_outro_file" ) ), xbmc.translatePath( _S_( "fpv_outro_folder" ) ), )[ int( _S_( "fpv_outro" ) ) > 1 ],
                                  genre=_L_( 32602 ),
                                 writer=_L_( 32602 ),
                          )
        for count in range( 0, ( xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() - p_size ) ):
            # Insert Feature Presentation Outro Label into Trigger List
            self.trigger_list.append( _L_( 32602 ) )
        # get movie theater experience outro videos
        xbmc.log( "[script.cinema.experience] - Adding Movie Theatre Outro Videos: %s Videos" % ( 0, 1, 1, 2, 3, 4, 5, )[ int( _S_( "mte_outro" ) ) ], level=xbmc.LOGNOTICE )
        p_size = xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size()
        _get_special_items( playlist=self.playlist,
                                  items=( 0, 1, 1, 2, 3, 4, 5, )[ int( _S_( "mte_outro" ) ) ],
                                   path=( xbmc.translatePath( _S_( "mte_outro_file" ) ), xbmc.translatePath( _S_( "mte_outro_folder" ) ), )[ int( _S_( "mte_outro" ) ) > 1 ],
                                  genre=_L_( 32617 ),
                                 writer=_L_( 32617 ),
                          )
        for count in range( 0, ( xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() - p_size ) ):
            # Insert Movie Theatre Outro Label into Trigger List
            self.trigger_list.append( _L_( 32617 ) )
        xbmc.log( "[script.cinema.experience] - Playlist Size: %s" % xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size(), level=xbmc.LOGNOTICE )
        xbmc.log( "[script.cinema.experience] - Trigger List Size: %d" % len(self.trigger_list), level=xbmc.LOGNOTICE )
        return self.trigger_list
