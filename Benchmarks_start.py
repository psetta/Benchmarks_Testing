# -*- coding: utf-8 -*-

import sys
import os
import re
import time
import modulos_lanzador.timecmd as timecmd

dir_root_scrips = "scripts"
dir_root_logs = "logs"

#GARDAR LOGS COMA ('XML' ou 'JSON'):
formato_log = "xml"

if formato_log == "json":
	import json
elif formato_log == "xml":
	pass
else:
	print "ERROR - Indica formato de log"
	sys.exit()

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
if args_text:
	args = [int(x) for x in args_text.split(" ")]
else:
	args = False

#INCREMENTO DOS ARGUMENTOS EN CADA VOLTA
args_add_text = raw_input(u">>> Increase arguments: ")
if args_add_text:
	args_add = [int(x) for x in args_add_text.split(" ")]

#VOLTAS QUE DA O BUCLE
voltas = raw_input(">>> Rounds: ")
while not voltas:
	voltas = raw_input(">>> Rounds: ")
	
try:
	voltas = int(voltas)
except:
	print "ERROR - require integer"

#TEMPO MÁXIMO (SEGUNDOS)
#Se un script tarda máis deixa de executarse nas seguintes voltas
tempo_max = False

#NOME DO LOG A CREAR
doc_log = "log_"+dir_scripts0+"_"+"0."+formato_log
cont_log = 1
while os.path.exists(dir_log+"/"+doc_log):
	doc_log = "log_"+dir_scripts0+"_"+str(cont_log)+"."+formato_log
	cont_log += 1

if formato_log == "xml":
	xml_execucions = ""
	xml_execucions += '<?xml version="1.0"?>\n'
	xml_execucions += '<root>\n'
else:
	json_execucions = {}
	for script in script_list:
		json_execucions[script] = []

print u"Benchmarks of:"
for script in script_list:
	print "\t"+script

for volta in range(voltas):
	time.sleep(3)
	if args:
		print ">>> "+ str(volta+1)+"/"+str(voltas)," args: "+" ".join(map(str,args))
	else:
		print ">>> "+ str(volta+1)+"/"+str(voltas)
	execution_string = ""
	if args:
		for arg in range(len(args)):
			execution_string += ' arg'+str(arg)+'="'+str(args[arg])+'"'
		
	if formato_log == "xml":
		xml_execucions += '\t<execucion'+execution_string+'>\n'
		
	for script in script_list:
		print "\t"+script
		formato = re.findall("\..[^\.]+$",script)[0]
		
		#FORMATOS DE ARQUIVOS QUE SE PODEN EXECUTAR
		#PYTHON
		if formato in [".py",".pyc",".pyw"]:
			app = "python"
		#RACKET
		elif formato == ".rkt":
			app = "racket"
		#JAVA
		elif formato == ".jar":
			app = "java -jar"
		#EXECUTABLE DE WINDOWS .EXE
		elif formato == ".exe":
			app = "start /WAIT"
		else:
			app = "unknown"
		
		if not app == "unknown":
			if args:
				command = (app+(' ' if app else '')+dir_scripts+"/"+
						script+' '+" ".join(map(str,args)))
			else:
				command = app+(' ' if app else '')+dir_scripts+"/"+script
			time_exec = timecmd.time_exec(command)
			if not time_exec == "error":
				print "\t\tcommand: "+command
				print "\t\ttime: "+time_exec
				
				if formato_log == "xml":
					xml_execucions += '\t\t<script nome="'+script+'">\n'
					xml_execucions += '\t\t\t'+time_exec
					xml_execucions += '\t\t</script>\n'
				else:
					if args:
						json_execucions[script].append([args[:],time_exec])
					else:
						json_execucions[script].append([args,time_exec])
						
				if tempo_max and float(time_exec.split("s")[0]) > tempo_max:
					script_list.remove(script)
					
			else:
				print "\t\tcommand: "+command
				print "\t\tCommand ERROR"
		else:
			print u"\t\tUnknown file extension: "+script
		
		time.sleep(2)
	
	if formato_log == "xml":
		xml_execucions += '\t</execucion>\n'
	if args:
		args = [x+y for x,y in zip(args,args_add)]

log = open(dir_log+"/"+doc_log, "w")

if formato_log == "xml":
	xml_execucions += '</root>'
	log.write(xml_execucions)
else:
	json_log = json.dump(json_execucions,log)
	
log.close()