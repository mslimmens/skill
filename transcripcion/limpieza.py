import os

# Lista de archivos que queremos eliminar
archivos_a_eliminar = [
    "clase.mp4", 
    "audio_extraido.mp3", 
    "transcripcion_final.txt"
]

print("--- Iniciando limpieza de archivos ---")

for archivo in archivos_a_eliminar:
    # Verificamos si el archivo existe antes de intentar borrarlo
    if os.path.exists(archivo):
        try:
            os.remove(archivo)
            print(f"✅ Eliminado: {archivo}")
        except Exception as e:
            print(f"❌ Error al eliminar {archivo}: {e}")
    else:
        print(f"ℹ️ El archivo '{archivo}' no existe, saltando...")

print("--- Proceso de limpieza finalizado ---")