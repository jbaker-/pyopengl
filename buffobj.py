from voxutil import *

from OpenGL.GL import *
from numpy import *
import numpy as np
import OpenGL.GL as GL
import OpenGL.GLUT as glut

standardVertexShaderProgram = '''
attribute vec3 a_position;
attribute vec4 a_color;

uniform float u_xtranslate;
uniform float u_ytranslate;
uniform float u_ztranslate;
uniform float u_xrotate;
uniform float u_yrotate;
uniform float u_zrotate;

uniform float u_scale;

varying vec4 v_color;

void main()
{
	mat3 rx = mat3(1,			     0,					  0,
				   0, 	cos(u_xrotate),	 	-sin(u_xrotate),
				   0, 	sin(u_xrotate), 	 cos(u_xrotate));

	mat3 ry = mat3(cos(u_yrotate), 0.0,	     sin(u_yrotate),
				   			  0.0, 1.0,				 	0.0,
				  -sin(u_yrotate), 0.0,  	 cos(u_yrotate));

	mat3 rz = mat3(cos(u_zrotate),	-sin(u_zrotate),	0.0,
				   sin(u_zrotate),	 cos(u_zrotate),	0.0,
				   			  0.0,				0.0,	1.0);

	vec3 tx = vec3(u_xtranslate,0.0,0.0);
	vec3 ty = vec3(0.0,u_ytranslate,0.0);
	vec3 tz = vec3(0.0,0.0,u_ztranslate);

    gl_Position = vec4((rx*ry*rz*(a_position+tx+ty+tz)), 1.0);
    v_color = a_color;
}
'''

standardFragShaderProgram = '''
varying vec4 v_color;

void main()
{
    gl_FragColor = v_color;
}
'''

class buffobj:
	def __init__(self,points,colors,num_points,rendertype="points",vertexShaderProgram=None,fragmentShaderProgram=None):
		self.xtranslate = 0.0
		self.ytranslate = 0.0
		self.ztranslate = 0.0
		self.xrotate = 0.0
		self.yrotate = 0.0
		self.zrotate = 0.0
		self.scale = 1.0

		self.rendertype = rendertype

		if vertexShaderProgram == None:
			vertexShaderProgram = standardVertexShaderProgram

		if fragmentShaderProgram == None:
			fragmentShaderProgram = standardFragShaderProgram

		#DECLARE GPU BUFFER

		self.gpubuffer = GL.glGenBuffers(1)

		vertexShader = GL.glCreateShader(GL.GL_VERTEX_SHADER)
		GL.glShaderSource(vertexShader, vertexShaderProgram)
		GL.glCompileShader(vertexShader)

		fragmentShader = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)
		GL.glShaderSource(fragmentShader, fragmentShaderProgram)
		GL.glCompileShader(fragmentShader)

		self.shaderProgram = GL.glCreateProgram()
		GL.glAttachShader(self.shaderProgram, vertexShader)
		GL.glAttachShader(self.shaderProgram, fragmentShader)

		GL.glLinkProgram(self.shaderProgram)
		GL.glValidateProgram(self.shaderProgram)
		GL.glUseProgram(self.shaderProgram)

		GL.glDetachShader(self.shaderProgram,vertexShader)
		GL.glDetachShader(self.shaderProgram,fragmentShader)

		self.data = np.zeros(num_points, dtype = [("a_position", np.float32, 3),
												  ("a_color",    np.float32, 4)])

		self.data['a_color'] = colors
		self.data['a_position'] = points

		GL.glBindBuffer(GL.GL_ARRAY_BUFFER,self.gpubuffer)
		GL.glBufferData(GL.GL_ARRAY_BUFFER,self.data.nbytes,self.data,GL.GL_DYNAMIC_DRAW)

		self.stride = self.data.strides[0]

		self.posoffset = ctypes.c_void_p(0)
		self.positionloc = GL.glGetAttribLocation(self.shaderProgram,"a_position")
		GL.glEnableVertexAttribArray(self.positionloc)
		#GL.glBindBuffer(GL.GL_ARRAY_BUFFER,self.gpubuffer)
		GL.glVertexAttribPointer(self.positionloc, 3, GL.GL_FLOAT, False, self.stride, self.posoffset)

		self.coloffset = ctypes.c_void_p(self.data.dtype["a_position"].itemsize)
		self.colorloc = GL.glGetAttribLocation(self.shaderProgram,"a_color")
		GL.glEnableVertexAttribArray(self.colorloc)
		#GL.glBindBuffer(GL.GL_ARRAY_BUFFER,self.gpubuffer)
		GL.glVertexAttribPointer(self.colorloc,4,GL.GL_FLOAT, False, self.stride, self.coloffset)

		#UNIFORM VARIABLES

		self.xtranslateloc = GL.glGetUniformLocation(self.shaderProgram, "u_xtranslate")
		self.ytranslateloc = GL.glGetUniformLocation(self.shaderProgram, "u_ytranslate")
		self.ztranslateloc = GL.glGetUniformLocation(self.shaderProgram, "u_ztranslate")
		self.xrotateloc = GL.glGetUniformLocation(self.shaderProgram, "u_xrotate")
		self.yrotateloc = GL.glGetUniformLocation(self.shaderProgram, "u_yrotate")
		self.zrotateloc = GL.glGetUniformLocation(self.shaderProgram, "u_zrotate")
		self.scaleloc = GL.glGetUniformLocation(self.shaderProgram, "u_scale")

		self.update()

	def draw(self):

		'''
		GL.glEnableVertexAttribArray(self.colorloc)
		GL.glEnableVertexAttribArray(self.positionloc)
		GL.glBindBuffer(GL.GL_ARRAY_BUFFER,self.gpubuffer)
		GL.glVertexAttribPointer(self.colorloc,4,GL.GL_FLOAT, False, self.stride, self.coloffset)
		GL.glVertexAttribPointer(self.positionloc, 3, GL.GL_FLOAT, False, self.stride, self.posoffset)
		''' # I have no idea, it seems like 

		self.update()

		GL.glUseProgram(self.shaderProgram)

		if self.rendertype == "points":
			GL.glDrawArrays(GL.GL_POINTS, 0, len(self.data))
		elif self.rendertype == "lines":
			GL.glDrawArrays(GL.GL_LINES, 0, len(self.data))
		elif self.rendertype == "line_loop":
			GL.glDrawArrays(GL.GL_LINE_LOOP,0,len(self.data))
		elif self.rendertype == "triangles":
			GL.glDrawArrays(GL.GL_TRIANGLES,0,len(self.data))
		elif self.rendertype == "line_strip":
			GL.glDrawArrays(GL.GL_LINE_STRIP,0,len(self.data))

	def update(self):
		GL.glUniform1f(self.xtranslateloc,self.xtranslate)
		GL.glUniform1f(self.ytranslateloc,self.ytranslate)
		GL.glUniform1f(self.ztranslateloc,self.ztranslate)
		GL.glUniform1f(self.xrotateloc,self.xrotate)
		GL.glUniform1f(self.yrotateloc,self.yrotate)
		GL.glUniform1f(self.zrotateloc,self.zrotate)
		GL.glUniform1f(self.scaleloc,self.scale)


	def set_rendertype(self,rendertype):
		self.rendertype = rendertype

	def set_translate(self,x,y,z):
		self.xtranslate = x
		self.ytranslate = y
		self.ztranslate = z

	def set_rotate(self,x,y,z):
		self.xrotate = x
		self.yrotate = y
		self.zrotate = z

