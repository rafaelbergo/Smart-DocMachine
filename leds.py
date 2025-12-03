# leds.py
import RPi.GPIO as GPIO
import time
import os
import threading
from audio import playAudio, start_recording, stop_recording, take_picture, text_to_audio, read_document, audio_to_text, ask_question, playAudio_async

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIOS_FOLDER = os.path.join(BASE_DIR, 'data', 'audios')
DATA_DIR = os.path.join(BASE_DIR, 'data')
AUDIO_PATH_QUESTION = os.path.join(DATA_DIR, 'audio_gravado.wav')  # arquivo de saada da gravaao
AUDIO_PATH_RESPONSE = os.path.join(DATA_DIR, 'resposta.wav')

BUTTON_PHOTO_PIN = 16   # botao que dispara foto/fluxo LED + audios
BUTTON_REC_PIN   = 12   # NOVO: botao que grava enquanto estiver pressionado
LED_PIN = 26

_initialized = False
_busy = False  # evita reentrancia da sequancia de foto

def _run_sequence(channel = None):
    """
    LED on -> 'processando' (async) -> 0.5s -> foto -> 5s -> LED off -> 'doc_processado' (sync)
    """
    try:
        #playAudio_async(os.path.join(AUDIOS_FOLDER, 'processando_doc.wav'))
        playAudio_async(os.path.join(AUDIOS_FOLDER, 'processando_documento.wav'))
        
        GPIO.output(LED_PIN, GPIO.HIGH)

        ok = take_picture()
        print("[leds] Foto capturada." if ok else "[leds] Falha ao tirar foto.")

        
        GPIO.output(LED_PIN, GPIO.LOW)
        print("[leds] LED desligado apas captura.")
        
        if not read_document():
            print('erro read_document')
            return
        
        playAudio(os.path.join(AUDIOS_FOLDER, 'documento_processado_sucesso.wav'))
    except: 
        print(f'ERRO | def _run_sequence | {str(e)}')


def _toggle_photo_sequence(channel):
    global _busy
    if _busy:
        print("[leds] Sequancia em andamento; ignorando novo toque.")
        return
    _busy = True
    GPIO.output(LED_PIN, GPIO.HIGH)
    print("[leds] LED ligado! Iniciando sequancia de foto.")
    threading.Thread(target=_run_sequence, daemon=True).start()
    

def _record_edge(channel):
    """
    Callback para o botao de gravaao (BCM 12).
    FALLING (pressionou)  -> inicia gravaao
    RISING  (soltou)      -> para gravaao
    """
    level = GPIO.input(BUTTON_REC_PIN)
    if level == GPIO.LOW:
        # pressionado
        print("[leds] botao REC pressionado -> start_recording")
        start_recording(AUDIO_PATH_QUESTION, sample_rate=44100, channels=1)
    else:
        # solto
        print("[leds] botao REC solto -> stop_recording")
        stop_recording()
        text = audio_to_text(AUDIO_PATH_QUESTION)
        if not text:
            return
        
        responsta_ia = ask_question(text)
        #responsta_ia = 'eu sou sofia, uma assistente de inteligencia aritificial do projeto smart-doc-machine. fui criada por alunos de engenharia da computacao para ajudar pessoas a entenderem documentos.'

        if not responsta_ia:
            return
                
        text_to_audio(responsta_ia, AUDIO_PATH_RESPONSE)
        
        playAudio(AUDIO_PATH_RESPONSE)
        

def setup():
    global _initialized
    if _initialized:
        return

    GPIO.setmode(GPIO.BCM)

    # botao da foto
    GPIO.setup(BUTTON_PHOTO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_PHOTO_PIN, GPIO.FALLING,
                          callback=_run_sequence, bouncetime=300)

    # botao de gravaao (segurar)
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
    # garante parar gravaao se ainda ativa
    try:
        stop_recording()
    except Exception:
        pass
    GPIO.cleanup()
    print("[leds] cleanup executado.")
