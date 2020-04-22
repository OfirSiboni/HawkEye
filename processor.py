FOCAL_LENGTH = 208.51606 # the focal constant

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

	
def processor(contours, pipeline):
	contours.sort(key=lambda contour: -contour_area(contour))

	selected = contours[0]
		
	data = contour_center(selected)
	x = data[0] - width/2
	y = height/2 - data[1]
		
	area = contour_area(selected)
	print(x, y, area)

	#if no target is returned then go to error function
	pipeline.putNumber("AX", x) #send the absolute X of the shape
	pipeline.putNumber("AY", y) #send the absolute Y of the shape
	pipeline.putNumber("area", area) #send area
	pipeline.putBoolean("valid", True) #send if target is found
	
	#distance on x axis between the line and the target
	pixels_error = x-X(y, pipeline)
	angle = math.degrees(math.atan(pixels_error/FOCAL_LENGTH))
	pipeline.putNumber("angle", angle)
	print("angle", angle)

	

def error(exception, pipeline):
	pipeline.putBoolean("valid", False)
	print(exception)
	#print error code

