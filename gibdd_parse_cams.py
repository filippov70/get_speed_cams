#!/usr/bin/env python3

import json
import os.path
import time
import sys
from geojson import Feature, Point, FeatureCollection, dump
import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


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
    if pos_a == -1:
        return ""
    # Returns chars after the found string.
    adjusted_pos_a = pos_a + len(a)
    if adjusted_pos_a >= len(value):
        return ""
    return value[adjusted_pos_a:]


request_counter = 0

options = Options()
options.add_argument('--headless')
#sys.path.extend(['/home/filippov/software/firefox'])
os.environ["PATH"] += os.pathsep + '/home/techopolis/soft/firefox'
driver = webdriver.Firefox('/home/techopolis/soft/firefox', options = options)  # options=options

#for region in range(1,99,1):
#url = 'https:/гибдд.рф/r/{region_id}/milestones'.format(region_id = region)
url = 'https://гибдд.рф/milestones?all=true'
driver.get(url)

data = driver.execute_script("return data;")

feature_list = []

for row in data['points']:
    info = row['properties']['balloonContentHeader']
    type_cam_all = row['properties']['balloonContentBody']
    type_cam = '?'
    type_cam_i = type_cam_all.find('li>')
    if type_cam_i != -1:
        type_cam_tmp = between(type_cam_all, 'li>', "</li")
        type_cam = type_cam_tmp.replace('</li><li>', '; ')

    hint = row['properties']['hintContent']
    coord = row['geometry']['coordinates']
    point = Point([coord[1], coord[0]])
    f_point = Feature(geometry=point, properties={"type": type_cam, "info": hint})
    feature_list.append(f_point)

f_coll = FeatureCollection(feature_list)

with open('myfile.geojson', 'w') as f:
   json.dump(f_coll, f)

driver.close()
driver.quit()
quit(0)
