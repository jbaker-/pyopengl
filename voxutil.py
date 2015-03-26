import sys,os,random,time,math

level = {
	#6 levels of intensity for each color
	0: 0,	# off
	1: 30,	#dark 
	2: 70,
	3: 120,	#...
	4: 170,
	5: 200,	#light 
	6: 255} # on

palatte = {# entries formatted as [key:{radius,r,g,b}]

	0:[-1,0,0,0], 		#when using this, make sure (-1) means dont draw

	#Smallest size dots - radius 1 - almost too small to use
	1:[1,level[1],level[1],level[1]], #grey range
	2:[1,level[2],level[2],level[2]],	#dark
	3:[1,level[3],level[3],level[3]],
	4:[1,level[4],level[4],level[4]],
	5:[1,level[5],level[5],level[5]],	#light
	6:[1,level[6],level[6],level[6]], #end greys

	7:[1,level[1],0,0],	#red range
	8:[1,level[2],0,0],	 #dark red
	9:[1,level[3],0,0],
	10:[1,level[4],0,0],
	11:[1,level[5],0,0],
	12:[1,level[6],0,0], #light red

	13:[1,0,level[1],0], #green range
	14:[1,0,level[2],0],  #dark green
	15:[1,0,level[3],0],
	16:[1,0,level[4],0],
	17:[1,0,level[5],0],
	18:[1,0,level[6],0],  #light green

	19:[1,0,0,level[1]], #blue range	
	20:[1,0,0,level[2]],  #dark blue
	21:[1,0,0,level[3]],
	22:[1,0,0,level[4]],
	23:[1,0,0,level[5]],
	24:[1,0,0,level[6]],  #light blue

	#Slightly larger dots - radius 2 - shows off color better
	25:[2,level[1],level[1],level[1]], #grey range
	26:[2,level[2],level[2],level[2]],	#dark
	27:[2,level[3],level[3],level[3]],
	28:[2,level[4],level[4],level[4]],
	29:[2,level[5],level[5],level[5]],	#light
	30:[2,level[6],level[6],level[6]], #end greys

	31:[2,level[1],0,0],	#red range
	32:[2,level[2],0,0],	 #dark red
	33:[2,level[3],0,0],
	34:[2,level[4],0,0],
	35:[2,level[5],0,0],
	36:[2,level[6],0,0], #light red

	37:[2,0,level[1],0], #green range
	38:[2,0,level[2],0],  #dark green
	39:[2,0,level[3],0],
	40:[2,0,level[4],0],
	41:[2,0,level[5],0],
	42:[2,0,level[6],0],  #light green

	43:[2,0,0,level[1]], #blue range	
	44:[2,0,0,level[2]],  #dark blue
	45:[2,0,0,level[3]],
	46:[2,0,0,level[4]],
	47:[2,0,0,level[5]],
	48:[2,0,0,level[6]]}  #light blue

