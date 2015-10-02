#!/usr/bin/python

import pifacedigitalio as p
import threading 
import os
from socket import *
import time

#Function for getting data using UDP
def getMessage(socket,time):
	data = None
	try:
		socket.settimeout(time)
		data = socket.recv(1024)
	except:
		pass
	socket.settimeout(None)
	return data



def main():

	#Local static IP
	MY_IP = "10.0.0.24" 
	
	#Server IP and Common Port
	UDP_IP = "10.0.0.22"
	UDP_PORT = 6000

	#For UDP Communications
	BUFFER_SIZE = 512


	#Setup socket server on specified IP and Port
	socket = socket(AF_INET, SOCK_DGRAM)
	socket.bind((MY_IP, UDP_PORT))
	#Send init message to server
	socket.sendto("player1:ready", (UDP_IP, UDP_PORT))

	#Setup and turn on LED indicator for player button
	pfd = p.PiFaceDigital()
	pfd.leds[7].turn_on()


	while True:
		#If switch is already pressed continuously, deny sending click messages to server	
		while pfd.switches[0].value == 1:
			pfd.leds[7].turn_off()
			print "punishment"
			time.sleep(1)
			pfd.leds[7].turn_on()

		#Get message from server
		data = getMessage(socket,0.3)
		print "received:", data
		
		#If it is current player's turn
		if data == "your turn":
			while True:

				#Send a click message to server when button is pressed
				if pfd.switches[0].value == 1:
					socket.sendto("player1:click", (UDP_IP, UDP_PORT))
					break
				else:
					#Check if you successfully sent a click message
					if getMessage(socket,0.01) == "turn over":
						break
					#Check for game over status from server
					elif data == "gameover":
						break

		#Check for game over status from server
		if data == "gameover":
			break				
				

if __name__ == "__main__":
    main()