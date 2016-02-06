# -*- coding: utf-8 -*-

import sys
import random
			
cont = int(sys.argv[1])			
lista = [random.randint(0,10000) for x in range(cont)]

print sorted(lista)