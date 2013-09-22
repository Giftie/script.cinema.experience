# -*- coding: utf-8 -*-

import sys, os
import xbmcgui, xbmc, xbmcaddon

trivia_settings          = sys.modules[ "__main__" ].trivia_settings
trailer_settings         = sys.modules[ "__main__" ].trailer_settings
general_settings         = sys.modules[ "__main__" ].general_settings
video_settings           = sys.modules[ "__main__" ].video_settings
audio_formats            = sys.modules[ "__main__" ].audio_formats
ha_settings              = sys.modules[ "__main__" ].ha_settings
BASE_CACHE_PATH          = sys.modules[ "__main__" ].BASE_CACHE_PATH
BASE_RESOURCE_PATH       = sys.modules[ "__main__" ].BASE_RESOURCE_PATH
BASE_CURRENT_SOURCE_PATH = sys.modules[ "__main__" ].BASE_CURRENT_SOURCE_PATH
__language__             = sys.modules[ "__main__" ].__language__
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

KEY_BUTTON_BACK  = 275
KEY_KEYBOARD_ESC = 61467

class GUI( xbmcgui.WindowXMLDialog ):
    def __init__( self, *args, **kwargs ):
        pass
        
    def onInit( self ):
        self.setup_all()
        
    def setup_all( self ):
        self.setFocusId( 100 )
    
    def clear_setting_properties( self ):
        self.getControl( 110 ).setLabel( "", label2 = "" )
        self.getControl( 111 ).setLabel( "", label2 = "" )
        self.getControl( 112 ).setLabel( "", label2 = "" )
        self.getControl( 113 ).setLabel( "", label2 = "" )
        self.getControl( 114 ).setLabel( "", label2 = "" )
        self.getControl( 115 ).setLabel( "", label2 = "" )
        self.getControl( 116 ).setLabel( "", label2 = "" )
        self.getControl( 117 ).setLabel( "", label2 = "" )
        self.getControl( 118 ).setLabel( "", label2 = "" )
        self.getControl( 119 ).setLabel( "", label2 = "" )
        self.getControl( 120 ).setLabel( "", label2 = "" )
        self.getControl( 121 ).setLabel( "", label2 = "" )
        self.getControl( 122 ).setLabel( "", label2 = "" )
        self.getControl( 123 ).setLabel( "", label2 = "" )
        self.getControl( 124 ).setLabel( "", label2 = "" )
        self.getControl( 125 ).setLabel( "", label2 = "" )
        self.getControl( 126 ).setLabel( "", label2 = "" )
        self.getControl( 127 ).setLabel( "", label2 = "" )
        self.getControl( 128 ).setLabel( "", label2 = "" )
        self.getControl( 129 ).setLabel( "", label2 = "" )
        self.getControl( 130 ).setLabel( "", label2 = "" )
        xbmcgui.Window(10001).clearProperty( "Setting.1" )
        xbmcgui.Window(10001).clearProperty( "Setting.2" )
        xbmcgui.Window(10001).clearProperty( "Setting.3" )
        xbmcgui.Window(10001).clearProperty( "Setting.4" )
        xbmcgui.Window(10001).clearProperty( "Setting.5" )
        xbmcgui.Window(10001).clearProperty( "Setting.6" )
        xbmcgui.Window(10001).clearProperty( "Setting.7" )
        xbmcgui.Window(10001).clearProperty( "Setting.8" )
        xbmcgui.Window(10001).clearProperty( "Setting.9" )
        xbmcgui.Window(10001).clearProperty( "Setting.10" )
        xbmcgui.Window(10001).clearProperty( "Setting.11" )
        xbmcgui.Window(10001).clearProperty( "Setting.12" )
        xbmcgui.Window(10001).clearProperty( "Setting.13" )
        xbmcgui.Window(10001).clearProperty( "Setting.14" )
        xbmcgui.Window(10001).clearProperty( "Setting.15" )
        xbmcgui.Window(10001).clearProperty( "Setting.16" )
        xbmcgui.Window(10001).clearProperty( "Setting.17" )
        xbmcgui.Window(10001).clearProperty( "Setting.18" )
        xbmcgui.Window(10001).clearProperty( "Setting.19" )
        xbmcgui.Window(10001).clearProperty( "Setting.20" )
        xbmcgui.Window(10001).clearProperty( "Setting.21" )
        
    def set_trivia_settings( self ):
        self.clear_setting_properties()
        xbmcgui.Window(10001).setProperty( "Setting", "Trivia" )
        # Heading 1
        self.getControl( 200 ).setLabel( __language__(32801) )
        # heading 2
        self.getControl( 201 ).setLabel( __language__(32925) )
        xbmcgui.Window(10001).setProperty( "Setting.1", "true" )
        self.getControl( 110 ).setLabel( __language__(32211), label2 = ( __language__(32281), __language__(32212), __language__(32213) )[ trivia_settings[ "trivia_mode" ] ] )
        if trivia_settings[ "trivia_mode" ] > 0:
            if trivia_settings[ "trivia_mode" ] == 1:
                xbmcgui.Window(10001).setProperty( "Setting.2", "true" )
                self.getControl( 111 ).setLabel( __language__(32200), label2 = "%s" % trivia_settings[ "trivia_total_time" ] )
                xbmcgui.Window(10001).setProperty( "Setting.3", "true" )
                self.getControl( 112 ).setLabel( __language__(32210), label2 = trivia_settings[ "trivia_folder" ] )
                xbmcgui.Window(10001).setProperty( "Setting.4", "true" )
                self.getControl( 113 ).setLabel( __language__(32221), label2 = "%s" % trivia_settings[ "trivia_slide_time_q" ] )
                xbmcgui.Window(10001).setProperty( "Setting.5", "true" )
                self.getControl( 114 ).setLabel( __language__(32222), label2 = "%s" % trivia_settings[ "trivia_slide_time_a" ] )
                xbmcgui.Window(10001).setProperty( "Setting.6", "true" )
                self.getControl( 115 ).setLabel( __language__(32223), label2 = "%s" % trivia_settings[ "trivia_slide_time_c" ] )
                xbmcgui.Window(10001).setProperty( "Setting.7", "true" )
                self.getControl( 116 ).setLabel( __language__(32220), label2 = "%s" % trivia_settings[ "trivia_slide_time_s" ] )
                xbmcgui.Window(10001).setProperty( "Setting.8", "true" )
                self.getControl( 117 ).setLabel( __language__(32231), label2 = ( __language__(32281), __language__(32243), __language__(32244) )[ trivia_settings[ "trivia_music" ] ] )
                if trivia_settings[ "trivia_music" ]:
                    if trivia_settings[ "trivia_music" ] == 1:
                        xbmcgui.Window(10001).setProperty( "Setting.9", "true" )
                        self.getControl( 118 ).setLabel( __language__(32230), label2 = trivia_settings[ "trivia_music_file" ] )
                    elif trivia_settings[ "trivia_music" ] == 2:
                        xbmcgui.Window(10001).setProperty( "Setting.9", "true" )
                        self.getControl( 118 ).setLabel( __language__(32230), label2 = trivia_settings[ "trivia_music_folder" ] )
                    xbmcgui.Window(10001).setProperty( "Setting.10", "true" )
                    self.getControl( 119 ).setLabel( __language__(32232), label2 = ( "False", "True" )[ trivia_settings[ "trivia_adjust_volume" ] ] )
                    if trivia_settings[ "trivia_adjust_volume" ]:
                        xbmcgui.Window(10001).setProperty( "Setting.11", "true" )
                        self.getControl( 120 ).setLabel( __language__(32240), label2 = "%s" % trivia_settings[ "trivia_music_volume" ] )
                        xbmcgui.Window(10001).setProperty( "Setting.12", "true" )
                        self.getControl( 121 ).setLabel( __language__(32241), label2 = ( "False", "True" )[ trivia_settings[ "trivia_fade_volume" ] ] )
                        if trivia_settings[ "trivia_fade_volume" ]:
                            xbmcgui.Window(10001).setProperty( "Setting.13", "true" )
                            self.getControl( 122 ).setLabel( __language__(32242), label2 = "%s" % trivia_settings[ "trivia_fade_time" ] )
                xbmcgui.Window(10001).setProperty( "Setting.14", "true" )
                self.getControl( 123 ).setLabel( __language__(32270), label2 = ( "False", "True" )[ trivia_settings[ "trivia_unwatched_only" ] ] )
                xbmcgui.Window(10001).setProperty( "Setting.15", "true" )
                self.getControl( 124 ).setLabel( __language__(32290), label2 = ( "False", "True" )[ trivia_settings[ "trivia_limit_query" ] ] )
                if trivia_settings[ "trivia_limit_query" ]:
                    xbmcgui.Window(10001).setProperty( "Setting.16", "true" )
                    self.getControl( 125 ).setLabel( __language__(32291), label2 = "%s" % trivia_settings[ "trivia_rating" ] )
            elif trivia_settings[ "trivia_mode" ] == 2:
                xbmcgui.Window(10001).setProperty( "Setting.2", "true" )
                self.getControl( 111 ).setLabel( __language__(32217), label2 = ( __language__(32214), __language__(32215) )[ trivia_settings[ "trivia_moviequiz_mode" ] ] )
                xbmcgui.Window(10001).setProperty( "Setting.3", "true" )
                self.getControl( 112 ).setLabel( __language__(32216), label2 = "%s" % trivia_settings[ "trivia_moviequiz_qlimit" ] )
                xbmcgui.Window(10001).setProperty( "Setting.4", "true" )
                self.getControl( 113 ).setLabel( __language__(32290), label2 = ( "False", "True" )[ trivia_settings[ "trivia_limit_query" ] ] )
                if trivia_settings[ "trivia_limit_query" ]:
                    xbmcgui.Window(10001).setProperty( "Setting.5", "true" )
                    self.getControl( 114 ).setLabel( __language__(32291), label2 = "%s" % trivia_settings[ "trivia_rating" ] )
        xbmcgui.Window(10001).setProperty( "CEmenu", "true" )
        
    def set_trailer_settings( self ):
        self.clear_setting_properties()
        xbmcgui.Window(10001).setProperty( "Setting", "Trailers" )
        # Heading 1
        self.getControl( 200 ).setLabel( __language__(32800) )
        # heading 2
        self.getControl( 201 ).setLabel( __language__(32925) )
        xbmcgui.Window(10001).setProperty( "Setting.1", "true" )
        self.getControl( 110 ).setLabel( __language__(32100), label2 = "%s" % trailer_settings[ "trailer_count" ] )
        if trailer_settings[ "trailer_count" ] > 0:
            xbmcgui.Window(10001).setProperty( "Setting.2", "true" )
            self.getControl( 111 ).setLabel( __language__(32110), label2 = trailer_settings[ "trailer_scraper" ] )
            # Apple Movie Trailers
            if trailer_settings[ "trailer_scraper" ] in ( "amt_database", "amt_current" ):
                xbmcgui.Window(10001).setProperty( "Setting.3", "true" )
                self.getControl( 112 ).setLabel( __language__(32185), label2 = ( __language__(32186), __language__(32187) )[ trailer_settings[ "trailer_play_mode" ] ] )
                xbmcgui.Window(10001).setProperty( "Setting.4", "true" )
                self.getControl( 113 ).setLabel( __language__(32170), label2 = ( trailer_settings[ "trailer_quality" ], __language__(32171) )[ trailer_settings[ "trailer_quality" ] == "Standard" ] ) 
                # TO-DO: remove all AMT Database settings, as script no longer works
                if trailer_settings[ "trailer_scraper" ] == "amt_database":
                    xbmcgui.Window(10001).setProperty( "Setting.5", "true" )
                    self.getControl( 114 ).setLabel( __language__(32180), label2 = ( "False", "True" )[ trailer_settings[ "trailer_hd_only" ] ] )
                    xbmcgui.Window(10001).setProperty( "Setting.6", "true" )
                    self.getControl( 115 ).setLabel( __language__(32160), label2 = ( "False", "True" )[ trailer_settings[ "trailer_newest_only" ] ] )
                    xbmcgui.Window(10001).setProperty( "Setting.7", "true" )
                    self.getControl( 116 ).setLabel( __language__(32120), label2 = trailer_settings[ "trailer_amt_db_file" ] )
                if not trailer_settings[ "trailer_play_mode" ]:
                    xbmcgui.Window(10001).setProperty( "Setting.8", "true" )
                    self.getControl( 117 ).setLabel( __language__(32188), label2 = trailer_settings[ "trailer_download_folder" ] )
            # Local Folder Scrape
            elif trailer_settings[ "trailer_scraper" ] == "local":
                xbmcgui.Window(10001).setProperty( "Setting.3", "true" )
                self.getControl( 112 ).setLabel( __language__(32113), label2 = trailer_settings[ "trailer_folder" ] )
            # XBMC Database Scrape
            elif trailer_settings[ "trailer_scraper" ] == "xbmc_library":
                xbmcgui.Window(10001).setProperty( "Setting.3", "true" )
                self.getControl( 112 ).setLabel( __language__(32929), label2 = ( "False", "True" )[ trailer_settings[ "trailer_unwatched_movie_only" ] ] )
                xbmcgui.Window(10001).setProperty( "Setting.4", "true" )
                self.getControl( 113 ).setLabel( __language__(32923), label2 = ( "False", "True" )[ trailer_settings[ "trailer_skip_youtube" ] ] )
            xbmcgui.Window(10001).setProperty( "Setting.9", "true" )
            self.getControl( 118 ).setLabel( __language__(32140), label2 = ( "False", "True" )[ trailer_settings[ "trailer_limit_mpaa" ] ] )
            if not trailer_settings[ "trailer_limit_mpaa" ]:
                xbmcgui.Window(10001).setProperty( "Setting.10", "true" )
                self.getControl( 119 ).setLabel( __language__(32150), label2 = trailer_settings[ "trailer_rating" ] )
            xbmcgui.Window(10001).setProperty( "Setting.11", "true" )
            self.getControl( 120 ).setLabel( __language__(32141), label2 = ( "False", "True" )[ trailer_settings[ "trailer_limit_genre" ] ] )
            xbmcgui.Window(10001).setProperty( "Setting.12", "true" )
            self.getControl( 121 ).setLabel( __language__(32190), label2 = ( "False", "True" )[ trailer_settings[ "trailer_unwatched_only" ] ] )
        xbmcgui.Window(10001).setProperty( "CEmenu", "true" )
            
    def set_special_video_settings( self ):
        self.clear_setting_properties()
        xbmcgui.Window(10001).setProperty( "Setting", "Special_Videos" )
        # Heading 1
        self.getControl( 200 ).setLabel( __language__(32802) )
        # heading 2
        self.getControl( 201 ).setLabel( __language__(32925) )
        xbmcgui.Window(10001).setProperty( "CEmenu", "true" )
    
    def temp( self ):
        xbmcgui.Window(10001).setProperty( "Setting.1", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.2", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.3", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.4", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.5", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.6", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.7", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.8", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.9", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.9", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.10", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.11", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.12", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.13", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.14", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.15", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.16", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.17", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.18", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.19", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.20", "true" )
        
    def set_general_settings( self ):
        self.clear_setting_properties()
        xbmcgui.Window(10001).setProperty( "Setting", "General" )
        # Heading 1
        self.getControl( 200 ).setLabel( __language__(32803) )
        # heading 2
        self.getControl( 201 ).setLabel( __language__(32925) )
        xbmcgui.Window(10001).setProperty( "Setting.1", "true" )
        self.getControl( 110 ).setLabel( __language__(32410), label2 = "%s" % ( general_settings[ "number_of_features" ] + 1 ) )
        if general_settings[ "number_of_features" ] > 0:
            xbmcgui.Window(10001).setProperty( "Setting.2", "true" )
            self.getControl( 111 ).setLabel( __language__(32445), label2 = ( "False", "True" )[ general_settings[ "enable_notification" ] ] )
        xbmcgui.Window(10001).setProperty( "Setting.3", "true" )
        self.getControl( 112 ).setLabel( __language__(32403), label2 = ( "False", "True" )[ general_settings[ "voxcommando" ] ] )
        xbmcgui.Window(10001).setProperty( "Setting.4", "true" )
        self.getControl( 113 ).setLabel( __language__(32922), label2 = ( "False", "True" )[ general_settings[ "override_play" ] ] )
        xbmcgui.Window(10001).setProperty( "CEmenu", "true" )
        
    def set_home_automation_settings( self ):
        self.clear_setting_properties()
        xbmcgui.Window(10001).setProperty( "Setting", "Home_Automation" )
        # Heading 1
        self.getControl( 200 ).setLabel( __language__(32805) )
        # heading 2
        self.getControl( 201 ).setLabel( __language__(32925) )
        xbmcgui.Window(10001).setProperty( "Setting.1", "true" )
        self.getControl( 110 ).setLabel( __language__(32920), label2 = ( "False", "True" )[ ha_settings[ "ha_enable" ] ] )
        if ha_settings[ "ha_enable" ]:
            xbmcgui.Window(10001).setProperty( "Setting.2", "true" )
            self.getControl( 111 ).setLabel( __language__(32900), label2 = ( "False", "True" )[ ha_settings[ "ha_multi_trigger" ] ] )
            xbmcgui.Window(10001).setProperty( "Setting.3", "true" )
            self.getControl( 112 ).setLabel( __language__(32901), label2 = ( "False", "True" )[ ha_settings[ "ha_script_start" ] ] )
            if trivia_settings[ "trivia_mode" ] > 0:
                if video_settings[ "trivia_intro" ] > 0:
                    xbmcgui.Window(10001).setProperty( "Setting.4", "true" )
                    self.getControl( 113 ).setLabel( __language__(32902), label2 = ( "False", "True" )[ ha_settings[ "ha_trivia_intro" ] ] )
                xbmcgui.Window(10001).setProperty( "Setting.5", "true" )
                self.getControl( 114 ).setLabel( __language__(32903), label2 = ( "False", "True" )[ ha_settings[ "ha_trivia_start" ] ] )
                if video_settings[ "trivia_outro" ] > 0:
                    xbmcgui.Window(10001).setProperty( "Setting.6", "true" )
                    self.getControl( 115 ).setLabel( __language__(32904), label2 = ( "False", "True" )[ ha_settings[ "ha_trivia_outro" ] ] )
            if trailer_settings[ "trailer_count" ] > 0:
                if video_settings[ "cav_intro" ] > 0:
                    xbmcgui.Window(10001).setProperty( "Setting.7", "true" )
                    self.getControl( 116 ).setLabel( __language__(32905), label2 = ( "False", "True" )[ ha_settings[ "ha_cav_intro" ] ] )
                xbmcgui.Window(10001).setProperty( "Setting.8", "true" )
                self.getControl( 117 ).setLabel( __language__(32906), label2 = ( "False", "True" )[ ha_settings[ "ha_trailer_start" ] ] )
                if video_settings[ "cav_outro" ] > 0:
                    xbmcgui.Window(10001).setProperty( "Setting.9", "true" )
                    self.getControl( 118 ).setLabel( __language__(32907), label2 = ( "False", "True" )[ ha_settings[ "ha_outro_outro" ] ] )
            if video_settings[ "mte_intro" ] > 0:
                xbmcgui.Window(10001).setProperty( "Setting.10", "true" )
                self.getControl( 119 ).setLabel( __language__(32908), label2 = ( "False", "True" )[ ha_settings[ "ha_mte_intro" ] ] )
            if video_settings[ "countdown_video" ] > 0:
                xbmcgui.Window(10001).setProperty( "Setting.11", "true" )
                self.getControl( 120 ).setLabel( __language__(32909), label2 = ( "False", "True" )[ ha_settings[ "ha_countdown_video" ] ] )
            if video_settings[ "enable_ratings" ]:
                xbmcgui.Window(10001).setProperty( "Setting.12", "true" )
                self.getControl( 121 ).setLabel( __language__(32910), label2 = ( "False", "True" )[ ha_settings[ "ha_mpaa_rating" ] ] )
            if video_settings[ "enable_audio" ]:
                xbmcgui.Window(10001).setProperty( "Setting.13", "true" )
                self.getControl( 122 ).setLabel( __language__(32911), label2 = ( "False", "True" )[ ha_settings[ "ha_audio_format" ] ] )
            if video_settings[ "fpv_intro" ] > 0:
                xbmcgui.Window(10001).setProperty( "Setting.14", "true" )
                self.getControl( 123 ).setLabel( __language__(32912), label2 = ( "False", "True" )[ ha_settings[ "ha_fpv_intro" ] ] )
            xbmcgui.Window(10001).setProperty( "Setting.15", "true" )
            self.getControl( 124 ).setLabel( __language__(32913), label2 = ( "False", "True" )[ ha_settings[ "ha_movie" ] ] )
            if video_settings[ "intermission_video" ] > 0:
                xbmcgui.Window(10001).setProperty( "Setting.16", "true" )
                self.getControl( 125 ).setLabel( __language__(32914), label2 = ( "False", "True" )[ ha_settings[ "ha_intermission" ] ] )
            if video_settings[ "fpv_ontro" ] > 0:
                xbmcgui.Window(10001).setProperty( "Setting.17", "true" )
                self.getControl( 126 ).setLabel( __language__(32915), label2 = ( "False", "True" )[ ha_settings[ "ha_fpv_outro" ] ] )
            if video_settings[ "mte_outro" ] > 0:
                xbmcgui.Window(10001).setProperty( "Setting.18", "true" )
                self.getControl( 127 ).setLabel( __language__(32916), label2 = ( "False", "True" )[ ha_settings[ "ha_mte_outro" ] ] )
            xbmcgui.Window(10001).setProperty( "Setting.19", "true" )
            self.getControl( 128 ).setLabel( __language__(32918), label2 = ( "False", "True" )[ ha_settings[ "ha_script_end" ] ] )
            xbmcgui.Window(10001).setProperty( "Setting.20", "true" )
            self.getControl( 129 ).setLabel( __language__(32918), label2 = ( "False", "True" )[ ha_settings[ "ha_paused" ] ] )
            xbmcgui.Window(10001).setProperty( "Setting.21", "true" )
            self.getControl( 130 ).setLabel( __language__(32919), label2 = ( "False", "True" )[ ha_settings[ "ha_resumed" ] ] )
        xbmcgui.Window(10001).setProperty( "CEmenu", "true" )
        
    def set_misc_settings( self ):
        self.clear_setting_properties()
        xbmcgui.Window(10001).setProperty( "Setting", "Misc" )
        # Heading 1
        self.getControl( 200 ).setLabel( __language__(32804) )
        # heading 2
        self.getControl( 201 ).setLabel( __language__(32925) )
        xbmcgui.Window(10001).setProperty( "Setting.1", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.2", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.3", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.4", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.5", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.6", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.7", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.8", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.9", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.9", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.10", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.11", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.12", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.13", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.14", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.15", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.16", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.17", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.18", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.19", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.20", "true" )
        xbmcgui.Window(10001).setProperty( "CEmenu", "true" )
        
    def onClick( self, controlId ):
        #print "Control ID: %s" % controlId
        if controlId == 202:
            if xbmcgui.Window(10001).getProperty( "Settings_Modify" ) == "True":
                xbmcgui.Window(10001).setProperty( "Settings_Modify", "False" )
                xbmc.sleep( 100 )
                self.setFocusId( 202 )
            else:          
                xbmcgui.Window(10001).setProperty( "Settings_Modify", "True" )
                self.setFocusId( 110 )
        if controlId == 106: #Exit
            # add module to save settings
            self.close()
        
    def onFocus( self, controlId ):
        if controlId == 100:
            self.set_trivia_settings()
        elif controlId == 101:
            self.set_trailer_settings()
        elif controlId == 102:
            self.set_general_settings()
        elif controlId == 103:
            self.set_special_video_settings()
        elif controlId == 104:
            self.set_home_automation_settings()
        elif controlId == 105:
            self.set_misc_settings()
        elif controlId == 106:
            xbmcgui.Window(10001).setProperty( "CEmenu", "false" )        
        if controlId in ( 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128  ) and not xbmcgui.Window(10001).getProperty( "help" ) == "true":
            xbmcgui.Window(10001).setProperty( "CEhelp", "true" )
        elif controlId not in ( 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128 ):
            xbmcgui.Window(10001).setProperty( "CEhelp", "false" )        
        
    def onAction( self, action ):
        buttonCode =  action.getButtonCode()
        actionID   =  action.getId()
        if (buttonCode == KEY_BUTTON_BACK or buttonCode == KEY_KEYBOARD_ESC):
            self.close()
        if actionID == 10:
            #log( "Closing", xbmc.LOGNOTICE )
            #dialog_msg( "close" )
            self.close()
        
        
def onAction( self, action ):
    buttonCode =  action.getButtonCode()
    actionID   =  action.getId()
    if (buttonCode == KEY_BUTTON_BACK or buttonCode == KEY_KEYBOARD_ESC):
        self.close()
    if ( action.getButtonCode() in CANCEL_DIALOG ):
        #log( "Closing", xbmc.LOGNOTICE )
        self.close()
