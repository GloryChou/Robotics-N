#python 2.7
#date:2016/06/23
#Auth:Robotics N
#test.py
#test gpio via python

import os
import time

inSenLeftPin=17
inSenRightPin=18

Moto1Pin1=198
Moto1Pin2=199
Moto2Pin1=200
Moto2Pin2=201

HIGH = 1
LOW = 0

'''
    Descriptions of Obstacles State:
	1: left: none,    right:none
	2: left: exist,   right:none
	3: left: none,    right:exist
	4: left: exist,   right:exist
'''
OBSTACLES_STATE1 = 1
OBSTACLES_STATE2 = 2
OBSTACLES_STATE3 = 3
OBSTACLES_STATE4 = 4

#Setup pinMode
def gpioSetup():
	# open export ports
	# infrared
	os.system("echo "+str(inSenLeftPin)+" > /sys/class/gpio/export")
	os.system("echo "+str(inSenRightPin)+" > /sys/class/gpio/export")
	# Motor
	os.system("echo "+str(Moto1Pin1)+" > /sys/class/gpio/export")
	os.system("echo "+str(Moto1Pin2)+" > /sys/class/gpio/export")
	os.system("echo "+str(Moto2Pin1)+" > /sys/class/gpio/export")
	os.system("echo "+str(Moto2Pin2)+" > /sys/class/gpio/export")

	# mode definition
	os.system("echo 'in' > /sys/class/gpio/gpio"+str(inSenLeftPin)+"/direction")
	os.system("echo 'in' > /sys/class/gpio/gpio"+str(inSenRightPin)+"/direction")
	
	os.system("echo 'in' > /sys/class/gpio/gpio"+str(Moto1Pin1)+"/direction")
	os.system("echo 'out' > /sys/class/gpio/gpio"+str(Moto1Pin2)+"/direction")
	os.system("echo 'in' > /sys/class/gpio/gpio"+str(Moto2Pin1)+"/direction")
	os.system("echo 'out' > /sys/class/gpio/gpio"+str(Moto2Pin2)+"/direction")

# clean all port
def gpioClean():
	os.system("echo "+str(inSenLeftPin)+" > /sys/class/gpio/unexport")
	os.system("echo "+str(inSenRightPin)+" > /sys/class/gpio/unexport")
	# Motor
	os.system("echo "+str(Moto1Pin1)+" > /sys/class/gpio/unexport")
	os.system("echo "+str(Moto1Pin2)+" > /sys/class/gpio/unexport")
	os.system("echo "+str(Moto2Pin1)+" > /sys/class/gpio/unexport")
	os.system("echo "+str(Moto2Pin2)+" > /sys/class/gpio/unexport")

# Motor Control
def setLevel(m11,m12,m21,m22):
	os.system("echo "+str(m11)+" > /sys/class/gpio/gpio"+str(Moto1Pin1)+"/direction")
	os.system("echo "+str(m12)+" > /sys/class/gpio/gpio"+str(Moto1Pin2)+"/direction")
	os.system("echo "+str(m21)+" > /sys/class/gpio/gpio"+str(Moto2Pin1)+"/direction")
	os.system("echo "+str(m22)+" > /sys/class/gpio/gpio"+str(Moto2Pin2)+"/direction")

def Forward():
	setLevel(HIGH,LOW,HIGH,LOW)
	
def Backward():
	setLevel(LOW,HIGH,LOW,HIGH)

def Stop():
	setLevel(LOW,LOW,LOW,LOW)

def Left():
	setLevel(LOW,HIGH,HIGH,LOW)

def Right():
	setLevel(HIGH,LOW,LOW,HIGH)

def getState():
	leftsensor = os.system("cat /sys/class/gpio/gpio"+str(inSenLeftPin)+"/direction")
	rightsensor = os.system("cat /sys/class/gpio/gpio"+str(inSenRightPin)+"/direction")

	if leftsensor == LOW and rightsensor == LOW:
		return OBSTACLES_STATE1
	elif leftsensor == HIGH and rightsensor == LOW:
		return OBSTACLES_STATE2
	elif leftsensor == LOW and rightsensor == HIGH:
		return OBSTACLES_STATE3
	elif leftsensor == HIGH and rightsensor == HIGH:
		return OBSTACLES_STATE4

def execMoving(cur_state, pre_state):
	if cur_state != pre_state:
		if cur_state == OBSTACLES_STATE1:
			Forward()
		elif cur_state == OBSTACLES_STATE2:
			Right()
		elif cur_state == OBSTACLES_STATE3:
			Left()
		elif cur_state == OBSTACLES_STATE4:
			Stop()
			while getState() != OBSTACLES_STATE1:
				Right()

if __name__ == '__main__':
	#clean the pinport
	gpioClean()
	#setup the pinport	
	gpioSetup()

	cur_state = OBSTACLES_STATE1 # current state
	pre_state = OBSTACLES_STATE4 # previous state

	try:
		print("This is a demo of Smart car Control Program")
		# get current state of infrared sensor
		cur_state = getState()

		# start controlling motor after both of infrared sensors are idle
		while cur_state != OBSTACLES_STATE1:
			cur_state = OBSTACLES_STATE1

		while True:
			cur_state = getState()
			execMoving(cur_state, pre_state)
			pre_state = cur_state
		
	except KeyboardInterrupt:
		print("quit!")
		gpioClean()
		exit()