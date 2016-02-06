# -*- coding: utf-8 -*-

import sys
import random

def sort_other(list):
	salida = [None for x in range(len(list))]
	for i in range(len(list)):
		num = list[i]
		pos = 0
		for x in list[0:i]+list[i+1:len(list)]:
			if num > x:
				pos += 1
		while salida[pos] == num:
			pos += 1
		salida[pos] = num
	return salida
			
cont = int(sys.argv[1])			
lista = [random.randint(0,10000) for x in range(cont)]

print sort_other(lista)