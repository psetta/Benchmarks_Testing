# -*- coding: utf-8 -*-

import sys
import random

def quicksort(list):
	if len(list) > 1:
		pivote_n_0 = len(list)/2
		pivote_n = pivote_n_0
		pivote = list[pivote_n]
		parte1 = [list[x] for x in range(0,pivote_n)]
		parte2 = [list[x] for x in range(pivote_n+1,len(list))]
		parte1_cont = 0
		for n in range(len(parte1)):
			e = parte1[n-parte1_cont]
			if e > pivote:
				parte2.append(e)
				del parte1[n-parte1_cont]
				parte1_cont += 1
		parte2_cont = 0
		for n in range(len(parte2)):
			e = parte2[n-parte2_cont]
			if e < pivote:
				parte1.append(e)
				del parte2[n-parte2_cont]
				parte2_cont += 1
		return quicksort(parte1)+[pivote]+quicksort(parte2)
	return list
			
cont = int(sys.argv[1])			
lista = [random.randint(0,cont) for x in range(cont)]

quicksort(lista)