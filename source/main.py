#!/usr/bin/python3

'''
This file is part of Hawk.

    Hawk is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Hawk is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Hawk.  If not, see <https://www.gnu.org/licenses/>.

'''

import sys
import os
import json
import numpy
from cscore import CameraServer
import cscore
from networktables import NetworkTables, NetworkTablesInstance
import cv2
import subprocess
from hawklib import *
sys.path.append(os.path.expanduser("~/.hawk/scripts/"))

#load general settings
#default settings
__pipe_name__ = "vision"
team_number = 0
width = 160
height = 120
fps = 30
cameras = []
grip_pipe = None
#paths
__config_path__ = os.path.expanduser('~') + '/.hawk'


def processor(pic,contours, pipeline, prolonged):
	pass
def error(exception, pipeline):
	pass
def process_Init(gripFile,CameraServer,capNumber,pipeline):
        pass

try:
	with open(__config_path__ + '/config.json', 'r') as file:
		config = json.loads(file.read())
		team_number = config['team_number']
		width = config['width']
		height = config['height']
		fps = config['fps']
		__pipe_name__ = config['pipe_name']
except Exception as e:
	print("Error loading config")
	print(e)

#networking
__instance__ = NetworkTablesInstance.getDefault()
__instance__.startClientTeam(team_number)
__pipeline__ = NetworkTables.getTable(__pipe_name__)
NetworkTables.initialize()
camera_server = CameraServer.getInstance()

#get all valid caps
def __get_ports__():
	ports = []
	for i in range(0, 100):
		cap = cv2.VideoCapture(i)
		if cap.read()[0]:
			cap.release()
			ports.append(i)
		else:
			cap.release()
	return ports

#get video for cameras and apply settings
def __get_cap__(id, index):
	camera = camera_server.startAutomaticCapture(dev=id, return_server=False)
	try:
		with open(__config_path__ + '/cameras/' + str(index) + '.json') as json_file:
			camera.setConfigJson("".join(i for i in json_file.readlines()))
	except:
		print("no json file for camera number " + str(id))
	camera.setResolution(width, height)
	camera.setFPS(fps)
	return camera

for index, id in enumerate(__get_ports__()):
	cameras.append(__get_cap__(id, index))

try:
	#loads grip pipeline and user script
	with open(__config_path__ + '/grips/' + config['grip_file']) as grip_file:
		exec("".join(i for i in grip_file.readlines()))
		grip_pipe = eval('GripPipeline()')
	with open(__config_path__ + '/scripts/' + config['script_file']) as script_file:
		exec("".join(i for i in script_file.readlines())) 
except Exception as e:
	print("error loading grip file or user script")
	print(e)

def get_video(index, image):
	return camera_server.getVideo(camera=cameras[index]).grabFrame(image)[1]
def process_Init(gripFile,CameraServer,capNumber,pipeline):
    grip_pipe = eval('GripPipeline()') #TODO: check
    _img_ = get_video(cupNumber,_img_)
    grip_pipe.process(_img_)
    _img_ = grip_pipe.rgb_threshold_output
    height, width, channels = _img_.shape
    CameraServer.putvideo('validation', width, height).putFrame(_img_)
    


__image__ = numpy.zeros(shape=(width, height, 3), dtype=numpy.uint8)
__index__ = int(__pipeline__.getNumber('cap_number', -1))
counter = 0
try:
        for x in range(1,4):
                process_Init(open(__config_path__ + '/pipelines' + (x*'i')),camera_server,__index__,pipeline)
                
except Exception as e:
        error(e,__pipeline__)
while True:
	try:
                __index__ = int(__pipeline__.getNumber('cap_number', -1))
		if __index__ != -1:
			__image__ = get_video(__index__, __image__)
			grip_pipe.process(__image__)
			counter++
		processor(image, grip_pipe.filter_contours_output or [], (counter > 10))
                if counter > 10:
                          counter = 0
	except Exception as e:
		error(e, __pipeline__)
