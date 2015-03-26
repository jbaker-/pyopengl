from voxutil import *

from OpenGL.GL import *
from numpy import *
import numpy as np
import OpenGL.GL as GL
import OpenGL.GLUT as glut

usersetx = 40
usersety = 40
usersetz = 40

num_points = 6 * usersetx * usersety * usersetz
print num_points

usersetx_np = np.linspace(-0.5, 0.5, usersetx, True, dtype=np.float32) # numpy function linspace(start,stop,steps,endpoints,retstep=False,dtype=None) - using float32 for opengl
usersety_np = np.linspace(-0.5, 0.5, usersety, True, dtype=np.float32)
usersetz_np = np.linspace(-0.5, 0.5, usersetz, True, dtype=np.float32)


data = np.zeros(num_points, dtype = [("position", np.float32, 3),
							("color",    np.float32, 4)])

def display():
	global pointsize
	GL.glPointSize(pointsize)
	GL.glClearColor(0.0,0.0,0.0,1.0)
	GL.glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	GL.glDrawArrays(GL.GL_POINTS, 0, len(data))
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
	elif key == 'q': # larger points
		pointsize +=0.3
	elif key == 'a': # smaller points
		pointsize -=0.3
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
	elif key == 'g': # print translations and rotations
		animationscale += 0.1
		animationscale = clamp(animationscale,0.0,3.0)
	elif key == 'p':
		animationscale -= 0.1
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

	clock += 1000/fps
	print clock

	xrotate += 0.01
	yrotate -= 0.01
	zrotate -= 0.01

   	GL.glUniform1f(xrotateloc,xrotate)
   	GL.glUniform1f(yrotateloc,yrotate)
   	GL.glUniform1f(zrotateloc,zrotate)

	glut.glutTimerFunc(1000/fps, timer, fps)
	glut.glutPostRedisplay()



glut.glutInit()

glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA | glut.GLUT_DEPTH | glut.GLUT_MULTISAMPLE)
GL.glEnable(GL.GL_DEPTH_TEST)
glut.glutCreateWindow('Display')
glut.glutReshapeWindow(800,800)
glut.glutReshapeFunc(reshape)
glut.glutDisplayFunc(display)
glut.glutKeyboardFunc(keyboard)
glut.glutTimerFunc(1000/60, timer, 60)
#glut.glutFullScreen() #does work -- 3/23

points = []
colors = []

#c = arange(24).reshape(2,3,4) 

x_values = array(array(usersetx_np))
y_values = array(array(usersety_np))
z_values = array(array(usersetz_np))

for x in range(0,usersetx):
	for y in range(0,usersety):
		for z in range(0,usersetz):

			points.append((x_values[x]+.01,y_values[y],z_values[z]))
			points.append((x_values[x]-.01,y_values[y],z_values[z]))
			points.append((x_values[x],y_values[y]+.01,z_values[z]))
			points.append((x_values[x],y_values[y]-.01,z_values[z]))
			points.append((x_values[x],y_values[y],z_values[z]+.01))
			points.append((x_values[x],y_values[y],z_values[z]-.01))

			for i in range(0,6):
				colors.append((0.5,0.5,0.5,0.1))
				#colors.append((random.random(),random.random(),random.random(),1))



data['color'] = colors
data['position'] = points

gpubuffer = GL.glGenBuffers(1)

GL.glBindBuffer(GL.GL_ARRAY_BUFFER,gpubuffer)

GL.glBufferData(GL.GL_ARRAY_BUFFER,data.nbytes,data,GL.GL_DYNAMIC_DRAW)

# vertex shader and compilation
vertexShaderProgram = """
	#version 130
	attribute vec3 position;
	attribute vec4 color;
	varying vec4 vcolor;
	varying vec3 vpos;

	uniform float xtranslate;
	uniform float ytranslate;
	uniform float ztranslate;
	uniform float xrotate;
	uniform float yrotate;
	uniform float zrotate;

	uniform float scale;


	mat4 rotationMatrix(vec3 axis, float angle)
	{
		//axis = normalize(axis);//not needed
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

		gl_Position = xrotation*yrotation*zrotation*scalematrix*vec4(position + vec3(xtranslate,ytranslate,ztranslate), 1.0);
		vcolor = color;
		vpos = position;

	}"""
vertexShader = GL.glCreateShader(GL.GL_VERTEX_SHADER)
GL.glShaderSource(vertexShader, vertexShaderProgram)
GL.glCompileShader(vertexShader)




# fragment shader and compilation
fragmentShaderProgram = """
	#version 130
	varying vec4 vcolor;
	varying vec3 vpos;
	void main() {
		gl_FragColor = vec4((vcolor.x-vpos.x),(vcolor.y-vpos.y),(vcolor.z-vpos.z),1.0);
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
loc = GL.glGetAttribLocation(shaderProgram,"position")
GL.glEnableVertexAttribArray(loc)
GL.glBindBuffer(GL.GL_ARRAY_BUFFER,gpubuffer)
GL.glVertexAttribPointer(loc, 3, GL.GL_FLOAT, False, stride, offset)

offset = ctypes.c_void_p(data.dtype["position"].itemsize)
loc = GL.glGetAttribLocation(shaderProgram,"color")
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