#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import random

def ordenada(list):
	for n in range(len(list)-1):
		if list[n] > list[n+1]:
			return False
	return True

def quicksort(lista):
    if len(lista) > 1:
        medio = len(lista) // 2
        pivote = lista[medio]
        esquerda = [e for i, e in enumerate(lista)
                    if i != medio and e <= pivote]
        dereita = [e for i, e in enumerate(lista)
                   if i != medio and e > pivote]
        return quicksort(esquerda)+[pivote]+quicksort(dereita)
    return lista

cont = int(sys.argv[1])
lista = [random.randint(0,cont) for x in range(cont)]

assert quicksort(lista) == sorted(lista)
