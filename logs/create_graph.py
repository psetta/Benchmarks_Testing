# -*- coding: utf-8 -*-

import modulos.extraer_xml as ext

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

#CREAR GRÁFICA EN OPENGL

#CONSTANTES

XML_INFO = ext.extraer_xml(".")

dict_xml = {}

for bench in XML_INFO:
	if bench[0] in dict_xml:
		dict_xml[bench[0]].append(bench[1:3])
	else:
		dict_xml[bench[0]] = []

for script in dict_xml:
	print ">>> "+script
	for bench in sorted(dict_xml[script],key=lambda x: float(x[0])):
		print "\t"+str(bench)
	
MAYOR_X = float(max(XML_INFO,key=lambda x: float(x[1]))[1])
MAYOR_Y = float(max(XML_INFO,key=lambda x: float(x[2]))[2])

ANCHO_VENTANA = 800
ALTO_VENTANA = 600

EJE_X = [0,MAYOR_X]
EJE_Y = [0,MAYOR_Y]

EJE_X_AUM = (EJE_X[1]-EJE_X[0])/10
EJE_Y_AUM = (EJE_Y[1]-EJE_Y[0])/10

GL_X_INICIAL = [EJE_X[0]-EJE_X_AUM,EJE_X[1]+EJE_X_AUM]
GL_Y_INICIAL = [EJE_Y[0]-EJE_Y_AUM,EJE_Y[1]+EJE_Y_AUM]

GL_X,GL_Y = GL_X_INICIAL[:],GL_Y_INICIAL[:]

COLOR_FONDO = 0

#VARIABLES

pos_camara = [0,0]

def main():

	global pos_camara
	global GL_X
	global GL_Y
	
	pygame.init()
	ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA), DOUBLEBUF|OPENGL)
	pygame.display.set_caption("Grafica_OpenGL")
	init_gl()
	
	while True:
	
		reloj = pygame.time.Clock()
		
		#LIMPIAR VENTANA ######
		
		limpiar_ventana()
		
		#DEBUXAR
		
			#LINHAS
			
		color_linha = [1,1,0,0.6]
		for script in dict_xml:
			vertices = sorted(dict_xml[script],key=lambda x: float(x[0]))
			debuxar_linha(vertices,color_linha)
			debuxar_puntos(vertices,color_linha[:3]+[1])
			color_linha[2] += 0.2
			color_linha[1] -= 0.1
			color_linha[0] -= 0.2
			color_linha[2] = min(color_linha[2],1)
			color_linha[1] = max(color_linha[1],0)
			color_linha[0] = max(color_linha[0],0)
		
			#EJE X
		
		debuxar_linha([[0,EJE_Y[0]],[0,EJE_Y[1]]],[1,1,1,1])
		
			#EJE Y
			
		debuxar_linha([[EJE_X[0],0],[EJE_X[1],0]],[1,1,1,1])
		
		#############################################################
		#EVENTOS ####################################################
		#############################################################
		
		zoom = (GL_X_INICIAL[1]/GL_X[1])
		
		#TECLAS ######
		
		tecla_pulsada = pygame.key.get_pressed()
		
		if (tecla_pulsada[K_UP] or tecla_pulsada[K_w]):
			pos_camara[1] -= EJE_Y_AUM/(20*zoom)
			
		elif tecla_pulsada[K_DOWN] or tecla_pulsada[K_s]:
			pos_camara[1] += EJE_Y_AUM/(20*zoom)
		
		if tecla_pulsada[K_LEFT] or tecla_pulsada[K_a]:
			pos_camara[0] += EJE_X_AUM/(20*zoom)
			
		elif tecla_pulsada[K_RIGHT] or tecla_pulsada[K_d]:
			pos_camara[0] -= EJE_X_AUM/(20*zoom)
		
		for event in pygame.event.get():
		
			#RATÓN
		
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 4:
					if zoom < 2:
						GL_X[0] += EJE_X_AUM/(10*zoom)
						GL_X[1] -= EJE_X_AUM/(10*zoom)
						GL_Y[0] += EJE_Y_AUM/(10*zoom)
						GL_Y[1] -= EJE_Y_AUM/(10*zoom)
				if event.button == 5:
					if zoom > 0.8:
						GL_X[0] -= EJE_X_AUM/(10*zoom)
						GL_X[1] += EJE_X_AUM/(10*zoom)
						GL_Y[0] -= EJE_Y_AUM/(10*zoom)
						GL_Y[1] += EJE_Y_AUM/(10*zoom)
						
			#TECLAS
		
			if event.type == pygame.KEYDOWN:
				
				if event.key == pygame.K_RETURN:
					pos_camara = [0,0]
					GL_X,GL_Y = GL_X_INICIAL[:],GL_Y_INICIAL[:]
					
			#QUIT
		
			if event.type == pygame.QUIT:
				pygame.quit()
				return
				
		#ACTUALIZAR VENTANA ######
		
		pygame.display.flip()
				
		reloj.tick(60)

##############################################################
#OPENGL	######################################################
##############################################################

def init_gl():
	glViewport(0, 0, ANCHO_VENTANA, ALTO_VENTANA)
	glClearColor(COLOR_FONDO, COLOR_FONDO, COLOR_FONDO, 1)
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glEnable(GL_LINE_SMOOTH)
	glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
	
def limpiar_ventana():
	glClear(GL_COLOR_BUFFER_BIT)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluOrtho2D(GL_X[0], GL_X[1], GL_Y[0], GL_Y[1])
	try:
		glTranslatef(0 + pos_camara[0],0 + pos_camara[1], 0)
	except:
		pass
	glMatrixMode(GL_MODELVIEW)
	
def debuxar_linha(vertices,color):
	glLineWidth(1)
	glColor4f(color[0],color[1],color[2],color[3])
	glBegin(GL_LINES)
	for v in range(len(vertices)-1):
		glVertex2f(float(vertices[v][0]), float(vertices[v][1]))
		glVertex2f(float(vertices[v+1][0]), float(vertices[v+1][1]))
	glEnd()
	
def debuxar_puntos(puntos,color):
	glLoadIdentity()
	glPointSize(2)
	glColor4f(color[0],color[1],color[2],color[3])
	glBegin(GL_POINTS)
	for p in puntos:
		glVertex2f(float(p[0]), float(p[1]))
	glEnd()
	
if __name__ == '__main__':
	main()