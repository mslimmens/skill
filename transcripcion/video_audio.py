import os
import whisper
from moviepy import VideoFileClip

VIDEO_FILE = "clase.mp4"
AUDIO_FILE = "audio_extraido.mp3"
TRANSCRIPT_FILE = "transcripcion_final.txt"

# 1. Extracción de Audio
if os.path.exists(AUDIO_FILE):
    print(f"El archivo de audio '{AUDIO_FILE}' ya existe.")
else:
    print(f"Extrayendo audio de {VIDEO_FILE}...")
    try:
        clip = VideoFileClip(VIDEO_FILE)
        clip.audio.write_audiofile(AUDIO_FILE)
        clip.close()
    except Exception as e:
        print(f"ERROR en MoviePy: {e}")
        exit()

# 2. Transcripción
print("Cargando Whisper...")
try:
    # En local (CPU) te conviene "base" o "small" para que no tarde horas
    model = whisper.load_model("base") 
except Exception as e:
    print(f"ERROR en Whisper: {e}")
    exit()

print("Transcribiendo...")
result = model.transcribe(AUDIO_FILE, fp16=False, verbose=False, language="es")

# 3. Guardado
with open(TRANSCRIPT_FILE, "w", encoding="utf-8") as f:
    f.write(result["text"])

print(f"¡Listo! Revisá el archivo {TRANSCRIPT_FILE}")