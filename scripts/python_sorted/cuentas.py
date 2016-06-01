# -*- coding: utf-8 -*-

import sys
import random

def sort_casilleros(list):
	min_l = min(list)
	max_l = max(list)
	list_casilleros = [0 for x in range(min_l,max_l+1)]
	salida = []
	for n in list:
		list_casilleros[n-min_l] += 1
	ini = min_l
	for n in list_casilleros:
		if n:
			for x in range(n):
				salida.append(ini)
		ini += 1
	return salida
			
cont = int(sys.argv[1])			
lista = [random.randint(0,cont) for x in range(cont)]

sort_casilleros(lista)