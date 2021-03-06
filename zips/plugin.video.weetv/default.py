# -*- coding: utf-8 -*-
import requests, xbmcgui, xbmcplugin, xbmc, re, sys, os, xbmcaddon, json, urllib
from lib import process
from lib import tvresolvers
from threading import Thread
ADDON_PATH = xbmc.translatePath('special://home/addons/plugin.video.weetv/')
ADDON = xbmcaddon.Addon(id='plugin.video.weetv')
ICON = ADDON_PATH + 'icon.png'
FANART = ADDON_PATH + 'fanart.jpg'
USERDATA_PATH = xbmc.translatePath('special://home/userdata/addon_data')
ADDON_DATA = os.path.join(USERDATA_PATH,'plugin.video.weetv')
favourites = os.path.join(ADDON_DATA,'favourites')
watched = os.path.join(ADDON_DATA,'watched')
imdb = os.path.join(ADDON_DATA,'imdb')
Dialog = xbmcgui.Dialog()
debug = ADDON.getSetting('debug')

base_icons = 'http://www.geetee.site/wizchannels/images/'
ca_us_icon = base_icons + 'ca_us.png'
ca_icon = base_icons + 'ca.png'
us_icon = base_icons + 'us.png'
uk_icon = base_icons + 'gb.png'
sports_icon = base_icons + 'sports.png'
news_icon = base_icons + 'news.png'
news_fan = base_icons + 'newsshow.jpg'
ca_fan = base_icons + 'beaver.jpg'
uk_fan = base_icons + 'derwentwater.jpg'
us_fan = base_icons + 'usflag.jpg'
sport_fan = base_icons + 'sport.jpg'
cbc = 'http://www.geetee.site/wizchannels/images/cbc.png' 
tvc = base_icons + 'tvcatchup.jpg'

def Main_Menu():
    process.Menu('[B]------TV------[/B]','',300,'','','','')
    process.Menu('TV Calendar','http://www.tvmaze.com/calendar',6,ICON,FANART,'','')
    process.Menu('IMDB Top 100 Shows','http://www.imdb.com/chart/tvmeter?ref_=m_nv_ch_tvm',301,ICON,FANART,'','')
    process.Menu('weeTV Shows','http://www.imdb.com/list/ls025776108/',16,'','','','')  
    process.Menu('UK Comedy Series','http://www.imdb.com/search/title?countries=gb&genres=comedy&languages=en&title_type=tv_series&sort=num_votes,desc',25,'','','','') 
    process.Menu('My Watched Shows','',21,'','','','')  
    process.Menu('Search TV Shows','',308,ICON,FANART,'','')
    process.Menu('[B]---------------[/B]','test_Main_Menu',310,'','','','')     
    process.Menu('Canada/US Live TV','ca3u',22,ca_us_icon,ca_fan,'','')
    process.Menu('UK Live TV','',23,uk_icon,us_fan,'','')
    process.Menu('News TV','news',24,news_icon,news_fan,'','')
    
    #process.Menu('My Watched Shows','',18,'','','','') 
    process.Menu('[B]-----MOVIES-----[/B]','',300,'','','','')
    process.Menu('Brit Rock','http://www.imdb.com/search/keyword?keywords=british-rock-music&sort=moviemeter,asc&mode=detail&page=1&ref_=kw_ref_key',26,'','','','')    
    process.Menu('Movies by Genre','',202,'','','','')
    process.Menu('Movies IMDB top 250','http://www.imdb.com/chart/top',206,'','','','')
    process.Menu('Search Movies','',207,'','','','')
    #process.Menu('[B]TV Shows & Movies[/B]','',300,'','','','')
    #process.Menu('[B]Movies[/B]','',200,'','','','')

    process.setView('movies', 'INFO')

def CAUS_Menu():
    process.Menu('[B]Canada Live TV[/B]','ca3u',401,ca_icon,ca_fan,'','')
    process.Menu('[B]US Live TV[/B]','us_basic',402,us_icon,us_fan,'','')
    process.Menu('[B]weeIPTV US/CAN[/B]','weeus',406,us_icon,ca_fan,'','')  
    process.Menu('[B]A ipTV US/CAN[/B]','aiptvus',405,us_icon,us_fan,'','') 
    process.Menu('[B]FluxusTV[/B], mainly US','fluxus',408,us_icon,us_fan,'','')

