from math import atan2,pi
try:
	while 1:
		x,y = input()
		ang = atan2(y,x)
		ang += 2 * pi if ang < 0 else 0
		print "%f %f,%f"%(ang,x,y)
except EOFError:
	pass
