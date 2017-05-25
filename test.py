# -*- coding: utf-8 -*-

import re
import os
import sys
import urllib
import urllib2
import shutil
from bs4 import BeautifulSoup

SUBHD_API  = 'http://www.subhd.com/search/%s'
#SUBHD_API  = 'http://www.sskzmz.com/index/search?tab=%s'
SUBHD_BASE = 'http://www.subhd.com'
#SUBHD_BASE = 'http://www.sskzmz.com'
UserAgent  = 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)'

#11:12:15 T:586692   DEBUG: Sub HD::__main__ - Search for [This.is.Us.S01E01.720p.HDTV.x264-KILLERS.mkv] by name. URL[http://www.subhd.com/search/Pilot]

item = {}
item['title'] = 'This.is.US'
def Search( item ):
    filename = 'c:\\Python\\我们这一天\\a.txt'
    filename = 'c:\\我们这一天\\a.txt'
    filename = 'c:\\Python\\This is Us\\a.txt'
    filename = 'cPython.This is Us.a.txt'
    filename = 'c:\\Python\\season 1\\aa.txt'
    filename = 'c:\\Python\\fdsa.s01E01.fdsa我们这s01E02一天\\a.txt'

    #showlist = []
    #fext = os.path.splitext( filename )[1].strip('.').upper()
    #print(fext)
    #xxx = '【%s】%s'%(fext, filename.decode('utf-8'))
    #print(xxx)
    #showlist.append(xxx)
   # print(showlist)
   # exit()

    dirname = os.path.basename( os.path.dirname(filename) )
    dirname = 'Season x1'
    #sp = re.search('s[0-9]{1,}e[0-9]{1,}', dirname.lower())
    #if sp!=None :
    #    print('noNone')
    #    print(sp.group())
    #else:
    #    print('None')
    #exit()
    sp = re.search('season[ -_+~#^()=]*[0-9]{1,}', dirname.lower())
    if sp!=None :
        print('noNone')
    else:
        print('None')
    exit()

    #dir = os.path.dirname( 'c:\\Python\\movie\\a.txt' ).split('\\')
    #print(dir[-1])
    #print('----------------------')
    #dir = os.path.dirname( 'c:\\我们这一天\\movie\\a.txt' ).split('\\')
    #print(dir[-1])
    #print(dir[-2])

    for (key,v) in enumerate(filename.split(' ')):
        print key
        print v
    exit()
    subtitles_list = []
    subtitles_ext = []

    url = SUBHD_API % (urllib.quote(item['title']))
    data = GetHttpData(url)
    try:
        soup = BeautifulSoup(data)
    except:
        return
    results = soup.find_all("div", class_="box")
    for it in results:
        link = SUBHD_BASE + it.find("div", class_="d_title").a.get('href').encode('utf-8')
        #name = '%s (%s)' % (version, ",".join(langs))
        name = it.find("div", class_="d_title").a.text.encode('utf-8')
        try:
            zmz = it.find("div", class_="d_zu").a.get('href').encode('utf-8')
            zmztit = it.find("div", class_="d_zu").a.text.encode('utf-8')
        except:
            zmz = ''
            zmztit = ''
        #version = it.find(text=re.compile('(字幕翻译|听译版本|机翻版本|官方译本)'.decode('utf-8'))).parent.get('title').encode('utf-8')
        #version = it.find_all("span", class_=re.compile("label"))[-1].get('title').encode('utf-8')
        #if version:
        #    if version.find('本字幕按 ') == 0:
        #        version = version.split()[1]
        #else:
        #    version = '未知版本'
        try:
            r2 = it.find_all("span", class_="label")
            langs = [x.text.encode('utf-8') for x in r2][:-1]
        except:
            langs = '未知'
        lname = "Chinese"
        lflag = "zh"
        if ('英文' in langs) and not(('简体' in langs) or ('繁体' in langs)):
            lname = "English"
            lflag = "en"
        #sskzmz
        if( zmz=='/zu/8' ):
            name = '【SSK】' + name
            subtitles_list.append({"language_name":lname, "filename":name, "link":link, "language_flag":lflag, "rating":"0", "lang":langs})
        else:
            subtitles_ext.append({"language_name":lname, "filename":name, "link":link, "language_flag":lflag, "rating":"0", "lang":langs})
    subtitles_list.extend(subtitles_ext)

    if subtitles_list:
        for it in subtitles_list:
            print(it['filename'])
            url = "plugin://%s/?action=download&link=%s&lang=%s" % (__scriptid__,
                                                                        it["link"],
                                                                        it["lang"]
                                                                        )
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=listitem,isFolder=False)

def GetHttpData(url, data=''):
    if data:
        req = urllib2.Request(url, data)
    else:
        req = urllib2.Request(url)
    req.add_header('User-Agent', UserAgent)
    try:
        response = urllib2.urlopen(req)
        httpdata = response.read()
        response.close()
    except:
        return ''
    return httpdata

Search( item )
