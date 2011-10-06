# -*- coding: utf-8 -*-

__scriptID__ = "script.cinema.experience"
__modname__ = "dharma_code.py"
log_message = "[ " + __scriptID__ + " ] - [ " + __modname__ + " ]"
log_sep = "-"*70

import xbmc, xbmcgui, xbmcaddon
import traceback, os
from urllib import quote_plus

_A_ = xbmcaddon.Addon( __scriptID__ )
# language method
_L_ = _A_.getLocalizedString
# settings method
_S_ = _A_.getSetting

def _build_playlist( movie_titles ):
    for movie in movie_titles:
        xbmc.log( "[script.cinema.experience] - Movie Title: %s" % movie, level=xbmc.LOGNOTICE )
        xbmc.executehttpapi( "SetResponseFormat()" )
        xbmc.executehttpapi( "SetResponseFormat(OpenField,)" )
        # select Movie path from movieview Limit 1
        sql = "SELECT movieview.c00, movieview.strPath, movieview.strFileName, movieview.c08, movieview.c14 FROM movieview WHERE c00 LIKE '%s' LIMIT 1" % ( movie.replace( "'", "''", ), )
        xbmc.log( "[script.cinema.experience]  - SQL: %s" % ( sql, ), level=xbmc.LOGDEBUG )
        # query database for info dummy is needed as there are two </field> formatters
        try:
            movie_title, movie_path, movie_filename, thumb, genre, dummy = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % quote_plus( sql ), ).split( "</field>" )
        except:
            xbmc.log( "[script.cinema.experience] - Unable to match movie", level=xbmc.LOGERROR )
            movie_title = movie_path = movie_filename = thumb = genre = dummy = ""
        movie_full_path = os.path.join(movie_path, movie_filename).replace("\\\\" , "\\")
        xbmc.log( "[script.cinema.experience] - Movie Title: %s" % movie_title, level=xbmc.LOGNOTICE )
        xbmc.log( "[script.cinema.experience] - Movie Path: %s" % movie_path, level=xbmc.LOGNOTICE )
        xbmc.log( "[script.cinema.experience] - Movie Filename: %s" % movie_filename, level=xbmc.LOGNOTICE )
        xbmc.log( "[script.cinema.experience] - Full Movie Path: %s" % movie_full_path, level=xbmc.LOGNOTICE )
        if movie_title:
            listitem = xbmcgui.ListItem(movie_title, thumbnailImage=thumb)
            listitem.setInfo('video', {'Title': movie_title, 'Genre': genre})
            playlist.add(url=movie_full_path, listitem=listitem, )
            xbmc.sleep( 50 )

def _store_playlist():
    p_list = []
    try:
        xbmc.log( "[script.cinema.experience] - Storing Playlist", level=xbmc.LOGNOTICE )
        true = True
        false = False
        null = None
        json_query = '{"jsonrpc": "2.0", "method": "VideoPlaylist.GetItems", "params": {"fields": ["file", "thumbnail"] }, "id": 1}'
        json_response = xbmc.executeJSONRPC(json_query)
        xbmc.log( "[script.cinema.experience] - JSONRPC - %s" % json_response, level=xbmc.LOGDEBUG )
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
            movie_title = movie["label"]
            movie_full_path = movie["file"].replace("\\\\" , "\\")
            try:
                movie_thumbnail = movie["thumbnail"]
            except:
                movie_thumbnail = os.path.join( os.path.split( movie_full_path )[ 0 ], "movie.tbn" )
            xbmc.log( "[script.cinema.experience] - Movie Title: %s" % movie_title, level=xbmc.LOGDEBUG )
            xbmc.log( "[script.cinema.experience] - Movie Thumbnail: %s" % movie_thumbnail, level=xbmc.LOGDEBUG )
            xbmc.log( "[script.cinema.experience] - Full Movie Path: %s" % movie_full_path, level=xbmc.LOGDEBUG )
            plot, plotoutline, runtime, mpaa, year, studio, genre, writer, director, tagline, votes, imdbcode, rating, votes, top250 =  _get_movie_details( movie_title, movie_thumbnail, movie_full_path )
            #runtime = int( runtime.strip("min") )
            rating = float( rating )
            year = int( year )
            top250 = int( top250 )
            listitem = xbmcgui.ListItem( movie_title, thumbnailImage=movie_thumbnail )
            listitem.setInfo('Video', {'Title': movie_title, 'Plot': plot, 'PlotOutline': plotoutline, 'MPAA': mpaa, 'Year': year, 'Studio': studio, 'Genre': genre, 'Writer': writer, 'Director': director, 'Tagline': tagline, 'Code': imdbcode, 'Top250': top250, 'Votes': votes, 'Rating': rating, } )
            playlist.add(url=movie_full_path, listitem=listitem, )
        except:
            traceback.print_exc()
        # give XBMC a chance to add to the playlist... May not be needed, but what's 50ms?
        xbmc.sleep( 50 )

