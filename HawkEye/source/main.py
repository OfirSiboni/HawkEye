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
import hawklib
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

def processor(pic,contours, pipeline, prolonged):
  pass
def error(exception, pipeline):
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
HOST = socket.gethostname()
TCP_IP = socket.gethostbyname(HOST)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((TCP_IP, 5000))
if __name__ == "__main__":
  #get all valid caps
  #os.system("v4l2-ctl -c exposure=6")
  #os.system("v4l2-ctl --set-fmt-video=width=160,height=120,pixelformat=BGR")
  cap1 = cv2.VideoCapture(-1)
  cap1.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
  cap1.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
  cap1.set(cv2.CAP_PROP_EXPOSURE,6)
def __get_ports__():
  ports = []
  cap = cv2.VideoCapture(-1) 
  if cap.read()[0]:
      cap.release()
      ports.append(0)
  else:
      cap.release()
  return ports

#get video for cameras and apply settings

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
if __name__ == "__main__":
  for index, id in enumerate(__get_ports__()):
    cameras.append(__get_cap__(id, index))

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

def get_video(index, image):
  return camera_server.getVideo(camera=cameras[index]).grabFrame(image)[1]
s.settimeout(0.01)
def process_Init():
    global prev,nex,conf,pt,done
    #prev,nex,conf,pt,done = False,False,False,False,False
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
            changed_vals(data)
          except Exception as e:
            print("no data recieved",end='\r')
          finally:
            #global prev,nex,conf,pt,done
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
            #print("config running for " + str(round(time.time() - s_time,1)) + " seconds",end='\r')
            if prev or nex or conf or pt or done:
              print(str(prev) + ' ' + str(nex) + ' ' + str(conf) + ' ' + str(pt) + ' ' + str(done))#,end='\r')
        except Exception as e:
          print(e)
#TODO: find a better solution!!
def changed_vals(val):
  global prev,nex,conf,pt,done
  print(val)
  val = str(val)
  if not val: return
  if val == "b'PREV'":
    prev = True
    return
  if val == "b'NEX'a":
    nex = True
    return
  if val == "b'SET_CONF'":
    conf = True
    return
  if val == "b'ADD_PT'":
    pt = True
  done = "b'DONE'"
  if val == done:
    Done = True #will get here only if nothing left
# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__
if __name__ == "__main__":
  process_Init()
                  
  while True:
    try:
                  __index__ = int(__pipeline__.getNumber('cap_number', 1))
                  
                  if __index__ != -1:
                          
                          __image__ = get_video(__index__, __image__)
                          grip_pipe.process(__image__)
                          counter = counter + 1 #change r u fucking dumb
                  processor(image, grip_pipe.filter_contours_output or [], (counter > 10))
                  if counter > 10:
                            counter = 0
    except Exception as e:
                  error(e, __pipeline__)

