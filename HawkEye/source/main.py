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
import socket 
from cscore import CameraServer
import cscore
from networktables import NetworkTables, NetworkTablesInstance
import cv2
import subprocess
from PIL import Image
import time
from threading import Thread
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
prev,nex,conf,pt,done = False,False,False,False,False
#paths
__config_path__ = os.path.expanduser('~') + '/.hawk'
# PSEYE camera settings
os.system("v4l2-ctl -c exposure=6")
os.system("v4l2-ctl --set-fmt-video=width=160,height=120,pixelformat=BGR")
#networking
__instance__ = NetworkTablesInstance.getDefault()
__instance__.startClientTeam(team_number)
__pipeline__ = NetworkTables.getTable(__pipe_name__)
NetworkTables.initialize()
camera_server = CameraServer.getInstance()
HOST = socket.gethostname()
TCP_IP = socket.gethostbyname(HOST)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((TCP_IP, 5000))

#region funcrions
def processor(pic,contours, pipeline, prolonged):
  pass
def error(exception, pipeline):
  pass
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
def __get_cap__(id, index):
  _camera_ = camera_server.startAutomaticCapture(dev=id, return_server=False)
  try:
    with open(__config_path__ + '/cameras/' + str(index) + '.json') as json_file:
      _camera_.setConfigJson("".join(i for i in json_file.readlines()))
  except:
    print("no json file for camera number " + str(id))
  _camera_.setResolution(width, height)
  _camera_.setFPS(fps)
  _camera_.setPixelFormat(cscore.VideoMode.PixelFormat.kYUYV)
  return _camera_
def get_video(index, image):
  return camera_server.getVideo(camera=cameras[index]).grabFrame(image)[1]
def process_Init():
    global prev,nex,conf,pt,done
    
    s_time = time.time()
    counter = 1
    source = cscore.CvSource("conf_stream",cscore.VideoMode(cscore.VideoMode.PixelFormat(cscore.VideoMode.PixelFormat.kMJPEG),width,height,fps))
    server = cscore.MjpegServer(name="conf_stream",port=1191)
    server.setSource(source)
    with open("/root/.hawk/pipelines/grip_i.py","r") as grip_file:
          exec("".join(i for i in grip_file.readlines()))
          grip_pipe = eval('GripPipeline()')
    while not done:
        try:
          #update vars
          try:
            data = s.recvfrom(1024)[0] 
            encoding = 'utf-8'
            data = data.decode(encoding)
            changed_vals(data)
          except Exception as e:
            print("no data recieved",end='\r')
          finally:
            if not conf:
              conf = False
            #adjust prev/next
              if prev:
                prev = False
                counter -=1
                if counter <= 0:
                  counter = 1
              if nex:
                nex = False
                counter += 1
                if counter > 4:
                  counter = 4
              #TODO: add pt add 
              if prev or nex:
                  with open("/root/.hawk/pipelines/grip_" + (counter * 'i') + '.py') as grip_file:
                    exec("".join(i for i in grip_file.readlines()))
                    grip_pipe = eval('GripPipeline()')
            ##get image from original 
            pic = cap1.read()[1]
            cv2.cvtColor(pic,84)
            ##process and get rgb threshold
            grip_pipe.process(pic)
            pic = grip_pipe.rgb_threshold_output
            ##publish to a new stream
            source.putFrame(pic)
            if prev or nex or conf or pt or done:
              print(str(prev) + ' ' + str(nex) + ' ' + str(conf) + ' ' + str(pt) + ' ' + str(done))
        except Exception as e:
          print(e)
def changed_vals(val):
  print('\n' + val)
  if not val: return
  global prev,nex,conf,pt,done
  if val == "PREV":
    prev = True
    return
  if val == "NEX":
    nex = True
    return
  if val == "SET_CONF":
    conf = True
    return
  if val == "ADD_PT":
    pt = True
    return
  if val == "DONE":
    Done = True
    return
def checkProcessInit():
  s.settimeout(0.01)
  data = s.recvfrom(1024)[0] 
  encoding = 'utf-8'
  data = data.decode(encoding)
  if data == "START":
    process_Init()
#endregion



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

if __name__ == "__main__":
  for index, id in enumerate(__get_ports__()):
    cameras.append(__get_cap__(id, index))
  cameras[0].setPixelFormat(cscore.VideoMode.PixelFormat.kYUYV)


  __index__ = int(__pipeline__.getNumber('cap_number', 1))
  __image__ = numpy.zeros(shape=(width, height, 3), dtype=numpy.uint8)
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

  #start check for process init start    
  while True:
    try:
                  __index__ = int(__pipeline__.getNumber('cap_number', 1)) #when connected to a robot, change 1 to -1        
                  if __index__ != -1:   
                          __image__ = get_video(__index__, __image__)
                          grip_pipe.process(__image__)
                  processor(image, grip_pipe.filter_contours_output or [])
    except Exception as e:
                  error(e, __pipeline__)

