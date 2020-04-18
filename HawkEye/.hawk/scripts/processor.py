import subprocess
import colorsys
FOCAL_LENGTH_X = 208.51606 # the focal constant
FOCAL_LENGTH_Y = 258.81351

os.system("v4l2-ctl -c exposure=6") 
cameras[0].setPixelFormat(cscore.VideoMode.PixelFormat.kYUYV)

#x = (y-y1)/m+x1
def X(y, pipeline):#compute the linear inverse graph
	CY = pipeline.getNumberArray("CY", [])
	CX = pipeline.getNumberArray("CX", [])
	if len(CY) == len(CX) and len(CX) > 1:
		m, b = numpy.polyfit(CY, CX, 1)
		return (m*y + b)
	else:
		return 0

	
def processor(pic,contours, pipeline, prolonged):
	print("here?")
	contours.sort(key=lambda contour: -contour_area(contour))

	selected = contours[0]

	#if no target is returned then go to error function
	
	data = contour_center(selected)
	x = data[0] - width/2
	y = height/2 - data[1]
	
	#distance on x axis between the line and the target
	pixels_error = x-X(y, pipeline)
	angle = math.degrees(math.atan(pixels_error/FOCAL_LENGTH))
	pitch = math.degrees(math.atan(y/FOCAL_LENGTH_Y))
	
	area = contour_area(selected)
	print(x, y, area)
	print("angle", angle)

	#send to file
	try:
                if prolonged:
                        color = pic[int(data[0]),int(data[1])]
                        color = colorsys.rgb_to_hsv(color)
                        subprocess.check_call("/scripts/addToHSV.sh " + str(str(color[0]) + ", " + str(color[1]) + ", " + str(color[2])),   shell=True)
                        subprocess.check_call("/scripts/adToYDis.sh " + str(y)) #TODO: EDIT LATER TO y - Dis
	except Exception as e:
                print(e)
	'''
  pipeline.putNumber("AX", x) #send the absolute X of the shape
	pipeline.putNumber("AY", y) #send the absolute Y of the shape
	pipeline.putNumber("area", area) #send area
	pipeline.putBoolean("valid", True) #send if target is found
	pipeline.putNumber("angle", angle)
	pipeline.putNumber("pitch", pitch)
	__instance__.flush()
 '''
	

def error(exception, pipeline):
	#print error code
	print(exception)
	pipeline.putBoolean("valid", False)
	__instance__.flush()




