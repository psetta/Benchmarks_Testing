# -*- coding: utf-8 -*-

import sys
import random

def sort_bubble(list):
	menor = 0
	maior = len(list)-1
	while True:
		cambio = True
		for i in range(menor,maior,1):
			if list[i] > list[i+1]:
				list[i], list[i+1] = list[i+1], list[i]
				cambio = False
		for i in range(maior,menor,-1):
			if list[i] < list[i-1]:
				list[i], list[i-1] = list[i-1], list[i]
				cambio = False
		maior -= 1
		menor += 1
		if cambio:
			return list
			
cont = int(sys.argv[1])			
lista = [random.randint(0,cont) for x in range(cont)]

print sort_bubble(lista)