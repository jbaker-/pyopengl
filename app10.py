from buffobj import *
from pointgenerator import *

windowtitle = "GLUT Display"
windowxdim = 800
windowydim = 800

allmodels = []

global camposition
global camdirection
global sc
camposition = [0.0,0.0,-0.5]
camdirection = [0.0,0.0,0.0]
sc = 1.0

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

	if key == '\033':
		sys.exit( )
	elif key == 'e':
		camposition[2] += 0.0001
	elif key == 'q':
		camposition[2] -= 0.0001
	elif key == 'w':
		camposition[1] += 0.0001
	elif key == 'x':
		camposition[1] -= 0.0001
	elif key == 'd':
		camposition[0] += 0.0001
	elif key == 'a':
		camposition[0] -= 0.0001
	elif key == 'h':
		camdirection[0] += 0.005
	elif key == 'k':
		camdirection[0] -= 0.005
	elif key == 'u':
		camdirection[1] += 0.005
	elif key == 'n':
		camdirection[1] -= 0.005
	elif key == 'y':
		camdirection[2] += 0.005
	elif key == 'i':
		camdirection[2] -= 0.005
	elif key == 'g':
		camposition = [0,0,0]
		camdirection = [0,0,0]
	elif key == 't':
		sc += 0.01
	elif key == 'r':
		sc -= 0.01


	for i in range(0,len(allmodels)):
		allmodels[i].campos = camposition
		allmodels[i].camdir = camdirection
		allmodels[i].scale = sc
		allmodels[i].update()



	#OTHER KEYS TO CONTROL THE PROGRAM

	glut.glutPostRedisplay()

def reshape(width,height):
	GL.glViewport(0, 0, width, height)
	GL.glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	aspect = width/height

	global camposition

	for i in range(0,len(allmodels)):
		allmodels[i].set_display_mat_variables(2.0,-2.0,2.0,-2.0,10,0.1)
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
#allmodels[0].set_display_mat_variables(1.0,-1.0,1.0,-1.0,0.5,0.000001)
print p.num_points

GL.glEnable(GL.GL_DEPTH_TEST)
GL.glEnable(GL.GL_BLEND)
GL.glBlendFunc(GL.GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

GL.glLineWidth(3.0)
GL.glPointSize(5.0)

#MAIN LOOP
glut.glutMainLoop()