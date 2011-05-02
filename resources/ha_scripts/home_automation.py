# This module's future home should be inside userdata/addon_data/script.cinema.experience/ha_scripts
# to make sure it does not get over written when updating the script

import xbmc, xbmcaddon

_A_ = xbmcaddon.Addon('script.cinema.experience')
_L_ = _A_.getLocalizedString
_S_ = _A_.getSetting

def activate_on( trigger = "None" ):
    """
        Scripting to trigger almost anything(HA, other scripts, etc...) when videos start.  
        
        Usage:
            activate_on( "Movie" )
            will trigger code that is set under the Movie heading.
            
    """
    if trigger == "None":
        xbmc.output( "[script.cinema.experience] - [ home_automation.py ] - No Trigger Sent, Returning", level=xbmc.LOGNOTICE )
        return
    xbmc.output( "[script.cinema.experience] - [ home_automation.py ] - activate_on( %s ) Triggered" % trigger, level=xbmc.LOGNOTICE )
    # Script Start
    if trigger == _L_( 32613 ) and _S_( "ha_script_start" ) == "true": 
        xbmc.output( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32613 ), level=xbmc.LOGNOTICE )
        # place code below this line
    # Trivia Intro
    elif trigger == _L_( 32609 ) and _S_( "ha_trivia_intro" ) == "true": 
        xbmc.output( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32609 ), level=xbmc.LOGNOTICE )
        # place code below this line
    # Trivia
    elif trigger ==_L_( 32615 ) and _S_( "ha_trivia_start" ) == "true": 
        xbmc.output( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32615 ), level=xbmc.LOGNOTICE )
        # place code below this line
    # Trivia Outro
    elif trigger ==_L_( 32610 ) and _S_( "ha_trivia_outro" ) == "true":
        xbmc.output( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32610 ), level=xbmc.LOGNOTICE )
        # place code below this line
    # Movie Theatre Intro
    elif trigger ==_L_( 32607 ) and _S_( "ha_mte_intro" ) == "true":
        xbmc.output( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32607 ), level=xbmc.LOGNOTICE )
        # place code below this line
    # Coming Attractions Intro
    elif trigger ==_L_( 32600 ) and _S_( "ha_cav_intro" ) == "true":
        xbmc.output( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32600 ), level=xbmc.LOGNOTICE )
        # place code below this line
    # Trailer
    elif trigger ==_L_( 32605 ) and _S_( "" ) == "true":
        xbmc.output( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32605 ), level=xbmc.LOGNOTICE )
        # place code below this line
    # Coming Attractions Outro
    elif trigger ==_L_( 32608 ) and _S_( "ha_cav_outro" ) == "true": 
        xbmc.output( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32608 ), level=xbmc.LOGNOTICE )
        # place code below this line
    # Feature Presentation Intro
    elif trigger ==_L_( 32601 ) and _S_( "ha_fpv_intro" ) == "true": 
        xbmc.output( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32601 ), level=xbmc.LOGNOTICE )
        # place code below this line
    # MPAA Rating
    elif trigger ==_L_( 32603 ) and _S_( "ha_mpaa_rating" ) == "true": 
        xbmc.output( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32603 ), level=xbmc.LOGNOTICE )
        # place code below this line
    # Countdown
    elif trigger ==_L_( 32611 ) and _S_( "ha_countdown_video" ) == "true":
        xbmc.output( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32611 ), level=xbmc.LOGNOTICE )
        # place code below this line
    # Audio Format
    elif trigger ==_L_( 32606 ) and _S_( "ha_audio_format" ) == "true":
        xbmc.output( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32606 ), level=xbmc.LOGNOTICE )
        # place code below this line
    # Movie
    elif trigger ==_L_( 32616 ) and _S_( "ha_movie" ) == "true": 
        xbmc.output( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32616 ), level=xbmc.LOGNOTICE )
        # place code below this line
    # Feature Presentation Outro
    elif trigger ==_L_( 32602 ) and _S_( "ha_fpv_outro" ) == "true":
        xbmc.output( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32602 ), level=xbmc.LOGNOTICE )
        # place code below this line
    # Movie Theatre Intro
    elif trigger ==_L_( 32617 ) and _S_( "ha_mte_outro" ) == "true": 
        xbmc.output( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32617 ), level=xbmc.LOGNOTICE )
        # place code below this line
    # Intermission
    elif trigger ==_L_( 32612 ) and _S_( "ha_intermission" ) == "true": 
        xbmc.output( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32612 ), level=xbmc.LOGNOTICE )
        # place code below this line
    # Script End
    elif trigger ==_L_( 32614 ) and _S_( "ha_script_end" ) == "true": 
        xbmc.output( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32614 ), level=xbmc.LOGNOTICE )
        # place code below this line
    # Paused
    elif trigger ==_L_( 32618 ) and _S_( "ha_paused" ) == "true": 
        xbmc.output( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32618 ), level=xbmc.LOGNOTICE )
        # place code below this line
    # Resumed
    elif trigger ==_L_( 32619 ) and _S_( "ha_resumed" ) == "true": 
        xbmc.output( "[script.cinema.experience] - [ home_automation.py ] - %s Triggered" % _L_( 32619 ), level=xbmc.LOGNOTICE )
        # place code below this line
    