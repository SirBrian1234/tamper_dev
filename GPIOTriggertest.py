import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print('Waiting to engage lock in GPIO input 18')
while True:
    input_state = GPIO.input(18)
   
    if input_state == False:
        print('Lock engaged')
        break
    else:
	time.sleep(0.2)

while True:
    input_state = GPIO.input(18)
    if input_state == True:
        print('Lock released')
	break
    else:
	time.sleep(0.2)


