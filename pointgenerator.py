from voxutil import *
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

		self.subd_sphere_squares(a,b,c,d,offset,0,stop)
		self.subd_sphere_squares(a,b,h,g,offset,0,stop)
		self.subd_sphere_squares(a,c,h,f,offset,0,stop)
		self.subd_sphere_squares(c,d,f,e,offset,0,stop)
		self.subd_sphere_squares(e,f,g,h,offset,0,stop)
		self.subd_sphere_squares(d,b,e,g,offset,0,stop)

	def subd_sphere_squares(self,a,b,c,d,offset,level,stop,color=None,normals=False):

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
			self.colors.append((random.rand(),random.rand(),random.rand(),1.0))

			self.points.append(b)
			self.colors.append((random.rand(),random.rand(),random.rand(),1.0))

			self.points.append(c)
			self.colors.append((random.rand(),random.rand(),random.rand(),1.0))



			#triangle 2

			self.points.append(b)
			self.colors.append((random.rand(),random.rand(),random.rand(),1.0))

			self.points.append(c)
			self.colors.append((random.rand(),random.rand(),random.rand(),1.0))

			self.points.append(d)
			self.colors.append((random.rand(),random.rand(),random.rand(),1.0))

			self.num_points += 6

		else:

			topmid = 	( (a[0]+b[0])/2 , (a[1]+b[1])/2 , (a[2]+b[2])/2 )
			sidemid1 = 	( (a[0]+c[0])/2 , (a[1]+c[1])/2 , (a[2]+c[2])/2 )
			sidemid2 = 	( (b[0]+d[0])/2 , (b[1]+d[1])/2 , (b[2]+d[2])/2 )
			bottommid = ( (c[0]+d[0])/2 , (c[1]+d[1])/2 , (c[2]+d[2])/2 )
			center = ( (a[0]+b[0]+c[0]+d[0])/4 , (a[1]+b[1]+c[1]+d[1])/4 , (a[2]+b[2]+c[2]+d[2])/4 )

			self.subd_sphere_squares( 		 a,   topmid,  sidemid1,    center, offset,level+1,stop,color,normals)
			self.subd_sphere_squares(   topmid, 	   b,  	 center,  sidemid2, offset,level+1,stop,color,normals)
			self.subd_sphere_squares( sidemid1,   center, 		  c, bottommid, offset,level+1,stop,color,normals)
			self.subd_sphere_squares(   center, sidemid2, bottommid, 	     d, offset,level+1,stop,color,normals)

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

	def gen_legacy_seed_block(self,_seed,ix,iy,iz,imin,imax):

		usersetx = ix
		usersety = iy
		usersetz = iz

		spacer = 2

		seed = _seed

		minextent = imin
		maxextent = imax

		self.num_points = usersetx * usersety * usersetz

		pointstyle = "single point per voxel"
		#pointstyle = "six points per voxel"
		#pointstyle = "27 points per voxel" 
		#pointstyle = "36 points per voxel"
		#pointstyle = "36 points per voxel + six"
		#pointstyle = "189 points per voxel"
		#pointstyle = "729 points per voxel"
		#pointstyle = "19683 points per voxel"
		#pointstyle = "531441 points per voxel"

		usersetx_np = np.linspace(minextent, maxextent, usersetx, True, True, dtype=np.float32) # numpy function linspace(start,stop,steps,endpoints,retstep=False,dtype=None) - using float32 for opengl
		usersety_np = np.linspace(minextent, maxextent, usersety, True, True, dtype=np.float32)
		usersetz_np = np.linspace(minextent, maxextent, usersetz, True, True, dtype=np.float32)

		if pointstyle == "single point per voxel":
			self.num_points = self.num_points
		elif pointstyle == "six points per voxel":
			self.num_points *= 6
		elif pointstyle == "27 points per voxel":
			self.num_points *= 27
		elif pointstyle == "36 points per voxel":
			self.num_points *= 36
		elif pointstyle == "36 points per voxel + six":
			self.num_points *= (36+6)
		elif pointstyle == "189 points per voxel":
			self.num_points *= 189
		elif pointstyle == "729 points per voxel":
			self.num_points *= 729
		elif pointstyle == "19683 points per voxel":
			self.num_points *= 19683
		elif pointstyle == "531441 points per voxel":
			self.num_points *= 531441
		print("Rendering "+str(usersetx)+"x "+str(usersety)+"y "+str(usersetz)+"z with "+pointstyle+" for a total of "+str(self.num_points))


		x_values = array(usersetx_np)[0]
		y_values = array(usersety_np)[0]
		z_values = array(usersetz_np)[0]

		x_step = array(usersetx_np)[1]
		y_step = array(usersety_np)[1]
		z_step = array(usersetz_np)[1]

		x_min = x_values[0]
		x_max = x_values[len(x_values)-1]

		y_min = y_values[0]
		y_max = y_values[len(y_values)-1]

		z_min = z_values[0]
		z_max = z_values[len(z_values)-1]

		t0 = time.time()

		for x in range(0,usersetx):
			for y in range(0,usersety):
				for z in range(0,usersetz):

					#colors

					col = (0.5,0.5,0.5,0.01)

					cur_x = x_values[x]
					cur_y = y_values[y]
					cur_z = z_values[z]

					if seed == 0:
						col == (0.5,0.5,0.5,1.0)
					elif seed == 1: # color the outside black - if these are just simple checks like this, they can be calculated on the gpu per vertex
						if (cur_x == x_min) or (cur_x == x_max) or (cur_y == y_min) or (cur_y == y_max) or (cur_z == z_min) or (cur_z == z_max):
							col = (0.3,0.3,0.3,1.0)
						else:
							col = (1.0,1.0,0.0,1.0)
					elif seed == 2: # Color the frame of the box (0.3,0.3,0.3,1.0) and the faces a different color
						if (cur_x == x_min and cur_y == y_min and cur_z == z_min) or (cur_x == x_min and cur_y == y_min and cur_z == z_max) or (cur_x == x_min and cur_y == y_max and cur_z == z_min) or (cur_x == x_min and cur_y == y_max and cur_z == z_max) or (cur_x == x_max and cur_y == y_min and cur_z == z_min) or (cur_x == x_max and cur_y == y_min and cur_z == z_max) or (cur_x == x_max and cur_y == y_max and cur_z == z_min) or (cur_x == x_max and cur_y == y_max and cur_z == z_max):
								col = (1.0,0.0,1.0,1.0) # corner color
						elif (cur_x == x_min and cur_y == y_min) or (cur_y == y_min and cur_z == z_min) or (cur_x == x_min and cur_z == z_min) or (cur_x == x_max and cur_y == y_max) or (cur_y == y_max and cur_z == z_max) or (cur_x == x_max and cur_z == z_max) or (cur_x == x_min and cur_z == z_max) or (cur_x == x_min and cur_y == y_max) or (cur_y == y_max and cur_z == z_min) or (cur_y == y_min and cur_z == z_max) or (cur_x == x_max and cur_z == z_min) or (cur_x == x_max and cur_y == y_min):
							col = (0.9,0.0,0.0,1.0) # edge color
						elif (cur_x == x_min) or (cur_x == x_max) or (cur_y == y_min) or (cur_y == y_max) or (cur_z == z_min) or (cur_z == z_max):
							col = (0.3,0.0,0.0,1.0) # face color
						else:
							col = (1.0,0.7,0.0,1.0) # interior color
					elif seed == 3: # balls on the corners + frame
						ballrad = 0.4
						if (dist(cur_x,cur_y,cur_z,x_min,y_min,z_min) < ballrad) or (dist(cur_x,cur_y,cur_z,x_min,y_min,z_max) < ballrad) or (dist(cur_x,cur_y,cur_z,x_min,x_max,z_min) < ballrad) or (dist(cur_x,cur_y,cur_z,x_min,x_max,z_max) < ballrad) or (dist(cur_x,cur_y,cur_z,x_max,x_min,z_min) < ballrad) or (dist(cur_x,cur_y,cur_z,x_max,x_min,z_max) < ballrad) or (dist(cur_x,cur_y,cur_z,x_max,x_max,z_min) < ballrad) or (dist(cur_x,cur_y,cur_z,x_max,x_max,z_max) < ballrad) or (dist(cur_x,cur_y,cur_z,0,0,0) < ballrad):
							col = (0.5,0.0,0.0,0.1) # ball color
						else:
							col = (0.0,0.0,0.0,0.1)	# negative space color

						if (cur_x == x_min and cur_y == y_min and cur_z == z_min) or (cur_x == x_min and cur_y == y_min and cur_z == z_max) or (cur_x == x_min and cur_y == y_max and cur_z == z_min) or (cur_x == x_min and cur_y == y_max and cur_z == z_max) or (cur_x == x_max and cur_y == y_min and cur_z == z_min) or (cur_x == x_max and cur_y == y_min and cur_z == z_max) or (cur_x == x_max and cur_y == y_max and cur_z == z_min) or (cur_x == x_max and cur_y == y_max and cur_z == z_max):
								col = (1.0,1.0,1.0,1.0) # corner color
						elif (cur_x == x_min and cur_y == y_min) or (cur_y == y_min and cur_z == z_min) or (cur_x == x_min and cur_z == z_min) or (cur_x == x_max and cur_y == y_max) or (cur_y == y_max and cur_z == z_max) or (cur_x == x_max and cur_z == z_max) or (cur_x == x_min and cur_z == z_max) or (cur_x == x_min and cur_y == y_max) or (cur_y == y_max and cur_z == z_min) or (cur_y == y_min and cur_z == z_max) or (cur_x == x_max and cur_z == z_min) or (cur_x == x_max and cur_y == y_min):
							col = (0.1,0.1,1.0,1.0) # edge color
					elif seed == 4: # earthoid
						surfmin = 0.37
						surfmax = 0.44

						mantlemin = 0.28
						mantlemax = surfmin

						outercoremin = 0.2
						outercoremax = mantlemin

						innercoremin = 0.1
						innercoremax = outercoremin
						
						centerdist = dist(cur_x,cur_y,cur_z,0,0,0)
						if centerdist > surfmin and centerdist < surfmax:
							if random.rand() > 03:
								col = (0.0,0.9*random.rand(),0.7*random.rand(),1.0)
							else:
								col = (0.0,0.3*random.rand(),random.rand(),1.0)
						elif centerdist > mantlemin and centerdist < mantlemax:
							col = (0.5*random.rand(),0.3*random.rand(),0.0,1.0)
						elif centerdist > outercoremin and centerdist < outercoremax:
							col = (0.6,0.3*random.rand(),0.0,1.0)
						elif centerdist > innercoremin and centerdist < innercoremax:
							col = (0.75,1.0*random.rand(),0.0,random.rand())
						elif centerdist < innercoremin:
							col = (1.0,0.0,0.0,1.0) 
						else:
							col = (0.3,0.3,0.3,0.001)

						if (cur_x == x_min and cur_y == y_min) or (cur_y == y_min and cur_z == z_min) or (cur_x == x_min and cur_z == z_min) or (cur_x == x_max and cur_y == y_max) or (cur_y == y_max and cur_z == z_max) or (cur_x == x_max and cur_z == z_max) or (cur_x == x_min and cur_z == z_max) or (cur_x == x_min and cur_y == y_max) or (cur_y == y_max and cur_z == z_min) or (cur_y == y_min and cur_z == z_max) or (cur_x == x_max and cur_z == z_min) or (cur_x == x_max and cur_y == y_min):
							col = (1.0,1.0,1.0,1.0) # edge color

					num = 1

					if pointstyle == "single point per voxel":
						num = num
					elif pointstyle == "six points per voxel":
						num *= 6
					elif pointstyle == "27 points per voxel":
						num *= 27
					elif pointstyle == "36 points per voxel":
						num *= 36
					elif pointstyle == "36 points per voxel + six":
						num *= (36+6)
					elif pointstyle == "189 points per voxel":
						num *= 189
					elif pointstyle == "729 points per voxel":
						num *= 729
					elif pointstyle == "19683 points per voxel":
						num *= 19683
					elif pointstyle == "531441 points per voxel":
						num *= 531441
					else:
						print(pointstyle+" is not supported")


					for i in range(0,num):
						self.colors.append((col))

					#now points
					if pointstyle == "531441 points per voxel":
						xoffset = 0
						x2offset = 0
						x3offset = 0
						x4offset = 0
						xspacer = x_step/spacer
						x2spacer = x_step/(spacer**2)
						x3spacer = x_step/(spacer**3)
						x4spacer = x_step/(spacer**4)

						yoffset = 0
						y2offset = 0
						y3spacer = 0
						y4spacer = 0
						yspacer = y_step/spacer
						y2spacer = y_step/(spacer**2)
						y3spacer = y_step/(spacer**3)
						y4spacer = y_step/(spacer**4)

						zoffset = 0
						z2offset = 0
						z3offset = 0
						z4offset = 0
						zspacer = z_step/spacer
						z2spacer = z_step/(spacer**2)
						z3spacer = z_step/(spacer**3)
						z4spacer = z_step/(spacer**4)

						for i in range(-1,2):
							xoffset = i*xspacer

							for j in range(-1,2):
								yoffset = j*yspacer

								for k in range(-1,2):
									zoffset = k*zspacer

									for l in range(-1,2):
										x2offset = l*x2spacer

										for m in range(-1,2):
											y2offset = m*y2spacer

											for n in range(-1,2):
												z2offset = n*z2spacer

												for o in range(-1,2):
													x3offset = o*x3spacer

													for p in range(-1,2):
														y3offset = p*y3spacer

														for q in range(-1,2):
															z3offset = q*z3spacer

															for r in range(-1,2):
																x4offset = r*x4spacer

																for s in range(-1,2):
																	y4offset = s*y4spacer

																	for t in range(-1,2):
																		z4offset = t*z4spacer

																		points.append(((x_values[x]+xoffset+x2offset+x3offset+x4offset),(y_values[y]+yoffset+y2offset+y3offset+y4offset),(z_values[z]+zoffset+z2offset+z3offset+z4offset)))
												print(str(x)+"/"+str(usersetx)+" "+str(y)+"/"+str(usersety)+" "+str(z)+"/"+str(usersetz)+"   "+str(i)+" "+str(j)+" "+str(k)+" "+str(l)+" "+str(m)+" "+str(n))
					
					elif pointstyle == "19683 points per voxel":
						xoffset = 0
						x2offset = 0
						x3offset = 0
						xspacer = x_step/spacer
						x2spacer = x_step/(spacer**2)
						x3spacer = x_step/(spacer**3)

						yoffset = 0
						y2offset = 0
						y3spacer = 0
						yspacer = y_step/spacer
						y2spacer = y_step/(spacer**2)
						y3spacer = y_step/(spacer**3)

						zoffset = 0
						z2offset = 0
						z3offset = 0
						zspacer = z_step/spacer
						z2spacer = z_step/(spacer**2)
						z3spacer = z_step/(spacer**3)

						for i in range(-1,2):
							xoffset = i*xspacer

							for j in range(-1,2):
								yoffset = j*yspacer

								for k in range(-1,2):
									zoffset = k*zspacer

									for l in range(-1,2):
										x2offset = l*x2spacer

										for m in range(-1,2):
											y2offset = m*y2spacer

											for n in range(-1,2):
												z2offset = n*z2spacer

												for o in range(-1,2):
													x3offset = o*x3spacer

													for p in range(-1,2):
														y3offset = p*y3spacer

														for q in range(-1,2):
															z3offset = q*z3spacer

															points.append((x_values[x]+xoffset+x2offset+x3offset,y_values[y]+yoffset+y2offset+y3offset,z_values[z]+zoffset+z2offset+z3offset))
												print(str(x)+" "+str(y)+" "+str(z)+"   "+str(i)+" "+str(j)+" "+str(k)+" "+str(l)+" "+str(m)+" "+str(n))

					elif pointstyle == "729 points per voxel":
						xoffset = 0
						x2offset = 0
						xspacer = x_step/spacer
						x2spacer = x_step/(spacer**2)

						yoffset = 0
						y2offset = 0
						yspacer = y_step/spacer
						y2spacer = y_step/(spacer**2)

						zoffset = 0
						z2offset = 0
						zspacer = z_step/spacer
						z2spacer = z_step/(spacer**2)

						for i in range(-1,2):
							xoffset = i*xspacer

							for j in range(-1,2):
								yoffset = j*yspacer

								for k in range(-1,2):
									zoffset = k*zspacer

									for l in range(-1,2):
										x2offset = l*x2spacer

										for m in range(-1,2):
											y2offset = m*y2spacer

											for n in range(-1,2):
												z2offset = n*z2spacer

												self.points.append((x_values[x]+xoffset+x2offset,y_values[y]+yoffset+y2offset,z_values[z]+zoffset+z2offset))
												print(str(x)+" "+str(y)+" "+str(z)+"   "+str(i)+" "+str(j)+" "+str(k)+" "+str(l)+" "+str(m)+" "+str(n))

					elif pointstyle == "189 points per voxel":
						xoffset = 0
						yoffset = 0
						zoffset = 0

						for i in range(-1,2):
							xoffset = i*(x_step/spacer)

							for j in range(-1,2):
								yoffset = j*(y_step/spacer)

								for k in range(-1,2):
									zoffset = k*(z_step/spacer)

									self.points.append((x_values[x]+xoffset,y_values[y]+yoffset,z_values[z]+zoffset))
									self.points.append(((x_values[x]+(x_step/(spacer**2)))+xoffset,y_values[y]+yoffset,z_values[z]+zoffset))
									self.points.append(((x_values[x]-(x_step/(spacer**2)))+xoffset,y_values[y]+yoffset,z_values[z]+zoffset))
									self.points.append((x_values[x]+xoffset,(y_values[y]+(y_step/(spacer**2)))+yoffset,z_values[z]+zoffset))
									self.points.append((x_values[x]+xoffset,(y_values[y]-(y_step/(spacer**2)))+yoffset,z_values[z]+zoffset))
									self.points.append((x_values[x]+xoffset,y_values[y]+yoffset,(z_values[z]+(z_step/(spacer**2)))+zoffset))
									self.points.append((x_values[x]+xoffset,y_values[y]+yoffset,(z_values[z]-(z_step/(spacer**2)))+zoffset))

					elif pointstyle == "36 points per voxel" or  pointstyle == "36 points per voxel + six":
						#looking back, the code got shorter as I covered more points

						self.points.append(((x_values[x]+(x_step/spacer))+(x_step/(spacer**2)),y_values[y],z_values[z]))
						self.points.append(((x_values[x]+(x_step/spacer))-(x_step/(spacer**2)),y_values[y],z_values[z]))
						self.points.append(((x_values[x]+(x_step/spacer)),y_values[y]+(y_step/(spacer**2)),z_values[z]))
						self.points.append(((x_values[x]+(x_step/spacer)),y_values[y]-(y_step/(spacer**2)),z_values[z]))
						self.points.append(((x_values[x]+(x_step/spacer)),y_values[y],z_values[z]+(z_step/(spacer**2))))
						self.points.append(((x_values[x]+(x_step/spacer)),y_values[y],z_values[z]-(z_step/(spacer**2))))

						self.points.append(((x_values[x]-(x_step/spacer))+(x_step/(spacer**2)),y_values[y],z_values[z]))
						self.points.append(((x_values[x]-(x_step/spacer))-(x_step/(spacer**2)),y_values[y],z_values[z]))
						self.points.append(((x_values[x]-(x_step/spacer)),y_values[y]+(y_step/(spacer**2)),z_values[z]))
						self.points.append(((x_values[x]-(x_step/spacer)),y_values[y]-(y_step/(spacer**2)),z_values[z]))
						self.points.append(((x_values[x]-(x_step/spacer)),y_values[y],z_values[z]+(z_step/(spacer**2))))
						self.points.append(((x_values[x]-(x_step/spacer)),y_values[y],z_values[z]-(z_step/(spacer**2))))

						self.points.append((x_values[x]+(x_step/(spacer**2)),(y_values[y]+(y_step/spacer)),z_values[z]))
						self.points.append((x_values[x]-(x_step/(spacer**2)),(y_values[y]+(y_step/spacer)),z_values[z]))
						self.points.append((x_values[x],(y_values[y]+(y_step/spacer))+(y_step/(spacer**2)),z_values[z]))
						self.points.append((x_values[x],(y_values[y]+(y_step/spacer))-(y_step/(spacer**2)),z_values[z]))
						self.points.append((x_values[x],(y_values[y]+(y_step/spacer)),z_values[z]+(z_step/(spacer**2))))
						self.points.append((x_values[x],(y_values[y]+(y_step/spacer)),z_values[z]-(z_step/(spacer**2))))

						self.points.append((x_values[x]+(x_step/(spacer**2)),(y_values[y]-(y_step/spacer)),z_values[z]))
						self.points.append((x_values[x]-(x_step/(spacer**2)),(y_values[y]-(y_step/spacer)),z_values[z]))
						self.points.append((x_values[x],(y_values[y]-(y_step/spacer))+(y_step/(spacer**2)),z_values[z]))
						self.points.append((x_values[x],(y_values[y]-(y_step/spacer))-(y_step/(spacer**2)),z_values[z]))
						self.points.append((x_values[x],(y_values[y]-(y_step/spacer)),z_values[z]+(z_step/(spacer**2))))
						self.points.append((x_values[x],(y_values[y]-(y_step/spacer)),z_values[z]-(z_step/(spacer**2))))

						self.points.append((x_values[x]+(x_step/(spacer**2)),y_values[y],(z_values[z]+(z_step/spacer))))
						self.points.append((x_values[x]-(x_step/(spacer**2)),y_values[y],(z_values[z]+(z_step/spacer))))
						self.points.append((x_values[x],y_values[y]+(y_step/(spacer**2)),(z_values[z]+(z_step/spacer))))
						self.points.append((x_values[x],y_values[y]-(y_step/(spacer**2)),(z_values[z]+(z_step/spacer))))
						self.points.append((x_values[x],y_values[y],(z_values[z]+(z_step/spacer))+(z_step/(spacer**2))))
						self.points.append((x_values[x],y_values[y],(z_values[z]+(z_step/spacer))-(z_step/(spacer**2))))

						self.points.append((x_values[x]+(x_step/(spacer**2)),y_values[y],(z_values[z]-(z_step/spacer))))
						self.points.append((x_values[x]-(x_step/(spacer**2)),y_values[y],(z_values[z]-(z_step/spacer))))
						self.points.append((x_values[x],y_values[y]+(y_step/(spacer**2)),(z_values[z]-(z_step/spacer))))
						self.points.append((x_values[x],y_values[y]-(y_step/(spacer**2)),(z_values[z]-(z_step/spacer))))
						self.points.append((x_values[x],y_values[y],(z_values[z]-(z_step/spacer))+(z_step/(spacer**2))))
						self.points.append((x_values[x],y_values[y],(z_values[z]-(z_step/spacer))-(z_step/(spacer**2))))

						if pointstyle == "36 points per voxel + six":
							self.points.append((x_values[x]+(x_step/spacer),y_values[y],z_values[z]))
							self.points.append((x_values[x]-(x_step/spacer),y_values[y],z_values[z]))
							self.points.append((x_values[x],y_values[y]+(y_step/spacer),z_values[z]))
							self.points.append((x_values[x],y_values[y]-(y_step/spacer),z_values[z]))
							self.points.append((x_values[x],y_values[y],z_values[z]+(z_step/spacer)))
							self.points.append((x_values[x],y_values[y],z_values[z]-(z_step/spacer)))

					elif pointstyle == "27 points per voxel":
						xoffset = 0
						yoffset = 0
						zoffset = 0

						for i in range(-1,2):
							xoffset = i*(x_step/spacer)

							for j in range(-1,2):
								yoffset = j*(y_step/spacer)

								for k in range(-1,2):
									zoffset = k*(z_step/spacer)

									self.points.append((x_values[x]+xoffset,y_values[y]+yoffset,z_values[z]+zoffset))

					elif pointstyle == "six points per voxel":

						self.points.append((x_values[x]+(x_step/spacer),y_values[y],z_values[z]))
						self.points.append((x_values[x]-(x_step/spacer),y_values[y],z_values[z]))
						self.points.append((x_values[x],y_values[y]+(y_step/spacer),z_values[z]))
						self.points.append((x_values[x],y_values[y]-(y_step/spacer),z_values[z]))
						self.points.append((x_values[x],y_values[y],z_values[z]+(z_step/spacer)))
						self.points.append((x_values[x],y_values[y],z_values[z]-(z_step/spacer)))

					elif pointstyle == "single point per voxel":

						self.points.append((x_values[x],y_values[y],z_values[z]))

			print("loading -- "+str(x+1)+"/"+str(usersetx)+"  "+str(100*(x+1)/usersetx)+" percent completed after "+str(time.time()-t0)+" seconds")
			#print(str(len(points))+"<points colors>"+str(len(colors)))
		print("completed "+str(usersetx)+"/"+str(usersetx)+" after "+str(time.time()-t0)+" seconds")
