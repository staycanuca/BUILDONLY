import time
import xbmc
import os
import xbmcgui
import urllib2
import utils
import sfile

def menuoptions():
    dialog = xbmcgui.Dialog()
    funcs = (
        function1,
        function2,
        function3,
        function4,
        function5,
        function6,
        function7,
        function8,
        function9
        )
        
    call = dialog.select('[B][COLOR=yellow]Live TV Menu[/COLOR][/B]', [
    '[B]      >> [COLOR=gold]Open TV Guide[/COLOR] << [/B]' , 
    '[B]      IPTV Lists (ALL) [/B]',
    '[B]      UK Freeview (with basic EPG data)[/B]',
    '[B]      BBC iPlayer[/B]', 
    '[B]      ITV Player[/B]', 
    '[B]      >> [COLOR=gold]24/7 TV[/COLOR] << [/B]',
    '[B]      [COLOR=orange]Kids TV Guide [/B][/COLOR]',
    '[B]      Kids TV[/B] (press back multi times to exit this)',
    '[B]      My TV Guide[/B] (make your own)'
    ])
    # dialog.selectreturns
    #   0 -> escape pressed
    #   1 -> first item
    #   2 -> second item
    if call:
        # esc is not pressed
        if call < 0:
            return
        func = funcs[call-9]
        return func()
    else:
        func = funcs[call]
        return func()
    return 


def function1():
    xbmc.executebuiltin('RunAddon(script.tvguide.cerebrotv.uk)')

def function2():
    xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.program.super.favourites/?label=[COLOR black]iptv[/COLOR]&mode=400&path=special%3A%2F%2Fprofile%2Faddon_data%2Fplugin.program.super.favourites%2FSuper%20Favourites%5Ciptv&sf_options=fanart%3Dspecial%3A%2F%2Fhome%2Faddons%5Cplugin.program.super.favourites%5Cfanart.jpg%26_options_sf",return)')

def function3():
    xbmc.executebuiltin('RunAddon(plugin.video.tvplayer)')

def function4():
    xbmc.executebuiltin('RunAddon(plugin.video.iplayerwww)')

def function5():
    xbmc.executebuiltin('RunAddon(plugin.video.itv)')

def function6():
    xbmc.executebuiltin('RunAddon(script.mtvbb247)')
    
def function7():
    xbmc.executebuiltin('RunAddon(script.tvguide.cerebrotv.kids)')
    
def function8():
    xbmc.executebuiltin('RunAddon(plugin.video.KongKidz)')

def function9():
    xbmc.executebuiltin('RunAddon(script.tvguide.cerebrotv.uk.2017)')
    
menuoptions()