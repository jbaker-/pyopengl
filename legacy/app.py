import sys
import os
import random, time
from graphics import *
import math

def dist(x1,y1,z1,x2,y2,z2):
	a = (x1,y1,z1) #data point 1
	b = (x2,y2,z2) #data point 2
	return math.fabs(math.sqrt(sum( (a - b)**2 for a, b in zip(a, b))))

class Voxel:
	def __init__(self,_x,_y,_z, seed = 0):
		self.x = _x #coordinates
		self.y = _y
		self.z = _z
		self.id = seed

class voxelBlock:

	def __init__(self, _x, _y, _z): 
		self.x = _x #dimensions
		self.y = _y
		self.z = _z

		self.space = [] #holds voxels
		self.seedValue = 0 #holds a seed value

	def seed(self,s):

		t2 = time.time()

		if s == -99:
			pass
		elif s == -10: #random sphere
			for i in range(0,self.x):
				for j in range(0,self.y): 
					for k in range(0,self.z):
						if dist(i,j,k,45,16,45) < 16 and not random.random()*dist(i,j,k,40,40,35) < 16:
							self.seedValue = random.randrange(-5000,10)
						else:
							self.seedValue = 1
						self.space.append(Voxel(i,j,k,self.seedValue))
		elif s == -9: #hollow sphere
			for i in range(0,self.x):
				for j in range(0,self.y): 
					for k in range(0,self.z):
						if (dist(i,j,k,5,16,20) < 16 or dist(i,j,k,22,0,0) < 16) and not(dist(i,j,k,16,16,16) < 16):
							self.seedValue = 3
						else:
							self.seedValue = random.randrange(-5000,10)
						self.space.append(Voxel(i,j,k,self.seedValue))
		elif s == -8: #sphere
			for i in range(0,self.x):
				for j in range(0,self.y): 
					for k in range(0,self.z):
						if dist(i,j,k,5,16,20) < 30:
							self.seedValue = 3
						else:
							self.seedValue = random.randrange(-5000,10)
						self.space.append(Voxel(i,j,k,self.seedValue))
		elif s == -7: #random wip
			for i in range(0,self.x):
				for j in range(0,self.y): 
					for k in range(0,self.z):
						self.seedValue = random.randrange(-5000,10)
						self.space.append(Voxel(i,j,k,self.seedValue))
		elif s == -6: #hull + corners + edges + randomly seeded interior
			for i in range(0,self.x):
				for j in range(0,self.y): 
					for k in range(0,self.z):

						if i == 0 or j == 0 or k == 0 or i == self.x-1 or j == self.y-1 or k == self.z-1:
							self.seedValue = 1
							if (i == 0 and j == 0) or (j == 0 and k == 0) or (i == 0 and k == 0) or (i == self.x-1 and j == self.y-1) or (j == self.y-1 and k == self.z-1) or (i == self.x-1 and k == self.z-1) or (i == 0 and k == self.z-1) or (i == 0 and j == self.y-1) or (j == self.y-1 and k == 0) or (j == 0 and k == self.z-1) or (i == self.x-1 and k == 0) or (i == self.x-1 and j == 0):
								self.seedValue = 4
							if (i == 0 and j == 0 and k == 0) or (i == 0 and j == 0 and k == self.z-1) or (i == 0 and j == self.y-1 and k == 0) or (i == 0 and j == self.y-1 and k == self.z-1) or (i == self.x-1 and j == 0 and k == 0) or (i == self.x-1 and j == 0 and k == self.z-1) or (i == self.x-1 and j == self.y-1 and k == 0) or(i == self.x-1 and j == self.y-1 and k == self.z-1):
								self.seedValue = 7
						else:
							self.seedValue =  random.randrange(15,8192)

						self.space.append(Voxel(i,j,k,self.seedValue))
		elif s == -5: #hull + corners + edges
			for i in range(0,self.x):
				for j in range(0,self.y): 
					for k in range(0,self.z):

						if i == 0 or j == 0 or k == 0 or i == self.x-1 or j == self.y-1 or k == self.z-1:
							self.seedValue = 2
						if (i == 0 and j == 0) or (j == 0 and k == 0) or (i == 0 and k == 0) or (i == self.x-1 and j == self.y-1) or (j == self.y-1 and k == self.z-1) or (i == self.x-1 and k == self.z-1) or (i == 0 and k == self.z-1) or (i == 0 and j == self.y-1) or (j == self.y-1 and k == 0) or (j == 0 and k == self.z-1) or (i == self.x-1 and k == 0) or (i == self.x-1 and j == 0):
							self.seedValue = 6
						if (i == 0 and j == 0 and k == 0) or (i == 0 and j == 0 and k == self.z-1) or (i == 0 and j == self.y-1 and k == 0) or (i == 0 and j == self.y-1 and k == self.z-1) or (i == self.x-1 and j == 0 and k == 0) or (i == self.x-1 and j == 0 and k == self.z-1) or (i == self.x-1 and j == self.y-1 and k == 0) or(i == self.x-1 and j == self.y-1 and k == self.z-1):
							self.seedValue = 10

						self.space.append(Voxel(i,j,k,self.seedValue))
		elif s == -4: #hull + corners
			for i in range(0,self.x):
				for j in range(0,self.y): 
					for k in range(0,self.z):

						'''
						if i == 0 or j == 0 or k == 0 or i == self.x-1 or j == self.y-1 or k == self.z-1:
							self.seedValue = 9
						else:
							self.seedValue = 0
						'''
						if i == 0 or j == 0 or k == 0 or i == self.x-1 or j == self.y-1 or k == self.z-1:
							self.seedValue = 2
						if (i == 0 and j == 0 and k == 0) or (i == 0 and j == 0 and k == self.z-1) or (i == 0 and j == self.y-1 and k == 0) or (i == 0 and j == self.y-1 and k == self.z-1) or (i == self.x-1 and j == 0 and k == 0) or (i == self.x-1 and j == 0 and k == self.z-1) or (i == self.x-1 and j == self.y-1 and k == 0) or(i == self.x-1 and j == self.y-1 and k == self.z-1):
							self.seedValue = 9


						self.space.append(Voxel(i,j,k,self.seedValue))
		elif s == -3: #corners
			for i in range(0,self.x):
				for j in range(0,self.y): 
					for k in range(0,self.z):

						'''
						if i == 0 or j == 0 or k == 0 or i == self.x-1 or j == self.y-1 or k == self.z-1:
							self.seedValue = 9
						else:
							self.seedValue = 0
						'''
						if (i == 0 and j == 0 and k == 0) or (i == 0 and j == 0 and k == self.z-1) or (i == 0 and j == self.y-1 and k == 0) or (i == 0 and j == self.y-1 and k == self.z-1) or (i == self.x-1 and j == 0 and k == 0) or (i == self.x-1 and j == 0 and k == self.z-1) or (i == self.x-1 and j == self.y-1 and k == 0) or(i == self.x-1 and j == self.y-1 and k == self.z-1):
							self.seedValue = 9
						else:
							self.seedValue = 0

						self.space.append(Voxel(i,j,k,self.seedValue))
		elif s == -2: #sizing based on (cell_x*cell_y*cell_z)/(self.x*self.y*self.z) and variants
			for i in range(0,self.x):
				for j in range(0,self.y): 
					for k in range(0,self.z):		
						self.seedValue = 3-(20*i*j*k)//(self.x*self.y*self.z)
						self.space.append(Voxel(i,j,k,self.seedValue))
		elif s == -1: #random seed
			for i in range(0,self.x):
				for j in range(0,self.y): 
					for k in range(0,self.z):					
						self.seedValue = random.randrange(-22,11)
						self.space.append(Voxel(i,j,k,self.seedValue))
		elif s == 0: #seed with zeroes
			for i in range(0,self.x):
				for j in range(0,self.y): 
					for k in range(0,self.z):
						self.seedValue = 0
						self.space.append(Voxel(i,j,k,self.seedValue))
		elif s == 1: #set only the edgemost cells (hull)
			for i in range(0,self.x):
				for j in range(0,self.y): 
					for k in range(0,self.z):
						if i == 0 or j == 0 or k == 0 or i == self.x-1 or j == self.y-1 or k == self.z-1:
							self.seedValue = 9
						else:
							self.seedValue = 0
						self.space.append(Voxel(i,j,k,self.seedValue))
		elif s == 2: #modulo coloring - of the form (cell_x*cell_y*cell_z) % [a constant]
			for i in range(0,self.x):
				for j in range(0,self.y): 
					for k in range(0,self.z):
						self.seedValue = (i*j*k) % 8
						self.space.append(Voxel(i,j,k,self.seedValue))


		print("seeding took   " + str(time.time()-t2) + " seconds")


	def access(self,ax,ay,az):
		return self.space[ax*self.y*self.z + ay*self.z + az]

	def window_display(self,win,xdim,ydim,corneratback,bgdots=0,colorscheme=0):

		t1 = time.time()

		spacer = 4 #defines the amount of space between each point on the screen

		cursorx = xdim//2 + 1
		cursory = ydim//2 + 1 

		if bgdots == 1:
			for x in range(self.x): #make background dots (this is dumb and also takes forever)
				for y in range(self.y):
					for z in range(self.z):
						circle = Point(cursorx, cursory)
						circle.draw(win)
						cursorx-=spacer
						cursory+=spacer
					cursorx+=spacer*self.z
					cursory-=spacer*(self.z + 1)
				cursorx+=spacer
				cursory+=spacer*(self.y+1)

		cursorx = xdim//2 + 1 #reset cursor to middle of the screen
		cursory = ydim//2 + 1

		if corneratback == 0:
			for x in range(0,self.x):
				for y in range(0,self.y):
					for z in range(0,self.z):
						temp = self.access(x,y,z)

						if colorscheme == 1:
							if temp.id > 350:
								current_color = "red4"
								radius = 0
								draw = False
							elif temp.id > 300:
								current_color = "red"
								radius = 7
								draw = True
							elif temp.id > 250:
								current_color = "orange"
								radius = 7
								draw = True
							elif temp.id > 200:
								current_color = "yellow"
								radius = 6
								draw = True
							elif temp.id > 150:
								current_color = "green"
								radius = 5
								draw = True
							elif temp.id > 100:
								current_color = "blue"
								radius = 4
								draw = True
							elif temp.id > 50:
								current_color = "purple"
								radius = 3
								draw = True
							elif temp.id > 10:
								current_color = "indigo"
								radius = 0
								draw = True
							else:
								current_color = color_rgb(15,15,15)
								radius = temp.id
								draw = False

						elif colorscheme == 0:
							factorx = 256 // self.x
							factory = 256 // self.y
							factorz = 256 // self.z

							current_color = color_rgb(temp.x*factorx, temp.y*factory, temp.z*factorz)

							if temp.id > 350:
								radius = 0
								draw = False
							elif temp.id > 250:
								radius = 7
								draw = True
							elif temp.id > 200:
								radius = 6
								draw = True
							elif temp.id > 150:
								radius = 5
								draw = True
							elif temp.id > 100:
								radius = 4
								draw = True
							elif temp.id > 50:
								radius = 3
								draw = True
							elif temp.id > 10:
								radius = 0
								draw = True
							else:
								radius = temp.id
								draw = True

						elif colorscheme == -1:

							if temp.id > 9:
								current_color = "red"
								draw = True
							elif temp.id > 6:
								current_color = "orange"
								draw = True
							elif temp.id > 3:
								current_color = "yellow"
								draw = True
							elif temp.id > 0:
								current_color = "green"
								draw = True
							else:
								current_color = "black"
								draw = False

						elif colorscheme == -2:

							if temp.id > 0:
								draw = True
							else:
								draw = False

							if temp.y % 2 == 0:
								current_color = "black"
							else:
								current_color = "white"


						if temp.id < 10:
							circle = Circle(Point(cursorx,cursory), temp.id)
						elif temp.id >= 10:
							circle = Circle(Point(cursorx,cursory), radius)
						else:
							circle = Circle(Point(cursorx,cursory), 0)


						circle.setFill(current_color)
						if temp.id > 0 and draw == True:
							circle.draw(win)

						cursorx-=spacer
						cursory+=spacer
					cursorx+=spacer*self.z
					cursory-=spacer*(self.z + 1)
				cursorx+=spacer
				cursory+=spacer*(self.y+1)
		elif corneratback == 1:
			for x in range(-1*(self.x),0):
				for y in range(-1*(self.y),0):
					for z in range(-1*(self.z),0):

						print(str(x)+str(y)+str(z))
						temp = self.access(x,y,z)
						circle = Circle(Point(cursorx,cursory), temp.id)
						#circle.setFill(color_rgb(x*4,y*4,z*4))
						#r = random.randrange(256)
						#b = random.randrange(256)
						#g = random.randrange(256)
						#color = color_rgb(r, g, b)
						#circle.setOutline(color_rgb(b,r,r))
						if colorscheme == 1:
							if temp.id > 350:
								current_color = "red4"
								radius = 0
							elif temp.id > 300:
								current_color = "red"
								radius = 7
							elif temp.id > 250:
								current_color = "orange"
								radius = 7
							elif temp.id > 200:
								current_color = "yellow"
								radius = 6
							elif temp.id > 150:
								current_color = "green"
								radius = 5
							elif temp.id > 100:
								current_color = "blue"
								radius = 4
							elif temp.id > 50:
								current_color = "purple"
								radius = 3
							elif temp.id > 10:
								current_color = "indigo"
								radius = 0
							else:
								current_color = color_rgb(15,15,15)
								radius = temp.id

						elif colorscheme == 0:
							factorx = 256 // self.x
							factory = 256 // self.y
							factorz = 256 // self.z

							current_color = color_rgb(temp.x*factorx, temp.y*factory, temp.z*factorz)

							if temp.id > 350:
								radius = 0
							elif temp.id > 250:
								radius = 7
							elif temp.id > 200:
								radius = 6
							elif temp.id > 150:
								radius = 5
							elif temp.id > 100:
								radius = 4
							elif temp.id > 50:
								radius = 3
							elif temp.id > 10:
								radius = 0
							else:
								radius = temp.id

						elif colorscheme == -1:

							if temp.id > 9:
								current_color = "red"
							elif temp.id > 6:
								current_color = "orange"
							elif temp.id > 3:
								current_color = "yellow"
							elif temp.id > 0:
								current_color = "green"
							else:
								current_color = "black"

						circle.setFill(current_color)
						if temp.id > 0:
							circle.draw(win)

						cursorx-=spacer
						cursory+=spacer
					cursorx+=spacer*self.z
					cursory-=spacer*(self.z + 1)
				cursorx+=spacer
				cursory+=spacer*(self.y+1)#this is going to take more work - theres wierdness happening
		elif corneratback == 2:
			pass
		print("rendering took " + str(time.time()-t1) + " seconds")



	def console_display(self):
		for i in range(0,self.x):
			for j in range(0,self.y):
				temp = []
				for k in range(0,self.z):
					temp = temp + [self.access(i,j,k).id]
				print temp
			print ("\n")

