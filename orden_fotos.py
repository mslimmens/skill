import os
import shutil
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS

def obtener_fecha_real(ruta_archivo):
    try:
        img = Image.open(ruta_archivo)
        exif = img._getexif()
        if exif:
            for tag, value in exif.items():
                if TAGS.get(tag) == 'DateTimeOriginal':
                    return datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
    except Exception:
        pass
    return datetime.fromtimestamp(os.path.getmtime(ruta_archivo))

def organizar_fotos(directorio_origen, directorio_destino):
    directorio_origen = directorio_origen.replace("'", "").replace('"', "").strip()
    directorio_destino = directorio_destino.replace("'", "").replace('"', "").strip()

    if not os.path.exists(directorio_origen):
        print(f"Error: La carpeta '{directorio_origen}' no existe.")
        return

    extensiones = ('.jpg', '.jpeg', '.png')
    ruta_duplicados = os.path.join(directorio_destino, "Duplicados")
    
    contador = 0
    duplicados = 0

    # os.walk recorre el directorio y todas sus subcarpetas
    for raiz, carpetas, archivos in os.walk(directorio_origen):
        for nombre_archivo in archivos:
            if nombre_archivo.lower().endswith(extensiones):
                ruta_completa = os.path.join(raiz, nombre_archivo)
                
                # Obtener fecha real
                fecha = obtener_fecha_real(ruta_completa)
                
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

    print(f"\nProceso finalizado. Organizados: {contador}, Duplicados: {duplicados}")

if __name__ == "__main__":
    origen = input("Carpeta con imágenes (origen): ")
    destino = input("Carpeta donde guardar (destino): ")
    organizar_fotos(origen, destino)