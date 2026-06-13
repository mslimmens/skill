from PIL import Image
import os

def crear_gif():
    # 1. Pedir paths
    carpeta_input = input("Ingresa la ruta de la carpeta con las imágenes: ").strip()
    ruta_output = input("Ingresa la ruta completa incluyendo el nombre del archivo (ej: /home/matias/mi_gif.gif): ").strip()
    
    # Asegurar que la ruta de salida tenga extensión .gif
    if not ruta_output.lower().endswith('.gif'):
        ruta_output += '.gif'
        print(f"Nota: Se añadió la extensión .gif automáticamente -> {ruta_output}")

    try:
        duracion = int(input("Ingresa la duración de cada transición en milisegundos (ej: 1000): "))
    except ValueError:
        print("Error: La duración debe ser un número entero.")
        return

    # 2. Obtener archivos de imagen (filtrando basura de Mac y asegurando formato)
    archivos = sorted([
        f for f in os.listdir(carpeta_input) 
        if f.lower().endswith(('.png', '.jpg', '.jpeg')) and not f.startswith('._')
    ])
    
    if not archivos:
        print("No se encontraron imágenes válidas en esa carpeta.")
        return

    frames = []
    print(f"Se encontraron {len(archivos)} imágenes. Procesando...")

    # 3. Procesar imágenes
    for archivo in archivos:
        path_img = os.path.join(carpeta_input, archivo)
        try:
            img = Image.open(path_img)
            
            # Redimensionar para evitar errores de memoria (max 800px ancho)
            if img.width > 800:
                ratio = 800 / float(img.width)
                new_height = int(float(img.height) * float(ratio))
                img = img.resize((800, new_height), Image.Resampling.LANCZOS)
            
            frames.append(img)
            print(f"Procesada: {archivo}")
        except Exception as e:
            print(f"No se pudo procesar {archivo}: {e}")

    # 4. Guardar GIF
    if frames:
        print("Guardando GIF, por favor espera...")
        frames[0].save(
            ruta_output,
            format='GIF',
            append_images=frames[1:],
            save_all=True,
            duration=duracion,
            loop=0,
            optimize=True
        )
        print(f"¡GIF creado con éxito en: {ruta_output}!")
    else:
        print("No se pudieron generar frames para el GIF.")

if __name__ == "__main__":
    crear_gif()