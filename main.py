# -*- coding: utf-8 -*-

#XOGO DA VIDA

import pygame
from pygame.locals import *
import random

#CONSTANTES

#PEDIR VARIABLES

print("")
print("--- XOGO DA VIDA ---")
print("")

LADO_CADRO = raw_input("Introduce o tamanho do lado de cada cadrado (defecto = 5): ")
NUM_CADROS_ANCHO = raw_input("Introduce o numero de cadrados por fila (defecto = 50): ")
NUM_CADROS_ALTO = raw_input("Introduce o numero de cadrados por columna (defecto = 50): ")
NIVEL_POBOACION_INICIAL = raw_input("Introduce nivel de poboacion (minimo:0 maximo:9) (defecto = 3): ")
VELOCIDADE = raw_input("Introduce a velocidade do xogo (minimo:0 maximo:5)(defecto = 2): ")

print("")
print("-CONTROLES-")
print("")
print("TECLA 'C' : Mostrar/Ocultar Cadricula")
print("TECLA 'ESPACIO' : Pausar/Reanudar Xogo")
print("BOTON ESQUERDO DO RATO : Crear Vida")
print("BOTON DEREITO DO RATO : Borrar Vida")
print("BOTON SUPR : Borrar Toda Vida")
print("<- : Disminuir Velocidade")
print("-> : Aumentar Velocidade")

if not LADO_CADRO.isdigit():
	LADO_CADRO = 5
if not NUM_CADROS_ANCHO.isdigit():
	NUM_CADROS_ANCHO = 50
if not NUM_CADROS_ALTO.isdigit():
	NUM_CADROS_ALTO = 50
if not NIVEL_POBOACION_INICIAL.isdigit() or (int(NIVEL_POBOACION_INICIAL)<0 or int(NIVEL_POBOACION_INICIAL)>9):
	NIVEL_POBOACION_INICIAL = 3
if not VELOCIDADE.isdigit():
	VELOCIDADE = 2
	
LADO_CADRO = int(LADO_CADRO)
NUM_CADROS_ANCHO = int(NUM_CADROS_ANCHO)
NUM_CADROS_ALTO = int(NUM_CADROS_ALTO)
NIVEL_POBOACION_INICIAL = int(NIVEL_POBOACION_INICIAL)
VELOCIDADE = int(VELOCIDADE)

VELOCIDADE = min(VELOCIDADE,5)

if VELOCIDADE == 0:
	CONT_VELOCIDADE_TOTAL = 60
elif VELOCIDADE == 1:
	CONT_VELOCIDADE_TOTAL = 30
elif VELOCIDADE == 2:
	CONT_VELOCIDADE_TOTAL = 10
elif VELOCIDADE == 3:
	CONT_VELOCIDADE_TOTAL = 5
elif VELOCIDADE == 4:
	CONT_VELOCIDADE_TOTAL = 2
elif VELOCIDADE == 5:
	CONT_VELOCIDADE_TOTAL = 1

cont_velocidade = CONT_VELOCIDADE_TOTAL

NUM_CADROS_TOTALES = NUM_CADROS_ANCHO * NUM_CADROS_ALTO

ANCHO_VENTANA = NUM_CADROS_ANCHO * LADO_CADRO
ALTO_VENTANA = NUM_CADROS_ALTO * LADO_CADRO

COLOR_FONDO = [0,0,0]
COLOR_CADRICULA = [60,60,60]
COLOR_VIDA = [0,200,0]

#VIDA CERCANA PARA NACEMENTO E PERMANENCIA DA VIDA

LISTA_PERMANENCIA = [2,3]
LISTA_NACEMENTO = [3]

#VARIABLES

lista_cadros = []

for i in range(NUM_CADROS_TOTALES):
	lista_cadros.append(0)

lista_indices_vida = []	

if NIVEL_POBOACION_INICIAL != 0:
	for i in range(NUM_CADROS_TOTALES/(10-NIVEL_POBOACION_INICIAL)):
		lista_indices_vida.append(random.randint(0, NUM_CADROS_TOTALES-1))

