import RPi.GPIO as GPIO

def button_callback(channel): # Funzione che verrà chiamata al verificarsi di un evento
	print("Bottone Premuto")

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # Imposta la numerazione fisica dei pin
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Imposta il pin 8 come input e lo imposta inizialmente ad off

GPIO.add_event_detect(8, GPIO.RISING, callback=button_callback) # Aggiunge la funzione button_callback all'evento legato al pin 8

message = input("Press enter to quit\n\n")
GPIO.cleanup()
