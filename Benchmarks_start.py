# -*- coding: utf-8 -*-

import os
import re
import time
import modulos_lanzador.timecmd as timecmd

dir_root_scrips = "scripts"
dir_root_logs = "logs"

if not os.path.exists(dir_root_scrips):
	print u"creating directory /"+dir_root_scrips+"..."
	os.mkdir(dir_root_scrips)
if not os.path.exists(dir_root_logs):
	print u"creating directory /"+dir_root_logs+"..."
	os.mkdir(dir_root_logs)

#DIRECTORIO DONDE ESTAN OS SCRIPTS A EXECUTAR
print u"dir scripts - "+dir_root_scrips+"/"
for dir in os.listdir(dir_root_scrips):
	print "\t- "+dir

print ""
dir_scripts0 = raw_input(u">>> Select script dir: "+dir_root_scrips+"/")
dir_scripts = dir_root_scrips+"/"+dir_scripts0

#LISTA DE SCRIPTS
script_list = os.listdir(dir_scripts)

#DIRECTORIO DONDE SE GARDAN OS LOGS
dir_log = dir_root_logs+"/"+dir_scripts0

if not os.path.exists(dir_log):
	os.mkdir(dir_log)

#ARGUMENTOS A PASAR AO EXECUTAR OS SCRIPTS
args_text = raw_input(u">>> Start arguments: ")
args = [int(x) for x in args_text.split(" ")]

#INCREMENTO DOS ARGUMENTOS EN CADA VOLTA
args_add_text = raw_input(u">>> Increase arguments: ")
args_add = [int(x) for x in args_add_text.split(" ")]

#VOLTAS QUE DA O BUCLE
voltas = raw_input(">>> Rounds: ")
voltas = int(voltas)

#TEMPO MÁXIMO (SEGUNDOS)
#Se un script tarda máis deixa de executarse nas seguintes voltas
tempo_max = False

#NOME DO LOG A CREAR
doc_log = "log_"+dir_scripts0+"_"+"0.xml"
cont_log = 1
while os.path.exists(dir_log+"/"+doc_log):
	doc_log = "log_"+dir_scripts0+"_"+str(cont_log)+".xml"
	cont_log += 1

log = open(dir_log+"/"+doc_log, "w")
log.write('<?xml version="1.0"?>\n')
log.write('<root>\n')

print u"Benchmarks of:"
for script in script_list:
	print "\t"+script

for volta in range(voltas):
	time.sleep(3)
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
		else:
			app = "unknown"
		
		if not app == "unknown":
			command = (app+(' ' if app else '')+dir_scripts+"/"+
						script+' '+" ".join(map(str,args)))
			time_exec = timecmd.time_exec(command)
			if not time_exec == "error":
				print "\t\tcommand: "+command
				print "\t\ttime: "+time_exec
				log.write('\t\t<script nome="'+script+'">\n')
				log.write('\t\t\t'+time_exec)
				log.write('\t\t</script>\n')
				if tempo_max and float(time_exec.split("s")[0]) > tempo_max:
					script_list.remove(script)
					
			else:
				print "\t\tcommand: "+command
				print "\t\tCommand ERROR"
		else:
			print u"\t\tUnknown file extension: "+script
		
		time.sleep(1.5)
		
	log.write('\t</execucion>\n')
	args = [x+y for x,y in zip(args,args_add)]
	
	
log.write('</root>')
log.close()