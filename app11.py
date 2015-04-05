from buffobj import *
from pointgenerator import *

windowtitle = "GLUT Display"
windowxdim = 800
windowydim = 800

global index
index = 0

global scale
global xrotate
global yrotate
global zrotate
global xtranslate
global ytranslate
global ztranslate
global allmodels
global pointsize

scale = 1.0
xrotate = 0.0
yrotate = 0.0
zrotate = 0.0
xtranslate = 0.0
ytranslate = 0.0
ztranslate = 0.0
allmodels = []
pointsize = 1.0

def exitfunc():

	global t0
	global frametimes
	fsum = 0.0
	fnum = 0.0

	for i in frametimes:
		fsum += i
		fnum += 1

	print("average fps was: " + str(1/(fsum/fnum)) + " over " + str(fsum) + " seconds")

#--------------------------------------------------------------------------------------
#   _ sets up the above function to run when sys.exit() is called
# / 
#v

sys.exitfunc = exitfunc

#--------------------------------------------------------------------------------------
#FPS Profiling stuff - frametimes is an array of the amounts of time it took to render
#each individual frame - its global because in the exit function, the average fps is
#calcluated and output to the command line
#--------------------------------------------------------------------------------------
global output_FPS_Profiling
output_FPS_Profiling = False

global framecount
framecount = 0

global tprev
global tcurr

global frametimes
frametimes = []

tprev = time.time()
tcurr = time.time()
#--------------------------------------------------------------------------------------


def display():

	GL.glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	global framecount
	global tcurr
	global tprev

	framecount += 1

	tprev = tcurr
	tcurr = time.time()
	tframe = tcurr - tprev
	frametimes.append(tframe)
	
	if output_FPS_Profiling:
		print(str(framecount) + "  which took " + str(tframe) + " seconds -- avg fps: " + str(1/tframe))

	for i in range(0,len(allmodels)):
		allmodels[i].draw()
		
	glut.glutSwapBuffers()
	glut.glutPostRedisplay()

def keyboard(key, x, y):

	global index

	global scale
	global xrotate
	global yrotate
	global zrotate
	global xtranslate
	global ytranslate
	global ztranslate
	global allmodels
	global pointsize

	if key == '\033': #the escape key
		sys.exit( )
	elif key == 'a' or key == 'A':
		xtranslate -= 0.01
	elif key == 'b' or key == 'B':
		pass
	elif key == 'c' or key == 'C':
		pass
	elif key == 'd' or key == 'D':
		xtranslate += 0.01
	elif key == 'e' or key == 'E':
		ztranslate -= 0.01
	elif key == 'f' or key == 'F':
		pass
	elif key == 'g' or key == 'G':
		pointsize -= 0.1
	elif key == 'h' or key == 'H':
		scale -= 0.01
	elif key == 'i' or key == 'I':
		xrotate += 0.01
	elif key == 'j' or key == 'J':
		yrotate += 0.01
	elif key == 'k' or key == 'K':
		xrotate -= 0.01
	elif key == 'l' or key == 'L':
		yrotate -= 0.01
	elif key == 'm' or key == 'M':
		pass
	elif key == 'n' or key == 'N':
		pass
	elif key == 'o' or key == 'O':
		zrotate -= 0.01
	elif key == 'p' or key == 'P':
		pass
	elif key == 'q' or key == 'Q':
		ztranslate += 0.01
	elif key == 'r' or key == 'R':
		pass
	elif key == 's' or key == 'S':
		ytranslate -= 0.01
	elif key == 't' or key == 'T':
		pointsize += 0.1
	elif key == 'u' or key == 'U':
		zrotate += 0.01
	elif key == 'v' or key == 'V':
		pass
	elif key == 'w' or key == 'W':
		ytranslate += 0.01
	elif key == 'x' or key == 'X':
		index += 1
		index = clamp(index,0,len(allmodels)-1)
	elif key == 'y' or key == 'Y':
		scale += 0.01
	elif key == 'z' or key == 'Z':
		index -= 1
		index = clamp(index,0,len(allmodels)-1)
	else:
		print("invalid go home")

	allmodels[index].set_translate(xtranslate,ytranslate,ztranslate)
	allmodels[index].set_rotate(xrotate,yrotate,zrotate)
	allmodels[index].set_scale(scale)
	allmodels[index].update()

	GL.glLineWidth(pointsize)
	GL.glPointSize(pointsize)


	'''
	for i in allmodels:
		i.update()
	'''

	glut.glutPostRedisplay()

def reshape(width,height):

	GL.glViewport(0, 0, width, height)
	GL.glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glut.glutPostRedisplay()

def timer(fps):
	glut.glutPostRedisplay()

def idle():
	glut.glutPostRedisplay()



#--------------------------------------------------------------------------------------
#GLUT/OpenGL context intialization
#--------------------------------------------------------------------------------------

glut.glutInit()
glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA | glut.GLUT_DEPTH | glut.GLUT_MULTISAMPLE)

glut.glutCreateWindow(windowtitle)
glut.glutReshapeWindow(windowxdim,windowydim)
glut.glutReshapeFunc(reshape)
glut.glutDisplayFunc(display)
glut.glutKeyboardFunc(keyboard)
glut.glutIdleFunc(idle)
glut.glutTimerFunc(1000/60, timer, 60)
#glut.glutFullScreen() #does work -- 3/23

GL.glEnable(GL.GL_DEPTH_TEST)
GL.glEnable(GL.GL_BLEND)
GL.glBlendFunc(GL.GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glEnable(GL.GL_POINT_SMOOTH)
GL.glClearColor(0.0,0.0,0.0,1.0)

#--------------------------------------------------------------------------------------
#Generation of points and declaration of buffer(s)
#--------------------------------------------------------------------------------------

p = pointgenerator()
p.gen_cube(6,6,6)

num_buffers = 10

print("rendering "+str(num_buffers*p.num_points)+" points in "+str(num_buffers)+" buffers")

for i in range(0,num_buffers):
	allmodels.append(buffobj(p.num_points,p.points,p.colors))
	allmodels[len(allmodels)-1].rendertype = GL.GL_POINTS

#--------------------------------------------------------------------------------------
glut.glutMainLoop()