def _get_movie_details( movie_title="", thumbnail="", movie_full_path="" ):
    xbmc.log( "[script.cinema.experience] - [ce_playlist.py] - _get_movie_details started", level=xbmc.LOGNOTICE )
    # format our records start and end
    xbmc.executehttpapi( "SetResponseFormat()" )
    xbmc.executehttpapi( "SetResponseFormat(OpenField,)" )
    # retrive plot(c01), plotoutline(c02), runtime(c11), mpaa(c12), year(c07), studio(c18), genre(c14), writer(c06), director(c15), tagline(c03), votes(c04), imdbcode(c09), rating(c05), top250(c13) from database
    sql_query = "SELECT c01, c02, c11, c12, c07, c18, c14, c06, c15, c03, c04, c09, c05, c13 FROM movieview WHERE c00='%s' LIMIT 1" % ( movie_title.replace( "'", "''", ), )
    # the dummy string is to catch the extra </field>
    try:
        plot, plotoutline, runtime, mpaa, year, studio, genre, writer, director, tagline, votes, imdbcode, rating, top250, dummy = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % quote_plus( sql_query ), ).split( "</field>" )
    except:
        plot = plotoutline = runtime = mpaa = year = studio = genre = writer = director = tagline = votes = imdbcode = rating = top250 = ""
    return plot, plotoutline, runtime, mpaa, year, studio, genre, writer, director, tagline, votes, imdbcode, rating, votes, top250
    
def _get_queued_video_info( feature = 0 ):
    xbmc.log( "%s - _get_queued_video_info() Started" % log_message, level=xbmc.LOGDEBUG )
    equivalent_mpaa = "NR"
    try:
        # get movie name
        movie_title = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )[ feature ].getdescription()
        # this is used to skip trailer for current movie selection
        movie = os.path.splitext( os.path.basename( xbmc.PlayList( xbmc.PLAYLIST_VIDEO )[ feature ].getfilename() ) )[ 0 ]
        # format our records start and end
        xbmc.executehttpapi( "SetResponseFormat()" )
        xbmc.executehttpapi( "SetResponseFormat(OpenField,)" )
        # TODO: verify the first is the best audio
        # setup the sql, we limit to 1 record as there can be multiple entries in streamdetails
        sql = "SELECT movie.c12, movie.c14, streamdetails.strAudioCodec FROM movie, streamdetails WHERE movie.idFile=streamdetails.idFile AND streamdetails.iStreamType=1 AND c00='%s' LIMIT 1" % ( movie_title.replace( "'", "''", ), )
        xbmc.log( "%s - SQL: %s" % ( log_message, sql, ), level=xbmc.LOGDEBUG )
        # query database for info dummy is needed as there are two </field> formatters
        mpaa, genre, audio, dummy = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % quote_plus( sql ), ).split( "</field>" )
        # TODO: add a check and new sql for videos queued from files mode, or try an nfo
        # calculate rating
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
        movie_title = mpaa = audio = genre = movie = equivalent_mpaa = ""
    # spew queued video info to log
    xbmc.log( "%s - Queued Movie Information" % log_message, level=xbmc.LOGDEBUG )
    xbmc.log( "%s %s" % ( log_message,log_sep ), level=xbmc.LOGDEBUG )
    xbmc.log( "%s - Title: %s" % ( log_message, movie_title, ), level=xbmc.LOGDEBUG )
    xbmc.log( "%s - Path: %s" % ( log_message, movie, ), level=xbmc.LOGDEBUG )
    xbmc.log( "%s - Genre: %s" % ( log_message, genre, ), level=xbmc.LOGDEBUG )
    xbmc.log( "%s - MPAA: %s" % ( log_message, mpaa, ), level=xbmc.LOGDEBUG )
    xbmc.log( "%s - Audio: %s" % ( log_message, audio, ), level=xbmc.LOGDEBUG )
    if _S_( "audio_videos_folder" ):
        xbmc.log( "%s - Folder: %s" % ( log_message, ( xbmc.translatePath( _S_( "audio_videos_folder" ) ) + { "dca": "DTS", "ac3": "Dolby", "dtsma": "DTSHD-MA", "dtshd_ma": "DTSHD-MA", "a_truehd": "Dolby TrueHD", "truehd": "Dolby TrueHD" }.get( audio, "Other" ) + xbmc.translatePath( _S_( "audio_videos_folder" ) )[ -1 ], ) ), level=xbmc.LOGDEBUG )
    xbmc.log( "%s  %s" % ( log_message, log_sep ), level=xbmc.LOGDEBUG )
    # return results
    return mpaa, audio, genre, movie, equivalent_mpaa