enterprise = [[5,3,8,27], #model of the enterprise designed for a 16x9x25 voxelblock
			  [5,3,9,27], #formatted [x,y,z,id], 27 being grey and 34 being red
			  [6,3,9,27],
			  [7,3,9,27],
			  [7,3,10,27],
			  [7,3,11,27],
			  [7,3,12,27],
			  [7,3,13,27],
			  [7,3,14,27],
			  [7,3,15,27],
			  [7,3,16,27],
			  [8,3,13,27],
			  [8,3,14,27],
			  [8,3,15,27],
			  [8,3,16,27],
			  [8,3,17,27],
			  [8,3,18,27],
			  [9,3,13,27],
			  [9,3,14,27],
			  [9,3,15,27],
			  [9,3,16,27],
			  [9,3,17,27],
			  [9,3,18,27],
			  [10,3,9,27],
			  [10,3,10,27],
			  [10,3,11,27],
			  [10,3,12,27],
			  [10,3,13,27],
			  [10,3,14,27],
			  [10,3,15,27],
			  [10,3,16,27],
			  [11,3,9,27],
			  [12,3,8,27],
			  [12,3,9,27],
			  [5,4,8,27],
			  [5,4,9,27],
			  [6,4,17,27],
			  [7,4,13,27],
			  [7,4,14,27],
			  [7,4,15,27],
			  [7,4,16,27],
			  [7,4,17,27],
			  [7,4,18,27],
			  [7,4,19,27],
			  [8,4,16,27],
			  [8,4,17,27],
			  [8,4,18,27],
			  [8,4,19,27],
			  [8,4,20,27],
			  [9,4,16,27],
			  [9,4,17,27],
			  [9,4,18,27],
			  [9,4,19,27],
			  [9,4,20,27],
			  [10,4,13,27],
			  [10,4,14,27],
			  [10,4,15,27],
			  [10,4,16,27],
			  [10,4,17,27],
			  [10,4,18,27],
			  [10,4,19,27],
			  [11,4,17,27],
			  [12,4,8,27],
			  [12,4,9,27],
			  [4,5,9,27],
			  [4,5,10,27],
			  [4,5,11,27],
			  [4,5,12,34],
			  [5,5,2,27],
			  [5,5,3,27],
			  [5,5,4,27],
			  [5,5,5,27],
			  [5,5,6,27],
			  [5,5,7,27],
			  [5,5,8,27],
			  [5,5,9,27],
			  [5,5,10,27],
			  [5,5,11,34],
			  [5,5,12,34],
			  [6,5,18,27],
			  [6,5,19,27],
			  [6,5,20,27],
			  [7,5,17,27],
			  [7,5,18,27],
			  [7,5,19,27],
			  [7,5,20,27],
			  [7,5,21,27],
			  [8,5,16,27],
			  [8,5,17,27],
			  [8,5,18,27],
			  [8,5,19,27],
			  [8,5,20,27],
			  [8,5,21,27],
			  [8,5,22,27],
			  [9,5,16,27],
			  [9,5,17,27],
			  [9,5,18,27],
			  [9,5,19,27],
			  [9,5,20,27],
			  [9,5,21,27],
			  [9,5,22,27],
			  [10,5,17,27],
			  [10,5,18,27],
			  [10,5,19,27],
			  [10,5,20,27],
			  [10,5,21,27],
			  [11,5,18,27],
			  [11,5,19,27],
			  [11,5,20,27],
			  [12,5,2,27],
			  [12,5,3,27],
			  [12,5,4,27],
			  [12,5,5,27],
			  [12,5,6,27],
			  [12,5,7,27],
			  [12,5,8,27],
			  [12,5,9,27],
			  [12,5,10,27],
			  [12,5,11,34],
			  [12,5,12,34],
			  [13,5,9,27],
			  [13,5,10,27],
			  [13,5,11,27],
			  [13,5,12,34],
			  [3,6,17,27],
			  [3,6,18,27],
			  [3,6,19,27],
			  [3,6,20,27],
			  [4,6,7,27],
			  [4,6,8,27],
			  [4,6,9,27],
			  [4,6,10,27],
			  [4,6,11,27],
			  [4,6,12,34],
			  [4,6,15,27],
			  [4,6,16,27],
			  [4,6,17,27],
			  [4,6,18,27],
			  [4,6,19,27],
			  [4,6,20,27],
			  [4,6,21,27],
			  [4,6,22,27],
			  [5,6,4,27],
			  [5,6,5,27],
			  [5,6,6,27],
			  [5,6,7,27],
			  [5,6,8,27],
			  [5,6,9,27],
			  [5,6,10,27],
			  [5,6,11,27],
			  [5,6,12,27],
			  [5,6,15,27],
			  [5,6,16,27],
			  [5,6,17,27],
			  [5,6,18,27],
			  [5,6,19,27],
			  [5,6,20,27],
			  [5,6,21,27],
			  [5,6,22,27],
			  [5,6,23,27],
			  [6,6,14,27],
			  [6,6,15,27],
			  [6,6,16,27],
			  [6,6,17,27],
			  [6,6,18,27],
			  [6,6,19,27],
			  [6,6,20,27],
			  [6,6,21,27],
			  [6,6,22,27],
			  [6,6,23,27],
			  [7,6,14,27],
			  [7,6,15,27],
			  [7,6,16,27],
			  [7,6,17,27],
			  [7,6,18,27],
			  [7,6,19,27],
			  [7,6,20,27],
			  [7,6,21,27],
			  [7,6,22,27],
			  [7,6,23,27],
			  [7,6,24,27],
			  [8,6,14,27],
			  [8,6,15,27],
			  [8,6,16,27],
			  [8,6,17,27],
			  [8,6,18,27],
			  [8,6,19,27],
			  [8,6,20,27],
			  [8,6,21,27],
			  [8,6,22,27],
			  [8,6,23,27],
			  [8,6,24,27],
			  [9,6,14,27],
			  [9,6,15,27],
			  [9,6,16,27],
			  [9,6,17,27],
			  [9,6,18,27],
			  [9,6,19,27],
			  [9,6,20,27],
			  [9,6,21,27],
			  [9,6,22,27],
			  [9,6,23,27],
			  [9,6,24,27],
			  [10,6,14,27],
			  [10,6,15,27],
			  [10,6,16,27],
			  [10,6,17,27],
			  [10,6,18,27],
			  [10,6,19,27],
			  [10,6,20,27],
			  [10,6,21,27],
			  [10,6,22,27],
			  [10,6,23,27],
			  [10,6,24,27],
			  [11,6,14,27],
			  [11,6,15,27],
			  [11,6,16,27],
			  [11,6,17,27],
			  [11,6,18,27],
			  [11,6,19,27],
			  [11,6,20,27],
			  [11,6,21,27],
			  [11,6,22,27],
			  [11,6,23,27],
			  [12,6,4,27],
			  [12,6,5,27],
			  [12,6,6,27],
			  [12,6,7,27],
			  [12,6,8,27],
			  [12,6,9,27],
			  [12,6,10,27],
			  [12,6,11,27],
			  [12,6,12,27],
			  [12,6,15,27],
			  [12,6,16,27],
			  [12,6,17,27],
			  [12,6,18,27],
			  [12,6,19,27],
			  [12,6,20,27],
			  [12,6,21,27],
			  [12,6,22,27],
			  [12,6,23,27],
			  [13,6,7,27],
			  [13,6,8,27],
			  [13,6,9,27],
			  [13,6,10,27],
			  [13,6,11,27],
			  [13,6,12,34],
			  [13,6,15,27],
			  [13,6,16,27],
			  [13,6,17,27],
			  [13,6,18,27],
			  [13,6,19,27],
			  [13,6,20,27],
			  [13,6,21,27],
			  [13,6,22,27],
			  [14,6,17,27],
			  [14,6,18,27],
			  [14,6,19,27],
			  [14,6,20,27],
			  [4,7,4,27],
			  [4,7,5,27],
			  [4,7,6,27],
			  [4,7,7,27],
			  [4,7,8,27],
			  [4,7,9,27],
			  [4,7,10,27],
			  [4,7,11,27],
			  [4,7,12,27],
			  [5,7,4,27],
			  [5,7,5,27],
			  [5,7,6,27],
			  [5,7,7,27],
			  [5,7,8,27],
			  [5,7,9,27],
			  [5,7,10,27],
			  [5,7,11,27],
			  [5,7,12,27],
			  [6,7,18,27],
			  [6,7,19,27],
			  [6,7,20,27],
			  [7,7,17,27],
			  [7,7,18,27],
			  [7,7,19,27],
			  [7,7,20,27],
			  [7,7,21,27],
			  [8,7,16,27],
			  [8,7,17,27],
			  [8,7,18,27],
			  [8,7,19,27],
			  [8,7,20,27],
			  [8,7,21,27],
			  [8,7,22,27],
			  [9,7,16,27],
			  [9,7,17,27],
			  [9,7,18,27],
			  [9,7,19,27],
			  [9,7,20,27],
			  [9,7,21,27],
			  [9,7,22,27],
			  [10,7,17,27],
			  [10,7,18,27],
			  [10,7,19,27],
			  [10,7,20,27],
			  [10,7,21,27],
			  [11,7,18,27],
			  [11,7,19,27],
			  [11,7,20,27],
			  [12,7,4,27],
			  [12,7,5,27],
			  [12,7,6,27],
			  [12,7,7,27],
			  [12,7,8,27],
			  [12,7,9,27],
			  [12,7,10,27],
			  [12,7,11,27],
			  [12,7,12,27],
			  [13,7,4,27],
			  [13,7,5,27],
			  [13,7,6,27],
			  [13,7,7,27],
			  [13,7,8,27],
			  [13,7,9,27],
			  [13,7,10,27],
			  [13,7,11,27],
			  [13,7,12,27]]


