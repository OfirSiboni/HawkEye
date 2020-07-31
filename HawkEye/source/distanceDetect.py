'''
this script is part of  HawkEYE and protected by MIT licence.
made by Ofir Siboni at 8/2020
'''

import math

class distanceDetector:
	targetHeight = 0
	cameraAngle = 0

	def __init__(self,cameraH = cameraHeight, targetH = targetHeight, cameraA = cameraAngle):
		self.targetHeight, self.cameraAngle = (cameraH - targetH),cameraA
		print("Distance detector is ready!")
	def detect(angle):
		return (targetHeight) / math.tan(targetHeight + angle)