def UK_Menu():
    process.Menu('[B]UK onNow[/B]','',313,tvc,uk_fan,'','')
    process.Menu('[B]UK onNext[/B]','',314,tvc,uk_fan,'','')
    process.Menu('[B]weeIPTV UK[/B]','weeuk',407,uk_icon,uk_fan,'','') 
    process.Menu('[B]A ipTV UK[/B]','aiptvuk',404,uk_icon,uk_fan,'','')     
 
def news_Menu():
    process.Menu('[B]Live News Channels[/B]','news',409,news_icon,news_fan,'','')
    process.Menu('[B]CBC Regional Newsfeeds[/B]','newscbc',410,'http://www.geetee.site/wizchannels/images/cbc.png',news_fan,'','')  
        
def Watched_Menu():
    process.Menu('Latest Episodes','',19,'','','','')
    process.Menu('Watched Shows','',21,'','','','')
    
def Latest_Shows():
    single_list = []
    Type = ''
    Choices = ['Watch now','Upcoming Episodes']
    decide = Dialog.select('Select Choice',Choices)
    if decide == 0:
        Choice = 'Watch now'
    elif decide == 1:
        Choice = 'Upcoming'     
    from datetime import datetime
    today = datetime.now().strftime("%d")
    this_month = datetime.now().strftime("%m")
    this_year = datetime.now().strftime("%y")
    todays_number = (int(this_year)*100)+(int(this_month)*31)+(int(today))
    if not os.path.exists(watched):
        watchedList = []
        watchedList.append(('weetv Watched Section', '', '', '', '', ''))
        a = open(watched, "w")
        a.write(json.dumps(watched))
        a.close()
    HTML = requests.get('http://www.tvmaze.com/calendar').content
    match = re.compile('<span class="dayofmonth">.+?<span class=".+?">(.+?)</span>(.+?)</span>(.+?)</div>',re.DOTALL).findall(HTML)
    for Day_Month,Date,Block in match:
        Date = Date.replace('\n','').replace('  ','').replace(' ','')
        Day_Month = Day_Month.replace('\n','').replace('  ','').replace('   ','')
        Final_Name = Day_Month.replace(',',' '+Date+' ')
        split_month = Day_Month+'>'
        Month_split = re.compile(', (.+?)>').findall(str(split_month))
        for items in Month_split:
                month_one = items.replace('January','1').replace('February','2').replace('March','3').replace('April','4').replace('May','5').replace('June','6')
                month = month_one.replace('July','7').replace('August','8').replace('September','9').replace('October','10').replace('November','11').replace('December','12')
        show_day = Date.replace('st','').replace('th','').replace('nd','').replace('rd','')
        shows_number = (int(this_year)*100)+(int(month)*31)+(int(show_day))
        if shows_number< todays_number:
            Aired = 'Watch now'
        else:
            Aired = 'Airs:'
        prog = re.compile('<span class="show">.+?<a href=".+?">(.+?)</a>:.+?</span>.+?<a href=".+?" title=".+?">(.+?)</a>',re.DOTALL).findall(str(Block))
        for prog, ep in prog:
            prog_check = prog.lower().replace(' ','')
            Split = 'season '+ep.replace('x',' episode ')+'>'
            season_check = re.compile('season (.+?) episode (.+?)>').findall(str(Split))
            for season, episode in season_check:
                season = season
                episode = episode
            f = json.loads(open(watched).read())
            for item in f:
                Watched_Name = item[0]
                Watched_Name = Watched_Name.lower().replace(' ','')
                if str(prog_check) in str(Watched_Name):
                    check_name = Watched_Name
                    check_season = item[3]
                    check_ep = item[4]                        
                    if prog_check == check_name:
                        if check_name == prog_check and int(season) >= int(check_season) and int(episode) > int(check_ep):
                            if Choice == 'Watch now':
                                if Aired == 'Watch now':
                                    if prog+'season:'+season+';episode:'+episode not in single_list:
                                        process.Menu(prog+' - Season '+ep.replace('x',' Episode '),'',8,'','','','year = '+item[2])
                                        single_list.append(prog+'season:'+season+';episode:'+episode)
                            elif Choice == 'Upcoming':
                                if Aired == 'Airs:':
                                    if prog+'season:'+season+';episode:'+episode not in single_list:
                                        process.Menu('[COLORwhite]'+Aired+' '+Date+' '+items+'[/COLOR] '+prog+' - Season '+ep.replace('x',' Episode '),'',8,'','','','year = '+str(item[2]))
                                        single_list.append(prog+'season:'+season+';episode:'+episode)
                            else:
                                pass    

