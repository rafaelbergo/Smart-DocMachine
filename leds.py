import RPi.GPIO as GPIO
import time

# Definir o modo de numeracao dos pinos
GPIO.setmode(GPIO.BCM)

# Definir os pinos
button_pin = 16  # Pino do botao (GPIO 16)
led_pin = 26     # Pino do MOSFET (GPIO 26)

# Configuraco do botao (entrada com resistor de pull-up interno)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Configuracao do pino de controle do MOSFET (sai­da)
GPIO.setup(led_pin, GPIO.OUT)

# Variavel para armazenar o estado da fita de LED
led_state = False

# Funcao para alternar o estado do LED
def toggle_led(channel):
    global led_state
    led_state = not led_state  # Alterna o estado
    if led_state:
        GPIO.output(led_pin, GPIO.HIGH)  # Liga o LED
        print("Fita de LED ligada!")
    else:
        GPIO.output(led_pin, GPIO.LOW)   # Desliga o LED
        print("Fita de LED desligada!")

# Configura a interrupcao para o botaoo (detecta a transicao de "pressionado")
GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=toggle_led, bouncetime=300)

try:
    while True:
        time.sleep(1)

finally:
    GPIO.cleanup()