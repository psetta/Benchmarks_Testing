# -*- coding: utf-8 -*-

import subprocess
import time

def time_exec(comando):

	init_time = time.time()
	
	try:
		execution = subprocess.check_output(comando, stderr=subprocess.STDOUT, shell=True)
	except:
		execution = "error"

	end_time = time.time()

	if not execution == "error":
		return str(end_time-init_time)+"s"
	else:
		return execution