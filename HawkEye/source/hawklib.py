
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


import cv2
import numpy
import math

EPSILON_SCALER_CONSTANT = 0.075

#these are just wrapper functions for opencv function to simplify the usage

#get the angle of the bounding elipse's axis and perform atan on it
def contour_slope(contour):
	return math.atan(math.radians(cv2.fitEllipse(contour)[2]-90))

#compute the center of mass for a contour
def contour_center(contour):
	moments = cv2.moments(contour)
	return (moments["m10"] / moments["m00"], moments["m01"] / moments["m00"])
        
#returns the distance from to points reprsented by a tuple
def distance(a:tuple, b:tuple):
	return ((a[0]-b[0])**2+(a[1]-b[1])**2)**0.5

#returns the area of contour
def contour_area(contour):
	return cv2.contourArea(contour)

#returns perimeter of a contour
def contour_perimeter(contour, closed_contour=True):
	return cv2.arcLength(contour, closed_contour)

#approximate contour to polygon
def approximate_polygon(contour, epsilon_scaler=EPSILON_SCALER_CONSTANT):
	return cv2.approxPolyDP(contour, epsilon_scaler*contour_perimeter(contour), True)

#returns the convex hull of a contour
def convex_hull(contour):
	return cv2.convexHull(contour)
