#!/usr/bin/python

import os
from socket import *
import time
import pygame

def getMessage(socket,time):
	data = None
	try:
		socket.settimeout(time)
		data = socket.recv(1024)
	except:
		pass
	socket.settimeout(None)
	return data

MY_IP = "10.0.0.21"

#IP and Port for server
SERVER_IP = "10.0.0.22"	
UDP_PORT = 

#For UDP Communications
BUFFER_SIZE = 512


pygame.mixer.init()

#Set up socket to listen in at specified port
socket = socket(AF_INET, SOCK_DGRAM)
socket.bind((MY_IP, UDP_PORT))

#Send init status to server
socket.sendto("sound:ready", (UDP_IP, UDP_PORT))

while True:
	try:	
		#Get message from server
		data = getMessage(socket,0.5)
		print "received:", data

		#If the game has started
		if data == "gamestart":
			#Stop all sounds and Load and play ingame sound
			pygame.mixer.music.stop()
			pygame.mixer.music.load("InGame.mp3")
			pygame.mixer.music.play()

		elif data == "gameover":
			#Stop all sounds and play Lose sound
			pygame.mixer.music.stop()
			pygame.mixer.music.load("Lose.mp3")
			pygame.mixer.music.play()
			#Wait till sound is done playing
			while pygame.mixer.music.get_busy():
				continue
			break
	#Exception handler for Keyboard Interrupts
	except (KeyboardInterrupt,SystemExit):
		sys.exit()
		break
