#!/usr/bin/env python3

import json
import os.path
import time
import sys
import requests
import substring

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

mp_file = open('speed_cams_gibdd.mp', 'w')

header = '''
; Generated by GPSMapEdit 1.24.2.0ASu
[IMG ID]
CodePage=65001
LblCoding=9
Locale=0x409
ID=
Name=
TypeSet=Navitel
Elevation=M
Preprocess=F
TreSize=511
TreMargin=0.000000
RgnLimit=127
POIIndex=Y
PAI5=Y
Levels=2
Level0=26
Level1=8
Zoom0=0
Zoom1=1
[END-IMG ID]

'''

poi_begin = '''
[POI]
Type=0x2c00
'''
poi_end = '''
[END]
'''

# https://www.dotnetperls.com/between-before-after-python
def between(value, a, b):
    # Find and validate before-part.
    pos_a = value.find(a)
    if pos_a == -1: return ""
    # Find and validate after part.
    pos_b = value.rfind(b)
    if pos_b == -1: return ""
    # Return middle part.
    adjusted_pos_a = pos_a + len(a)
    if adjusted_pos_a >= pos_b: return ""
    return value[adjusted_pos_a:pos_b]

def before(value, a):
    # Find first part and return slice before it.
    pos_a = value.find(a)
    if pos_a == -1: return ""
    return value[0:pos_a]

def after(value, a):
    # Find and validate first part.
    pos_a = value.rfind(a)
    if pos_a == -1: return ""
    # Returns chars after the found string.
    adjusted_pos_a = pos_a + len(a)
    if adjusted_pos_a >= len(value): return ""
    return value[adjusted_pos_a:]

request_counter = 0
mp_file.write(header)
options = Options()
options.add_argument('--headless')
#sys.path.extend(['/home/filippov/software/firefox'])
os.environ["PATH"] += os.pathsep + '/home/filippov/software/firefox'
driver = webdriver.Firefox('/home/filippov/software/firefox', options = options)  # options=options

#for region in range(1,99,1):
#url = 'https:/гибдд.рф/r/{region_id}/milestones'.format(region_id = region)
url = 'https://гибдд.рф/milestones?all=true'
driver.get(url)

data = driver.execute_script("return data;")
#response_json = json.loads(data)

for row in data['points']:
    info = row['properties']['balloonContentHeader']
    type_cam_all = row['properties']['balloonContentBody']
    type_cam = '?'
    type_cam_i = type_cam_all.find('li>')
    if type_cam_i != -1:
        type_cam_tmp = between(type_cam_all, 'li>', "</li")
        type_cam = type_cam_tmp.replace('</li><li>', '; ')
    print ('Type cam = {0}', type_cam)
    hint = row['properties']['hintContent']
    coord = row['geometry']['coordinates']
    mp_file.write(';ТИП='+ type_cam + '\n')
    mp_file.write(';ДОП_ИНФО=' + hint + '\n')
    mp_file.write(poi_begin)
    mp_file.write('Label='+info +'\n')
    mp_file.write('Data0=(' + str(coord[0]) + ',' + str(coord[1])  + ')')
    mp_file.write(poi_end + '\n')

driver.close()
driver.quit()
quit(0)