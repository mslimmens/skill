from pathlib import Path
from PIL import Image

def optimizar_imagenes():
    # 1. Solicitar ruta de origen
    origen_input = input("Ingresa la ruta de la carpeta con las imágenes originales: ").strip()
    origen_input = origen_input.replace("'", "").replace('"', "")
    carpeta_origen = Path(origen_input).expanduser().resolve()
    
    if not carpeta_origen.exists() or not carpeta_origen.is_dir():
        print("❌ La ruta de origen ingresada no es válida.")
        return

    # 2. Solicitar ruta de destino
    destino_input = input("Ingresa la ruta de la carpeta donde se guardarán las optimizadas: ").strip()
    destino_input = destino_input.replace("'", "").replace('"', "")
    carpeta_destino = Path(destino_input).expanduser().resolve()
    
    # Crear la carpeta de destino si no existe (incluyendo carpetas intermedias si fuera necesario)
    carpeta_destino.mkdir(parents=True, exist_ok=True)

    extensiones = (".jpg", ".jpeg", ".png", ".webp", ".JPG", ".JPEG", ".PNG", ".WEBP")
    archivos = [f for f in carpeta_origen.iterdir() if f.is_file() and f.suffix in extensiones]

    if not archivos:
        print("⚠️ No se encontraron imágenes compatibles en la carpeta de origen.")
        return

    print(f"\n🚀 Procesando {len(archivos)} imágenes...")

    for archivo in archivos:
        try:
            with Image.open(archivo) as img:
                # Si es PNG con transparencia, se preserva el formato y canal alfa
                if img.format == "PNG" and img.mode in ("RGBA", "LA"):
                    salida = carpeta_destino / f"{archivo.stem}.png"
                    img.save(salida, "PNG", optimize=True)
                else:
                    # Para fotos estándar (JPEG/WebP), convertimos a RGB y aplicamos calidad alta (88)
                    if img.mode != "RGB":
                        img = img.convert("RGB")
                    
                    salida = carpeta_destino / f"{archivo.stem}.jpg"
                    img.save(salida, "JPEG", quality=88, optimize=True)
                    
            print(f"  [OK] Optimizado: {archivo.name}")
        except Exception as e:
            print(f"  [ERROR] No se pudo procesar {archivo.name}: {e}")

    print(f"\n✅ ¡Proceso terminado! Tus imágenes optimizadas están en: {carpeta_destino}")

if __name__ == "__main__":
    optimizar_imagenes()