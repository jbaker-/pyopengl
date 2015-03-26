from voxutil import *

from OpenGL.GL import *
from numpy import *
import numpy as np
import OpenGL.GL as GL
import OpenGL.GLUT as glut

usersetx = 40
usersety = 40
usersetz = 40

spacer = 2

seed = 4

minextent = -0.5
maxextent =  0.5

windowtitle = "GLUT Window"

#pointstyle = "six points per voxel"
pointstyle = "single point per voxel"

global rendertype
rendertype = "points"
#rendertype = "lines"

if pointstyle == "single point per voxel":
	num_points = usersetx * usersety * usersetz
elif pointstyle == "six points per voxel":
	num_points = 6 * usersetx * usersety * usersetz

print num_points

usersetx_np = np.linspace(minextent, maxextent, usersetx, True, True, dtype=np.float32) # numpy function linspace(start,stop,steps,endpoints,retstep=False,dtype=None) - using float32 for opengl
usersety_np = np.linspace(minextent, maxextent, usersety, True, True, dtype=np.float32)
usersetz_np = np.linspace(minextent, maxextent, usersetz, True, True, dtype=np.float32)


data = np.zeros(num_points, dtype = [("a_position", np.float32, 3),
							("a_color",    np.float32, 4)])

def display():
	global rendertype

	GL.glClearColor(0.0,0.0,0.0,1.0)
	GL.glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	if rendertype == "points":
		GL.glDrawArrays(GL.GL_POINTS, 0, len(data))
	elif rendertype == "lines":
		GL.glDrawArrays(GL.GL_LINES, 0, len(data))
	elif rendertype == "line_loop":
		GL.glDrawArrays(GL.GL_LINE_LOOP,0,len(data))
	elif rendertype == "triangles":
		GL.glDrawArrays(GL.GL_TRIANGLES,0,len(data))
	glut.glutSwapBuffers()


def reshape(width,height):
	GL.glViewport(0, 0, width, height)

def keyboard( key, x, y ):


	global xtranslate 	#allows for translation on all three axes
	global xtranslateloc
	global ytranslate
	global ytranslateloc
	global ztranslate
	global ztranslateloc

	global xrotate 		#allows for rotation about three cardinal axes
	global xrotateloc
	global yrotate
	global yrotateloc
	global zrotate
	global zrotateloc

	global scale
	global scaleloc

	global pointsize
	global animationscale


	if key == '\033':
		sys.exit( )
	elif key == 'q': # larger points/lines
		pointsize +=0.3
		pointsize = clamp(pointsize,0.0,5.0)
		GL.glPointSize(pointsize)
		GL.glLineWidth(pointsize)
	elif key == 'a': # smaller points/lines
		pointsize -=0.3
		pointsize = clamp(pointsize,0.0,5.0)
		GL.glPointSize(pointsize)
		GL.glLineWidth(pointsize)
	elif key == 'w': # increase scale
		scale += 0.1
		GL.glUniform1f(scaleloc,scale)
		print scale
	elif key == 's': # decrease scale
		scale -= 0.1
		GL.glUniform1f(scaleloc,scale)
		print scale
	elif key == 'h': # move to positive x
		xtranslate += .01
		GL.glUniform1f(xtranslateloc,xtranslate)
	elif key == 'f': # move to negative x
		xtranslate -= .01
		GL.glUniform1f(xtranslateloc,xtranslate)
	elif key == 'y': # move to positive y
		ytranslate += .01
		GL.glUniform1f(ytranslateloc,ytranslate)
	elif key == 'v': # move to negative y
		ytranslate -= .01
		GL.glUniform1f(ytranslateloc,ytranslate)
	elif key == 'b': # move to positive z
		ztranslate += .01
		GL.glUniform1f(ztranslateloc,ztranslate)
	elif key == 't': # move to negative z
		ztranslate -= .01
		GL.glUniform1f(ztranslateloc,ztranslate)
	elif key == 'j': # rotate, positive around x axis
		xrotate += 0.1
		GL.glUniform1f(xrotateloc,xrotate)
	elif key == 'd': # rotate, negative around x axis
		xrotate -= 0.1
		GL.glUniform1f(xrotateloc,xrotate)
	elif key == 'u': # rotate, positive around y axis
		yrotate += 0.1
		GL.glUniform1f(yrotateloc,yrotate)
	elif key == 'c': # rotate, negative around y axis
		yrotate -= 0.1
		GL.glUniform1f(yrotateloc,yrotate)
	elif key == 'n': # rotate, positive around z axis
		zrotate += 0.1
		GL.glUniform1f(zrotateloc,zrotate)
	elif key == 'r': # rotate, negative around z axis
		zrotate -= 0.1
		GL.glUniform1f(zrotateloc,zrotate)
	elif key == 'g': # reset
		animationscale = 0.0
		xtranslate = 0.0
		xrotate = 0.0
		ytranslate = 0.0
		yrotate = 0.0
		ztranslate = 0.0
		zrotate = 0.0
		scale = 1.0

		GL.glUniform1f(xtranslateloc,xtranslate)
		GL.glUniform1f(xrotateloc,xrotate)
		GL.glUniform1f(ytranslateloc,ytranslate)
		GL.glUniform1f(yrotateloc, yrotate)
		GL.glUniform1f(ztranslateloc,ztranslate)
		GL.glUniform1f(zrotateloc,zrotate)
		GL.glUniform1f(scaleloc,scale)

	elif key == 'p':
		animationscale += 0.001
		animationscale = clamp(animationscale,0.0,3.0)

		
	glut.glutPostRedisplay()

