from __future__ import division
import math
import sys

def factorial(x):
	resultado = 1
	for n in range(2,x+1):
		resultado *= n
	return resultado

num = int(sys.argv[1])
	
print factorial(num)