for i in lista_indices_vida:
	lista_cadros[i] = 1
	
cadricula = False
pausa = False

modificacion = False

#CLASES

class punto:
	def __init__(self,x,y):
		self.x = x
		self.y = y
	def __add__(self,other):
		return punto(self.x + other.x, self.y + other.y)
		
#FUNCIONS

def indice_a_pos(indice):
	pos_y = indice / NUM_CADROS_ALTO
	pos_x = indice - NUM_CADROS_ANCHO*pos_y
	return punto(pos_x,pos_y)
	
def pos_a_indice(pos):
	indice = pos[0] + pos[1] * NUM_CADROS_ALTO
	return indice

def indices_colindantes(indice):
	sum_indices = [-(NUM_CADROS_ANCHO+1),-NUM_CADROS_ANCHO,-(NUM_CADROS_ANCHO-1),-1,1,(NUM_CADROS_ANCHO-1),NUM_CADROS_ANCHO,(NUM_CADROS_ANCHO+1)]
	indices_incorrectos = []
	indices_salida = []
	if indice in range(0,NUM_CADROS_TOTALES,NUM_CADROS_ANCHO):
		indices_incorrectos = [-(NUM_CADROS_ANCHO+1),-1,(NUM_CADROS_ANCHO-1)]
	if indice in range(NUM_CADROS_ANCHO-1,NUM_CADROS_TOTALES,NUM_CADROS_ANCHO):
		indices_incorrectos = indices_incorrectos + [-(NUM_CADROS_ANCHO-1),1,(NUM_CADROS_ANCHO+1)]
	if indice < NUM_CADROS_ANCHO:
		indices_incorrectos = indices_incorrectos + [-(NUM_CADROS_ANCHO+1),-NUM_CADROS_ANCHO,-(NUM_CADROS_ANCHO-1)]
	if indice >= NUM_CADROS_TOTALES-NUM_CADROS_ANCHO:
		indices_incorrectos = indices_incorrectos + [(NUM_CADROS_ANCHO-1),NUM_CADROS_ANCHO,(NUM_CADROS_ANCHO+1)]
	indices_incorrectos = list(set(indices_incorrectos))
	for i in indices_incorrectos:
		sum_indices.remove(i)
	for i in sum_indices:
		indices_salida.append(indice+i)
	return indices_salida

def numero_vida_colindante(indice):
	lista_indices_colindantes = indices_colindantes(indice)
	numero_vida = 0
	for i in lista_indices_colindantes:
		if lista_cadros[i]:
			numero_vida += 1
	return numero_vida
	
#INICIAR PYGAME

pygame.init()

#PANTALLA

ventana = pygame.display.set_mode([ANCHO_VENTANA, ALTO_VENTANA])

pygame.display.set_caption("Xogo da Vida")

#SUPERFICIA CON CADRICULA

superficie_cadricula = pygame.Surface((ANCHO_VENTANA,ALTO_VENTANA), pygame.SRCALPHA)

#CREACION CADRICULA
		
for i in range(NUM_CADROS_ALTO):
	pygame.draw.line(superficie_cadricula,COLOR_CADRICULA,(0,i*LADO_CADRO),(ANCHO_VENTANA,i*LADO_CADRO))
for i in range(NUM_CADROS_ANCHO):
	pygame.draw.line(superficie_cadricula,COLOR_CADRICULA,(i*LADO_CADRO,0),(i*LADO_CADRO,ALTO_VENTANA))

#BUCLE XOGO ########################################################3

ON = True

