import RPi.GPIO as GPIO
import time
import os
import threading
from audio import playAudio, playAudio_async
from document import take_picture

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIOS_FOLDER = os.path.join(BASE_DIR, 'data', 'audios')

BUTTON_PIN = 16
LED_PIN = 26

_initialized = False
_busy = False

def _run_sequence():
    global _busy
    try:
        playAudio_async(os.path.join(AUDIOS_FOLDER, 'processando_doc.wav'))

        time.sleep(0.5)
        ok = take_picture()
        if not ok:
            print("[LEDS] Falha ao tirar foto.")
        else:
            print("[LEDS] Foto capturada com sucesso.")

        time.sleep(5)

        # Desliga LED
        GPIO.output(LED_PIN, GPIO.LOW)
        print("[LEDS] LED desligado apos captura.")

        audio_ok = playAudio(os.path.join(AUDIOS_FOLDER, 'doc_processado.wav'))
        if not audio_ok:
            print("[LEDS] Falha ao tocar 'doc_processado.wav'")
    finally:
        _busy = False

def _toggle_led(channel):
    global _busy
    if _busy:
        print("[LEDS] Codigo ja rodando, ignorando.")
        return

    _busy = True
    GPIO.output(LED_PIN, GPIO.HIGH)
    threading.Thread(target=_run_sequence, daemon=True).start()

def setup():
    global _initialized
    if _initialized:
        return
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=_toggle_led, bouncetime=300)
    _initialized = True

def cleanup():
    try:
        GPIO.remove_event_detect(BUTTON_PIN)
    except Exception:
        pass
    GPIO.cleanup()
    