from buffobj import *
from numpy import linalg as LA


windowtitle = "GLUT Display"
windowxdim = 800
windowydim = 800

def exitfunc(): #runs when sys.exit() is called

 	print "exiting"

sys.exitfunc = exitfunc

def display():

	global d
	global e
	global f

	GL.glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	#DRAW CALLS HERE
	d.draw()
	e.draw()
	f.draw()

	glut.glutSwapBuffers()
	glut.glutPostRedisplay()

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

	global d
	global e
	global f

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
glut.glutReshapeWindow(windowxdim,windowydim)
glut.glutReshapeFunc(reshape)
glut.glutDisplayFunc(display)
glut.glutKeyboardFunc(keyboard)
glut.glutTimerFunc(1000/60, timer, 60)
#glut.glutFullScreen() #does work -- 3/23

#POINTS

global points
global colors
global num_points

points = []
colors = []
num_points = 0


def gen_sphere(offset,stop,normals=False):
	#center assumed at 0,0,0

	a = (offset,offset,offset)
	b = (-offset,offset,offset)
	c = (offset,offset,-offset)
	d = (-offset,offset,-offset)
	e = (-offset,-offset,-offset)
	f = (offset,-offset,-offset)
	g = (-offset,-offset,offset)
	h = (offset,-offset,offset)

	color = (random.rand(),random.rand(),random.rand(),random.rand())

	subd_sphere_squares(a,b,c,d,offset,0,stop,color,normals)
	subd_sphere_squares(a,b,h,g,offset,0,stop,color,normals)
	subd_sphere_squares(a,c,h,f,offset,0,stop,color,normals)
	subd_sphere_squares(c,d,f,e,offset,0,stop,color,normals)
	subd_sphere_squares(e,f,g,h,offset,0,stop,color,normals)
	subd_sphere_squares(d,b,e,g,offset,0,stop,color,normals)

def subd_sphere_squares(a,b,c,d,offset,level,stop,color,normals):
	global points
	global colors
	global num_points

	if level == stop:

		lena = sqrt(a[0]**2+a[1]**2+a[2]**2)
		lenb = sqrt(b[0]**2+b[1]**2+b[2]**2)
		lenc = sqrt(c[0]**2+c[1]**2+c[2]**2)
		lend = sqrt(d[0]**2+d[1]**2+d[2]**2)

		a = (offset*(a[0]/lena),offset*(a[1]/lena),offset*(a[2]/lena))
		b = (offset*(b[0]/lenb),offset*(b[1]/lenb),offset*(b[2]/lenb))
		c = (offset*(c[0]/lenc),offset*(c[1]/lenc),offset*(c[2]/lenc))
		d = (offset*(d[0]/lend),offset*(d[1]/lend),offset*(d[2]/lend))

		#triangle 1

		points.append(a)
		colors.append(color)

		points.append(b)
		colors.append(color)

		points.append(c)
		colors.append(color)

		#triangle 2

		points.append(b)
		colors.append(color)

		points.append(c)
		colors.append(color)

		points.append(d)
		colors.append(color)

		num_points += 6

	else:

		topmid = 	( (a[0]+b[0])/2 , (a[1]+b[1])/2 , (a[2]+b[2])/2 )
		sidemid1 = 	( (a[0]+c[0])/2 , (a[1]+c[1])/2 , (a[2]+c[2])/2 )
		sidemid2 = 	( (b[0]+d[0])/2 , (b[1]+d[1])/2 , (b[2]+d[2])/2 )
		bottommid = ( (c[0]+d[0])/2 , (c[1]+d[1])/2 , (c[2]+d[2])/2 )
		center = ( (a[0]+b[0]+c[0]+d[0])/4 , (a[1]+b[1]+c[1]+d[1])/4 , (a[2]+b[2]+c[2]+d[2])/4 )

		subd_sphere_squares( 		a,   topmid,  sidemid1,    center, offset,level+1,stop,color,normals)
		subd_sphere_squares(   topmid, 		  b, 	center,  sidemid2, offset,level+1,stop,color,normals)
		subd_sphere_squares( sidemid1, 	 center, 		 c, bottommid, offset,level+1,stop,color,normals)
		subd_sphere_squares(   center, sidemid2, bottommid, 	    d, offset,level+1,stop,color,normals)

gen_sphere(0.5,6)

print num_points

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

global d
d = buffobj(num_points,points,colors)
d.rendertype = "triangles"

points = []
colors = []
num_points = 0

gen_sphere(0.1,4)
print num_points

global e
e = buffobj(num_points,points,colors)
e.set_translate(-0.5,-0.5,0.0)
e.rendertype = 'triangles'

points = []
colors = []
num_points = 0

gen_sphere(0.2,5)
print num_points

global f
f = buffobj(num_points,points,colors)
f.set_translate(0.5,0.5,0.0)
f.rendertype = 'points'



#BUFFERS

glut.glutMainLoop()