def timer(fps):
	global clock
	global animationscale

	global scale
	global scaleloc

	global xrotate
	global xrotateloc
	global yrotate
	global yrotateloc
	global zrotate
	global zrotateloc

	xrotate += animationscale
	yrotate -= animationscale
	#zrotate -= animationscale

   	GL.glUniform1f(xrotateloc,xrotate)
   	GL.glUniform1f(yrotateloc,yrotate)
   	GL.glUniform1f(zrotateloc,zrotate)

	glut.glutTimerFunc(1000/fps, timer, fps)
	glut.glutPostRedisplay()



glut.glutInit()

glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA | glut.GLUT_DEPTH | glut.GLUT_MULTISAMPLE)
GL.glEnable(GL.GL_DEPTH_TEST)
GL.glEnable(GL.GL_BLEND)
GL.glBlendFunc(GL.GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glut.glutCreateWindow(windowtitle)
glut.glutReshapeWindow(800,800)
glut.glutReshapeFunc(reshape)
glut.glutDisplayFunc(display)
glut.glutKeyboardFunc(keyboard)
glut.glutTimerFunc(1000/60, timer, 60)
#glut.glutFullScreen() #does work -- 3/23


#Prep for seeding - get min and max values

points = []
colors = []

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

for x in range(0,usersetx):
	for y in range(0,usersety):
		for z in range(0,usersetz):

			col = (0.5,0.5,0.5,1.0)

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
				ballrad = 0.4
				if dist(cur_x,cur_y,cur_z,0,0,0) < ballrad:
					col = (clamp(0.5*random.rand(),0.0,0.3),0.9*random.rand(),0.7*random.rand(),1.0)
				else:
					col = (0.0,0.0,0.0,0.0)

				if (cur_x == x_min and cur_y == y_min) or (cur_y == y_min and cur_z == z_min) or (cur_x == x_min and cur_z == z_min) or (cur_x == x_max and cur_y == y_max) or (cur_y == y_max and cur_z == z_max) or (cur_x == x_max and cur_z == z_max) or (cur_x == x_min and cur_z == z_max) or (cur_x == x_min and cur_y == y_max) or (cur_y == y_max and cur_z == z_min) or (cur_y == y_min and cur_z == z_max) or (cur_x == x_max and cur_z == z_min) or (cur_x == x_max and cur_y == y_min):
					col = (1.0,1.0,1.0,1.0) # edge color

			if pointstyle == "six points per voxel":

				points.append((x_values[x]+(x_step/spacer),y_values[y],z_values[z]))
				points.append((x_values[x]-(x_step/spacer),y_values[y],z_values[z]))
				points.append((x_values[x],y_values[y]+(y_step/spacer),z_values[z]))
				points.append((x_values[x],y_values[y]-(y_step/spacer),z_values[z]))
				points.append((x_values[x],y_values[y],z_values[z]+(z_step/spacer)))
				points.append((x_values[x],y_values[y],z_values[z]-(z_step/spacer)))

				for i in range(0,6):
					colors.append(col)
					#colors.append((random.random(),random.random(),random.random(),1))

			elif pointstyle == "single point per voxel":

				points.append((x_values[x],y_values[y],z_values[z]))
				colors.append(col)





data['a_color'] = colors
data['a_position'] = points

gpubuffer = GL.glGenBuffers(1)

GL.glBindBuffer(GL.GL_ARRAY_BUFFER,gpubuffer)

GL.glBufferData(GL.GL_ARRAY_BUFFER,data.nbytes,data,GL.GL_DYNAMIC_DRAW)

# vertex shader and compilation
vertexShaderProgram = """
	#version 130
	attribute vec3 a_position;
	attribute vec4 a_color;
	varying vec4 v_color;
	varying vec3 v_pos;

	uniform float xtranslate;
	uniform float ytranslate;
	uniform float ztranslate;
	uniform float xrotate;
	uniform float yrotate;
	uniform float zrotate;

	uniform float scale;


	mat4 rotationMatrix(vec3 axis, float angle)
	{
		axis = normalize(axis);
		float s = sin(angle);
		float c = cos(angle);
		float oc = 1.0 - c;
		return mat4(oc * axis.x * axis.x + c, oc * axis.x * axis.y - axis.z * s, oc * axis.z * axis.x + axis.y * s, 0.0,
			oc * axis.x * axis.y + axis.z * s, oc * axis.y * axis.y + c, oc * axis.y * axis.z - axis.x * s, 0.0,
			oc * axis.z * axis.x - axis.y * s, oc * axis.y * axis.z + axis.x * s, oc * axis.z * axis.z + c, 0.0,
			0.0, 0.0, 0.0, 1.0);
	} 

	void main() {

		mat4 xrotation = rotationMatrix(vec3(1,0,0),xrotate);
		mat4 yrotation = rotationMatrix(vec3(0,1,0),yrotate);
		mat4 zrotation = rotationMatrix(vec3(0,0,1),zrotate);

		mat4 scalematrix = mat4(scale,0,0,0,
								0,scale,0,0,
								0,0,scale,0,
								0,0,0,1.0);

		gl_Position = xrotation*yrotation*zrotation*scalematrix*vec4(a_position + vec3(xtranslate,ytranslate,ztranslate), 1.0);
		v_color = a_color;
		v_pos = a_position;

	}"""
vertexShader = GL.glCreateShader(GL.GL_VERTEX_SHADER)
GL.glShaderSource(vertexShader, vertexShaderProgram)
GL.glCompileShader(vertexShader)




# fragment shader and compilation
fragmentShaderProgram = """
	#version 130
	varying vec4 v_color;
	varying vec3 v_pos;
	void main() {
		//gl_FragColor = vec4(clamp((v_color.x-v_pos.x),0.0,1.0),clamp((v_color.y-v_pos.y),0.0,1.0),clamp((v_color.z-v_pos.z),0.0,1.0),v_color.w);
		gl_FragColor = v_color;
	}"""
fragmentShader = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)
GL.glShaderSource(fragmentShader, fragmentShaderProgram)
GL.glCompileShader(fragmentShader)




