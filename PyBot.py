#!/usr/bin/env python3
import socket;
HOST = "irc.freenode.net"
PORT = 6667
NICK = "TimsPyBot"
channels = [ "#botwar" ];
s = socket.socket()
s.connect((HOST, PORT))
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
