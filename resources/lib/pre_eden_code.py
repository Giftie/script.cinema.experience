# -*- coding: utf-8 -*-
__scriptID__ = "script.cinema.experience"
__modname__ = "pre_eden_code.py"
log_message = "[ " + __scriptID__ + " ] - [ " + __modname__ + " ]"
log_sep = "-"*70

import xbmc, xbmcgui, xbmcaddon
import traceback, os
from json_utils import find_movie_details

_A_ = xbmcaddon.Addon( __scriptID__ )
# language method
_L_ = _A_.getLocalizedString
# settings method
_S_ = _A_.getSetting

def _store_playlist():
    p_list = []
    try:
        xbmc.log( "[script.cinema.experience] - Storing Playlist", level=xbmc.LOGNOTICE )
        true = True
        false = False
        null = None
        json_query = '{"jsonrpc": "2.0", "method": "VideoPlaylist.GetItems", "params": {"fields": ["title", "file", "thumbnail", "plot", "plotoutline", "mpaa", "rating", "studio", "tagline", "top250", "votes", "year", "director", "writingcredits", "imdbnumber", "runtime", "genre"] }, "id": 1}'
        json_response = xbmc.executeJSONRPC(json_query)
        xbmc.log( "[script.cinema.experience] - JSONRPC -\n%s" % json_response, level=xbmc.LOGDEBUG )
        response = json_response
        if response.startswith( "{" ):
            response = eval( response )
        result = response['result']
        p_list = result['items']
    except:
        xbmc.log( "[script.cinema.experience] - Error - Playlist Empty", level=xbmc.LOGNOTICE )
    return p_list

def _rebuild_playlist( plist ): # rebuild movie playlist
    xbmc.log( "[script.cinema.experience] - [ce_playlist.py] - Rebuilding Playlist", level=xbmc.LOGNOTICE )
    playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
    playlist.clear()
    print plist
    for movie in plist:
        try:
            xbmc.log( "[script.cinema.experience] - Movie Title: %s" % movie["title"], level=xbmc.LOGDEBUG )
            xbmc.log( "[script.cinema.experience] - Movie Thumbnail: %s" % movie["thumbnail"], level=xbmc.LOGDEBUG )
            xbmc.log( "[script.cinema.experience] - Full Movie Path: %s" % movie["file"], level=xbmc.LOGDEBUG )
            listitem = xbmcgui.ListItem( movie["title"], thumbnailImage=movie["thumbnail"] )
            listitem.setInfo('Video', {'Title': movie["title"], 'Plot': movie["plot"], 'PlotOutline': movie["plotoutline"], 'MPAA': movie["mpaa"], 'Year': movie["year"], 'Studio': movie["studio"], 'Genre': movie["genre"], 'Writer': movie["writingcredits"], 'Director': movie["director"], 'Rating': movie["rating"], 'Code': movie["imdbnumber"], 'Top250': movie["top250"], 'Tagline': movie["tagline"], } )
            playlist.add(url=movie["file"].replace("\\\\" , "\\"), listitem=listitem, )
        except:
            traceback.print_exc()
        # give XBMC a chance to add to the playlist... May not be needed, but what's 50ms?
        xbmc.sleep( 50 )

def obtain_audio_codec( movie_db, movie ):
    """ obtain_audio_codec()
    
        Supplied with a movie from JSON RPC and retrives the first audio codec(normally the main one)
       
    """
    matched_movie = find_movie_details( movie_db=movie_db, field="title", match_value=movie )
    audio_codec = ['streamDetails']['audio'][0]['codec']
    return audio_codec

def _get_queued_video_info( movie_db=None, feature = 0 ):
    xbmc.log( "%s - _get_queued_video_info() Started" % log_message, level=xbmc.LOGDEBUG )
    equivalent_mpaa = "NR"
    if not movie_db:
        from json_utils import retrieve_movie_db
    try:
        # get movie name
        movie_title = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )[ feature ].getdescription()
        # this is used to skip trailer for current movie selection
        movie = os.path.splitext( os.path.basename( xbmc.PlayList( xbmc.PLAYLIST_VIDEO )[ feature ].getfilename() ) )[ 0 ]
        movie_details = find_movie_details( movie_db=movie_db, field="title", match_value=movie_title )
        mpaa = movie_details['mpaa']
        genre = movie_details['genre']
        audio = movie_details['streamDetails']['audio'][0]['codec']
        path = movie_details['file']
        if mpaa == "":
            mpaa = "NR"
        elif mpaa.startswith("Rated"):
            mpaa = mpaa.split( " " )[ 1 - ( len( mpaa.split( " " ) ) == 1 ) ]
            mpaa = ( mpaa, "NR", )[ mpaa not in ( "G", "PG", "PG-13", "R", "NC-17", "Unrated", ) ]
        elif mpaa.startswith("UK"):
            mpaa = mpaa.split( ":" )[ 1 - ( len( mpaa.split( ":" ) ) == 1 ) ]
            mpaa = ( mpaa, "NR", )[ mpaa not in ( "12", "12A", "PG", "15", "18", "R18", "MA", "U", ) ]
        else:
            mpaa = ( mpaa, "NR", )[ mpaa not in ( "12", "12A", "PG", "15", "18", "R18", "MA", "U", ) ]
        if mpaa not in ( "G", "PG", "PG-13", "R", "NC-17", "Unrated", "NR" ):
            if mpaa in ("12", "12A",):
                equivalent_mpaa = "PG-13"
            elif mpaa == "15":
                equivalent_mpaa = "R"
            elif mpaa == "U":
                equivalent_mpaa = "G"
            elif mpaa in ("18", "R18", "MA",):
                equivalent_mpaa = "NC-17"
        else:
            equivalent_mpaa = mpaa
    except:
        traceback.print_exc()
        movie_title = path = mpaa = audio = genre = movie = equivalent_mpaa = ""
    # spew queued video info to log
    xbmc.log( "%s - Queued Movie Information" % log_message, level=xbmc.LOGDEBUG )
    xbmc.log( "%s %s" % ( log_message,log_sep ), level=xbmc.LOGDEBUG )
    xbmc.log( "%s - Title: %s" % ( log_message, movie_title, ), level=xbmc.LOGDEBUG )
    xbmc.log( "%s - Path: %s" % ( log_message, path, ), level=xbmc.LOGDEBUG )
    xbmc.log( "%s - Genre: %s" % ( log_message, genre, ), level=xbmc.LOGDEBUG )
    xbmc.log( "%s - MPAA: %s" % ( log_message, mpaa, ), level=xbmc.LOGDEBUG )
    xbmc.log( "%s - Audio: %s" % ( log_message, audio, ), level=xbmc.LOGDEBUG )
    if _S_( "audio_videos_folder" ):
        xbmc.log( "%s - Folder: %s" % ( log_message, ( xbmc.translatePath( _S_( "audio_videos_folder" ) ) + { "dca": "DTS", "ac3": "Dolby", "dtsma": "DTSHD-MA", "dtshd_ma": "DTSHD-MA", "a_truehd": "Dolby TrueHD", "truehd": "Dolby TrueHD" }.get( audio, "Other" ) + xbmc.translatePath( _S_( "audio_videos_folder" ) )[ -1 ], ) ), level=xbmc.LOGDEBUG )
    xbmc.log( "%s  %s" % ( log_message, log_sep ), level=xbmc.LOGDEBUG )
    # return results
    return mpaa, audio, genre, movie, equivalent_mpaa