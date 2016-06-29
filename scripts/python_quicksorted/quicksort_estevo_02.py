#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import random

def quicksort(lista):
    if len(lista) > 1:
        medio = len(lista) // 2
        pivote = lista[medio]
        esquerda = []
        dereita = []
        for i, e in enumerate(lista):
            if i == medio:
                continue
            if e > pivote:
                dereita.append(e)
            else:
                esquerda.append(e)
        return quicksort(esquerda)+[pivote]+quicksort(dereita)
    return lista

cont = int(sys.argv[1])
lista = [random.randint(0,cont) for x in range(cont)]

quicksort(lista)