#CLASSES

class Voxel:
	def __init__(self,_x,_y,_z, _id = 0):
		self.x = _x #coordinates
		self.y = _y
		self.z = _z
		self.id = _id

#METHODS

def dist(x1,y1,z1,x2,y2,z2): #takes two points in (x,y,z) format and returns the absolute value of the distance
	a = (x1,y1,z1) #data point 1
	b = (x2,y2,z2) #data point 2
	return math.fabs(math.sqrt(sum( (a - b)**2 for a, b in zip(a, b))))

def clamp(a,amin,amax): #clamps a to the minimum extent min and the maximum extent max
	return max(min(a, amax), amin)

#BELOW FROM http://www.labri.fr/perso/nrougier/teaching/opengl/scripts/transforms.py
# came with a great tutorial that got a little hand-wavy but it me started(like almost singlehandedly - jb 3/23/2015), available at http://www.labri.fr/perso/nrougier/teaching/opengl/#hello-flat-world


"""
Very simple transformation library that is needed for some examples.
"""

import math
import numpy
import numpy as np


def translate(M, x, y=None, z=None):
    """
    translate produces a translation by (x, y, z) . 
    
    Parameters
    ----------
    x, y, z
        Specify the x, y, and z coordinates of a translation vector.
    """
    if y is None: y = x
    if z is None: z = x
    T = [[ 1, 0, 0, x],
         [ 0, 1, 0, y],
         [ 0, 0, 1, z],
         [ 0, 0, 0, 1]]
    T = np.array(T, dtype=np.float32).T
    M[...] = np.dot(M,T)


