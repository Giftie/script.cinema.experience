import xbmc, xbmcaddon
import sys, os, traceback

__scriptID__     = sys.modules[ "__main__" ].__scriptID__
ha_settings      = sys.modules[ "__main__" ].ha_settings

_A_ = xbmcaddon.Addon( __scriptID__ )
BASE_CURRENT_SOURCE_PATH = os.path.join( xbmc.translatePath( "special://profile/addon_data/" ).decode('utf-8'), os.path.basename( _A_.getAddonInfo('path') ) )

try:
    sys.path.append( os.path.join( BASE_CURRENT_SOURCE_PATH, "ha_scripts" ) )
    from home_automation import Automate
    # Import HA module set ha_imported to True if successful
    ha_imported = True
except ImportError:
    # or ha_imported to False if unsuccessful
    xbmc.log( "[ script.cinema.experience ] - Failed to import Automate", level=xbmc.LOGNOTICE )
    ha_imported = False
except:
    traceback.print_exc()
    ha_imported = False

class Launch_automation():
    def __init__(self, *args, **kwargs):
        pass

    def launch_automation( self, trigger = None, prev_trigger = None, mode="normal" ):
        if ha_settings[ "ha_enable" ]:
            prev_trigger = Automate().activate_ha( trigger, prev_trigger, mode )
        return prev_trigger

