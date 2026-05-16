import os
import whisper
#from moviepy.editor import VideoFileClip # O from moviepy import VideoFileClip, si eso te funciona mejor.
from moviepy import VideoFileClip

# --- Configuración de Archivos ---
VIDEO_FILE = "clase.mp4"
AUDIO_FILE = "audio_extraido.mp3"
TRANSCRIPT_FILE = "transcripcion_final.txt"

# --- Parte 1: Extracción Condicional de Audio ---

# Comprobamos si el archivo de audio ya existe
if os.path.exists(AUDIO_FILE):
    print(f"1. El archivo de audio '{AUDIO_FILE}' ya existe. Saltando la extracción de video.")
else:
    print(f"1. Extrayendo audio de {VIDEO_FILE}...")
    try:
        # Nota: Usamos la importación que ha funcionado en pasos anteriores.
        # Si te funcionó 'from moviepy import VideoFileClip', usa esa línea al inicio.
        # Asumo que estás usando la versión MoviePy 1.0.3, por eso el .editor está ahí.
        clip = VideoFileClip(VIDEO_FILE) 
        
        # Línea corregida que funciona con MoviePy 1.0.3
        clip.audio.write_audiofile(AUDIO_FILE) 
        
        clip.close()
        print("   -> Audio extraído exitosamente.")
    except Exception as e:
        print(f"ERROR al extraer audio: {e}")
        # Si la extracción falla, salimos del script, ya que el paso de transcripción no funcionará.
        exit()

# --- Parte 2: Transcripción del Audio con Whisper ---

print(f"2. Cargando modelo de Whisper (puede tomar unos segundos)...")
# # Usaremos el mismo modelo 'base' para un equilibrio entre velocidad y precisión.
# try:
#     model = whisper.load_model("base")
#     #model = whisper.load_model("small")
# except AttributeError:
#     print("\nERROR de Whisper: Asegúrate de haber instalado 'openai-whisper' correctamente.")
#     print("Vuelve a intentarlo con: pip install -U openai-whisper")
#     exit()

try:
    print("Intentando cargar Whisper...")
    model = whisper.load_model("base")
    print("¡Modelo cargado!")
except Exception as e:
    print(f"\nEL ERROR REAL ES: {e}")
    import traceback
    traceback.print_exc() # Esto nos dirá exactamente en qué línea y por qué falla
    exit()

print(f"3. Transcribiendo audio a texto...")
# REALIZA LA TRANSCRIPCIÓN CON BARRA DE PROGRESO (verbose=False)
# El argumento 'fp16=False' es para evitar problemas comunes en CPU y algunas GPUs.
# El argumento 'verbose=False' habilita la barra de progreso de tqdm.
result = model.transcribe(AUDIO_FILE, fp16=False, verbose=False) 

# 'language="es"' asegura que transcriba en español
# 'task="transcribe"' es el valor por defecto (puedes omitirlo, pero sirve para ser claro)
# result = model.transcribe(AUDIO_FILE, fp16=False, verbose=False, language="es")

# --- Parte 3: Guardar la Transcripción en un Archivo TXT ---
transcription_text = result["text"]

with open(TRANSCRIPT_FILE, "w", encoding="utf-8") as f:
    f.write(transcription_text)

print(f"4. ¡Proceso completado! La transcripción se guardó en '{TRANSCRIPT_FILE}'")