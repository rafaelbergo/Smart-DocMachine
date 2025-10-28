import os, time, json, subprocess, requests
import whisper
from paddleocr import PaddleOCR
from gtts import gTTS
import sounddevice as sd
import soundfile as sf
from dotenv import load_dotenv
from audio import *
import leds

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FOLDER = BASE_DIR
DOCUMENT_PATH = os.path.join(FOLDER, 'document.jpg')
AUDIOS_FOLDER = os.path.join(FOLDER, 'data', 'audios')

load_dotenv()
api_key = os.getenv('API_KEY') or ""
api_base_endpoint = os.getenv('API_ENDPOINT') or ""
api_url = api_base_endpoint + api_key

AUDIO_PATH_RESPONSE = os.path.join(FOLDER, 'audio_offline.mp3')
AUDIO_PATH_QUESTION = os.path.join(FOLDER, 'audio_gravado.wav')
audio_test = os.path.join(AUDIOS_FOLDER, 'processando_doc.wav')

if __name__ == '__main__':
    try:
        leds.setup()
        print("[MAIN] iniciado.")
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Programa interrompido.")
    finally:
        leds.cleanup()
