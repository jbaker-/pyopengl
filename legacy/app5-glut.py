from buffobj import *

windowtitle = "GLUT Display"

def exitfunc(): #runs when sys.exit() is called
 	print "exiting"

sys.exitfunc = exitfunc

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

global dscale
global escale
global fscale
dscale = 0.0
escale = 0.0
fscale = 0.0

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

	global dscale
	global escale
	global fscale


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
	elif key == 'u':
		dscale += 0.001
	elif key == 'j':
		escale += 0.001
	elif key == 'm':
		fscale += 0.001



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

	global dscale
	global escale
	global fscale

	dxrotate,dyrotate,dzrotate = dxrotate+dscale,dyrotate+dscale,dzrotate+dscale
	exrotate,eyrotate,ezrotate = exrotate+escale,eyrotate+escale,ezrotate+escale
	fxrotate,fyrotate,fzrotate = fxrotate+fscale,fyrotate+fscale,fzrotate+fscale

	d.set_rotate(dxrotate,dyrotate,dzrotate)
	e.set_rotate(exrotate,eyrotate,ezrotate)
	f.set_rotate(fxrotate,fyrotate,fzrotate)

	glut.glutTimerFunc(1000/fps, timer, fps)

glut.glutInit()
glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA | glut.GLUT_DEPTH | glut.GLUT_MULTISAMPLE)

GL.glEnable(GL.GL_DEPTH_TEST)
GL.glEnable(GL.GL_BLEND)
GL.glBlendFunc(GL.GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
GL.glClearColor(0.0,0.0,0.0,1.0)

glut.glutCreateWindow(windowtitle)
glut.glutReshapeWindow(800,800)
glut.glutReshapeFunc(reshape)
glut.glutDisplayFunc(display)
glut.glutKeyboardFunc(keyboard)
glut.glutTimerFunc(1000/60, timer, 60)
#glut.glutFullScreen() #does work -- 3/23

#==================================================================================================================

usersetx1 = 50
usersety1 = 50
usersetz1 = 50
num_points1 = usersetx1 * usersety1 * usersetz1

minextent1 = -0.4
maxextent1 =  0.4

usersetx_np1 = np.linspace(minextent1, maxextent1, usersetx1, True, False, dtype=np.float32)
usersety_np1 = np.linspace(minextent1, maxextent1, usersety1, True, False, dtype=np.float32)
usersetz_np1 = np.linspace(minextent1, maxextent1, usersetz1, True, False, dtype=np.float32)

x_values1 = array(usersetx_np1)
y_values1 = array(usersety_np1)
z_values1 = array(usersetz_np1)

points1 = []
colors1 = []

for x in range(0,usersetx1):
	for y in range(0,usersety1):
		for z in range(0,usersetz1):
			points1.append((x_values1[x],y_values1[y],z_values1[z]))
			colors1.append((0.3*random.rand(),0.7*random.rand(),0.01*random.rand(),1.0))

#=================================================================================================================

usersetx2 = 30
usersety2 = 30
usersetz2 = 30
num_points2 = usersetx2 * usersety2 * usersetz2

minextent2 = -0.3
maxextent2 =  0.3

usersetx_np2 = np.linspace(minextent2, maxextent2, usersetx2, True, False, dtype=np.float32)
usersety_np2 = np.linspace(minextent2, maxextent2, usersety2, True, False, dtype=np.float32)
usersetz_np2 = np.linspace(minextent2, maxextent2, usersetz2, True, False, dtype=np.float32)

x_values2 = array(usersetx_np2)
y_values2 = array(usersety_np2)
z_values2 = array(usersetz_np2)

points2 = []
colors2 = []

for x in range(0,usersetx2):
	for y in range(0,usersety2):
		for z in range(0,usersetz2):
			points2.append((x_values2[x],y_values2[y],z_values2[z]))
			colors2.append((0.4*random.rand(),0.01*random.rand(),0.9*random.rand(),1.0))

#===================================================================================================================

usersetx3 = 15
usersety3 = 15
usersetz3 = 15
num_points3 = usersetx3 * usersety3 * usersetz3

minextent3 = -0.2
maxextent3 =  0.2

usersetx_np3 = np.linspace(minextent3, maxextent3, usersetx3, True, False, dtype=np.float32)
usersety_np3 = np.linspace(minextent3, maxextent3, usersety3, True, False, dtype=np.float32)
usersetz_np3 = np.linspace(minextent3, maxextent3, usersetz3, True, False, dtype=np.float32)

x_values3 = array(usersetx_np3)
y_values3 = array(usersety_np3)
z_values3 = array(usersetz_np3)

points3 = []
colors3 = []

for x in range(0,usersetx3):
	for y in range(0,usersety3):
		for z in range(0,usersetz3):
			points3.append((x_values3[x],y_values3[y],z_values3[z]))
			colors3.append((random.rand(),random.rand(),random.rand(),1.0))

#===================================================================================================================

d = buffobj(num_points1,points1,colors1,None)
d.set_translate(0.5,0.5,0.0)
d.update()

e = buffobj(num_points2,points2,colors2,None)
e.set_translate(-0.5,-0.5,0.0)
e.rendertype = "lines"
e.update()

f = buffobj(num_points3,points3,colors3,None)

glut.glutMainLoop(),num_points3,