'''
	def exitfunc(): #runs when sys.exit() is called
 	print "exiting"

	sys.exitfunc = exitfunc
'''

#code starts here
t0 = time.time()

v = voxelBlock(64,64,64)
v.seed(-9)
#v.console_display()

def main(v,t0):

	xdim = 1500
	ydim = 870

	win = GraphWin("Display", xdim,ydim)

	v.window_display(win,xdim,ydim,0,0,0)

	print("program total  " + str(time.time()-t0) + " seconds")

	win.getMouse() # Pause to view result
	win.close()    # Close window when done
	#sys.exit(1)

main(v,t0)


'''
 for i in range(5000):
   r = random.randrange(256)
   b = random.randrange(256)
   g = random.randrange(256)
   color = color_rgb(r, g, b) 
   #color = color_rgb(r//(1/.0988), g//(1/.0094), b//(1/0.08111)) 
   #custom weighting using floor division(floor() wasnt available and this is quick) -- jb
        
   radius = random.randrange(4, 33)
   x = random.randrange(5, 295) 
   y = random.randrange(5, 295) 

   x = (x / 10) * 10
   y = (y / 10) * 10
   
   circle = Circle(Point(x,y), radius)
   circle.setFill(color)
   circle.draw(win)
   #print i
   #time.sleep(.05)
'''
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