def scale(M, x, y=None, z=None):
    """
    scale produces a non uniform scaling along the x, y, and z axes. The three
    parameters indicate the desired scale factor along each of the three axes.

    Parameters
    ----------
    x, y, z
        Specify scale factors along the x, y, and z axes, respectively.
    """
    if y is None: y = x
    if z is None: z = x
    S = [[ x, 0, 0, 0],
         [ 0, y, 0, 0],
         [ 0, 0, z, 0],
         [ 0, 0, 0, 1]]
    S = np.array(S,dtype=np.float32).T
    M[...] = np.dot(M,S)


def xrotate(M,theta):
    t = math.pi*theta/180
    cosT = math.cos( t )
    sinT = math.sin( t )
    R = numpy.array(
        [[ 1.0,  0.0,  0.0, 0.0 ],
         [ 0.0, cosT,-sinT, 0.0 ],
         [ 0.0, sinT, cosT, 0.0 ],
         [ 0.0,  0.0,  0.0, 1.0 ]], dtype=np.float32)
    M[...] = np.dot(M,R)

def yrotate(M,theta):
    t = math.pi*theta/180
    cosT = math.cos( t )
    sinT = math.sin( t )
    R = numpy.array(
        [[ cosT,  0.0, sinT, 0.0 ],
         [ 0.0,   1.0,  0.0, 0.0 ],
         [-sinT,  0.0, cosT, 0.0 ],
         [ 0.0,  0.0,  0.0, 1.0 ]], dtype=np.float32)
    M[...] = np.dot(M,R)

def zrotate(M,theta):
    t = math.pi*theta/180
    cosT = math.cos( t )
    sinT = math.sin( t )
    R = numpy.array(
        [[ cosT,-sinT, 0.0, 0.0 ],
         [ sinT, cosT, 0.0, 0.0 ],
         [ 0.0,  0.0,  1.0, 0.0 ],
         [ 0.0,  0.0,  0.0, 1.0 ]], dtype=np.float32)
    M[...] = np.dot(M,R)


def rotate(M, angle, x, y, z, point=None):
    """
    rotate produces a rotation of angle degrees around the vector (x, y, z).
    
    Parameters
    ----------
    M
       Current transformation as a numpy array

    angle
       Specifies the angle of rotation, in degrees.

    x, y, z
        Specify the x, y, and z coordinates of a vector, respectively.
    """
    angle = math.pi*angle/180
    c,s = math.cos(angle), math.sin(angle)
    n = math.sqrt(x*x+y*y+z*z)
    x /= n
    y /= n
    z /= n
    cx,cy,cz = (1-c)*x, (1-c)*y, (1-c)*z
    R = numpy.array([[ cx*x + c  , cy*x - z*s, cz*x + y*s, 0],
                     [ cx*y + z*s, cy*y + c  , cz*y - x*s, 0],
                     [ cx*z - y*s, cy*z + x*s, cz*z + c,   0],
                     [          0,          0,        0,   1]]).T
    M[...] = np.dot(M,R)


def ortho( left, right, bottom, top, znear, zfar ):
    assert( right  != left )
    assert( bottom != top  )
    assert( znear  != zfar )
    
    M = np.zeros((4,4), dtype=np.float32)
    M[0,0] = +2.0/(right-left)
    M[3,0] = -(right+left)/float(right-left)
    M[1,1] = +2.0/(top-bottom)
    M[3,1] = -(top+bottom)/float(top-bottom)
    M[2,2] = -2.0/(zfar-znear)
    M[3,2] = -(zfar+znear)/float(zfar-znear)
    M[3,3] = 1.0
    return M
        
def frustum( left, right, bottom, top, znear, zfar ):
    assert( right  != left )
    assert( bottom != top  )
    assert( znear  != zfar )

    M = np.zeros((4,4), dtype=np.float32)
    M[0,0] = +2.0*znear/(right-left)
    M[2,0] = (right+left)/(right-left)
    M[1,1] = +2.0*znear/(top-bottom)
    M[3,1] = (top+bottom)/(top-bottom)
    M[2,2] = -(zfar+znear)/(zfar-znear)
    M[3,2] = -2.0*znear*zfar/(zfar-znear)
    M[2,3] = -1.0
    return M

def perspective(fovy, aspect, znear, zfar):
    assert( znear != zfar )
    h = np.tan(fovy / 360.0 * np.pi) * znear
    w = h * aspect
    return frustum( -w, w, -h, h, znear, zfar )