def Watched_Shows():
    watched_list = []
    watched_ = json.loads(open(watched).read())
    imdb_ = json.loads(open(imdb).read())
    for item in watched_:
        watched_name = item[0]
        watched_name = watched_name.lower().replace(' ','')
        watched_list.append(watched_name)
    for i in imdb_:
        imdb_name = i[0]
        imdb_name = imdb_name.lower().replace(' ','')
        if '(' in imdb_name:
            imdb_name = re.findall('(.+?)\(',str(imdb_name))[0]
        if imdb_name in watched_list:
            process.Menu(i[0],i[1],305,i[2],'','',i[0])
    
def get_list_movie(url):
    html = requests.get(url).content
    block = re.findall('<div class="list_item(.+?)<div class="clear"',html,re.DOTALL)
    for blocky in block:
        url = re.findall('href="(.+?)"',str(blocky))[0]
        image = re.findall('img src="(.+?)"',str(blocky))[0]
        name = re.findall('<div class="info">.+?href=.+?>(.+?)</a>',str(blocky),re.DOTALL)[0]
        year = re.findall('<span class="year_type">(.+?)</span>',str(blocky))[0]
        desc,length = re.findall('"item_description">(.+?)<span>(.+?)</span>',str(blocky))[0]
        process.Menu(name+' '+year,'Movies',1501,image,'',length+' '+desc,'>'+name+'>'+year+'>')
    
def get_list_tv(url):
    html = requests.get(url).content    
    block = re.findall('<div class="list_item(.+?)<div class="button_strip">',html,re.DOTALL)  
    #block = re.findall('<div class="list_item(.+?)<div class="clear"',html,re.DOTALL)
    for blocky in block:
        url = re.findall('href="(.+?)"',str(blocky))[0]
        image = re.findall('img src="(.+?)"',str(blocky))[0]
        name = re.findall('<div class="info">.+?href=.+?>(.+?)</a>',str(blocky),re.DOTALL)[0]   
        year = re.findall('<span class="year_type">(.+?)</span>',str(blocky))[0]
        #desc,length = re.findall('"item_description">(.+?)<span>(.+?)</span>',str(blocky))[0]      
        desc = re.findall('"item_description">(.+?)</div>',str(blocky))[0]                      
        year = re.sub("[^()0123456789\.]","",year)
        process.Menu(name+' '+year,'http://imdb.com'+url,305,image,'',desc,name.encode('utf-8')+year.encode('utf-8'))
        process.setView('movies', 'INFO')       
        
def get_imdb_britC(url):
    html = requests.get(url).content    
    #block = re.findall('<div class="list_item(.+?)<div class="button_strip">',html,re.DOTALL)  
    block = re.findall('<div class="lister-top-right">(.+?) <p class="sort-num_votes-visible">',html,re.DOTALL)
    for blocky in block:
        url = re.findall('href="(.+?)"',str(blocky))[0]
        image = re.findall('loadlate="(.+?)"',str(blocky))[0]
        name = re.findall('<span class="lister-item-index unbold text-primary">.+?href=.+?>(.+?)</a>',str(blocky),re.DOTALL)[0]
        year = re.findall('unbold">(.+?)</span>',str(blocky))[0]
        #desc,length = re.findall('"item_description">(.+?)<span>(.+?)</span>',str(blocky))[0]      
        desc = ('<p class="text-muted">(.+?).</p>',str(blocky))[0]                      
        year = re.sub("[^()0123456789\.]","-",year)
        process.Menu(name+' '+year,'http://imdb.com'+url,305,image,'',desc,name.encode('utf-8')+year.encode('utf-8'))
        process.setView('movies', 'INFO')
        
