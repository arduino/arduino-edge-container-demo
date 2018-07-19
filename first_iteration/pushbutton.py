import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # Imposta la numerazione fisica dei pin
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Imposta il pin 8 come input e lo imposta inizialmente ad off

while True:
	if GPIO.input(8) == GPIO.HIGH: # Quando viene premuto il tasto
		print("Bottone premuto")
