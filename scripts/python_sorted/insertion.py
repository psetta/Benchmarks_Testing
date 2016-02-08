# -*- coding: utf-8 -*-

import sys
import random

def sort_insertion(list):
	for i in range(1,len(list)):
		for x in range(i):
			if list[i] <= list[x]:
				list.insert(x,list[i])
				del list[i+1]
	return list
			
			
cont = int(sys.argv[1])			
lista = [random.randint(0,cont) for x in range(cont)]

sort_insertion(lista)