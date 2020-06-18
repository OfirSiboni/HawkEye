import subprocess
import colorsys
import os
from hawklib import *
#from smbus2 import SMBus, ic_msg
FOCAL_LENGTH_X = 208.51606 # the focal constant
FOCAL_LENGTH_Y = 258.81351

#x = (y-y1)/m+x1
def X(y, pipeline):#compute the linear inverse graph
  CY = pipeline.getNumberArray("CY", [])
  CX = pipeline.getNumberArray("CX", [])
  if len(CY) == len(CX) and len(CX) > 1:
    m, b = numpy.polyfit(CY, CX, 1)
    return (m*y + b)
  else:
    return 0

prev_perimeter , err , counter = 0 , 10 , 0
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
  print(x, y, area)
  print("angle ", angle)

  #send to file
  counter = 0
  try:
    if prev_perimeter - err <= contour_perimeter(selected) <= prev_perimeter + err: counter+=1
    if counter >= 10:
      counter = 0
      color = pic[int(data[0]),int(data[1])]
      color = colorsys.rgb_to_hsv(color)
      subprocess.check_call("~/HawkEye/scripts/addToHSV.sh " + str(str(color[0]) + ", " + str(color[1]) + ", " + str(color[2])),   shell=True)
      subprocess.check_call("~/HawkEye/scripts/adToYDis.sh " + str(y)) #TODO: EDIT LATER TO y - Dis
                      
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
    #msg = i2c_msg.write(80,[x,y,angle]) #you can send more data, add it to the array(more data -> solwer)
    #bus.i2c_rdwr(msg)
	

def error(exception, pipeline):
	#print error code
	print(exception)
	pipeline.putBoolean("valid", False)





