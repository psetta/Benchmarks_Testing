# -*- coding: utf-8 -*-

import os
import re
import time

#DIRECTORIO DONDE SE GARDAN OS LOGS
dir_log = "logs"

#DIRECTORIO DONDE ESTAN OS SCRIPTS A EXECUTAR
dir_scripts = "scripts"

script_list = os.listdir("scripts")

#ARGUMENTOS A PASAR AO EXECUTAR OS SCRIPTS
args = [1000000, 5000000]

#VOLTAS QUE DA O BUCLE
voltas = 1

#INCREMENTO DOS ARGUMENTOS EN CADA VOLTA
incremento = [0, 100000]

#NOME DO LOG A CREAR
doc_log = "log_0.xml"
cont_log = 1
while os.path.exists(dir_log+"/"+doc_log):
	doc_log = "log_"+str(cont_log)+".xml"
	cont_log += 1

log = open(dir_log+"/"+doc_log, "w")
log.write('<?xml version="1.0"?>\n')
log.write('<root>\n')

print u"Medindo tempos de execucións de :"
for script in script_list:
	print "\t"+script

for volta in range(voltas):
	time.sleep(5)
	print ">>> "+ str(volta+1)+"/"+str(voltas)," args: "+" ".join(map(str,args))
	execution_string = ""
	for arg in range(len(args)):
		execution_string += ' arg'+str(arg)+'="'+str(args[arg])+'"'
	log.write('\t<execucion'+execution_string+'>\n')
	for script in script_list:
		
		print "\t"+script
	
		formato = re.findall("\..[^\.]+$",script)[0]
		
		if formato == ".py":
			app = "python"
		elif formato == ".rkt":
			app = "racket"
		elif formato == ".jar":
			app = "java -jar"
		elif formato == ".exe":
			app = "start /WAIT"
		
		command = 'python timecmd.py "'+app+(' ' if app else '')+dir_scripts+"/"+script+' '+" ".join(map(str,args))+'"'
		time_exec = os.popen(command).read()
		print "\t\t"+command
		print "\t\t"+time_exec,
		
		log.write('\t\t<script nome="'+script+'">\n')
		log.write('\t\t\t'+time_exec)
		log.write('\t\t</script>\n')
		
		time.sleep(3)
		
	log.write('\t</execucion>\n')
	args = [x+y for x,y in zip(args,incremento)]
	
	
log.write('</root>')
log.close()