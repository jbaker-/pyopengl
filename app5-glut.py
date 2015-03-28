from buffobj import *

windowtitle = "GLUT Display"

def display():
	GL.glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	d.draw()
	e.draw()
	f.draw()

	glut.glutSwapBuffers()
	glut.glutPostRedisplay()

global dxrotate
global dyrotate
global dzrotate
dxrotate = 0.0
dyrotate = 0.0
dzrotate = 0.0

global exrotate
global eyrotate
global ezrotate
exrotate = 0.0
eyrotate = 0.0
ezrotate = 0.0

global fxrotate
global fyrotate
global fzrotate
fxrotate = 0.0
fyrotate = 0.0
fzrotate = 0.0

def keyboard(key, x, y):
	global dxrotate
	global dyrotate
	global dzrotate
	global exrotate
	global eyrotate
	global ezrotate
	global fxrotate
	global fyrotate
	global fzrotate

	if key == '\033':
		sys.exit( )
	elif key == 'r': # rotate
		dxrotate += 0.1
	elif key == 'f':
		dyrotate += 0.1
	elif key == 'v':
		dzrotate += 0.1
	elif key == 't':
		exrotate += 0.1
	elif key == 'g':
		eyrotate += 0.1
	elif key == 'b':
		ezrotate += 0.1
	elif key == 'y':
		fxrotate += 0.1
	elif key == 'h':
		fyrotate += 0.1
	elif key == 'n':
		fzrotate += 0.1


	glut.glutPostRedisplay()

def reshape(width,height):
	GL.glViewport(0, 0, width, height)
	GL.glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glut.glutPostRedisplay()

def timer(fps):
	global dxrotate
	global dyrotate
	global dzrotate
	global exrotate
	global eyrotate
	global ezrotate
	global fxrotate
	global fyrotate
	global fzrotate

	d.set_rotate(dxrotate,dyrotate,dzrotate)
	d.update()

	e.set_rotate(exrotate,eyrotate,ezrotate)
	e.update()

	f.set_rotate(fxrotate,fyrotate,fzrotate)
	f.update()

	glut.glutTimerFunc(1000/fps, timer, fps)


def exitfunc(): #runs when sys.exit() is called
 	print "exiting"

sys.exitfunc = exitfunc

glut.glutInit()
glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA | glut.GLUT_DEPTH | glut.GLUT_MULTISAMPLE)

GL.glEnable(GL.GL_DEPTH_TEST)
GL.glEnable(GL.GL_BLEND)
GL.glBlendFunc(GL.GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
GL.glClearColor(0.0,0.0,0.0,1.0)
GL.glPointSize(5.0)

glut.glutCreateWindow(windowtitle)
glut.glutReshapeWindow(800,800)
glut.glutReshapeFunc(reshape)
glut.glutDisplayFunc(display)
glut.glutKeyboardFunc(keyboard)
glut.glutTimerFunc(1000/60, timer, 60)
#glut.glutFullScreen() #does work -- 3/23

usersetx = 50
usersety = 50
usersetz = 50
num_points = usersetx * usersety * usersetz

minextent = -0.5
maxextent =  0.5

usersetx_np = np.linspace(minextent, maxextent, usersetx, True, False, dtype=np.float32)
usersety_np = np.linspace(minextent, maxextent, usersety, True, False, dtype=np.float32)
usersetz_np = np.linspace(minextent, maxextent, usersetz, True, False, dtype=np.float32)

x_values = array(usersetx_np)
y_values = array(usersety_np)
z_values = array(usersetz_np)

points = []
colors = []

for x in range(0,usersetx):
	for y in range(0,usersety):
		for z in range(0,usersetz):

			points.append((x_values[x],y_values[y],z_values[z]))
			colors.append((0.5,0.5,0.5,1.0))

d = buffobj(points,colors,num_points)
d.set_translate(0.5,0.5,0.0)
d.update()

e = buffobj(points,colors,num_points)
e.set_translate(-0.5,-0.5,0.0)
e.update()

f = buffobj(points,colors,num_points)

glut.glutMainLoop()