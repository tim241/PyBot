#!/usr/bin/env python3
import socket;
import sys;
HOST = "irc.freenode.net"
PORT = 6667
NICK = "TimsPyBot"
channels = [ "#botwar" ];
s = socket.socket()
s.connect((HOST, PORT))
def msg(msg, rec):
	send("PRIVMSG " + rec + " :" + msg)
def send(msg):
	print(msg)
	s.sendall((msg + "\r\n").encode())
send("NICK " + NICK)
send("USER " + NICK + " 0 * :" + NICK)
while True:
	data = s.recv(1024).decode()
	raw = data.split()
	print(data)
	if raw[0] == "PING":
		send("PONG " + raw[1])
	if raw[1] == "001":
		for channel in channels:
			send("JOIN " + channel)
	if len(raw) > 3:
		nick = raw[0].split('!')[0][1:]
		if raw[3] == ":>help":
				msg("Commands: help, kick", raw[2])
		elif raw[3] == ":>kick":
				send("KICK " + raw[2] + " " +  raw[4] + " :kick requested by " + nick)
		elif raw[3] == ":>join":
				send("JOIN " + raw[4]) 
		elif raw[3] == ":>quit":
				send("QUIT")
				print("Quit requested by " + nick)
				sys.exit(1)
				

		
	