while ON:
	
	reloj = pygame.time.Clock()
	
	#DEBUXADO
	
	#RELLENADO DE COLOR
	
	if modificacion:
		ventana.fill(COLOR_FONDO)
	
		#CADROS VIVOS
	
	if not cont_velocidade:
		lista_cadros_comodin = lista_cadros[:]
		
	for i in range(NUM_CADROS_TOTALES):
	
		if modificacion:
			if lista_cadros[i]:
				pos_cadros = indice_a_pos(i)
				rect_cadro = pygame.Rect(pos_cadros.x*LADO_CADRO,pos_cadros.y*LADO_CADRO,LADO_CADRO,LADO_CADRO)
				pygame.draw.rect(ventana,COLOR_VIDA,rect_cadro)
			
			#VIDA DOS CADROS
			
		if not cont_velocidade:
		
			if not pausa:
				num_vidas_col = numero_vida_colindante(i)
				if lista_cadros[i] and not num_vidas_col in LISTA_PERMANENCIA:
					lista_cadros_comodin[i] = 0
				elif num_vidas_col in  LISTA_NACEMENTO:
					lista_cadros_comodin[i] = 1
					
	if not cont_velocidade:
		lista_cadros = lista_cadros_comodin
		
	#DEBUXADO CADRICULA
	
	if cadricula and (modificacion or cont_velocidade <= 0):
		ventana.blit(superficie_cadricula,(0,0))
	
	#VALOR FALSE EN MODIFICACION
	
	modificacion = False
	
	if cont_velocidade <= 0:
		cont_velocidade = CONT_VELOCIDADE_TOTAL
		modificacion = True
	else:
		cont_velocidade -= 1
		
	#ACTUALIZAR PANTALLA
	
	pygame.display.update()
	
	#EVENTOS RATO
	
	pos_mouse = pygame.mouse.get_pos()
	
	cadro_mouse = [pos_mouse[0]/LADO_CADRO, pos_mouse[1]/LADO_CADRO]
	
	boton_rato = pygame.mouse.get_pressed()
	
	if boton_rato[0] == 1:
		indice = pos_a_indice(cadro_mouse)
		lista_cadros[indice] = 1
		modificacion = True
	
	if boton_rato[2] == 1:
		indice = pos_a_indice(cadro_mouse)
		lista_cadros[indice] = 0
		modificacion = True
	
	#EVENTOS TACLADO
	
	for e in pygame.event.get():
	
		if e.type == pygame.KEYDOWN:
	
		#PONHER E QUITAR CADRICULA
		
			if e.key == pygame.K_c:
				if cadricula:
					cadricula = False
				else:
					cadricula = True
				modificacion = True
					
		#PAUSA
		
			if e.key == pygame.K_SPACE:
				if pausa:
					pausa = False
				else:
					pausa = True
				modificacion = True
					
		#ELIMINACION DA VIDA
		
			if e.key == pygame.K_DELETE:
				for i in range(len(lista_cadros)):
					lista_cadros[i] = 0
				modificacion = True
				
		#AUMENTO E DISMINUCION DA VELOCIDADE
		
			if e.key == pygame.K_RIGHT or e.key == pygame.K_LEFT:
			
				if e.key == pygame.K_RIGHT:
					VELOCIDADE += 1
				else:
					VELOCIDADE -= 1
			
				VELOCIDADE = min(VELOCIDADE,5)
				VELOCIDADE = max(VELOCIDADE,0)
				
				if VELOCIDADE == 0:
					CONT_VELOCIDADE_TOTAL = 60
				elif VELOCIDADE == 1:
					CONT_VELOCIDADE_TOTAL = 30
				elif VELOCIDADE == 2:
					CONT_VELOCIDADE_TOTAL = 10
				elif VELOCIDADE == 3:
					CONT_VELOCIDADE_TOTAL = 5
				elif VELOCIDADE == 4:
					CONT_VELOCIDADE_TOTAL = 2
				elif VELOCIDADE == 5:
					CONT_VELOCIDADE_TOTAL = 1
						
	#EVENTOS ESPECIALES
		
		#QUIT
	
		if e.type == pygame.QUIT:
			pygame.display.quit()
			ON = False
	
	reloj.tick(60)
		
