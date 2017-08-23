#!/usr/bin/env python3
import socket as so;
import sys;
HOST = "irc.sorcery.net"
PORT = 6667
SSL = False
NICK = "TimsPyBot"
PREFIX = ">"
channels = [ "#botwar" ];
p = PREFIX
if SSL:
	import ssl
	c = ssl.create_default_context()
	s = c.wrap_socket(so.socket(so.AF_INET), server_hostname=HOST)	
else:
	s = so.socket()
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
		if raw[3] == ":" + p + "help":
				msg("Commands: help, kick, join, quit", raw[2])
		elif raw[3] == ":" + p + "kick":
				if len(raw) > 5:
					send("KICK " + raw[2] + " " + raw[4] + " :" + raw[5])
				else:
					send("KICK " + raw[2] + " " +  raw[4] + " :kick requested by " + nick)
		elif raw[3] == ":" + p + "join":
				send("JOIN " + raw[4]) 
		elif raw[3] == ":" + p + "quit":
				send("QUIT")
				print("Quit requested by " + nick)
				sys.exit(1)
