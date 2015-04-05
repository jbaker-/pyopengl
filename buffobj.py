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

uniform float u_top;
uniform float u_bottom;
uniform float u_near;
uniform float u_far;
uniform float u_right;
uniform float u_left;
uniform float u_scale;

uniform vec3 u_campos;
uniform vec3 u_camdir;

varying vec4 v_color;

void main()
{

	float e1_1 = (2.0*u_near)/(u_right-u_left);
	float e2_2 = (2.0*u_near)/(u_top-u_bottom);
	float e1_3 = (u_right+u_left)/(u_right-u_left);
	float e2_3 = (u_top+u_bottom)/(u_top-u_bottom);
	float e3_3 = (-1.0*(u_far+u_near))/(u_far-u_near);
	float e3_4 = (-2.0*u_far*u_near)/(u_far-u_near);

	vec4 col1 = vec4( e1_1,  0.0,  0.0,  0.0);
	vec4 col2 = vec4(  0.0, e2_2,  0.0,  0.0);
	vec4 col3 = vec4( e1_3, e2_3, e3_3, -1.0);
	vec4 col4 = vec4(  0.0,  0.0, e3_4,  0.0);

	mat4 proje = mat4(col1,col2,col3,col4);

	col1 = vec4(1,0,0,0);
	col2 = vec4(0,cos(u_xrotate),sin(u_xrotate),0);
	col3 = vec4(0,-sin(u_xrotate),cos(u_xrotate),0);
	col4 = vec4(0,0,0,1);

	mat4 rx = mat4(col1,col2,col3,col4);

	col1 = vec4(1,0,0,0);
	col2 = vec4(0,cos(u_camdir.x),sin(u_camdir.x),0);
	col3 = vec4(0,-sin(u_camdir.x),cos(u_camdir.x),0);
	col4 = vec4(0,0,0,1);
	
	mat4 crx = mat4(col1,col2,col3,col4);

	col1 = vec4(cos(u_yrotate),0,-sin(u_yrotate),0);
	col2 = vec4(0,1,0,0);
	col3 = vec4(sin(u_yrotate),0,cos(u_yrotate),0);
	col4 = vec4(0,0,0,1);
	
	mat4 ry = mat4(col1,col2,col3,col4);

	col1 = vec4(cos(u_camdir.y),0,-sin(u_camdir.y),0);
	col2 = vec4(0,1,0,0);
	col3 = vec4(sin(u_camdir.y),0,cos(u_camdir.y),0);
	col4 = vec4(0,0,0,1);

	mat4 cry = mat4(col1,col2,col3,col4);

	col1 = vec4(cos(u_zrotate),sin(u_zrotate),0,0);
	col2 = vec4(-sin(u_zrotate),cos(u_zrotate),0,0);
	col3 = vec4(0,0,1,0);
	col4 = vec4(0,0,0,1);

	mat4 rz = mat4(col1,col2,col3,col4);

	col1 = vec4(cos(u_camdir.z),sin(u_camdir.z),0,0);
	col2 = vec4(-sin(u_camdir.z),cos(u_camdir.z),0,0);
	col3 = vec4(0,0,1,0);
	col4 = vec4(0,0,0,1);

	mat4 crz = mat4(col1,col2,col3,col4);

	mat4 r  =   rx * ry  * rz;
	mat4 cr =  crx * cry * crz;

	col1 = vec4(1,0,0,0);
	col2 = vec4(0,1,0,0);
	col3 = vec4(0,0,1,0);
	col4 = vec4(u_xtranslate,u_ytranslate,u_ztranslate,1);

	mat4 tr = mat4(col1,col2,col3,col4);

	col1 = vec4(u_scale,0,0,0);
	col2 = vec4(0,u_scale,0,0);
	col3 = vec4(0,0,u_scale,0);
	col4 = vec4(0,0,0,1);

	mat4 sc = mat4(col1,col2,col3,col4);

	mat4 mv = tr*sc*r;

    gl_Position = mv*vec4(a_position,1.0);  //cr*(proje*(tr*sc*r*vec4(a_position,1.0) - vec4(u_campos,0.0)));
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
	def __init__(self,num_points,points,colors,rendertype=GL.GL_POINTS,vertexShaderProgram=standardVertexShaderProgram,fragmentShaderProgram=standardFragShaderProgram):
		self.xtranslate = 0.0
		self.ytranslate = 0.0
		self.ztranslate = 0.0
		self.xrotate = 0.0
		self.yrotate = 0.0
		self.zrotate = 0.0
		self.scale = 1.0

		self.rendertype = rendertype

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

		self.data = np.zeros(num_points, dtype = [("a_position", np.float32, 3),("a_color",    np.float32, 4)])
		
		self.data['a_color'] = colors
		self.data['a_position'] = points

		GL.glBindBuffer(GL.GL_ARRAY_BUFFER,self.gpubuffer)
		GL.glBufferData(GL.GL_ARRAY_BUFFER,self.data.nbytes,self.data,GL.GL_DYNAMIC_DRAW)

		self.stride = self.data.strides[0]

		self.posoffset = ctypes.c_void_p(0)
		self.positionloc = GL.glGetAttribLocation(self.shaderProgram,"a_position")
		GL.glEnableVertexAttribArray(self.positionloc)
		GL.glVertexAttribPointer(self.positionloc, 3, GL.GL_FLOAT, False, self.stride, self.posoffset)

		self.coloffset = ctypes.c_void_p(self.data.dtype["a_position"].itemsize)
		self.colorloc = GL.glGetAttribLocation(self.shaderProgram,"a_color")
		GL.glEnableVertexAttribArray(self.colorloc)
		GL.glVertexAttribPointer(self.colorloc,4,GL.GL_FLOAT, False, self.stride, self.coloffset)

		#UNIFORM VARIABLES

		self.xtranslateloc = GL.glGetUniformLocation(self.shaderProgram, "u_xtranslate")
		self.ytranslateloc = GL.glGetUniformLocation(self.shaderProgram, "u_ytranslate")
		self.ztranslateloc = GL.glGetUniformLocation(self.shaderProgram, "u_ztranslate")
		self.xrotateloc = GL.glGetUniformLocation(self.shaderProgram, "u_xrotate")
		self.yrotateloc = GL.glGetUniformLocation(self.shaderProgram, "u_yrotate")
		self.zrotateloc = GL.glGetUniformLocation(self.shaderProgram, "u_zrotate")
		self.scaleloc = GL.glGetUniformLocation(self.shaderProgram, "u_scale")

		self.camposloc = GL.glGetUniformLocation(self.shaderProgram, "u_campos")
		self.camdirloc = GL.glGetUniformLocation(self.shaderProgram, "u_camdir")

		self.toploc = GL.glGetUniformLocation(self.shaderProgram, "u_top")
		self.bottomloc = GL.glGetUniformLocation(self.shaderProgram, "u_bottom")
		self.farloc = GL.glGetUniformLocation(self.shaderProgram, "u_far")
		self.nearloc = GL.glGetUniformLocation(self.shaderProgram, "u_near")
		self.rightloc = GL.glGetUniformLocation(self.shaderProgram, "u_right")
		self.leftloc = GL.glGetUniformLocation(self.shaderProgram, "u_left")

		self.top =  1.0
		self.bottom = -1.0
		self.right = 1.0
		self.left = -1.0
		self.far = 5
		self.near = 0.001

		self.campos = [0,0,0]
		self.camdir = [0,0,0]


		self.update_display_mat_variables()
		self.update()

	def draw(self):


		GL.glUseProgram(self.shaderProgram)

		self.update()

		GL.glBindBuffer(GL.GL_ARRAY_BUFFER,self.gpubuffer)
		GL.glEnableVertexAttribArray(self.colorloc)
		GL.glVertexAttribPointer(self.colorloc,4,GL.GL_FLOAT, False, self.stride, self.coloffset)
		GL.glEnableVertexAttribArray(self.positionloc)
		GL.glVertexAttribPointer(self.positionloc, 3, GL.GL_FLOAT, False, self.stride, self.posoffset)

		if self.rendertype is not None:
			GL.glDrawArrays(self.rendertype, 0, len(self.data))

	def update(self):
		GL.glUniform1f(self.xtranslateloc,self.xtranslate)
		GL.glUniform1f(self.ytranslateloc,self.ytranslate)
		GL.glUniform1f(self.ztranslateloc,self.ztranslate)
		GL.glUniform1f(self.xrotateloc,self.xrotate)
		GL.glUniform1f(self.yrotateloc,self.yrotate)
		GL.glUniform1f(self.zrotateloc,self.zrotate)
		GL.glUniform1f(self.scaleloc,self.scale)
		self.update_display_mat_variables()

	def update_display_mat_variables(self):
		GL.glUniform1f(self.toploc,self.top)
		GL.glUniform1f(self.bottomloc,self.bottom)
		GL.glUniform1f(self.farloc,self.far)
		GL.glUniform1f(self.nearloc,self.near)
		GL.glUniform1f(self.rightloc,self.right)
		GL.glUniform1f(self.leftloc,self.left)
		GL.glUniform3f(self.camposloc,self.campos[0],self.campos[1],self.campos[2])
		GL.glUniform3f(self.camdirloc,self.camdir[0],self.camdir[1],self.camdir[2])

	def kill(self): #I dont know, its not really neccesary
		GL.glDisableVertexAttribArray(self.colorloc)
		GL.glDisableVertexAttribArray(self.positionloc)
		GL.glDisableVertexAttribArray(self.normloc)
		GL.glDeleteProgram(self.shaderProgram)
		GL.glDeleteShader(self.fragmentShader)
		GL.glDeleteShader(self.vertexShader)
		GL.glDeleteBuffers(1,[self.gpubuffer])
		GL.glDeleteVertexArrays(1,[self.gpubuffer])

		#GL.glDetachShader(self.shaderProgram,vertexShader)
		#GL.glDetachShader(self.shaderProgram,fragmentShader)
	
	def set_display_mat_variables(self,top,bottom,right,left,far,near):
		self.top = top
		self.bottom = bottom
		self.right = right
		self.left = left
		self.far = far
		self.near = near

	def set_rendertype(self,rendertype):
		self.rendertype = rendertype

	def set_translate(self,x,y,z):
		self.xtranslate = x
		self.ytranslate = y
		self.ztranslate = z
		self.update()

	def set_rotate(self,x,y,z):
		self.xrotate = x
		self.yrotate = y
		self.zrotate = z
		self.update()

	def set_scale(self,newscale):
		self.scale = newscale
		self.update()

