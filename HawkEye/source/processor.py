import subprocess
import colorsys
import os,sys
from hawklib import *
#from smbus2 import SMBus, ic_msg
FOCAL_LENGTH_X = 208.51606 # the focal constant
FOCAL_LENGTH_Y = 258.81351
prev_perimeter , err,counter = 0 ,500,0
#x = (y-y1)/m+x1
def X(y, pipeline):#compute the linear inverse graph
  CY = pipeline.getNumberArray("CY", [])
  CX = pipeline.getNumberArray("CX", [])
  if len(CY) == len(CX) and len(CX) > 1:
    m, b = numpy.polyfit(CY, CX, 1)
    return (m*y + b)
  else:
    return 0


def processor(pic,contours, pipeline,h = 160,w = 120):
  contours.sort(key=lambda contour: -contour_area(contour))

  selected = contours[0]

  #if no target is returned then go to error function
	
  data = contour_center(selected)
  x = data[0] - w/2
  y = h/2 - data[1]
	
  #distance on x axis between the line and the target
  pixels_error = x-X(y, pipeline)
  angle = math.degrees(math.atan(pixels_error/FOCAL_LENGTH_X))
  pitch = math.degrees(math.atan(y/FOCAL_LENGTH_Y))
	
  area = contour_area(selected)
  per = contour_perimeter(selected)
  print(x, y, area, per ,angle, end="/r")

  #send to file

  try:
    global counter
    print(counter, end = "\r")
    if prev_perimeter - err <= per <= prev_perimeter + err:
      counter+=1
    if counter > 9:
      counter = 0
      color = pic[int(len(pic) if data[0] > len(pic) else data[0]),int(data[1])]
      hsvcolor = colorsys.rgb_to_hsv(color[2]/256,color[1]/256,color[0]/256)
      fixedhsvcolor = []
      fixedhsvcolor.append(round(hsvcolor[0]*360,0)) #(also the next 2 lines) convert HSV from decimal to presentable HSV color
      fixedhsvcolor.append(round(hsvcolor[1]*100,0))
      fixedhsvcolor.append(round(hsvcolor[2]*100,0))
      os.system("bash /root/HawkEye/HawkEye/scripts/addToHSV.sh '{0} {1} {2}' '{1} {2}'".format(fixedhsvcolor[0],fixedhsvcolor[2],fixedhsvcolor[1]))
      #input("bgr: {0} , hsv: {1}, hsvnot: {2}".format(color,fixedhsvcolor,hsvcolor)) #for debugging perposes
                           
  except Exception as e:
    error(e,pipeline)
    os.system(e + "> /root/output.txt")
  #cause problem in debugging
  pipeline.putNumber("AX", x) #send the absolute X of the shape
  pipeline.putNumber("AY", y) #send the absolute Y of the shape
  pipeline.putNumber("area", area) #send area
  pipeline.putBoolean("valid", True) #send if target is found
  pipeline.putNumber("angle", angle)
  pipeline.putNumber("pitch", pitch)
  
  #with SMBus(1) as bus: #comment becuase it needs to be connected 
    #msg = i2c_msg.write(80,[x,y,angle]) #you can send more data, add it to the array(more data -> slower)
    #bus.i2c_rdwr(msg)
	

def error(exception, pipeline):
	print("error: " + str(exception))
	pipeline.putBoolean("valid", False)
  





