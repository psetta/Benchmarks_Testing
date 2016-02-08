# -*- coding: utf-8 -*-

import sys
import random

def sort_gnome(list):
	while True:
		cambio = True
		i = 0
		while i < len(list)-1:
			if list[i] > list[i+1]:
				list[i], list[i+1] = list[i+1], list[i]
				cambio = False
			else:
				i += 1
		if cambio:
			return list
			
cont = int(sys.argv[1])			
lista = [random.randint(0,cont) for x in range(cont)]

sort_gnome(lista)