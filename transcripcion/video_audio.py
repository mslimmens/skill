import os
import whisper
import subprocess
import glob
import shlex

VIDEO_FILE = "clase.mp4"
AUDIO_FILE = "audio_extraido.mp3"
TRANSCRIPT_FILE = "transcripcion_final.txt"
TMP_DIR = "chunks_audio" # Directorio para guardar los trozos de audio

# 1. Extracción de Audio eficiente (sin cargar todo el video en RAM)
# Usamos ffmpeg directamente para no saturar la memoria
if not os.path.exists(AUDIO_FILE):
    print(f"Extrayendo audio con ffmpeg...")
    cmd = f"ffmpeg -i {shlex.quote(VIDEO_FILE)} -vn -acodec libmp3lame -q:a 2 {shlex.quote(AUDIO_FILE)}"
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"ERROR al extraer audio: {e}")
        exit()

# 2. Carga del modelo (Forzamos CPU y un modelo PEQUEÑO para no agotar la RAM)
# 'tiny' es el más rápido y ligero, ideal para equipos con poca memoria.
print("Cargando Whisper (modelo tiny)...")
try:
    # Usar device="cpu" es VITAL en este escenario.
    model = whisper.load_model("tiny", device="cpu") 
except Exception as e:
    print(f"ERROR al cargar Whisper: {e}")
    exit()

# 3. Transcripción por segmentos (para clases largas)
# Si el audio es muy largo, procesarlo todo a la vez agota la RAM.
# Lo dividiremos en trozos pequeños.

if not os.path.exists(TMP_DIR):
    os.makedirs(TMP_DIR)

print("Dividiendo el audio en trozos pequeños para ahorrar memoria...")
# Dividimos en trozos de 10 minutos (600 segundos)
cmd_split = f"ffmpeg -i {shlex.quote(AUDIO_FILE)} -f segment -segment_time 600 -c copy {shlex.quote(TMP_DIR)}/chunk_%03d.mp3"
subprocess.run(cmd_split, shell=True, check=True)

# Lista de todos los trozos de audio generados
audio_chunks = sorted(glob.glob(os.path.join(TMP_DIR, "*.mp3")))
full_transcript = ""

print(f"Transcribiendo {len(audio_chunks)} trozos (esto puede tardar, por favor espera)...")
for chunk in audio_chunks:
    print(f"Procesando: {os.path.basename(chunk)}...")
    # fp16=False es VITAL en CPU para evitar errores y exceso de consumo.
    result = model.transcribe(chunk, fp16=False, language="es")
    full_transcript += result["text"] + "\n\n" # Añadimos espacio entre transcripciones

# 4. Guardado final
with open(TRANSCRIPT_FILE, "w", encoding="utf-8") as f:
    f.write(full_transcript)

# Limpieza: borrar los trozos temporales
print("Limpiando archivos temporales...")
for chunk in audio_chunks:
    os.remove(chunk)
os.rmdir(TMP_DIR)

print(f"¡Listo! Archivo guardado: {TRANSCRIPT_FILE}")