import os
from pathlib import Path
from rembg import remove
from PIL import Image

def quitar_fondo(ruta_entrada):
    # Limpiamos la ruta
    path_recurso = Path(ruta_entrada.strip().replace('"', '').replace("'", ""))
    
    if not path_recurso.exists() or not path_recurso.is_file():
        print(f"❌ No se encontró el archivo en: {path_recurso}")
        return

    try:
        print(f"⏳ Procesando '{path_recurso.name}'... (la primera vez puede tardar un poco)")
        
        # Abrimos la imagen original
        input_image = Image.open(path_recurso)
        
        # Eliminamos el fondo
        output_image = remove(input_image)
        
        # Creamos el nombre de salida (siempre PNG para mantener la transparencia)
        ruta_destino = path_recurso.parent / f"{path_recurso.stem}_sin_fondo.png"
        
        # Guardamos el resultado
        output_image.save(ruta_destino)
        
        print(f"✅ ¡Fondo eliminado con éxito!")
        print(f"📍 Guardado en: {ruta_destino}")

    except Exception as e:
        print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    ruta = input("Pega la ruta de la imagen (ej. /Users/matydev/.../seVoz.png): ")
    quitar_fondo(ruta)