from buffobj import *

'''

FIRST DRAFT - 3/28/2015

This assumes you have both: 

	buffobj.py (for gpu based buffobj's - none declared by default but its included) and 
	voxutil.py (for some random code stuff - distance formula, clamp, some projection stuff I haven't quite figured out yet) 

in the same directory as this script. If you don't, it's not likely to run.

This code sets up the most basic of the essential glut callbacks and starts glutMainLoop(). Notes have been added as to where
to add what - points, animation, colors - this makes a really nice template for any project that 
needs to have some objects displayed on the screen with minimal work.

The user can choose whether to use glutTimerFunc (will run after /at least/ the amount of time you specify) or 
glutIdleFunc (will run whenever glut is not busy - runs faster on faster machines) to change things over time.

'''

windowtitle = "GLUT Display"
windowxdim = 800
windowydim = 800

def exitfunc(): #runs when sys.exit() is called

 	print "exiting"

sys.exitfunc = exitfunc

def display():

	GL.glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	#DRAW CALLS HERE

	glut.glutSwapBuffers()
	glut.glutPostRedisplay()

def keyboard(key, x, y):

	if key == '\033': #the escape key
		sys.exit( )
	elif key == 'a' or key == 'A':
		pass
	elif key == 'b' or key == 'B':
		pass
	elif key == 'c' or key == 'C':
		pass
	elif key == 'd' or key == 'D':
		pass
	elif key == 'e' or key == 'E':
		pass
	elif key == 'f' or key == 'F':
		pass
	elif key == 'g' or key == 'G':
		pass
	elif key == 'h' or key == 'H':
		pass
	elif key == 'i' or key == 'I':
		pass
	elif key == 'j' or key == 'J':
		pass
	elif key == 'k' or key == 'K':
		pass
	elif key == 'l' or key == 'L':
		pass
	elif key == 'm' or key == 'M':
		pass
	elif key == 'n' or key == 'N':
		pass
	elif key == 'o' or key == 'O':
		pass
	elif key == 'p' or key == 'P':
		pass
	elif key == 'q' or key == 'Q':
		pass
	elif key == 'r' or key == 'R':
		pass
	elif key == 's' or key == 'S':
		pass
	elif key == 't' or key == 'T':
		pass
	elif key == 'u' or key == 'U':
		pass
	elif key == 'v' or key == 'V':
		pass
	elif key == 'w' or key == 'W':
		pass
	elif key == 'x' or key == 'X':
		pass
	elif key == 'y' or key == 'Y':
		pass
	elif key == 'z' or key == 'Z':
		pass
	else:
		print("invalid go home")

	#OTHER KEYS TO CONTROL THE PROGRAM

	glut.glutPostRedisplay()

def reshape(width,height):

	GL.glViewport(0, 0, width, height)
	GL.glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glut.glutPostRedisplay()
'''
def timer(fps):

	#ANY ANIMATION GOES HERE

	glut.glutTimerFunc(1000/fps, timer, fps)
'''

global outputfpsprofiling
outputfpsprofiling = False

global framecount
framecount = 0

global tprev
global tcurr

tprev = time.time()
tcurr = time.time()

def idle():

	global framecount
	global tcurr
	global tprev

	framecount += 1

	tprev = tcurr
	tcurr = time.time()
	
	if outputfpsprofiling:
		tframe = tcurr - tprev
		print(str(framecount) + "  which took " + str(tframe) + " seconds -- avg fps: " + str(1/tframe))

	glut.glutPostRedisplay()

glut.glutInit()
glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA | glut.GLUT_DEPTH | glut.GLUT_MULTISAMPLE)

GL.glEnable(GL.GL_DEPTH_TEST)
GL.glEnable(GL.GL_BLEND)
GL.glBlendFunc(GL.GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
GL.glClearColor(0.0,0.0,0.0,1.0)

glut.glutCreateWindow(windowtitle)
glut.glutReshapeWindow(windowxdim,windowydim)
glut.glutReshapeFunc(reshape)
glut.glutDisplayFunc(display)
glut.glutKeyboardFunc(keyboard)
#glut.glutTimerFunc(1000/60, timer, 60)
glut.glutIdleFunc(idle)
#glut.glutFullScreen() #does work -- 3/23

'''

GENERATE POINTS AND DECLARE BUFFER OBJECTS HERE 
THIS MAY PROVE HELPFUL - FROM BUFFOBJ.PY'S BUFFOBJ CLASS:

	def __init__(self,points,colors,num_points,rendertype="points",vertexShaderProgram=None,fragmentShaderProgram=None)

	+ - points - ((0.0,0.0,0.0),...) uses vec3 of floats
	+ - colors - ((0.0,0.0,0.0,1.0),...) uses vec4 of floats

	+ - num_points is a number that should match the length of both colors and points (e.g. len(colors) == len(points) == num_points)

	+ - rendertype is not needed (default argument) but can be used to switch to triangles or lines

	+ - The shader variables will accept a custom vertex shader or fragment shader as an argument or use the standard ones if there
		is not one specified when the object is declared.

	Basically, d = buffobj(points1,colors1,num_points1) is a valid call to the constructor, as long as you've made sure that 
	the lengths match.

'''

glut.glutMainLoop()