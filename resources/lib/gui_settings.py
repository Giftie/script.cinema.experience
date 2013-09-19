# -*- coding: utf-8 -*-

import sys, os
import xbmcgui, xbmc, xbmcaddon

trivia_settings          = sys.modules[ "__main__" ].trivia_settings
trailer_settings         = sys.modules[ "__main__" ].trailer_settings
feature_settings         = sys.modules[ "__main__" ].feature_settings
video_settings           = sys.modules[ "__main__" ].video_settings
audio_formats            = sys.modules[ "__main__" ].audio_formats
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
     
    def set_setting_properties( self ):
        xbmcgui.Window(10001).setProperty( "Setting.1", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.2", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.3", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.4", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.5", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.6", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.7", "true" )
        xbmcgui.Window(10001).setProperty( "Setting.8", "true" )
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
        
    def clear_setting_properties( self ):
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
        
    def set_trivia_settings( self ):
        self.clear_setting_properties()
        xbmcgui.Window(10001).setProperty( "Setting", "Trivia" )
        self.getControl( 200 ).setLabel( __language__(32801) )
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
                self.getControl( 124 ).setLabel( __language__(32291), label2 = "%s" % trivia_settings[ "trivia_rating" ] )
            elif trivia_settings[ "trivia_mode" ] == 2:
                xbmcgui.Window(10001).setProperty( "Setting.2", "true" )
                self.getControl( 111 ).setLabel( __language__(32217), label2 = ( __language__(32214), __language__(32215) )[ trivia_settings[ "trivia_moviequiz_mode" ] ] )
                xbmcgui.Window(10001).setProperty( "Setting.3", "true" )
                self.getControl( 112 ).setLabel( __language__(32216), label2 = "%s" % trivia_settings[ "trivia_moviequiz_qlimit" ] )
                xbmcgui.Window(10001).setProperty( "Setting.4", "true" )
                self.getControl( 113 ).setLabel( __language__(32290), label2 = ( "False", "True" )[ trivia_settings[ "trivia_limit_query" ] ] )
            xbmcgui.Window(10001).setProperty( "Setting", "Trivia" )
            
    def set_special_video_settings( self ):
        self.clear_setting_properties()
        
    def set_trailer_settings( self ):
        self.clear_setting_properties()
        
    def set_feature_settings( self ):
        self.clear_setting_properties()
        
    def set_home_automation_settings( self ):
        self.clear_setting_properties()
        
    def set_misc_settings( self ):
        self.clear_setting_properties()
        
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
            self.set_special_video_settings()
        elif controlId == 102:
            self.set_trailer_settings()
        elif controlId == 103:
            self.set_feature_settings()
        elif controlId == 104:
            self.set_home_automation_settings()
        elif controlId == 105:
            self.set_misc_settings()
        if controlId in ( 110, 111 ) and not xbmcgui.Window(10001).getProperty( "help" ) == "true":
            xbmcgui.Window(10001).setProperty( "help", "true" )
        elif controlId not in ( 110, 111 ):
            xbmcgui.Window(10001).setProperty( "help", "false" )
        
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