# shader program 
shaderProgram = GL.glCreateProgram()
GL.glAttachShader(shaderProgram, vertexShader)
GL.glAttachShader(shaderProgram, fragmentShader)

# link the program
GL.glLinkProgram(shaderProgram)

# validate the program
GL.glValidateProgram(shaderProgram)

# activate the program
GL.glUseProgram(shaderProgram)

GL.glDetachShader(shaderProgram,vertexShader)
GL.glDetachShader(shaderProgram,fragmentShader)

# specify the layout of vertex data
stride = data.strides[0]

offset = ctypes.c_void_p(0)
loc = GL.glGetAttribLocation(shaderProgram,"a_position")
GL.glEnableVertexAttribArray(loc)
GL.glBindBuffer(GL.GL_ARRAY_BUFFER,gpubuffer)
GL.glVertexAttribPointer(loc, 3, GL.GL_FLOAT, False, stride, offset)

offset = ctypes.c_void_p(data.dtype["a_position"].itemsize)
loc = GL.glGetAttribLocation(shaderProgram,"a_color")
GL.glEnableVertexAttribArray(loc)
GL.glBindBuffer(GL.GL_ARRAY_BUFFER,gpubuffer)
GL.glVertexAttribPointer(loc,4,GL.GL_FLOAT, False, stride, offset)

#SHADER VARIABLES - manipulated in keyboardfunc
#also for timerfunc
global clock
clock = 0.0

global xtranslate
global xtranslateloc
global ytranslate
global ytranslateloc
global ztranslate
global ztranslateloc

xtranslate = 0.0
ytranslate = 0.0
ztranslate = 0.0
xtranslateloc = GL.glGetUniformLocation(shaderProgram, "xtranslate")
ytranslateloc = GL.glGetUniformLocation(shaderProgram, "ytranslate")
ztranslateloc = GL.glGetUniformLocation(shaderProgram, "ztranslate")
GL.glUniform1f(xtranslateloc,xtranslate)
GL.glUniform1f(ytranslateloc,ytranslate)
GL.glUniform1f(ztranslateloc,ztranslate)

global xrotate
global xrotateloc
global yrotate
global yrotateloc
global zrotate
global zrotateloc

xrotate = 0.0
yrotate = 0.0
zrotate = 0.0
xrotateloc = GL.glGetUniformLocation(shaderProgram, "xrotate")
yrotateloc = GL.glGetUniformLocation(shaderProgram, "yrotate")
zrotateloc = GL.glGetUniformLocation(shaderProgram, "zrotate")
GL.glUniform1f(xrotateloc,xrotate)
GL.glUniform1f(yrotateloc,yrotate)
GL.glUniform1f(zrotateloc,zrotate)

global scale
global scaleloc
scale = 1.0
scaleloc = GL.glGetUniformLocation(shaderProgram, "scale")
GL.glUniform1f(scaleloc,scale)


global pointsize
global animationscale

pointsize = 1.0
animationscale = 0.0


glut.glutMainLoop()