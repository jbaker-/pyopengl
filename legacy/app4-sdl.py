from voxutil import *

import ctypes

import numpy as np

import sdl2
from OpenGL import GL

def run():
	if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
		print(sdl2.SDL_GetError())
		return

	window = sdl2.SDL_CreateWindow(
	b"Example 1", 
	sdl2.SDL_WINDOWPOS_UNDEFINED, sdl2.SDL_WINDOWPOS_UNDEFINED, 640, 480,
	sdl2.SDL_WINDOW_OPENGL)

	context = sdl2.SDL_GL_CreateContext(window)

	data = np.zeros(4, dtype = [("position", np.float32, 3),
								("color",    np.float32, 4)])

	data['color'] = [(1.0,0.0,0.0,1.0),(0.0,1.0,0.0,1.0),(0.0,0.0,1.0,1.0),(1.0,1.0,0.0,1.0)]
	data['position'] = [(-1.0,-1.0,0.0),(-1.0,1.0,0.0),(1.0,-1.0,0.0),(1.0,1.0,0.1)]

	# get Vertex Array Object name
	#vao = GL.glGenVertexArrays(1)
	# set this new VAO to the active one
	#GL.glBindVertexArray(vao)

	gpubuffer = GL.glGenBuffers(1)

	GL.glBindBuffer(GL.GL_ARRAY_BUFFER,gpubuffer)

	GL.glBufferData(GL.GL_ARRAY_BUFFER,data.nbytes,data,GL.GL_DYNAMIC_DRAW)

	# vertex shader and compilation
	vertexShaderProgram = """
		#version 130
		attribute vec3 position;
		attribute vec4 color;
		varying vec4 vcolor;

		void main() {
			gl_Position = vec4(position, 1.0);
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
	positionAttrib = GL.glGetAttribLocation(shaderProgram, b"position")
	print(positionAttrib)
	GL.glEnableVertexAttribArray(positionAttrib)
	GL.glVertexAttribPointer(positionAttrib, 3, GL.GL_FLOAT, False, 0, ctypes.c_voidp(0))

	colorAttrib = GL.glGetAttribLocation(shaderProgram, b"color")
	GL.glEnableVertexAttribArray(colorAttrib)
	GL.glVertexAttribPointer(colorAttrib , 3, GL.GL_FLOAT, False, 0, ctypes.c_voidp(0))

	# do the actual drawing
	GL.glClearColor(0.0, 0.5, 0.0, 1.0)
	GL.glClear(GL.GL_COLOR_BUFFER_BIT)
	GL.glDrawArrays(GL.GL_TRIANGLES, 0, len(data))#None - verticies

	# show the back buffer
	sdl2.SDL_GL_SwapWindow(window)

	# wait for somebody to close the window
	event = sdl2.SDL_Event()
	while sdl2.SDL_WaitEvent(ctypes.byref(event)):
		if event.type == sdl2.SDL_QUIT:
			break

	# cleanup
	GL.glDeleteProgram(shaderProgram)
	sdl2.SDL_GL_DeleteContext(context)
	sdl2.SDL_Quit()


if __name__ == "__main__":
    run()