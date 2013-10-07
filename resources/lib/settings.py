# -*- coding: utf-8 -*- 
import sys, os
import xbmcgui, xbmc, xbmcaddon, xbmcvfs

__script__               = sys.modules[ "__main__" ].__script__
__scriptID__             = sys.modules[ "__main__" ].__scriptID__
__addon__                = xbmcaddon.Addon( __scriptID__ )
__setting__              = __addon__.getSetting
BASE_CACHE_PATH          = sys.modules[ "__main__" ].BASE_CACHE_PATH
BASE_RESOURCE_PATH       = sys.modules[ "__main__" ].BASE_RESOURCE_PATH
BASE_CURRENT_SOURCE_PATH = sys.modules[ "__main__" ].BASE_CURRENT_SOURCE_PATH
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import utils

true = True
false = False
null = None

class settings():
  def __init__( self, *args, **kwargs ):
    utils.log( 'settings() - __init__' )
    self.start()
     
  def start(self):
    utils.log('settings() - start')
    self.trivia_settings            = {         "trivia_mode": int( __setting__( "trivia_mode" ) ),
                                          "trivia_total_time": int( float( __setting__( "trivia_total_time" ) ) ),
                                        "trivia_slide_time_s": int( float( __setting__( "trivia_slide_time_s" ) ) ),
                                        "trivia_slide_time_q": int( float( __setting__( "trivia_slide_time_q" ) ) ),
                                        "trivia_slide_time_c": int( float( __setting__( "trivia_slide_time_c" ) ) ),
                                        "trivia_slide_time_a": int( float( __setting__( "trivia_slide_time_a" ) ) ),
                                               "trivia_music": int( __setting__( "trivia_music" ) ),
                                              "trivia_folder": xbmc.translatePath( __setting__( "trivia_folder" ) ).decode('utf-8'),
                                       "trivia_adjust_volume": eval( __setting__( "trivia_adjust_volume" ) ),
                                         "trivia_fade_volume": eval( __setting__( "trivia_fade_volume" ) ),
                                           "trivia_fade_time": int( float( __setting__( "trivia_fade_time" ) ) ),
                                          "trivia_music_file": xbmc.translatePath( __setting__( "trivia_music_file" ) ).decode('utf-8'),
                                        "trivia_music_folder": xbmc.translatePath( __setting__( "trivia_music_folder" ) ).decode('utf-8'),
                                        "trivia_music_volume": int( float( __setting__( "trivia_music_volume" ) ) ),
                                      "trivia_unwatched_only": eval( __setting__( "trivia_unwatched_only" ) ), 
                                         "trivia_limit_query": eval( __setting__( "trivia_limit_query" ) ),
                                      "trivia_moviequiz_mode": int( __setting__( "trivia_moviequiz_mode" ) ),
                                    "trivia_moviequiz_qlimit": int( float( __setting__( "trivia_moviequiz_qlimit" ) ) ),
                                              "trivia_rating": __setting__( "trivia_rating" )
                                      }
                              
    self.trailer_settings           = {       "trailer_count": ( 0, 1, 2, 3, 4, 5, 10, )[int( float( __setting__( "trailer_count" ) ) ) ],
                                            "trailer_scraper": ( "amt_database", "amt_current", "local", "xbmc_library", )[int( float( __setting__( "trailer_scraper" ) ) ) ],
                                          "trailer_play_mode": int( float( __setting__( "trailer_play_mode" ) ) ),
                                    "trailer_download_folder": xbmc.translatePath( __setting__( "trailer_download_folder" ) ).decode('utf-8'),
                                             "trailer_folder": xbmc.translatePath( __setting__( "trailer_folder" ) ).decode('utf-8'),
                                        "trailer_amt_db_file": xbmc.translatePath( __setting__( "trailer_amt_db_file" ) ).decode('utf-8'),
                                        "trailer_newest_only": eval( __setting__( "trailer_newest_only" ) ),
                                            "trailer_quality": ( "Standard", "480p", "720p", "1080p" )[ int( float( __setting__( "trailer_quality" ) ) ) ],
                                        "trailer_quality_url": ( "", "_480p", "_720p", "_720p", )[ int( float( __setting__( "trailer_quality" ) ) ) ],
                                            "trailer_hd_only": eval( __setting__( "trailer_hd_only" ) ),
                                         "trailer_limit_mpaa": eval( __setting__( "trailer_limit_mpaa" ) ),
                                        "trailer_limit_genre": eval( __setting__( "trailer_limit_genre" ) ),
                                             "trailer_rating": __setting__( "trailer_rating" ),
                               "trailer_unwatched_movie_only": eval( __setting__( "trailer_unwatched_movie_only" ) ),
                                     "trailer_unwatched_only": eval( __setting__( "trailer_unwatched_only" ) ),
                                       "trailer_skip_youtube": eval( __setting__( "trailer_skip_youtube" ) )
                                      }

    self.video_settings             = {           "mte_intro": ( 0, 1, 1, 2, 3, 4, 5, )[ int( float( __setting__( "mte_intro" ) ) ) ],
                                             "mte_intro_type": ( "file", "folder" )[ int( float( __setting__( "mte_intro" ) ) ) > 1 ],
                                             "mte_intro_file": xbmc.translatePath( __setting__( "mte_intro_file" ) ).decode('utf-8'),
                                           "mte_intro_folder": xbmc.translatePath( __setting__( "mte_intro_folder" ) ).decode('utf-8'),
                                                  "mte_outro": ( 0, 1, 1, 2, 3, 4, 5, )[ int( float( __setting__( "mte_outro" ) ) ) ],
                                             "mte_outro_type": ( "file", "folder" )[ int( float( __setting__( "mte_outro" ) ) ) > 1 ],
                                             "mte_outro_file": xbmc.translatePath( __setting__( "mte_outro_file" ) ).decode('utf-8'),
                                           "mte_outro_folder": xbmc.translatePath( __setting__( "mte_outro_folder" ) ).decode('utf-8'),
                                                  "fpv_intro": ( 0, 1, 1, 2, 3, 4, 5, )[ int( float( __setting__( "fpv_intro" ) ) ) ],
                                             "fpv_intro_type": ( "file", "folder" )[ int( float( __setting__( "fpv_intro" ) ) ) > 1 ],
                                             "fpv_intro_file": xbmc.translatePath( __setting__( "fpv_intro_file" ) ).decode('utf-8'),
                                           "fpv_intro_folder": xbmc.translatePath( __setting__( "fpv_intro_folder" ) ).decode('utf-8'),
                                                  "fpv_outro": ( 0, 1, 1, 2, 3, 4, 5, )[ int( float( __setting__( "fpv_outro" ) ) ) ],
                                             "fpv_outro_type": ( "file", "folder" )[ int( float( __setting__( "fpv_outro" ) ) ) > 1 ],
                                             "fpv_outro_file": xbmc.translatePath( __setting__( "fpv_outro_file" ) ).decode('utf-8'),
                                           "fpv_outro_folder": xbmc.translatePath( __setting__( "fpv_outro_folder" ) ).decode('utf-8'),
                                             "enable_ratings": eval( __setting__( "enable_ratings" ) ),
                                       "rating_videos_folder": xbmc.translatePath( __setting__( "rating_videos_folder" ) ).decode('utf-8'),
                                               "enable_audio": eval( __setting__( "enable_audio" ) ),
                                        "audio_videos_folder": xbmc.translatePath( __setting__( "audio_videos_folder" ) ).decode('utf-8'),
                                            "countdown_video": ( 0, 1, 1, 2, 3, 4, 5, )[ int( float( __setting__( "countdown_video" ) ) ) ],
                                       "countdown_video_type": ( "file", "folder" )[ int( float( __setting__( "countdown_video" ) ) ) > 1 ],
                                       "countdown_video_file": xbmc.translatePath( __setting__( "countdown_video_file" ) ).decode('utf-8'),
                                     "countdown_video_folder": xbmc.translatePath( __setting__( "countdown_video_folder" ) ).decode('utf-8'),
                                                  "cav_intro": ( 0, 1, 1, 2, 3, 4, 5, )[ int( float( __setting__( "cav_intro" ) ) ) ],
                                             "cav_intro_type": ( "file", "folder" )[ int( float( __setting__( "cav_intro" ) ) ) > 1 ],
                                             "cav_intro_file": xbmc.translatePath( __setting__( "cav_intro_file" ) ).decode('utf-8'),
                                           "cav_intro_folder": xbmc.translatePath( __setting__( "cav_intro_folder" ) ).decode('utf-8'),
                                                  "cav_outro": ( 0, 1, 1, 2, 3, 4, 5, )[ int( float( __setting__( "cav_outro" ) ) ) ],
                                             "cav_outro_type": ( "file", "folder" )[ int( float( __setting__( "cav_outro" ) ) ) > 1 ],
                                             "cav_outro_file": xbmc.translatePath( __setting__( "cav_outro_file" ) ).decode('utf-8'),
                                           "cav_outro_folder": xbmc.translatePath( __setting__( "cav_outro_folder" ) ).decode('utf-8'),
                                               "trivia_intro": ( 0, 1, 1, 2, 3, 4, 5, )[ int( float( __setting__( "trivia_intro" ) ) ) ],
                                          "trivia_intro_type": ( "file", "folder" )[ int( float( __setting__( "trivia_intro" ) ) ) > 1 ],
                                          "trivia_intro_file": xbmc.translatePath( __setting__( "trivia_intro_file" ) ).decode('utf-8'),
                                        "trivia_intro_folder": xbmc.translatePath( __setting__( "trivia_intro_folder" ) ).decode('utf-8'),
                                               "trivia_outro": ( 0, 1, 1, 2, 3, 4, 5, )[ int( float( __setting__( "trivia_outro" ) ) ) ],
                                          "trivia_outro_type": ( "file", "folder" )[ int( float( __setting__( "trivia_outro" ) ) ) > 1 ],
                                          "trivia_outro_file": xbmc.translatePath( __setting__( "trivia_outro_file" ) ).decode('utf-8'),
                                        "trivia_outro_folder": xbmc.translatePath( __setting__( "trivia_outro_folder" ) ).decode('utf-8')
                                           }

    self.ha_settings            = {               "ha_enable": eval( __setting__( "ha_enable" ) ),
                                           "ha_multi_trigger": eval( __setting__( "ha_multi_trigger" ) ),
                                            "ha_script_start": eval( __setting__( "ha_script_start" ) ),
                                            "ha_trivia_intro": eval( __setting__( "ha_trivia_intro" ) ),
                                            "ha_trivia_start": eval( __setting__( "ha_trivia_start" ) ),
                                            "ha_trivia_outro": eval( __setting__( "ha_trivia_outro" ) ),
                                               "ha_mte_intro": eval( __setting__( "ha_mte_intro" ) ),
                                               "ha_cav_intro": eval( __setting__( "ha_cav_intro" ) ),
                                           "ha_trailer_start": eval( __setting__( "ha_trailer_start" ) ),
                                               "ha_cav_outro": eval( __setting__( "ha_cav_outro" ) ),
                                               "ha_fpv_intro": eval( __setting__( "ha_fpv_intro" ) ),
                                             "ha_mpaa_rating": eval( __setting__( "ha_mpaa_rating" ) ),
                                         "ha_countdown_video": eval( __setting__( "ha_countdown_video" ) ),
                                            "ha_audio_format": eval( __setting__( "ha_audio_format" ) ),
                                                   "ha_movie": eval( __setting__( "ha_movie" ) ),
                                               "ha_fpv_outro": eval( __setting__( "ha_fpv_outro" ) ),
                                               "ha_mte_outro": eval( __setting__( "ha_mte_outro" ) ),
                                            "ha_intermission": eval( __setting__( "ha_intermission" ) ),
                                              "ha_script_end": eval( __setting__( "ha_script_end" ) ),
                                                  "ha_paused": eval( __setting__( "ha_paused" ) ),
                                                 "ha_resumed": eval( __setting__( "ha_resumed" ) )
                                  }

    self.extra_settings         = {     "enable_notification": eval( __setting__( "enable_notification" ) ),
                                         "number_of_features": int( float( __setting__( "number_of_features" ) ) ),
                                         "intermission_video": ( 0, 1, 1, 2, 3, 4, 5, )[ int( float( __setting__( "intermission_video" ) ) ) ],
                                    "intermission_video_type": ( "file", "folder" )[ int( __setting__( "intermission_video" ) ) > 1 ],
                                    "intermission_video_file": xbmc.translatePath( __setting__( "intermission_video_file" ) ).decode('utf-8'),
                                  "intermission_video_folder": xbmc.translatePath( __setting__( "intermission_video_folder" ) ).decode('utf-8'),
                                         "intermission_audio": eval( __setting__( "intermission_audio" ) ),
                                       "intermission_ratings": eval( __setting__( "intermission_ratings" ) ),
                                                "voxcommando": eval( __setting__( "voxcommando" ) ),
                                              "override_play": eval( __setting__( "override_play" ) )
                                  }

    self.audio_formats          = {                    "dts": "DTS",
                                                        "dca": "DTS",
                                                      "dtsma": "DTS-MA",
                                                   "dtshd_ma": "DTSHD-MA",
                                                  "dtshd_hra": "DTS-HR",
                                                      "dtshr": "DTS-HR",
                                                        "ac3": "Dolby",
                                                   "a_truehd": "Dolby TrueHD",
                                                     "truehd": "Dolby TrueHD"
                                   }
    self.triggers               = ( "Script Start", "Trivia Intro", "Trivia", "Trivia Outro", "Coming Attractions Intro", "Movie Trailer", 
                                "Coming Attractions Outro", "Movie Theater Intro", "Countdown", "Feature Presentation Intro", "Audio Format", 
                                "MPAA Rating", "Movie", "Feature Presentation Outro", "Movie Theatre Outro", "Intermission", "Script End", "Pause", "Resume" )
