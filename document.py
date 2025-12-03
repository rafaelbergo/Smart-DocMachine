import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

DOCUMENT_PATH = os.path.join(DATA_DIR, 'document.jpg')

def take_picture() -> bool:
    try:
        print(f"[document] Capturando foto em: {DOCUMENT_PATH}")
        # -n = sem preview
        # -t 100 = tempo de exposiÃ§Ã£o de 100ms (ajustÃ¡vel)
        result = subprocess.run(
            ['libcamera-still', '-n', '-t', '100', '-o', DOCUMENT_PATH],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"[document] Foto salva com sucesso: {DOCUMENT_PATH}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"[document] Erro libcamera:\n{e.stderr}")

    except Exception as e:
        print(f"ERRO | def take_picture | {e}")
       
    return False
    
