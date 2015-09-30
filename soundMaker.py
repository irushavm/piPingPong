#!/usr/bin/python

import os
from socket import *
import time
import pygame

def getMessage(time):
	data = None
	try:
		socket.settimeout(time)
		data = socket.recv(1024)
	except:
		pass
	socket.settimeout(None)
	return data

MY_IP = "10.0.0.21"
UDP_IP = "10.0.0.22"
UDP_PORT = 6000
BUFFER_SIZE = 512


pygame.mixer.init()

#inGameSound = pygame.mixer.Sound("InGame.mp3")
#loseSound = pygame.mixer.Sound("Lose.mp3")
socket = socket(AF_INET, SOCK_DGRAM)
socket.bind((MY_IP, UDP_PORT))

while True:
	try:	
		data = getMessage(0.5)
		print "received:", data
		if data == "gamestart":
			pygame.mixer.music.load("InGame.mp3")
			pygame.mixer.music.play()
			#pygame.mixer.stop()
			#inGameSound.play(loops=-1)
		elif data == 'gameover':
			pygame.mixer.music.stop()
			pygame.mixer.music.load("Lose.mp3")
			pygame.mixer.music.play()
			while pygame.mixer.music.get_busy():
				continue
			break
			#loseSound.play()
	except (KeyboardInterrupt,SystemExit):
		sys.exit()
		break
