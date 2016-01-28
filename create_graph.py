# -*- coding: utf-8 -*-

import modulos_graph.extraer_xml as ext

import pygame
import os
import sys
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

try:
	if os.name == 'nt' and sys.getwindowsversion()[0] >= 6:
		ctypes.windll.user32.SetProcessDPIAware()
except:
	pass

#CREAR GRÁFICA EN OPENGL

#CONSTANTES

dir_logs = raw_input("indica o directorio dos logs a cargar: ")

XML_INFO = ext.extraer_xml(dir_logs)

dict_xml = {}

for bench in XML_INFO:
	if bench[0] in dict_xml:
		dict_xml[bench[0]].append(bench[1:3])
	else:
		dict_xml[bench[0]] = []
		dict_xml[bench[0]].append(bench[1:3])

for script in dict_xml:
	print ">>> "+script
	for bench in sorted(dict_xml[script],key=lambda x: float(x[0])):
		print "\t"+str(bench)
	
MAYOR_X = float(max(XML_INFO,key=lambda x: float(x[1]))[1])
MAYOR_Y = float(max(XML_INFO,key=lambda x: float(x[2]))[2])

MENOR_X =float(min(XML_INFO,key=lambda x: float(x[1]))[1])
MENOR_Y = float(min(XML_INFO,key=lambda x: float(x[2]))[2])

ANCHO_VENTANA = 800
ALTO_VENTANA = 600

EJE_X = [int(MENOR_X),round(MAYOR_X+0.5)]
EJE_Y = [int(MENOR_Y),round(MAYOR_Y+0.5)]

EJE_X_AUM = (EJE_X[1]-EJE_X[0])/10
EJE_Y_AUM = (EJE_Y[1]-EJE_Y[0])/10

GL_X_INICIAL = [EJE_X[0]-EJE_X_AUM,EJE_X[1]+EJE_X_AUM]
GL_Y_INICIAL = [EJE_Y[0]-EJE_Y_AUM,EJE_Y[1]+EJE_Y_AUM]

GL_X,GL_Y = GL_X_INICIAL[:],GL_Y_INICIAL[:]

COLOR_FONDO = 0

#VARIABLES

pos_camara = [0,0]

zoom = 1

def main():

	global ANCHO_VENTANA
	global ALTO_VENTANA
	global pos_camara
	global GL_X
	global GL_Y
	global zoom
	
	zoom_ant = zoom
	temp = 1
	resizable = False
	
	pygame.init()
	ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA),DOUBLEBUF|OPENGL|RESIZABLE)
	pygame.display.set_caption("Grafica_OpenGL")
	init_gl()
	
	#CREAR LISTAS DE OPENGL
	
	ID_LISTA_TEXTO = glGenLists(1)
	ID_LISTA_LINHAS = glGenLists(1)
	ID_LISTA_GRAFICA = glGenLists(1)
	
	def crear_listas_gl():
		crear_gllist_texto(ID_LISTA_TEXTO)
		crear_gllist_linhas(ID_LISTA_LINHAS)
		crear_gllist_grafica(ID_LISTA_GRAFICA)
		
	crear_listas_gl()
	
	while True:
	
		reloj = pygame.time.Clock()
		
		#LIMPIAR VENTANA ######
		
		limpiar_ventana()
		
		#CREAR LISTA TEXTO SE HAI ZOOM####
		
		if not zoom == zoom_ant and temp == 1: 
			ID_LISTA_TEXTO = glGenLists(1)
			crear_gllist_texto(ID_LISTA_TEXTO)
			zoom_ant = zoom
			temp = 60
		else:
			temp = max(1,temp-1)
		
		#CREAR LISTAS SE HAI REDIMENSIONAMENTO####
		
		if resizable:
			ID_LISTA_TEXTO = glGenLists(1)
			ID_LISTA_LINHAS = glGenLists(1)
			ID_LISTA_GRAFICA = glGenLists(1)
			crear_listas_gl()
			resizable = False
		
		#DEBUXAR #########################
		##################################
		
			#LINHAS
		glCallList(ID_LISTA_LINHAS)
		
			#GRAFICA
		glCallList(ID_LISTA_GRAFICA)
		
			#TEXTO
		glCallList(ID_LISTA_TEXTO)
		
		#############################################################
		#EVENTOS ####################################################
		#############################################################
		
		zoom = (GL_X_INICIAL[1]/GL_X[1])
		
		#POSICIÓN RATÓN
		
		pos_mouse = pygame.mouse.get_pos()
		
		pos_mouse_gl = [
				(pos_mouse[0]*(GL_X[1]-GL_X[0])/ANCHO_VENTANA-(pos_camara[0]-GL_X[0])),
				((GL_Y[1]-GL_Y[0])-(pos_mouse[1]*(GL_Y[1]-GL_Y[0])/ALTO_VENTANA)-(pos_camara[1]-GL_Y[0]))
				]
				
		if (EJE_X[0] < pos_mouse_gl[0] < EJE_X[1] and
				EJE_Y[0] < pos_mouse_gl[1] < EJE_Y[1]):
			vertices_linhas = [[EJE_X[0],pos_mouse_gl[1]],[pos_mouse_gl[0],
								pos_mouse_gl[1]],[pos_mouse_gl[0],EJE_Y[0]]]
			debuxar_linha(vertices_linhas,[1,1,1,0.4])
			drawText(pos_mouse_gl[0], pos_mouse_gl[1], 
						str([round(x,2) for x in pos_mouse_gl]), 20)
		
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
		
			#RODA RATÓN
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 4:
					if (GL_X[1]-EJE_X_AUM > GL_X[0] and 
						GL_Y[1]-EJE_Y_AUM > GL_Y[0]):
						GL_X[0] += EJE_X_AUM/(10*zoom)
						GL_X[1] -= EJE_X_AUM/(10*zoom)
						GL_Y[0] += EJE_Y_AUM/(10*zoom)
						GL_Y[1] -= EJE_Y_AUM/(10*zoom)
				if event.button == 5:
					GL_X[0] -= EJE_X_AUM/(10*zoom)
					GL_X[1] += EJE_X_AUM/(10*zoom)
					GL_Y[0] -= EJE_Y_AUM/(10*zoom)
					GL_Y[1] += EJE_Y_AUM/(10*zoom)
					if GL_X[1] > GL_X_INICIAL[1]:
						zoom = 1
						GL_X,GL_Y = GL_X_INICIAL[:],GL_Y_INICIAL[:]
						
			#TECLAS
			if event.type == pygame.KEYDOWN:
				
				if event.key == pygame.K_RETURN:
					pos_camara = [0,0]
					GL_X,GL_Y = GL_X_INICIAL[:],GL_Y_INICIAL[:]
					
			#REDIMENSIONAR
			
			if event.type == VIDEORESIZE:
		
				ANCHO_VENTANA = event.dict['size'][0]
				ALTO_VENTANA = event.dict['size'][1]
				ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA), DOUBLEBUF|OPENGL|RESIZABLE )
				init_gl()
				resizable = True
					
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

