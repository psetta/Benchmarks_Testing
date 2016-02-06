# -*- coding: utf-8 -*-

import sys
import random

def sort_bubble(list):
	while True:
		cambio = True
		for i in range(len(list)-1):
			if list[i] > list[i+1]:
				list[i], list[i+1] = list[i+1], list[i]
				cambio = False
		if cambio:
			return list
			
cont = int(sys.argv[1])			
lista = [random.randint(0,10000) for x in range(cont)]

print sort_bubble(lista)