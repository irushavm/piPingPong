import select
from socket import *
import RPi.GPIO as GPIO
import time
import sys

DONE = False
MY_IP = "10.0.0.22"
MY_PORT = 6000

UDP_IP_P1 = "10.0.0.24"
UDP_PORT_P1 = 6000

UDP_IP_P2 = "10.0.0.23"
UDP_PORT_P2 = 6000

UDP_IP_S = "10.0.0.21"

LIGHT_DELAY = 0.5


def led_drive(reps, multiple, direction):           # define function to drive
    for i in range(reps):                      # repetitions, single or multiple
        for port_num in direction:                  # and direction
            GPIO.output(port_num, 1)                # switch on an led
            time.sleep(LIGHT_DELAY)                             # wait for ~0.11 seconds
            if not multiple:                        # if we're not leaving it on
                GPIO.output(port_num, 0)            # switch it off again


def clearMessages(socket):
	while not DONE:
		data = socket.recv(1024)
		print "cleared message"


def getMessage(socket,time):
	data = None
	addr = None
	try:
		socket.settimeout(time)
		data = socket.recv(1024)
		print data
	except:
		pass
	socket.settimeout(None)
	return data


#Main function
def main():

	player1PiReady = False
	player2PiReady = False
	soundPiReady = False

	player1hit = False
	player2hit = False

	socket = socket(AF_INET, SOCK_DGRAM)
	socket.bind((MY_IP, MY_PORT))
	socket.setblocking(1)

	round = 0

	board_type = sys.argv[-1]

	if GPIO.RPI_REVISION == 1:      # check Pi Revision to set port 21/27 correctly
    		# define ports list for Revision 1 Pi
    		ports = [25, 24, 23, 22, 21, 18, 17, 11, 10, 9, 8, 7]
	else:
    		# define ports list all others
    		ports = [25, 24, 23, 22, 27, 18, 17, 11, 10, 9, 8, 7]   
	ports_rev = ports[:]                            # make a copy of ports list
	ports_rev.reverse()                             # and reverse it as we need both

	GPIO.setmode(GPIO.BCM)                                  # initialise RPi.GPIO

	for port_num in ports:
    		GPIO.setup(port_num, GPIO.OUT)                  # set up ports for output

    #Check to ssee if all evices are initialized and ready
	while not player1PiReady or not player2PiReady or not soundPiReady:
		data = getMessage(socket,1.5)
		if data is not None and "sound:ready" in data:
			soundPiReady=True
		if data is not None and "player1:ready" in data:
			player1PiReady=True
		if data is not None and "player2:ready" in data:
			player1PiReady=True
	
	socket.sendto("gamestart",(UDP_IP_S,MY_PORT))

	while True:
		player1hit = False
		player2hit = False
		
		#move LEDs to towards player 1
		led_drive(1, 0, ports)  
		
		#Send signal to player 1 that it has to hit
		socket.sendto("your turn", (UDP_IP_P1, UDP_PORT_P1))
		print "Turn activated for Player 1"
		

		for rep in range(0,7):
			#Get response data
			data = getMessage(socket,0.2)
			print "exited method. Data: ", data

			if data is not None and "player1:click" in data:
				player1hit=True
				print "hit"
				break;

		if player1hit==False:
			print "Player 1 Lose"
			socket.sendto("You Lost!", (UDP_IP_P1, UDP_PORT_P1))
			socket.sendto("You Win!", (UDP_IP_P2, UDP_PORT_P2))
			break

		socket.settimeout(None)
		socket.sendto("turn over", (UDP_IP_P1, UDP_PORT_P1))
		getMessage(socket,0.01)

		#move LEDs to towards player 2
		led_drive(1, 0, ports_rev)
		
		#Send signal to player 2 that it has to hit
		socket.sendto("your turn", (UDP_IP_P2, UDP_PORT_P2))
		for rep in range(0,7):
			data = getMessage(socket,0.2)	
			if data is not None and "player2:click" in data:
				player2hit=True
				print "hit"
				break

		if player2hit==False:
			print "Player 2 Lose"
			socket.sendto("You Win!", (UDP_IP_P1, UDP_PORT_P1))
			socket.sendto("You Lost!", (UDP_IP_P2, UDP_PORT_P2))
			break

		socket.settimeout(None)
		socket.sendto("turn over", (UDP_IP_P2, UDP_PORT_P2))
		getMessage(socket,0.01)
		
		round+=1
		if round % 2 ==0:
			LIGHT_DELAY*=0.7

	#Send game over status to all Rpi's
	socket.sendto("gameover",(UDP_IP_P1,UDP_PORT_P1))
	socket.sendto("gameover", (UDP_IP_P2,UDP_PORT_P2))
	socket.sendto("gameover", (UDP_IP_S,MY_PORT))
	
	print "Game over. Rounds Survived: ", round


if __name__ == "__main__":
    main()