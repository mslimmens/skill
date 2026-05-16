import os
from PIL import Image
from pathlib import Path

def optimizar_recurso(ruta_entrada, calidad=80):
    path_recurso = Path(ruta_entrada.strip().replace('"', '').replace("'", ""))
    
    if not path_recurso.exists():
        print(f"❌ El archivo o ruta no existe: {path_recurso}")
        return

    # Definimos la función interna de procesamiento para no repetir código
    def procesar_archivo(archivo):
        extensiones = ('.jpg', '.jpeg', '.png', '.bmp')
        if archivo.suffix.lower() in extensiones:
            try:
                with Image.open(archivo) as img:
                    # Creamos el nombre de salida: nombre_original_opt.webp
                    nuevo_nombre = f"{archivo.stem}_opt.webp"
                    ruta_destino = archivo.parent / nuevo_nombre
                    
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    
                    img.save(ruta_destino, "WEBP", quality=calidad, optimize=True)
                    
                    tamano_orig = os.path.getsize(archivo) / 1024
                    tamano_final = os.path.getsize(ruta_destino) / 1024
                    ahorro = 100 - (tamano_final / tamano_orig * 100)
                    
                    print(f"✅ ¡Optimizado!: {archivo.name}")
                    print(f"   📉 {tamano_orig:.1f}KB -> {tamano_final:.1f}KB (Ahorro: {ahorro:.1f}%)")
                    print(f"   📍 Ubicación: {ruta_destino}")
            except Exception as e:
                print(f"⚠️ Error procesando {archivo.name}: {e}")

    # Lógica de decisión: ¿Es archivo o es carpeta?
    if path_recurso.is_file():
        procesar_archivo(path_recurso)
    elif path_recurso.is_dir():
        print(f"📂 Carpeta detectada. Procesando imágenes en {path_recurso}...")
        for item in path_recurso.iterdir():
            procesar_archivo(item)
    else:
        print("❌ El formato de ruta no es válido.")

if __name__ == "__main__":
    print("--- Optimizador de Imágenes para Web ---")
    ruta = input("Pega la ruta del archivo o carpeta: ")
    optimizar_recurso(ruta)