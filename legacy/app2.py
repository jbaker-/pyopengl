import sys
import os
import random, time
from graphics import *
import math

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

def dist(x1,y1,z1,x2,y2,z2): #takes two points in (x,y,z) format and returns the absolute value of the distance
	a = (x1,y1,z1) #data point 1
	b = (x2,y2,z2) #data point 2
	return math.fabs(math.sqrt(sum( (a - b)**2 for a, b in zip(a, b))))

def clamp(a,min,max): #clamps a to the minimum extent min and the maximum extent max
	if a > max:
		return max
	elif a < min:
		return min
	else:
		return a


#def isbetween(x0,y0,z0,x1,y1,z1,x2,y2,z2,tol): #tells whether (x2,y2,z2) lies on the line between (x0,y0,z0) and (x1,y1,z1) with a tolerance of tol


class Voxel:
	def __init__(self,_x,_y,_z, _id = 0):
		self.x = _x #coordinates
		self.y = _y
		self.z = _z
		self.id = _id

class VoxelBlock:
	def __init__(self, _x_dim = None, _y_dim = None, _z_dim = None, seed = 0,randmin = -50,randmax = 4,fread = None):
		
		if _x_dim is None:
			pass
		else:
			self.x = _x_dim

		if _y_dim is None:
			pass
		else:
			self.y = _y_dim

		if _z_dim is None:
			pass
		else:
			self.z = _z_dim

		self.space = [] #holds voxels
		self.seedValue = 0 #holds a seed value

		if seed == 0: #initalizes all cells to zero
			for i in range(0,self.x):
				for j in range(0,self.y):
					for k in range(0,self.z):
						self.space.append(Voxel(i,j,k,0))
		elif seed == 1: #hull
			for i in range(0,self.x):
				for j in range(0,self.y): 
					for k in range(0,self.z):
						if i == 0 or j == 0 or k == 0 or i == self.x-1 or j == self.y-1 or k == self.z-1:
							self.space.append(Voxel(i,j,k,1)) #occupied - on the outer layer
						else:
							self.space.append(Voxel(i,j,k,0)) #empty
		elif seed == 2: #hull + edges + corners (zeroes inside)
			for i in range(0,self.x):
				for j in range(0,self.y): 
					for k in range(0,self.z):
						self.seedValue = 0
						if i == 0 or j == 0 or k == 0 or i == self.x-1 or j == self.y-1 or k == self.z-1:
							self.seedValue = 1 #hull
						if (i == 0 and j == 0) or (j == 0 and k == 0) or (i == 0 and k == 0) or (i == self.x-1 and j == self.y-1) or (j == self.y-1 and k == self.z-1) or (i == self.x-1 and k == self.z-1) or (i == 0 and k == self.z-1) or (i == 0 and j == self.y-1) or (j == self.y-1 and k == 0) or (j == 0 and k == self.z-1) or (i == self.x-1 and k == 0) or (i == self.x-1 and j == 0):
							self.seedValue = 2 #edges
						if (i == 0 and j == 0 and k == 0) or (i == 0 and j == 0 and k == self.z-1) or (i == 0 and j == self.y-1 and k == 0) or (i == 0 and j == self.y-1 and k == self.z-1) or (i == self.x-1 and j == 0 and k == 0) or (i == self.x-1 and j == 0 and k == self.z-1) or (i == self.x-1 and j == self.y-1 and k == 0) or(i == self.x-1 and j == self.y-1 and k == self.z-1):
							self.seedValue = 3 #corners
						self.space.append(Voxel(i,j,k,self.seedValue))
		elif seed == 3: #hull + edges + corners (random values inside)
			for i in range(0,self.x):
				for j in range(0,self.y): 
					for k in range(0,self.z):
						self.seedValue = random.randrange(randmin,randmax)
						if i == 0 or j == 0 or k == 0 or i == self.x-1 or j == self.y-1 or k == self.z-1:
							self.seedValue = 1 #hull
						if (i == 0 and j == 0) or (j == 0 and k == 0) or (i == 0 and k == 0) or (i == self.x-1 and j == self.y-1) or (j == self.y-1 and k == self.z-1) or (i == self.x-1 and k == self.z-1) or (i == 0 and k == self.z-1) or (i == 0 and j == self.y-1) or (j == self.y-1 and k == 0) or (j == 0 and k == self.z-1) or (i == self.x-1 and k == 0) or (i == self.x-1 and j == 0):
							self.seedValue = 2 #edges
						if (i == 0 and j == 0 and k == 0) or (i == 0 and j == 0 and k == self.z-1) or (i == 0 and j == self.y-1 and k == 0) or (i == 0 and j == self.y-1 and k == self.z-1) or (i == self.x-1 and j == 0 and k == 0) or (i == self.x-1 and j == 0 and k == self.z-1) or (i == self.x-1 and j == self.y-1 and k == 0) or(i == self.x-1 and j == self.y-1 and k == self.z-1):
							self.seedValue = 3 #corners
						self.space.append(Voxel(i,j,k,self.seedValue))
		elif seed == 4: #sphere surrounded by random values
			for i in range(0,self.x):
				for j in range(0,self.y): 
					for k in range(0,self.z):
						if dist(i,j,k,self.x//2,self.y//2,self.z//2) < 6:
							self.space.append(Voxel(i,j,k,3))
						else:
							self.space.append(Voxel(i,j,k,0))
		elif seed == 5: #sphere surrounded by random values
			for i in range(0,self.x):
				for j in range(0,self.y): 
					for k in range(0,self.z):
						if dist(i,j,k,self.x//2,self.y//2,self.z//2) < 7:
							self.space.append(Voxel(i,j,k,2))
						else:
							self.space.append(Voxel(i,j,k,random.randrange(randmin,randmax)))
		elif seed == 6:	#just random
			for i in range(0,self.x):
				for j in range(0,self.y): 
					for k in range(0,self.z):
						self.space.append(Voxel(i,j,k,random.randrange(randmin,randmax)))
		elif seed == 99: #manual entry
			for i in range(0,self.x):
				for j in range(0,self.y): 
					for k in range(0,self.z):
						self.space.append(Voxel(i,j,k,0))
			print("hello and welcome to manual input -- im sorry this happened to you")
			print("all cells have been set to be equal to 0 in anticipation of your visit")
			print("extents are x: 1 - " + str(self.x) + " y: 1 - " + str(self.y) + " z: 1 - " + str(self.z))
			while True:
				choice = raw_input("Enter your choice (q to quit,n for next)").lower()
				if choice == "q":
					break
				elif choice == "n":
					num1 = input("enter first index (x): ")
					num2 = input("enter second index (y): ")
					num3 = input("enter third index (z): ")
					seed = input("set to? (valid seeds: 0-48):")
					self.setcell(num1,num2,num3,seed)
				elif choice == "l": #user enters two points to draw a line between
					'''thresholds = [1.0,1.0,1.0]
					distances = [-1.0,-1.0,-1.0]
					x1 = input("enter first point (x1): ")
					y1 = input("enter first point (y1): ")
					z1 = input("enter first point (z1): ")
					x2 = input("enter second point (x2): ")
					y2 = input("enter second point (y2): ")
					z2 = input("enter second point (z2): ")

					for i in self.space:
						distances[0] = math.fabs()
						distances[1] = math.fabs()
						distances[2] = math.fabs()'''
					pass




		#	for i in enterprise:
		#		self.setcell(i[0],i[1],i[2],i[3])
		else: #load voxels from file
			if fread is None:
				print("invalid seed passed to VoxelBlock init")
			else:
				f = open(fread,'r')
				self.x = int(f.readline())
				self.y = int(f.readline())
				self.z = int(f.readline())
				for i in range(0,self.x):
					for j in range(0,self.y): 
						for k in range(0,self.z):
							self.space.append(Voxel(i,j,k,int(f.readline()))) 
				for i in self.space:
					if i.id == 0:
						i.id = 1


	def output(self, output_type, fsave = None, window = None,screenx = 0, screeny = 0,spacing = 4,fillcolor = "white",routline=False):
		if output_type == "window" or "window especial":
			window = GraphWin("Rendered Output",screenx,screeny)

		if output_type ==  "window especial":
			print ("outputting to " + output_type + ".......")
			if window is None or (screenx and screeny == 0):
				print("no window recieved")
			else: #main display

				l1 = Line(Point(screenx/2,0),Point(screenx/2,screeny))#vertical divider
				l2 = Line(Point(0,screeny/2),Point(screenx,screeny/2))#horizontal divider
				l1.draw(window)
				l2.draw(window)

				'''	cursorx = (screenx/2)//2 + 1
					cursory = (screeny/2)//3 + 1 '''
			#three views
				#view 1 from positive y face "top"

				minscreenx = 0
				maxscreenx = screenx//2
				'''top left hand side of screen'''
				minscreeny = 0
				maxscreeny = screeny//2

				cursorx = minscreenx + 5
				cursory = minscreeny + 5
				subt = 0

				draw = False

				xfactor = 256//self.x
				yfactor = 256//self.y
				zfactor = 256//self.z

				for i in range(0,self.y):
					for j in range(0,self.z):
						for k in range(0,self.x):
							temp = self.access_id(k,i,j)
							if temp.id in palatte:
								if palatte[temp.id][0] == -1:
									draw = False
								else:
									draw = True
								color1 = color_rgb(palatte[temp.id][1],palatte[temp.id][2],palatte[temp.id][3])
								radius = palatte[temp.id][0]
							else:
								color1 = color_rgb(255,0,255)
								radius = 1.2
								print("cell " + str(k) + " /" + str(i) + " /" + str(j) + " is of a non-palatte id " + str(temp))
								draw = True

							if draw:
								circle = Circle(Point(cursorx,cursory),radius)
								circle.setFill(color1)
								if routline:
									circle.setOutline(color_rgb(k*xfactor,i*yfactor,j*zfactor))
								circle.draw(window)

							cursory+=spacing
							subt+=spacing
						cursory-=subt
						subt=0
						cursorx+=spacing
					cursorx = minscreenx + 5
					cursory = minscreeny + 5

				#view 2 from positive x face "right side"

				minscreenx = screenx//2
				maxscreenx = screenx
				'''top right hand side of screen'''
				minscreeny = 0
				maxscreeny = screeny//2

				cursory = minscreeny + 5
				cursorx = minscreenx + 5

				for i in range(0,self.z):
					for j in range(0,self.y):
						jtemp = j
						j = self.y - j -1
						for k in range(0,self.x):
							temp = self.access_id(k,j,i)
							if temp.id in palatte:
								if palatte[temp.id][0] == -1:
									draw = False
								else:
									draw = True
								color1 = color_rgb(palatte[temp.id][1],palatte[temp.id][2],palatte[temp.id][3])
								radius = palatte[temp.id][0]
							else:
								color1 = color_rgb(255,0,255)
								radius = 1.2
								print("cell " + str(k) + " /" + str(j) + " /" + str(i) + " is of a non-palatte id " + str(temp))
								draw = True

							if draw:
								circle = Circle(Point(cursorx,cursory),radius)
								circle.setFill(color1)
								if routline:
									circle.setOutline(color_rgb(k*xfactor,i*yfactor,j*zfactor))
								circle.draw(window)

							cursory+=spacing
							subt+=spacing
						cursory-=subt
						subt=0
						cursorx+=spacing
						j = jtemp
					cursorx = minscreenx + 5
					cursory = minscreeny + 5


				#view 3 from positive z face "front"

				minscreenx = 0
				maxscreenx = screenx//2
				'''bottom left hand side of screen'''
				minscreeny = screeny//2
				maxscreeny = screeny

				cursorx = minscreenx + 5
				cursory = minscreeny + 5

				for i in range(0,self.x):
					for j in range(0,self.z):
						for k in range(0,self.y):
							ktemp = k
							k = self.y - k - 1
							temp = self.access_id(i,k,j)
							if temp.id in palatte:
								if palatte[temp.id][0] == -1:
									draw = False
								else:
									draw = True
								color1 = color_rgb(palatte[temp.id][1],palatte[temp.id][2],palatte[temp.id][3])
								radius = palatte[temp.id][0]
							else:
								color1 = color_rgb(255,0,255)
								radius = 1.2
								print("cell " + str(k) + " /" + str(i) + " /" + str(j) + " is of a non-palatte id " + str(temp))
								draw = True

							if draw:
								circle = Circle(Point(cursorx,cursory),radius)
								circle.setFill(color1)
								if routline:
									circle.setOutline(color_rgb(k*xfactor,i*yfactor,j*zfactor))
								circle.draw(window)

							cursory+=spacing
							subt+=spacing
							k = ktemp
						cursory-=subt
						subt=0
						cursorx+=spacing
					cursorx = minscreenx + 5
					cursory = minscreeny + 5


				#perspective

				minscreenx = screenx//2
				maxscreenx = screenx
				'''bottom right hand side of screen'''
				minscreeny = screeny//2
				maxscreeny = screeny

				cursory = (minscreeny + maxscreeny) //2
				cursorx = (minscreenx + maxscreenx) //2

				for x in range(0,self.x):
					for y in range(0,self.y):
						for z in range(0,self.z):
							temp = self.access_id(x,y,z)

							#color1 = color_rgb(random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
							if temp.id in palatte:
								if palatte[temp.id][0] == -1:
									draw = False
								else:
									draw = True
								color1 = color_rgb(palatte[temp.id][1],palatte[temp.id][2],palatte[temp.id][3])
								radius = palatte[temp.id][0]
							else:
								color1 = color_rgb(255,0,255)
								radius = 2
								print("cell " + str(x) + " /" + str(y) + " /" + str(z) + " is of a non-palatte id " + str(temp))
								draw = True

							if draw:
								circle = Circle(Point(cursorx,cursory),radius)
								circle.setFill(color1)
								if routline:
									circle.setOutline(color_rgb(x*xfactor,y*yfactor,z*zfactor))
								circle.draw(window)

							cursorx-=spacing
							cursory+=spacing
						cursorx+=spacing*self.z
						cursory-=spacing*(self.z + 1)
					cursorx+=spacing
					cursory+=spacing*(self.y+1)


			print("output done")
			return window
		elif output_type == "window":
			print("outputting to " + output_type + ".......")
			if window is None or (screenx and screeny == 0):
				print("no window recieved")
			else: #main display
				cursorx = screenx//2 + 1
				cursory = screeny//3 + 1 #improvement over last version -- centers the block

				#color1 = fillcolor #color_rgb(random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))

				xfactor = 256//self.x
				yfactor = 256//self.y
				zfactor = 256//self.z

				for x in range(0,self.x):
					for y in range(0,self.y):
						for z in range(0,self.z):
							temp = self.access_id(x,y,z)

							#color1 = color_rgb(random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
							if temp.id in palatte:
								if palatte[temp.id][0] == -1:
									draw = False
								else:
									draw = True
								color1 = color_rgb(palatte[temp.id][1],palatte[temp.id][2],palatte[temp.id][3])
								radius = palatte[temp.id][0]
							else:
								color1 = color_rgb(255,0,255)
								radius = 2
								print("cell " + str(x) + " /" + str(y) + " /" + str(z) + " is of a non-palatte id " + str(temp))
								draw = True

							if draw:
								circle = Circle(Point(cursorx,cursory),radius)
								circle.setFill(color1)
								if routline:
									circle.setOutline(color_rgb(x*xfactor,y*yfactor,z*zfactor))
								circle.draw(window)

							cursorx-=spacing
							cursory+=spacing
						cursorx+=spacing*self.z
						cursory-=spacing*(self.z + 1)
					cursorx+=spacing
					cursory+=spacing*(self.y+1)

			print("output done")
			return window
		elif output_type == "console":
			print("outputting to " + output_type + ".......")
			for i in range(0,self.x):
				for j in range(0,self.y):
					temp = []
					for k in range(0,self.z):
						temp = temp + [self.access(i,j,k).id]
					print temp
				print ("\n")
			print("output done")
		elif output_type == "file": #prompt for a filename and then output
			print("outputting to " + output_type + ".......")
			f = open(fsave,'w')
			f.write(str(self.x) + "\n")
			f.write(str(self.y) + "\n")
			f.write(str(self.z) + "\n")
			for i in self.space:
				f.write(str(i.id) + "\n")
			print("output done")
		else:
			print("no valid output type specified")

	def access_id(self,ax,ay,az):
		return self.space[ax*self.y*self.z + ay*self.z + az]

	def setcell(self,sx,sy,sz,id):
		self.space[sx*self.y*self.z + sy*self.z + sz].id = id


def exitfunc(): #runs when sys.exit() is called
 	print "exiting"

sys.exitfunc = exitfunc

def main(seed,x,y,z,screenx,screeny,output,randmin,randmax,spacing,color,fread,fsave,rcolor):
	t0 = time.time()
	v = VoxelBlock(x,y,z,seed,randmin,randmax,fread) #dimensions[][][], seed, randmin, randmax	

	if seed == 99:
		print("initialization took 		" + str(time.time()-t0) + " seconds -- this result relied upon user input and means little")
	else:
		print("initialization took 		" + str(time.time()-t0) + " seconds")

	if seed == -1 and fread is not None:
		print("voxels loaded from file: 	" + str(len(v.space)))# + " " + str(v.x*v.y*v.z)) # - the same thing
	else:
		print("voxels generated:			" + str(len(v.space)))

	print("current block is (x*y*z)    " + str(v.x) + " * " + str(v.y) + " * " + str(v.z))

	if output == "window" or "window especial":
		window = None
		t1 = time.time()
		window = v.output(output,fsave,window,screenx,screeny,spacing,color,rcolor)
		print("rendering total 			" + str(time.time()-t1) + " seconds")
		print("program total  				" + str(time.time()-t0) + " seconds")
		window.getMouse()
		window.close()
	else:
		v.output(output,fsave) #if console or file output is desired
		print("program total  				" + str(time.time()-t0) + " seconds")

	sys.exit(1)

"""intialization function"""
def go(): #this could be grouped into an initialization object with labels for each course of action
	x = 16
	y = 9	#[x.y.z] = [16.9.25] for enterprise
	z = 25

	fread = 'enterprise.dat'
	fsave = 'data.dat'

	seed = -1	  #selected seed - options
					#(-1)- read from file - requires fread to be set to the filename
					#   0- set all cells to zero
					#	1-	hull
					#	2- hull + edges + corners (zeroes inside)
					#	3- hull + edges + corners (random inside)
					#	4- sphere located at center
					#	5- sphere located at center, random values in other cells
					#	6- just random between randmin and randmax for every cell
					#  99- manual entry of values



	screenx = 1200 #screen dimensions
	screeny = 800

	randmin = 0 #these set the random extents for the seeding in __init__ for the voxelblock
	randmax = 49	

	output =  "window especial" #options: "console", "file", "window", or "window especial"

	spacing = 4

	fillcolor = "black"
	rainbowoutline = False

	main(seed,x,y,z,screenx,screeny,output,randmin,randmax,spacing,fillcolor,fread,fsave,rainbowoutline)

go()