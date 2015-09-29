#!/usr/bin/python

import pifacedigitalio as p
import threading 
import os
from socket import *
import time

def getMessage(time):
	data = None
	try:
		socket.settimeout(time)
		data = socket.recv(1024)
	except:
		pass
	socket.settimeout(None)
	return data

MY_IP = "10.0.0.24"
UDP_IP = "10.0.0.22"
UDP_PORT = 6000
BUFFER_SIZE = 512

pfd = p.PiFaceDigital()

socket = socket(AF_INET, SOCK_DGRAM)
socket.bind((MY_IP, UDP_PORT))

pfd.leds[7].turn_on()
while True:
	
	while pfd.switches[0].value == 1:
		pfd.leds[7].turn_off()
		print "punishment"
		time.sleep(1)
		pfd.leds[7].turn_on()
	data = getMessage(0.3)
	print "received:", data
	if data == "your turn":
		while True:
			if pfd.switches[0].value == 1:
				socket.sendto("click", (UDP_IP, UDP_PORT))
				break
			else:
				if getMessage(0.01) == "turn over":
					break
				elif data == "gameover":
					break
	if data == "gameover":
		break				
				