def get_imdb_rock(url):
    html = requests.get(url).content     
    block = re.findall('e" data-tconst="(.+?)Votes:</span>',html,re.DOTALL)
    for blocky in block:
        url = re.findall('href="(.+?)"',str(blocky))[0]
        image = re.findall('loadlate="(.+?)"',str(blocky))[0]
        name = re.findall('<a href="/title.+?alt="(.+?)"',str(blocky),re.DOTALL)[0]
        year = re.findall('unbold">(.+?)</span>',str(blocky))[0]
        #length = re.findall('<span class="runtime">(.+?)min</span>',str(blocky))[0]      
        desc = ('<p class="text-muted">(.+?).</p>',str(blocky))[0]                      
        year = re.sub("[^()0123456789\.]","",year)
        #process.Menu(name+' '+year,'http://imdb.com'+url,305,image,'',desc,name.encode('utf-8')+year.encode('utf-8'))
        process.Menu(name+' '+year,'Movies',1501,image,'','','>'+name+'>'+year+'>')     
        #process.Menu(name+' '+year,'Movies',1501,image,'',length+' '+desc,'>'+name+'>'+year+'>')           

def TV_Calender_Day(url):
    from datetime import datetime
    today = datetime.now().strftime("%d")
    this_month = datetime.now().strftime("%m")
    this_year = datetime.now().strftime("%y")
    todays_number = (int(this_year)*100)+(int(this_month)*31)+(int(today))
    HTML = process.OPEN_URL(url)
    match = re.compile('<span class="dayofmonth">.+?<span class=".+?">(.+?)</span>(.+?)</span>(.+?)</div>',re.DOTALL).findall(HTML)
    #match = re.compile('<span class="hide-for-medium-up">(.+?)</span>(.+?)</span>(.+?)</div>',re.DOTALL).findall(HTML) 
    for Day_Month,Date,Block in match:
        Date = Date.replace('\n','').replace('  ','').replace(' ','')
        Day_Month = Day_Month.replace('\n','').replace('  ','').replace('   ','')
        Final_Name = Day_Month.replace(',',' '+Date+' ')
        split_month = Day_Month+'>'
        Month_split = re.compile(', (.+?)>').findall(str(split_month))
        for item in Month_split:
            month_one = item.replace('January','1').replace('February','2').replace('March','3').replace('April','4').replace('May','5').replace('June','6')
            month = month_one.replace('July','7').replace('August','8').replace('September','9').replace('October','10').replace('November','11').replace('December','12')
        show_day = Date.replace('st','').replace('th','').replace('nd','').replace('rd','')
        shows_number = (int(this_year)*100)+(int(month)*31)+(int(show_day))
        if shows_number>= todays_number:
            process.Menu('[COLORred]*'+''+Final_Name+'[/COLOR]','',7,'','','',Block)
            process.setView('movies', 'INFO')
        else:
            process.Menu('[COLORgreen]*'+'[COLORwhite]'+Final_Name+'[/COLOR]','',7,'','','',Block)
            process.setView('movies', 'INFO')

def TV_Calender_Prog(extra):
    match = re.compile('<span class="show">.+?<a href=".+?">(.+?)</a>:.+?</span>.+?<a href=".+?" title=".+?">(.+?)</a>',re.DOTALL).findall(str(extra))
    for prog, ep in match:
        process.Menu(prog+' - Season '+ep.replace('x',' Episode '),'',8,'','','',prog)
        process.setView('movies', 'INFO')
        
