from voxutil import *

from OpenGL.GL import *
from numpy import *
import numpy as np
import OpenGL.GL as GL
import OpenGL.GLUT as glut

standardVertexShader = '''
attribute vec3 a_position;
attribute vec4 a_color;
void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
    v_color = a_color;
}
'''

standardFragShader = '''
varying vec4 v_color;

void main()
{
    gl_FragColor = v_color;
}
'''

class buffobj:
	def __init__(self,vertexshader,fragmentshader,points,colors):
		self.xtranslate = 0.0
		self.ytranslate = 0.0
		self.ztranslate = 0.0
		self.xrotate = 0.0
		self.yrotate = 0.0
		self.zrotate = 0.0

		self.gpubuffer = GL.glGenBuffers(1)

		GL.glBindBuffer(GL.GL_ARRAY_BUFFER,self.gpubuffer)

		GL.glBufferData(GL.GL_ARRAY_BUFFER,data.nbytes,data,GL.GL_DYNAMIC_DRAW)

	def set_translate(self,x,y,z):
		self.xtranslate = x
		self.ytranslate = y
		self.ztranslate = z

	def set_rotate(self,x,y,z):
		self.xrotate = x
		self.yrotate = y
		self.zrotate = z

