from voxutil import *

from OpenGL.GL import *
import numpy as np
import OpenGL.GL as GL
import OpenGL.GLUT as glut


data = np.zeros(325, dtype = [("position", np.float32, 3),
							("color",    np.float32, 4)])

def display():
	global pointsize
	GL.glEnable(GL_DEPTH_TEST)
	GL.glPointSize(pointsize)
	GL.glClearColor(0.0,0.0,0.0,1.0)
	GL.glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	GL.glDrawArrays(GL.GL_POINTS, 0, len(data))
	glut.glutSwapBuffers()


def reshape(width,height):
	GL.glViewport(0, 0, width, height)

def keyboard( key, x, y ):
	global timer
	global pointsize
	global loc
	if key == '\033':
		sys.exit( )
	elif key == 'k':
		timer = timer - 0.5
		GL.glUniform1f(loc,timer)
	elif key == 'i':
		timer = timer + 0.5
		GL.glUniform1f(loc,timer)
	elif key == 'e':
		pointsize = pointsize + 0.5
	elif key == 'd':
		pointsize = pointsize - 0.5
		
	glut.glutPostRedisplay()



glut.glutInit()

glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA)
glut.glutCreateWindow('Display')
glut.glutReshapeWindow(800,800)
glut.glutReshapeFunc(reshape)
glut.glutDisplayFunc(display)
glut.glutKeyboardFunc(keyboard)
#glut.glutIdleFunc(timer)
GL.glEnable(GL.GL_DEPTH_TEST)
#glut.glutFullScreen() #does work -- 3/23

#data['color'] = [(1.0,0.0,0.0,1.0),(0.0,1.0,0.0,1.0),(0.0,0.0,1.0,1.0),(1.0,1.0,0.0,1.0)]
#data['position'] = [(-1.0,-1.0,0.0),(-1.0,1.0,0.0),(1.0,-1.0,0.0),(1.0,1.0,0.1)]

#manipulate points here

points = []
colors = []

for i in range(0,325):
	points.append((.03*enterprise[i][0],.03*enterprise[i][1],.03*enterprise[i][2]))
	if enterprise[i][3] == 27:
		colors.append((0.3,0.3,0.3,1.0))
	else:
		colors.append((0.9,0.0,0.0,1.0))

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
	uniform float timer;
	void main() {

		mat3 rotation = mat3(
			vec3( cos(timer), sin(timer), 0.0),
			vec3(-sin(timer), cos(timer), sin(timer)),
			vec3( 0.0, cos(timer), 1.0)
		);

		gl_Position = vec4(rotation*position, 1.0);
		vcolor = color;
	}"""
vertexShader = GL.glCreateShader(GL.GL_VERTEX_SHADER)
GL.glShaderSource(vertexShader, vertexShaderProgram)
GL.glCompileShader(vertexShader)




# fragment shader and compilation
fragmentShaderProgram = """
	#version 130
	varying vec4 vcolor;
	void main() {
		gl_FragColor = vcolor;
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

# specify the layout of our vertex data
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

global loc 
loc = GL.glGetUniformLocation(shaderProgram, "timer")
global timer 
timer = 0.0
GL.glUniform1f(loc, timer)

global pointsize
pointsize = 1.0


glut.glutMainLoop()