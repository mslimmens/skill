## reducción de video, solicita path mas el peso objetivo en mb, calcula bitrate y comprime con ffmpeg a ese peso aproximado.

import subprocess
import os

def obtener_duracion(ruta_video):
    """Obtiene la duración del video en segundos usando ffprobe."""
    cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', 
           '-of', 'default=noprint_wrappers=1:nokey=1', ruta_video]
    resultado = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(resultado.stdout)

def comprimir_video_interactivo():
    # 1. Pedir ruta y validar
    ruta_input = input("Ingresa la ruta completa del video: ").strip().replace("'", "")
    if not os.path.exists(ruta_input):
        print("Error: El archivo no existe.")
        return

    # 2. Pedir peso objetivo
    try:
        peso_mb = int(input("Ingresa el peso objetivo en MB (ej. 10): "))
    except ValueError:
        print("Por favor, ingresa un número válido.")
        return

    # 3. Preparar rutas de salida
    directorio = os.path.dirname(ruta_input)
    nombre_sin_ext, ext = os.path.splitext(os.path.basename(ruta_input))
    ruta_output = os.path.join(directorio, f"{nombre_sin_ext}_v{peso_mb}MB{ext}")

    # 4. Cálculo de bitrate
    duracion = obtener_duracion(ruta_input)
    peso_bits = peso_mb * 1024 * 1024 * 8
    bitrate = int(peso_bits / duracion)

    print(f"\nProcesando: {nombre_sin_ext}")
    print(f"Duración: {int(duracion // 60)}m {int(duracion % 60)}s")
    print(f"Comprimiendo a {peso_mb}MB...")

    # 5. Ejecutar FFmpeg
    comando = [
        'ffmpeg', '-i', ruta_input, 
        '-b:v', str(bitrate), 
        '-maxrate', str(bitrate),
        '-bufsize', str(bitrate * 2),
        '-vcodec', 'libx265', 
        '-acodec', 'aac', 
        '-y', ruta_output
    ]
    
    try:
        subprocess.run(comando, check=True)
        print(f"\n¡Éxito! Video guardado en:\n{ruta_output}")
    except subprocess.CalledProcessError:
        print("Ocurrió un error durante la compresión.")

if __name__ == "__main__":
    comprimir_video_interactivo()