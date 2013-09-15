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
        
    def set_trivia_settings( self ):
        if trivia_settings[ "trivia_mode" ] > 0:
            xbmcgui.Window(10001).setProperty( "trivia", "true" )
        if trivia_settings[ "trivia_mode" ] == 0:
            xbmcgui.Window(10001).setProperty( "trivia", "false" )
        self.getControl( 120 ).setLabel( ( __language__(32281), __language__(32212), __language__(32213) )[ trivia_settings[ "trivia_mode" ] ] )
        self.getControl( 121 ).setLabel( "%s" % trivia_settings[ "trivia_total_time" ] )
        
    def set_special_video_settings( self ):
        pass
        
    def set_trailer_settings( self ):
        pass
        
    def set_feature_settings( self ):
        pass
        
    def set_home_automation_settings( self ):
        pass
        
    def set_misc_settings( self ):
        pass
        
    def onFocus( self, controlId ):
        #
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
        
    def onClick( self, controlId ):
        if controlId == 100:
            pass
        if controlId == 101:
            pass
        if controlId == 102:
            pass
        if controlId == 103:
            pass
        if controlId == 104:
            pass
        if controlId == 105:
            pass
        if controlId == 106: #Exit
            # add module to save settings
            self.close()
        
def onAction( self, action ):
    buttonCode =  action.getButtonCode()
    actionID   =  action.getId()
    if (buttonCode == KEY_BUTTON_BACK or buttonCode == KEY_KEYBOARD_ESC):
        self.close()
    if ( action.getButtonCode() in CANCEL_DIALOG ):
        #log( "Closing", xbmc.LOGNOTICE )
        self.close()