def send_to_search(name,extra):
    year = ''
    xbmc.log(extra,xbmc.LOGNOTICE)
    if 'year' in extra:
        year = re.findall('year = (.+?)>',str(extra)+'>')[0]
    title,season,episode = re.findall('<(.+?)- Season (.+?) Episode (.+?)>','<'+str(name)+'>')[0]
    if 'COLOR' in name:
        name = re.compile('- (.+?)>').findall(str(name)+'>')
        for name in name:
            name = name
    dp =  xbmcgui.DialogProgress()
    dp.create('Checking for stream ss')
    from lib import Scrape_Wee
    Scrape_Wee.scrape_episode(title,'',year,season,episode,'')
    
def movie_search(extra):
    title,year = re.findall('>(.+?)>(.+?)>',str(extra))[0]
    from lib import Scrape_Wee
    Scrape_Wee.scrape_movie(title,year,'')
################### 
def addon_settings():
    xbmcaddon.Addon().openSettings()
    xbmcaddon.Addon('script.module.weescrapers').openSettings()  

def wee_settings():
    xbmcaddon.Addon('script.module.weescrapers').openSettings() 
    
def clear_cache():
    dialog = xbmcgui.Dialog()
    dialog.yesno('Wee Scrapers', "Clear Scraper Cache?")
    import weescrapers
    weescrapers.clear_cache()   

def clear_data():
    dialog = xbmcgui.Dialog()
    dialog.yesno('weeTV', "Clear weeTV Cache?")
    myfile= imdb
    xbmc.log('IWATCHEDB:'+imdb,xbmc.LOGNOTICE)
## if file exists, delete it ##
    if os.path.isfile(myfile):
        os.remove(myfile)
    else:    ## Show an error ##
        xbmc.log('weetv:file not exist',xbmc.LOGNOTICE)

def clear_watched():
    dialog = xbmcgui.Dialog()
    dialog.yesno('weeTV', "Clear weeTV Watched List?")
    myfile= watched
    xbmc.log('IWATCHEDB:'+imdb,xbmc.LOGNOTICE)
## if file exists, delete it ##
    if os.path.isfile(myfile):
        os.remove(myfile)
    else:    ## Show an error ##
        xbmc.log('weetv:file not exist',xbmc.LOGNOTICE)

####################################################    
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2: 
                params=sys.argv[2] 
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}    
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
        
params=get_params()
url=None
name=None
iconimage=None
mode=None
fanart=None
description=None
trailer=None
fav_mode=None
extra=None

try:
    extra=urllib.unquote_plus(params["extra"])
except:
    pass
try:
    fav_mode=int(params["fav_mode"])
except:
    pass
try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass

#####################################################END PROCESSES##############################################################        
        
if mode == None: Main_Menu()
elif mode == 1 : process.queueItem()
elif mode == 2 : Search()
elif mode == 3 : tvresolvers.PlayLive(name,url,iconimage)
elif mode == 6 : TV_Calender_Day(url)
elif mode == 7 : TV_Calender_Prog(extra)
elif mode == 8 : send_to_search(name,extra)
elif mode == 10: from lib import process;process.getFavourites()
elif mode==11:
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    process.addFavorite(name, url, fav_mode, iconimage, fanart, description, extra)
elif mode==12:
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    process.rmFavorite(name)
elif mode == 15: get_list_movie(url)
elif mode == 16: get_list_tv(url)
elif mode == 17:     
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    process.rmWatched(name)
elif mode == 18: Watched_Menu()
elif mode == 19: Latest_Shows()                             
elif mode == 20: from lib import process;process.Big_Resolve(name,url)
elif mode == 21: Watched_Shows()
elif mode == 22: CAUS_Menu()
elif mode == 23: UK_Menu()
elif mode == 24: news_Menu()
elif mode == 25: get_imdb_britC(url)
elif mode == 26: get_imdb_rock(url)

elif mode == 30: addon_settings()
elif mode == 31: wee_settings()
elif mode == 32: clear_cache()
elif mode == 33: clear_data()
elif mode == 34: clear_watched()
                                 
