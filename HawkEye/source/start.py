'''
this file is part of HawkEYE and protected by MIT licence.
made by Ofir Siboni at 4/2020
'''


#!/usr/bin/python3
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
from processor import *
import mlgrip
import time
#region functions
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
<<<<<<< Updated upstream
def __get_cap__(id, index):
  _camera_ = camera_server.startAutomaticCapture(dev=id, return_server=False)
=======


def __get_cap__(id, index,cam):
  _camera_ = cam.startAutomaticCapture(dev=id, return_server=False)
>>>>>>> Stashed changes
  try:
    with open(__config_path__ + '/cameras/' + str(index) + '.json') as json_file:
      _camera_.setConfigJson("".join(i for i in json_file.readlines()))
  except:
    print("no json file for camera number " + str(id))
  _camera_.setResolution(width, height)
  _camera_.setFPS(fps)
  _camera_.setPixelFormat(cscore.VideoMode.PixelFormat.kYUYV)
  return _camera_
<<<<<<< Updated upstream
def get_video(index, image):
  return camera_server.getVideo(camera=cameras[index]).grabFrame(image)[1]
=======
black_img = numpy.zeros(shape=(320, 240, 3), dtype=numpy.uint8)  
def get_video(index, image):
  obj = camera_server.getVideo(camera=cameras[0]).grabFrame(image)
  if obj[0] == 0:
    return black_img
  return obj[1]
 
>>>>>>> Stashed changes
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
                  os.system("reboot")
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
<<<<<<< Updated upstream
=======
 
>>>>>>> Stashed changes
def changed_vals(val):
  print('\n' + val)
  if not val: return
  print(val)
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
<<<<<<< Updated upstream
=======
 
>>>>>>> Stashed changes
def checkProcessInit():
    try:
      s.settimeout(0.0001)
      data = s.recvfrom(1024)[0] 
      encoding = 'utf-8'
      data = data.decode(encoding)
      if data == "START":
        process_Init()
    except: 
      pass  
def error(e, pipeline):
  print(e)
  pipeline.putBoolean("valid", False)
#endregion
<<<<<<< Updated upstream
if __name__ == "__main__":
    #region init
    __pipe_name__ = "vision"
    team_number = 0
    width = 160
    height = 120
    fps = 30
    cameras = []
    prev,nex,conf,pt,done = False,False,False,False,False
    os.system("rm -f ~/output.txt") # delete!
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
    (Thread(checkProcessInit())).start()
    #endregion
=======

#region init
__pipe_name__ = "vision"
team_number = 0
width = 320
height = 240
fps = 75
cameras = []
prev,nex,conf,pt,done = False,False,False,False,False
os.system("rm -f ~/output.txt") # delete!
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
''' uncomment if you use the HawkEYE client
HOST = socket.gethostname()
TCP_IP = socket.gethostbyname(HOST)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((TCP_IP, 5000))
(Thread(checkProcessInit())).start()
'''
#endregion
    
def main():
>>>>>>> Stashed changes
    try: #load JSON settings file
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
    
    for index, id in enumerate(__get_ports__()): #load Camera, can take a while!
        cameras.append(__get_cap__(id, index,camera_server))
    cameras[0].setPixelFormat(cscore.VideoMode.PixelFormat.kYUYV)

    __index__ = int(__pipeline__.getNumber('cap_number', 1))
    #black picture array
    blackIMG = numpy.zeros(shape=(width, height, 3), dtype=numpy.uint8)
    __index__ = int(__pipeline__.getNumber('cap_number', 1)) #when connected to a robot, change 1 to -1
    #load GRIP
    gripScript = mlgrip.GripPipeline()
    while True:
        t = 0
        try:
            __image__ = blackIMG
            t = time.process_time()    
            if __index__ != -1:   
                    __image__ = get_video(__index__, __image__)
                    gripScript.process(__image__)
            processor(__image__, gripScript.filter_contours_output or [],__pipeline__)
        except Exception as e:
                    exc_type,exc_obj,exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type,fname,exc_tb.tb_lineno)
                    error(e, __pipeline__)
        finally:
            print((time.process_time() - t))
                    


    
if __name__ == "__main__":
  main()