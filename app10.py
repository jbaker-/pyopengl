from buffobj import *
from pointgenerator import *

windowtitle = "GLUT Display"
windowxdim = 800
windowydim = 800

allmodels = []

global camposition
global camdirection
global sc
camposition = [0.0,0.0,0.0]
camdirection = [0.0,0.0,0.0]
sc = 1.0

global camnear
camnear = 1.0

def exitfunc(): #runs when sys.exit() is called
 	print "exiting"

sys.exitfunc = exitfunc

def display():
	
	GL.glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	global camposition

	for i in range(0,len(allmodels)):
		allmodels[i].draw()
		
	glut.glutSwapBuffers()
	glut.glutPostRedisplay()

def keyboard(key, x, y):

	global camposition
	global camdirection
	global sc
	global camnear



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
		sc += 0.1
		allmodels[0].set_scale(sc)
		print allmodels[0].scale
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
		sc -= 0.1
		allmodels[0].set_scale(sc)
		print allmodels[0].scale
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

	'''
	for i in range(0,len(allmodels)):
		allmodels[i].campos = camposition
		allmodels[i].camdir = camdirection
		allmodels[i].scale = sc
		allmodels[i].update()
	'''

	glut.glutPostRedisplay()

def reshape(width,height):
	GL.glViewport(0, 0, width, height)
	GL.glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	aspect = width/height

	global camposition
	global camnear

	for i in range(0,len(allmodels)):
		allmodels[i].set_display_mat_variables(2,-2,2,-2,3,camnear)  # top,bottom,right,left,far,near
		allmodels[i].camposition = camposition;

	glut.glutPostRedisplay()

def timer(fps):

	#ANY ANIMATION GOES HERE

	glut.glutTimerFunc(1000/fps, timer, fps)


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
glut.glutTimerFunc(1000/60, timer, 60)
#glut.glutFullScreen() #does work -- 3/23

'''
GENERATE POINTS AND DECLARE BUFFER OBJECTS() HERE 
'''
p = pointgenerator()

p.reset()
p.gen_legacy_seed_block(4,32,32,32,-0.4,0.4)

allmodels.append(buffobj(p.num_points,p.points,p.colors))
allmodels[0].rendertype = GL.GL_LINES
print p.num_points

GL.glEnable(GL.GL_DEPTH_TEST)
GL.glEnable(GL.GL_BLEND)
GL.glBlendFunc(GL.GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

GL.glLineWidth(3.0)
GL.glPointSize(5.0)

#MAIN LOOP
glut.glutMainLoop()