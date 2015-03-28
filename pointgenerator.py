import math
from numpy import *
import numpy as np

class pointgenerator:

	def __init__(self,desired=None):
		self.reset()

	def reset(self):
		self.colors = []
		self.points = []
		self.num_points = 0

	def gen_sphere(self,offset,stop,normals=False): #uses subd_sphere_squares
		#center assumed at 0,0,0

		self.reset()

		a = (offset,offset,offset)
		b = (-offset,offset,offset)
		c = (offset,offset,-offset)
		d = (-offset,offset,-offset)
		e = (-offset,-offset,-offset)
		f = (offset,-offset,-offset)
		g = (-offset,-offset,offset)
		h = (offset,-offset,offset)

		color = (random.rand(),random.rand(),random.rand(),1.0)

		self.subd_sphere_squares(a,b,c,d,offset,0,stop,color,normals)
		self.subd_sphere_squares(a,b,h,g,offset,0,stop,color,normals)
		self.subd_sphere_squares(a,c,h,f,offset,0,stop,color,normals)
		self.subd_sphere_squares(c,d,f,e,offset,0,stop,color,normals)
		self.subd_sphere_squares(e,f,g,h,offset,0,stop,color,normals)
		self.subd_sphere_squares(d,b,e,g,offset,0,stop,color,normals)

	def subd_sphere_squares(self,a,b,c,d,offset,level,stop,color,normals):

		if level == stop:

			lena = sqrt(a[0]**2+a[1]**2+a[2]**2)
			lenb = sqrt(b[0]**2+b[1]**2+b[2]**2)
			lenc = sqrt(c[0]**2+c[1]**2+c[2]**2)
			lend = sqrt(d[0]**2+d[1]**2+d[2]**2)

			a = (offset*(a[0]/lena),offset*(a[1]/lena),offset*(a[2]/lena))
			b = (offset*(b[0]/lenb),offset*(b[1]/lenb),offset*(b[2]/lenb))
			c = (offset*(c[0]/lenc),offset*(c[1]/lenc),offset*(c[2]/lenc))
			d = (offset*(d[0]/lend),offset*(d[1]/lend),offset*(d[2]/lend))

			#triangle 1

			self.points.append(a)
			self.colors.append(color)

			self.points.append(b)
			self.colors.append(color)

			self.points.append(c)
			self.colors.append(color)



			#triangle 2

			self.points.append(b)
			self.colors.append(color)

			self.points.append(c)
			self.colors.append(color)

			self.points.append(d)
			self.colors.append(color)

			self.num_points += 6

		else:

			topmid = 	( (a[0]+b[0])/2 , (a[1]+b[1])/2 , (a[2]+b[2])/2 )
			sidemid1 = 	( (a[0]+c[0])/2 , (a[1]+c[1])/2 , (a[2]+c[2])/2 )
			sidemid2 = 	( (b[0]+d[0])/2 , (b[1]+d[1])/2 , (b[2]+d[2])/2 )
			bottommid = ( (c[0]+d[0])/2 , (c[1]+d[1])/2 , (c[2]+d[2])/2 )
			center = ( (a[0]+b[0]+c[0]+d[0])/4 , (a[1]+b[1]+c[1]+d[1])/4 , (a[2]+b[2]+c[2]+d[2])/4 )

			self.subd_sphere_squares( 		a,   topmid,  sidemid1,    center, offset,level+1,stop,color,normals)
			self.subd_sphere_squares(   topmid, 		  b, 	center,  sidemid2, offset,level+1,stop,color,normals)
			self.subd_sphere_squares( sidemid1, 	 center, 		 c, bottommid, offset,level+1,stop,color,normals)
			self.subd_sphere_squares(   center, sidemid2, bottommid, 	    d, offset,level+1,stop,color,normals)

	def gen_cube(self,usersetx,usersety,usersetz,color=None,minextent=-0.5,maxextent=0.5):

		self.reset()

		self.num_points = usersetx * usersety * usersetz

		usersetx_np = np.linspace(minextent, maxextent, usersetx, True, False, dtype=np.float32)
		usersety_np = np.linspace(minextent, maxextent, usersety, True, False, dtype=np.float32)
		usersetz_np = np.linspace(minextent, maxextent, usersetz, True, False, dtype=np.float32)

		x_values = array(usersetx_np)
		y_values = array(usersety_np)
		z_values = array(usersetz_np)

		for x in range(0,usersetx):
			for y in range(0,usersety):
				for z in range(0,usersetz):
					self.points.append((x_values[x],y_values[y],z_values[z]))
					if color is None:
						self.colors.append((random.rand(),random.rand(),random.rand(),1.0))
					else:
						self.colors.append(color)
