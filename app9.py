from buffobj import *
from pointgenerator import *

windowtitle = "GLUT Display"
windowxdim = 800
windowydim = 800

allmodels = []
modelrotationscales = []

global newcampos
newcampos = [0.0,0.0,0.0]

def exitfunc(): #runs when sys.exit() is called
 	print "exiting"

sys.exitfunc = exitfunc

def display():
	
	GL.glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	global newcampos

	for i in range(0,len(allmodels)):
		allmodels[i].draw()
		allmodels[i].campos = newcampos;
		allmodels[i].update()

	glut.glutSwapBuffers()
	glut.glutPostRedisplay()

def keyboard(key, x, y):

	global newcampos

	if key == '\033':
		sys.exit( )
	elif key == 'd':
		newcampos[1] += 0.1
	elif key == 'e':
		newcampos[1] -= 0.1

	#OTHER KEYS TO CONTROL THE PROGRAM

	glut.glutPostRedisplay()

def reshape(width,height):
	GL.glViewport(0, 0, width, height)
	GL.glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	aspect = width/height

	global newcampos

	for i in range(0,len(allmodels)):
		allmodels[i].set_display_mat_variables(2.0,-2.0,2.0,-2.0,0.5,0.1)
		allmodels[i].campos = newcampos;

	glut.glutPostRedisplay()

def timer(fps):

	#ANY ANIMATION GOES HERE
	for i in range(0,len(allmodels)):
		allmodels[i].set_rotate(allmodels[i].xrotate+modelrotationscales[i][0],allmodels[i].yrotate+modelrotationscales[i][1],allmodels[i].zrotate+modelrotationscales[i][2])

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

p.gen_legacy_seed_block(4,32,32,32,-0.1,0.5)

allmodels.append(buffobj(p.num_points,p.points,p.colors))
allmodels[0].set_translate(0.5,0.5,0.0)
#allmodels[0].rendertype = GL.GL_LINE_STRIP
modelrotationscales.append((0.01,0.0,0.0))
print p.num_points

p.reset()
p.gen_legacy_seed_block(4,32,32,32,-0.3,0.4)

allmodels.append(buffobj(p.num_points,p.points,p.colors))
allmodels[1].set_translate(-0.5,-0.5,0.0)
#allmodels[1].rendertype = GL.GL_LINES
modelrotationscales.append((0.0,0.01,-0.01))
print p.num_points

p.reset()
p.gen_legacy_seed_block(4,32,32,32,-0.3,0.4)

allmodels.append(buffobj(p.num_points,p.points,p.colors))
allmodels[2].set_translate(0.5,0.5,0.0)
#allmodels[1].rendertype = GL.GL_LINES
modelrotationscales.append((0.0,0.01,0.01))
print p.num_points

p.reset()
p.gen_legacy_seed_block(4,32,32,32,-0.5,0.5)

allmodels.append(buffobj(p.num_points,p.points,p.colors))
#allmodels[0].set_display_mat_variables(1.0,-1.0,1.0,-1.0,0.5,0.000001)
modelrotationscales.append((0.0,-0.01,0.01))
print p.num_points

GL.glEnable(GL.GL_DEPTH_TEST)
GL.glEnable(GL.GL_BLEND)
GL.glBlendFunc(GL.GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

GL.glLineWidth(3.0)
GL.glPointSize(5.0)

#MAIN LOOP
glut.glutMainLoop()