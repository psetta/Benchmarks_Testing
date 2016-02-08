# -*- coding: utf-8 -*-

import sys
import random

def sort_casilleros(list):
	dict_casilleros = {}
	salida = []
	for n in list:
		if n in dict_casilleros:
			dict_casilleros[n] += 1
		else:
			dict_casilleros[n] = 1
	for n in dict_casilleros:
		for i in range(dict_casilleros[n]):
			salida.append(n)
	return salida
			
cont = int(sys.argv[1])			
lista = [random.randint(0,cont) for x in range(cont)]

sort_casilleros(lista)