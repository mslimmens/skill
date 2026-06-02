## reduce video, al maximo manteniendo calidad, solicita path y comprime con ffmpeg a ese peso aproximado.

import subprocess
import os

def comprimir_video():
    # 1. Pedir la ruta del video al usuario
    ruta_input = input("Ingresa la ruta completa del video (ej. /home/matias/video.mp4): ").strip().replace("'", "")
    
    if not os.path.exists(ruta_input):
        print("Error: El archivo no existe. Por favor, verifica la ruta.")
        return

    # 2. Generar el nombre de salida en la misma carpeta
    directorio = os.path.dirname(ruta_input)
    nombre_base = os.path.basename(ruta_input)
    nombre_sin_ext, ext = os.path.splitext(nombre_base)
    
    ruta_output = os.path.join(directorio, f"{nombre_sin_ext}_comprimido{ext}")

    # 3. Comprimir
    try:
        print(f"Comprimiendo: {nombre_base}...")
        print(f"Guardando en: {ruta_output}")
        
        comando = [
            'ffmpeg', '-i', ruta_input, 
            '-vcodec', 'libx265', 
            '-crf', '24', 
            '-acodec', 'aac', 
            '-y', ruta_output
        ]
        
        subprocess.run(comando, check=True)
        print("¡Proceso completado con éxito!")
        
    except subprocess.CalledProcessError as e:
        print(f"Hubo un error al procesar el video: {e}")

if __name__ == "__main__":
    comprimir_video()