elif mode==51:from lib import test;test.GetContentX(name,url,iconimage,fanart)
elif mode==52:from lib import test;test.PLAYLINK(name,url,iconimage)
elif mode==53:from lib import test;test.GETMULTI(name,url,iconimage)
elif mode==54:from lib import test;test.PLAYSD(name,url,iconimage)
elif mode==55:from lib import test;test.SEARCH()
elif mode==56:from lib import test;test.YOUTUBE_CHANNEL(url)
elif mode==57:from lib import test;test.PLAYVIDEO(url)
elif mode==58:from lib import test;test.GETMULTI_SD(name,url,iconimage)

elif mode == 100 : ADDON.openSettings(sys.argv[0])
elif mode == 200 : from lib import Movies;Movies.Movie_Main(url)
elif mode == 202 : from lib import Movies;Movies.Movie_Genre(url)
elif mode == 203 : from lib import Movies;Movies.IMDB_Grab(url)
elif mode == 204 : from lib import Movies;Movies.Check_Link(name,url,image)
elif mode == 205 : from lib import Movies;Movies.Get_Menulink(url)
elif mode == 206 : from lib import Movies;Movies.IMDB_Top250(url)
elif mode == 207 : from lib import Movies;Movies.search_movies()
elif mode == 208 : from lib import Movies;Movies.movie_channels()
elif mode == 300 : from lib import multitv;multitv.multiv_Main_Menu(url)
elif mode == 301 : from lib import multitv;multitv.IMDB_TOP_100_EPS(url)
elif mode == 302 : from lib import multitv;multitv.Popular(url)
elif mode == 303 : from lib import multitv;multitv.Genres()
elif mode == 304 : from lib import multitv;multitv.Genres_Page(url)
elif mode == 305 : from lib import multitv;multitv.IMDB_Get_Season_info(url,iconimage,extra)
elif mode == 306 : from lib import multitv;multitv.IMDB_Get_Episode_info(url,extra)
elif mode == 307 : from lib import multitv;multitv.SPLIT(extra)
elif mode == 308 : from lib import multitv;multitv.Search_TV()
#elif mode == 309 : from lib import multitv;multitv.IMDB_shows(url)

elif mode == 310 : from lib import test;test.test_Main_Menu(url)

#lif mode==311: from lib.tvc import common;common.play(url)
#elif mode==312: from lib.tvc import common;common.tvcatchup(url)
elif mode==313: from lib.tvc import tvc;tvc.tvc()
elif mode==314: from lib.tvc import tvcn;tvcn.tvc_next()

elif mode==315: from lib.tvc import common;common.play(url)
elif mode==316: from lib.tvc import common;common.tvcatchup(url)
elif mode==317: from lib.tvc import common;common.tvcatchup_next(url)
#####
elif mode == 400 : from lib import livetv;livetv.livetv_Main_Menu(url)
elif mode == 401 : from lib import livetv;livetv.ca3u()
elif mode == 402 : from lib import livetv;livetv.usbasic()
elif mode == 403 : from lib import livetv;livetv.ukonnow()
elif mode == 404 : from lib import livetv;livetv.aiptvuk()
elif mode == 405 : from lib import livetv;livetv.aiptvus()
elif mode == 406 : from lib import livetv;livetv.weeus()
elif mode == 407 : from lib import livetv;livetv.weeuk()
elif mode == 408 : from lib import livetv;livetv.fluxus()
elif mode == 409 : from lib import livetv;livetv.news()
elif mode == 410 : from lib import livetv;livetv.newscbc()
elif mode == 411 : from lib import test;test.GetMenuX()
elif mode == 412 : from lib import livetv;livetv.ukonnext()

elif mode==542:from lib import test;test.YOUTUBE_PLAYLIST(url)
elif mode==543:from lib import test;test.YOUTUBE_PLAYLIST_PLAY(url)
elif mode==571:from lib import test;test.YOUTUBE_CHANNEL(url)
elif mode==572:from lib import test;test.YOUTUBE_CHANNEL_PART2(url)

elif mode == 1501: movie_search(extra)
#########################
elif mode==9999:
    url = tvresolvers.resolve(url)
    liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels='')
    liz.setProperty("IsPlayable","true")
    liz.setPath(url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)

xbmcplugin.endOfDirectory(int(sys.argv[1]))