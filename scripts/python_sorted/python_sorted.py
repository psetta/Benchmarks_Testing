# -*- coding: utf-8 -*-

import sys
import random
			
cont = int(sys.argv[1])			
lista = [random.randint(0,cont) for x in range(cont)]

sorted(lista)