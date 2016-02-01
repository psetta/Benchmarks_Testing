# -*- coding: utf-8 -*-

import subprocess
import time

def time_exec(comando):

	init_time = time.time()
	
	try:
		error = subprocess.check_output(comando, stderr=subprocess.STDOUT, shell=True)
	except:
		error = 1

	end_time = time.time()

	if not error:
		return str(end_time-init_time)+"s"
	else:
		return "error"