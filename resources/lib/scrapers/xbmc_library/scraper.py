# -*- coding: utf-8 -*-

__scriptID__ = "script.cinema.experience"
__modname__ = "XBMC Library scraper"
"""
XBMC Movie Library Trailer Scraper
"""

import sys
import os
import xbmcaddon
import xbmc

from random import shuffle
from urllib import quote_plus
import datetime, traceback
if sys.version_info < (2, 7):
    import simplejson
else:
    import json as simplejson

logmessage = "[ " + __scriptID__ + " ] - [ " + __modname__ + " ]"
_A_ = xbmcaddon.Addon('script.cinema.experience')
_L_ = _A_.getLocalizedString
trailer_settings   = sys.modules[ "__main__" ].trailer_settings
BASE_RESOURCE_PATH = sys.modules[ "__main__" ].BASE_CURRENT_SOURCE_PATH
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )
from ce_playlist import _get_thumbnail, _get_trailer_thumbnail
unwatched_movie_only = True
__useragent__ = "QuickTime/7.2 (qtver=7.2;os=Windows NT 5.1Service Pack 3)"


class Main:
    xbmc.log( "%s - XBMC Movie Library Trailer Scraper" % logmessage, level=xbmc.LOGNOTICE )
    BASE_CURRENT_SOURCE_PATH = BASE_RESOURCE_PATH

    def __init__( self, equivalent_mpaa=None, mpaa=None, genre=None, settings=None, movie=None ):
        self.settings = settings
        if settings['trailer_limit_mpaa']:
            self.mpaa = "Rated %s" % mpaa
        else:
            self.mpaa = ""
        if settings['trailer_limit_genre'] and settings['trailer_rating'] == '--':
            self.genre = ""
        else:
            self.genre = genre.split( " / " )[ 0 ]
        self.movie = movie
        #  initialize our trailer list
        self.trailers = []

    def fetch_trailers( self ):        
        # get watched list
        self._get_watched()
        count = 0
        if self.settings[ "trailer_unwatched_movie_only" ]:
            jsonquery = '''{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": { "sort": { "order": "ascending", "method": "title", "ignorearticle": true }, "properties" : ["trailer", "mpaa", "genre", "thumbnail", "plot"], "filter": { "and": [  { "field": "playcount", "operator": "is", "value": "0" }, { "field": "mpaarating", "operator": "contains", "value": "%s" }, { "field": "genre", "operator": "contains", "value": "%s" }, { "field": "hastrailer", "operator": "true", "value": "true" } ] }  }, "id": 1}''' % ( self.mpaa, self.genre )
        else:
            jsonquery = '''{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": { "sort": { "order": "ascending", "method": "title", "ignorearticle": true }, "properties" : ["trailer", "mpaa", "genre", "thumbnail", "plot"], "filter": { "and": [  { "field": "mpaarating", "operator": "contains", "value": "%s" }, { "field": "genre", "operator": "contains", "value": "%s" }, { "field": "hastrailer", "operator": "true", "value": "true" } ] }  }, "id": 1}''' % ( self.mpaa, self.genre )
        jsonresponse = xbmc.executeJSONRPC( jsonquery )
        data = simplejson.loads( jsonresponse )
        if data.has_key('result'):
            if data['result'].has_key('movies'):
                trailers = data['result']['movies']
                shuffle( trailers )
                for trailer in trailers:
                    trailer_rating = trailer['mpaa']
                    # shorten MPAA/BBFC ratings
                    if trailer_rating == "":
                        trailer_rating = "NR"
                    elif trailer_rating.startswith("Rated"):
                        trailer_rating = trailer_rating.split( " " )[ 1 - ( len( trailer_rating.split( " " ) ) == 1 ) ]
                        trailer_rating = ( trailer_rating, "NR", )[ trailer_rating not in ( "G", "PG", "PG-13", "R", "NC-17", "Unrated", ) ]
                    elif trailer_rating.startswith("UK"):
                        trailer_rating = trailer_rating.split( ":" )[ 1 - ( len( trailer_rating.split( ":" ) ) == 1 ) ]
                        trailer_rating = ( trailer_rating, "NR", )[ trailer_rating not in ( "12", "12A", "PG", "15", "18", "R18", "MA", "U", ) ]
                    else:
                        trailer_rating = ( trailer_rating, "NR", )[ trailer_rating not in ( "12", "12A", "PG", "15", "18", "R18", "MA", "U", ) ]
                    # add trailer to our final list
                    if not trailer['trailer'].startswith( 'plugin://' ):
                        trailer_info = ( xbmc.getCacheThumbName( trailer['trailer'] ), # id
                                         trailer['label'], # title
                                         trailer['trailer'], # trailer
                                         trailer['thumbnail'], # thumb
                                         trailer['plot'], # plot
                                         '', # runtime
                                         trailer_rating, # mpaa
                                         '', # release date
                                         '', # studio
                                         trailer['genre'], # genre
                                         'Trailer', # writer
                                         '', # director 32613
                                        )
                        self.trailers += [ trailer_info ]
                        # add id to watched file TODO: maybe don't add if not user preference
                        self.watched += [ xbmc.getCacheThumbName( trailer['trailer'] ) ]
                        # increment counter
                        count += 1
                        # if we have enough exit
                        if count == self.settings[ "trailer_count" ]:
                           break
            self._save_watched()
            return self.trailers

    def _get_watched( self ):
        xbmc.log("%s - Getting Watched List" % logmessage, level=xbmc.LOGNOTICE )
        try:
            # base path to watched file
            base_path = os.path.join( self.BASE_CURRENT_SOURCE_PATH, self.settings[ "trailer_scraper" ] + "_watched.txt" )
            # open path
            usock = open( base_path, "r" )
            # read source
            self.watched = eval( usock.read() )
            # close socket
            usock.close()
        except:
            self.watched = []

    def _reset_watched( self ):
        xbmc.log("%s - Resetting Watched List" % logmessage, level=xbmc.LOGNOTICE )
        base_path = os.path.join( self.BASE_CURRENT_SOURCE_PATH, self.settings[ "trailer_scraper" ] + "_watched.txt" )
        if os.path.isfile( base_path ):
            os.remove( base_path )
            self.watched = []

    def _save_watched( self ):
        xbmc.log("%s - Saving Watched List" % logmessage, level=xbmc.LOGNOTICE )
        try:
            # base path to watched file
            base_path = os.path.join( self.BASE_CURRENT_SOURCE_PATH, self.settings[ "trailer_scraper" ] +"_watched.txt" )
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
            pass

