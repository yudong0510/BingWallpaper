# coding=utf-8
# -*- conding:utf-8 -*-

'''
https://www.python.org/dev/peps/pep-0263/

More precisely, the first or second line must match the following regular expression:

^[ \t\v]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)
'''

import re
import urllib.request
import os
import time
from PIL import Image
import win32gui
import win32con


def get_jpg_url():
    print('Parsing html...')
    while True :
        try:
            html = urllib.request.urlopen('http://cn.bing.com/').read().decode('utf-8')
            if html != None:
                break
        except Exception as e:
            print("Exception occured during urlopen. Retrying...")
            continue
    jpg_url = re.findall(r'([\w\/_-]+?.jpg)',html)[0]
    print(jpg_url)
    jpg_name = re.search(r'[\w_-]+?.jpg',jpg_url).group(0)
    print(jpg_name)
    return (jpg_url,jpg_name)


def get_jpg_file(jpg_url):
    if "com" not in jpg_url:
        jpg_url = 'com/az/hprichbg/rb' + jpg_url
    jpg_url = 'http://cn.bing.' + jpg_url
    print('Downloading %s' % jpg_url)
    urllib.request.urlretrieve(jpg_url,jpg_name)
    print('Done!')


def set_wallpaper(jpg_name):
    bmp_name = jpg_name[0:len(jpg_name)-3]+"bmp"
    print('Converting %s to %s' % (jpg_name,bmp_name))
    img = Image.open(jpg_name)
    img.save(bmp_name)
    print('Done!')
    print('Setting wallpaper...')
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,bmp_name,0)
    os.remove(bmp_name)
    oem_path=r"C:\Windows\System32\oobe\info\backgrounds"
    size = ((1600,900),(1366,768),(1280,800),(1280,720),(1024,576),(854,480))
    i=0
    while os.path.exists(oem_path):
        print("Resizing img to size {size}...".format(size=size[i]))
        b_img = img.resize(size[i])
        b_img.save(oem_path+r"\backgroundDefault.jpg")
        if os.path.getsize(oem_path+r"\backgroundDefault.jpg")<=256000 or i==5:
            break
        i+=1
    print('Done!')


if __name__ == '__main__':
    while(True):
        print('In while loop...')
        jpg_url,jpg_name=get_jpg_url()
        if not os.path.exists(jpg_name):
            get_jpg_file(jpg_url)
            set_wallpaper(jpg_name)
        print('Sleep for 12 hours!')
        time.sleep(60*60*12)
