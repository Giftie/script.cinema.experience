# This module's future home should be inside userdata/addon_data/script.cinema.experience/ha_scripts
# to make sure it does not get over written when updating the script

import xbmc, xbmcaddon
import sys, urllib2, os
from threading import Thread
from urllib import urlencode

__script__               = sys.modules[ "__main__" ].__script__
__scriptID__             = sys.modules[ "__main__" ].__scriptID__
triggers                 = sys.modules[ "__main__" ].triggers
ha_settings              = sys.modules[ "__main__" ].ha_settings
BASE_RESOURCE_PATH       = sys.modules["__main__"].BASE_RESOURCE_PATH
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )
import utils

class Automate:
    def __init__( self ):
        pass
    
    def sab_pause(self, mode):
        apikey = ""
        ip = "127.0.0.1" # address 
        port = "5000"
        url = "http://%s:%s/sabnzbd/" % ( ip, port )
        query = {}
        query[ "mode" ] = mode
        query["apikey"] = apikey
        response = urllib2.urlopen( urllib2.Request( url + "api?", urlencode( query ) ) )
        response_data = response.read()
      
    def activate_ha( self, trigger = None, prev_trigger = None, mode="thread" ):
        if ha_settings[ "ha_enable" ]:
            if ha_settings[ "ha_multi_trigger" ] and prev_trigger == trigger:
                pass
            elif mode != "thread":
                self.activate_on( trigger )
            else:
                thread = Thread( name='ha_trigger', target=self.activate_on, args=( trigger, ) )
                thread.start()
        return prev_trigger

    def activate_on( self, trigger = None ):
        """
            Scripting to trigger almost anything(HA, other scripts, etc...) when videos start.  
            
            Usage:
                activate_on( "Movie" )
                will trigger code that is set under the Movie heading.
                
        """
        if not trigger:
            utils.log( " - [ home_automation.py ] - No Trigger Sent, Returning", xbmc.LOGNOTICE )
            return
        utils.log( " - [ home_automation.py ] - activate_on( %s ) Triggered" % trigger, xbmc.LOGNOTICE )
        if trigger in triggers:
            utils.log( " - [ home_automation.py ] - Trigger %s" % trigger, xbmc.LOGNOTICE )
        # Script Start
        if trigger == "Script Start" and ha_settings[ "ha_script_start" ]: 
            # place code below this line
            pass
        # Trivia Intro
        elif trigger == "Trivia Intro" and ha_settings[ "ha_trivia_intro" ]: 
            pass
            # place code below this line
        # Trivia
        elif trigger == "Trivia" and ha_settings[ "ha_trivia_start" ]: 
            pass
            # place code below this line
        # Trivia Outro
        elif trigger == "Trivia Outro" and ha_settings[ "ha_trivia_outro" ]:
            pass
            # place code below this line
        # Movie Theatre Intro
        elif trigger == "Movie Theater Intro" and ha_settings[ "ha_mte_intro" ]:
            pass
            # place code below this line
        # Coming Attractions Intro
        elif trigger == "Coming Attractions Intro" and ha_settings[ "ha_cav_intro" ]:
            pass
            # place code below this line
        # Trailer
        elif trigger == "Movie Trailer" and ha_settings[ "ha_trailer_start" ]:
            pass
            # place code below this line
        # Coming Attractions Outro
        elif trigger == "Coming Attractions Outro" and ha_settings[ "ha_cav_outro" ]: 
            pass
            # place code below this line
        # Feature Presentation Intro
        elif trigger == "Feature Presentation Intro" and ha_settings[ "ha_fpv_intro" ]: 
            pass
            # place code below this line
        # MPAA Rating
        elif trigger == "MPAA Rating" and ha_settings[ "ha_mpaa_rating" ]: 
            pass
            # place code below this line
        # Countdown
        elif trigger == "Countdown" and ha_settings[ "ha_countdown_video" ]:
            pass
            # place code below this line
        # Audio Format
        elif trigger == "Audio Format" and ha_settings[ "ha_audio_format" ]:
            pass
            # place code below this line
        # Movie
        elif trigger == "Movie" and ha_settings[ "ha_movie" ]: 
            pass
            # place code below this line
        # Feature Presentation Outro
        elif trigger == "Feature Presentation Outro" and ha_settings[ "ha_fpv_outro" ]:
            pass
            # place code below this line
        # Movie Theatre Intro
        elif trigger == "Movie Theatre Outro" and ha_settings[ "ha_mte_outro" ]: 
            pass
            # place code below this line
        # Intermission
        elif trigger == "Intermission" and ha_settings[ "ha_intermission" ]: 
            pass
            # place code below this line
        # Script End
        elif trigger == "Script End" and ha_settings[ "ha_script_end" ]: 
            pass
            # place code below this line
        # Paused
        elif trigger == "Pause" and ha_settings[ "ha_paused" ]: 
            pass
            # place code below this line
        # Resumed
        elif trigger == "Resume" and ha_settings[ "ha_resumed" ]: 
            pass
            # place code below this line
        else:
            utils.log( " - [ home_automation.py ] - Opps. Something happened", xbmc.LOGNOTICE )
