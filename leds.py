# leds.py
import RPi.GPIO as GPIO
import time
import os
import threading
from audio import playAudio, playAudio_async, start_recording, stop_recording
from document import take_picture

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIOS_FOLDER = os.path.join(BASE_DIR, 'data', 'audios')
DATA_DIR = os.path.join(BASE_DIR, 'data')
AUDIO_PATH_QUESTION = os.path.join(DATA_DIR, 'audio_gravado.wav')  # arquivo de saída da gravação

BUTTON_PHOTO_PIN = 16   # botão que dispara foto/fluxo LED + áudios
BUTTON_REC_PIN   = 12   # NOVO: botão que grava enquanto estiver pressionado
LED_PIN = 26

_initialized = False
_busy = False  # evita reentrância da sequência de foto

def _run_sequence():
    """
    LED on -> 'processando' (async) -> 0.5s -> foto -> 5s -> LED off -> 'doc_processado' (sync)
    """
    global _busy
    try:
        playAudio_async(os.path.join(AUDIOS_FOLDER, 'processando_doc.wav'))
        time.sleep(0.5)

        ok = take_picture()
        print("[leds] Foto capturada." if ok else "[leds] Falha ao tirar foto.")

        time.sleep(5)
        GPIO.output(LED_PIN, GPIO.LOW)
        print("[leds] LED desligado após captura.")
        playAudio(os.path.join(AUDIOS_FOLDER, 'doc_processado.wav'))
    finally:
        _busy = False

def _toggle_photo_sequence(channel):
    global _busy
    if _busy:
        print("[leds] Sequência em andamento; ignorando novo toque.")
        return
    _busy = True
    GPIO.output(LED_PIN, GPIO.HIGH)
    print("[leds] LED ligado! Iniciando sequência de foto.")
    threading.Thread(target=_run_sequence, daemon=True).start()

def _record_edge(channel):
    """
    Callback para o botão de gravação (BCM 12).
    FALLING (pressionou)  -> inicia gravação
    RISING  (soltou)      -> para gravação
    """
    level = GPIO.input(BUTTON_REC_PIN)
    if level == GPIO.LOW:
        # pressionado
        print("[leds] botão REC pressionado -> start_recording")
        start_recording(AUDIO_PATH_QUESTION, sample_rate=44100, channels=1)
    else:
        # solto
        print("[leds] botão REC solto -> stop_recording")
        stop_recording()

def setup():
    global _initialized
    if _initialized:
        return

    GPIO.setmode(GPIO.BCM)

    # botão da foto
    GPIO.setup(BUTTON_PHOTO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_PHOTO_PIN, GPIO.FALLING,
                          callback=_toggle_photo_sequence, bouncetime=300)

    # botão de gravação (segurar)
    GPIO.setup(BUTTON_REC_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_REC_PIN, GPIO.BOTH,   # ambas as bordas
                          callback=_record_edge, bouncetime=50)

    # LED
    GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)

    _initialized = True
    print("[leds] setup concluido.")

def cleanup():
    try:
        GPIO.remove_event_detect(BUTTON_PHOTO_PIN)
    except Exception:
        pass
    try:
        GPIO.remove_event_detect(BUTTON_REC_PIN)
    except Exception:
        pass
    # garante parar gravação se ainda ativa
    try:
        stop_recording()
    except Exception:
        pass
    GPIO.cleanup()
    print("[leds] cleanup executado.")
