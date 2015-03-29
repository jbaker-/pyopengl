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

    gl_Position = (proje*cr*(r*tr*sc*(vec4(a_position,1.0))))-vec4(u_campos,0.0);
    v_color = a_color;
}
'''


#if this gets used, itll need to be updated
standardVertexShaderProgramWithNormals = '''
attribute vec3 a_position;
attribute vec4 a_color;
attribute vec3 a_normal;

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
uniform float u_scale;

varying vec4 v_color;

void main()
{

	float f = 1/tan(u_fovy/2);

	mat4 proj = ((f/u_aspect),	0.0,	0.0,	0.0,
				  0.0,			  f,	0.0,	0.0,
				  0.0,			0.0,	((u_far+u_near)/(u_near-u_far)),	((2*u_near*u_far)/(u_near-u_far)),
				  0.0,			0.0,   -1.0,	0.0);


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

    gl_Position = proj*vec4((rx*ry*rz*(a_position+tx+ty+tz)), 1.0);
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
	def __init__(self,num_points,points,colors,normals=None,rendertype=GL.GL_POINTS,vertexShaderProgram=None,fragmentShaderProgram=None):
		self.xtranslate = 0.0
		self.ytranslate = 0.0
		self.ztranslate = 0.0
		self.xrotate = 0.0
		self.yrotate = 0.0
		self.zrotate = 0.0
		self.scale = 1.0

		self.rendertype = rendertype

		if vertexShaderProgram == None and normals is None:
			vertexShaderProgram = standardVertexShaderProgram
		elif vertexShaderProgram == None and normals is not None:
			vertexShaderProgram = standardVertexShaderProgramWithNormals

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

		#GL.glDetachShader(self.shaderProgram,vertexShader)
		#GL.glDetachShader(self.shaderProgram,fragmentShader)

		self.hasnormals = False

		if normals is None:
			self.data = np.zeros(num_points, dtype = [("a_position", np.float32, 3),("a_color",    np.float32, 4)])
		else:
			self.data = np.zeros(num_points, dtype = [("a_position", np.float32, 3),("a_color",    np.float32, 4),("a_normal",   np.float32, 3)])
			self.data['a_normal'] = normals
			self.hasnormals = True


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

		if self.hasnormals:
			self.normoffset = ctypes.c_void_p(self.data.dtype["a_position"].itemsize+self.data.dtype["a_color"].itemsize)
			self.normloc = GL.glGetAttribLocation(self.shaderProgram,"a_normal")
			GL.glEnableVertexAttribArray(self.normloc)
			GL.glVertexAttribPointer(self.normloc,3,GL.GL_FLOAT, False, self.stride, self.normoffset)

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

		self.update()

		GL.glBindBuffer(GL.GL_ARRAY_BUFFER,self.gpubuffer)
		GL.glEnableVertexAttribArray(self.colorloc)
		GL.glVertexAttribPointer(self.colorloc,4,GL.GL_FLOAT, False, self.stride, self.coloffset)
		GL.glEnableVertexAttribArray(self.positionloc)
		GL.glVertexAttribPointer(self.positionloc, 3, GL.GL_FLOAT, False, self.stride, self.posoffset)
		if self.hasnormals:
			GL.glEnableVertexAttribArray(self.normloc)
			GL.glVertexAttribPointer(self.normloc,3,GL.GL_FLOAT, False, self.stride, self.normoffset)

		GL.glUseProgram(self.shaderProgram)

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

	def kill(self):
		GL.glDisableVertexAttribArray(self.colorloc)
		GL.glDisableVertexAttribArray(self.positionloc)
		GL.glDisableVertexAttribArray(self.normloc)
		GL.glDeleteProgram(self.shaderProgram)
		GL.glDeleteShader(self.fragmentShader)
		GL.glDeleteShader(self.vertexShader)
		GL.glDeleteBuffers(1,[self.gpubuffer])
		GL.glDeleteVertexArrays(1,[self.gpubuffer])
	
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

