from buffobj import *
from pointgenerator import *

windowtitle = "GLUT Display"
windowxdim = 800
windowydim = 800

def exitfunc(): #runs when sys.exit() is called

 	print "exiting"

sys.exitfunc = exitfunc

def display():
	global buffobjs
	global drawing
	global moving

	GL.glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	for i in buffobjs:
		i.draw()

	glut.glutSwapBuffers()
	glut.glutPostRedisplay()

def keyboard(key, x, y):

	if key == '\033':
		sys.exit( )

	#OTHER KEYS TO CONTROL THE PROGRAM

	glut.glutPostRedisplay()

def reshape(width,height):

	GL.glViewport(0, 0, width, height)
	GL.glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glut.glutPostRedisplay()

def timer(fps):
	global buffobjs
	global clock

	clock += 0.0001

	index = 0.0

	for i in buffobjs:
		#i.set_translate(i.xtranslate+sin(clock),i.ytranslate+sin(clock),i.ztranslate+sin(clock))
		i.set_rotate(index*i.xrotate+clock,index*i.yrotate+clock,index*i.zrotate+clock)
		i.update()
		index += 0.5

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

#generate points and declare buffers

global buffobjs
global clock
buffobjs = []
clock = 0.0

p = pointgenerator()
p.gen_sphere(0.5,4)

buffobjs.append(buffobj(p.num_points,p.points,p.colors))

p.reset()
p.gen_sphere(0.2,2)

buffobjs.append(buffobj(p.num_points,p.points,p.colors))

p.reset()
p.gen_cube(15,15,15)

buffobjs.append(buffobj(p.num_points,p.points,p.colors))

global drawing
global moving
drawing = True
moving = False


glut.glutMainLoop()