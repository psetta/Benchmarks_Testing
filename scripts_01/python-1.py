# -*- coding: utf-8 -*-

import random
import sys

def eliminar_elementos_unicos(lista):
	#CREAMOS DICCIONARIO VACIO
	d = {}
	#RECORREMOS A LISTA DE NUMEROS
	for i in lista:
		#SE O NUMERO NON EXISTE COMO CLAVE DO DICCIONARIO CREASE CO VALOR 1,
		# SE EXISTE SUMASELLE 1.
		d[i] = d[i]+1 if i in d else 1
		#RECORREMOS A LISTA E DEVOLVEMOS AS CLAVES QUE TEÑAN UN VALOR DIFERENTE A 1
	return [i for i in lista if d[i] != 1]
	
rango = int(sys.argv[1])
num = int(sys.argv[2])

lista_entrada = [random.randint(0,rango) for x in range(num)]
	
eliminar_elementos_unicos(lista_entrada)