def drawText(x, y, text, tamanho):                                                
	position = (x, y, 0)                                                       
	font = pygame.font.Font(None, int(tamanho))                                          
	textSurface = font.render(text, True, (255,255,255,255), (0,0,0,0))                                   
	textData = pygame.image.tostring(textSurface, "RGBA", True)              
	glRasterPos3d(*position)                                                
	glDrawPixels(textSurface.get_width(), textSurface.get_height(),         
					GL_RGBA, GL_UNSIGNED_BYTE, textData)   

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
	glColor4f(*color)
	glBegin(GL_POINTS)
	for p in puntos:
		glVertex2f(float(p[0]), float(p[1]))
	glEnd()
	
def debuxar_rect(vertices,color):
	glLoadIdentity()
	glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
	glColor4f(*color)
	glBegin(GL_POLYGON)
	for vertice in vertices:
		glVertex2f(vertice[0],vertice[1])
	glEnd()
	
def crear_gllist_texto(id):
	glNewList(id, GL_COMPILE)
	glLoadIdentity()
	salto_rango_x = max(int(10/zoom),int(((EJE_X[1]-EJE_X[0])/10)/zoom)*10)
	salto_rango_y = max(int(10/zoom),int(((EJE_Y[1]-EJE_Y[0])/10)/zoom)*10)
	frango_x = [i/10.0 for i in range(int(EJE_X[0])*10,
								(int(EJE_X[1]))*10,salto_rango_x)]
	frango_y = [i/10.0 for i in range(int(EJE_Y[0])*10,
								(int(EJE_Y[1]))*10,salto_rango_y)]
	for x in frango_x:
		debuxar_linha([[x,(EJE_Y[0]+EJE_Y_AUM/10)],[x,EJE_Y[0]]],[1,1,1,1])
		drawText(x,((EJE_Y[0]-EJE_Y_AUM/3))/zoom,str(x),16*zoom)
	for y in frango_y:
		debuxar_linha([[(EJE_X[0]+EJE_X_AUM/10),y],[EJE_X[0],y]],[1,1,1,1])
		drawText(((EJE_X[0]-EJE_X_AUM/(3*zoom))),y,str(y),16*zoom)
	drawText((EJE_X[0]-EJE_X_AUM)/zoom,EJE_Y[1],"y : segundos",20*zoom)
	drawText(EJE_X[0],(EJE_Y[0]-EJE_Y_AUM)/zoom,"x : argumento",20*zoom)
	glEndList()
	
def crear_gllist_linhas(id):
	glNewList(id, GL_COMPILE)
	glLoadIdentity()
	color_linha = [1,1,0,0.6]
	for script in dict_xml:
		vertices = sorted(dict_xml[script],key=lambda x: float(x[0]))
		debuxar_linha(vertices,color_linha)
		debuxar_puntos(vertices,color_linha[:3]+[1])
		x_f,y_f = vertices[len(vertices)-1]
		#drawText(x_f,y_f,script,20*zoom)
		drawText(float(x_f),float(y_f),script,20*zoom)
		color_linha[2] += 0.2
		color_linha[1] -= 0.1
		color_linha[0] -= 0.2
		color_linha[2] = min(color_linha[2],1)
		color_linha[1] = max(color_linha[1],0)
		color_linha[0] = max(color_linha[0],0)
	glEndList()
	
def crear_gllist_grafica(id):
	glNewList(id, GL_COMPILE)
	glLoadIdentity()
	vertices_grafica = [[EJE_X[0],EJE_Y[0]],
						[EJE_X[1],EJE_Y[0]],
						[EJE_X[1],EJE_Y[1]],
						[EJE_X[0],EJE_Y[1]]]
	debuxar_rect(vertices_grafica,[0.5,0.5,0.5,0.1])
	debuxar_linha([[EJE_X[0],EJE_Y[0]],[EJE_X[0],EJE_Y[1]]],[1,1,1,1])
	debuxar_linha([[EJE_X[0],EJE_Y[0]],[EJE_X[1],EJE_Y[0]]],[1,1,1,1])
	glEndList()

if __name__ == '__main__':
	main()