import os
import shutil
from datetime import datetime

def organizar_videos(directorio_origen, directorio_destino):
    directorio_origen = directorio_origen.replace("'", "").replace('"', "").strip()
    directorio_destino = directorio_destino.replace("'", "").replace('"', "").strip()

    # Extensiones de video comunes
    extensiones = ('.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv')
    
    ruta_duplicados = os.path.join(directorio_destino, "Duplicados")
    contador = 0
    duplicados = 0

    print("Iniciando organización de videos...")

    for raiz, carpetas, archivos in os.walk(directorio_origen):
        for nombre_archivo in archivos:
            if nombre_archivo.lower().endswith(extensiones):
                ruta_completa = os.path.join(raiz, nombre_archivo)
                
                # Usamos la fecha de creación/modificación del archivo
                timestamp = os.path.getmtime(ruta_completa)
                fecha = datetime.fromtimestamp(timestamp)
                
                nombre_subcarpeta = fecha.strftime('%Y/%m')
                ruta_destino_final = os.path.join(directorio_destino, nombre_subcarpeta)
                ruta_final_archivo = os.path.join(ruta_destino_final, nombre_archivo)

                os.makedirs(ruta_destino_final, exist_ok=True)

                if not os.path.exists(ruta_final_archivo):
                    shutil.copy2(ruta_completa, ruta_final_archivo)
                    print(f"Organizado: {nombre_archivo}")
                    contador += 1
                else:
                    os.makedirs(ruta_duplicados, exist_ok=True)
                    shutil.copy2(ruta_completa, os.path.join(ruta_duplicados, nombre_archivo))
                    print(f"Duplicado: {nombre_archivo}")
                    duplicados += 1

    print(f"\nProceso finalizado. Videos organizados: {contador}, Duplicados encontrados: {duplicados}")

if __name__ == "__main__":
    origen = input("Carpeta con videos (origen): ")
    destino = input("Carpeta donde guardar (destino): ")
    organizar_videos(origen, destino)