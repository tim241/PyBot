#!/usr/bin/env python3
import socket as so;
import sys;
import requests;
import html;
from urllib.parse import urlsplit
HOST = "irc.freenode.net"
PORT = 6697
SSL = True
JOIN = True
NICK = "TimsPyBot"
channels = [ "#botwar" ];
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
def GetTitle(link, rec):
	try:
		domain = "{0.scheme}://{0.netloc}/".format(urlsplit(link))
		hearders = {'headers':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0'}
		title = requests.get(link, headers=hearders).text
		msg("[ " + html.unescape(title[title.find('<title>') + 7 : title.find('</title>')]) + " ] - " + domain, rec)
	except:
		print("Invalid link!")
send("NICK " + NICK)
send("USER " + NICK + " 0 * :" + NICK)
while True:
	data = s.recv(1024).decode()
	raw = data.split()
	print(data)
	if len(raw) > 1:
		if raw[0] == "PING":
			send("PONG " + raw[1])
		if raw[1].isdigit() & JOIN:
			JOIN = False
			for channel in channels:
				send("JOIN " + channel)
	if len(raw) > 3:
		if raw[3].startswith(":https://"):
			GetTitle(raw[3][1:], raw[2])
		elif raw[3].startswith(":http://"):
			GetTitle(raw[3][1:], raw[2])
		elif raw[3].startswith(":www."):
			GetTitle(raw[3][1:], raw[2])
