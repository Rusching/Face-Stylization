import math

def radians(degrees):
	return degrees * math.pi / 180

def degrees(radians):
	return radians * 180 / math.pi

def is_valid(triangle):
	min_degree = 15
	X1 = triangle[0][0]
	Y1 = triangle[0][1]
	X2 = triangle[1][0]
	Y2 = triangle[1][1]
	X3 = triangle[2][0]
	Y3 = triangle[2][1]

	x1 = X2 - X1
	y1 = Y2 - Y1
	x2 = X3 - X1
	y2 = Y3 - Y1
	d1 = math.sqrt(x1*x1 + y1*y1)
	d2 = math.sqrt(x2*x2 + y2*y2)
	x1 /= d1
	y1 /= d1
	x2 /= d2
	y2 /= d2
    
	a1 = degrees(math.acos(x1*x2 + y1*y2))

	x1 = X1 - X2
	y1 = Y1 - Y2
	x2 = X3 - X2
	y2 = Y3 - Y2
	d1 = math.sqrt(x1*x1 + y1*y1)
	d2 = math.sqrt(x2*x2 + y2*y2)
	x1 /= d1
	y1 /= d1
	x2 /= d2
	y2 /= d2
	a2 = degrees(math.acos(x1*x2 + y1*y2))
	a3 = 180 - a1 - a2
	return a1 > min_degree and a2 > min_degree and a3 > min_degree