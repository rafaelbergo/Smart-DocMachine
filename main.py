import whisper
from paddleocr import PaddleOCR
from gtts import gTTS
import subprocess
import os, requests, json
import sounddevice as sd
import soundfile as sf
from dotenv import load_dotenv

from audio import *

load_dotenv()
api_key = os.getenv('API_KEY')
api_base_endpoint = os.getenv('API_ENDPOINT')

api_url = api_base_endpoint + api_key

FOLDER = os.getcwd()
DOCUMENT_PATH = os.path.join(FOLDER, 'document.jpg')
AUDIOS_FOLDER = os.path.join(FOLDER, 'data', 'audios')



AUDIO_PATH_RESPONSE = os.path.join(FOLDER, 'audio_offline.mp3')
AUDIO_PATH_QUESTION = os.path.join(FOLDER, 'audio_gravado.wav')
audio_test = os.path.join(AUDIOS_FOLDER, 'processando_doc.wav')

if __name__ == '__main__':
    playAudio(os.path.join(AUDIOS_FOLDER, 'processando_doc.wav'))
    #text_to_audio("Processando documento, aguarde.", audio_test)
