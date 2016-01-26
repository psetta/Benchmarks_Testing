# -*- coding: utf-8 -*-

import os
import sys
import time

init_time = time.time()

if sys.argv[1]:
	comando = sys.argv[1]
	execucion = os.system(comando)

end_time = time.time()

print str(end_time-init_time)+"s"
