import os
from PIL import Image, ImageDraw

def hacer_ico_circular():
    print("--- Convertidor de Imagen a Icono Circular (.ico) ---")
    
    # 1. Pedir la ruta de la imagen de origen
    ruta_entrada = input("Arrastra la imagen original aquí (o escribe su ruta) y presiona Enter: ").strip()
    
    # Limpiar comillas por si arrastraron el archivo a la terminal
    ruta_entrada = ruta_entrada.strip("'\"")
    
    # Validar que el archivo exista
    if not os.path.exists(ruta_entrada):
        print(f"❌ Error: No se encontró ningún archivo en la ruta: {ruta_entrada}")
        return

    # 2. Pedir la ruta del directorio donde se guardará el .ico
    directorio_salida = input("Arrastra la carpeta donde quieres guardarlo (o escribe su ruta) y presiona Enter: ").strip()
    directorio_salida = directorio_salida.strip("'\"")
    
    # Validar que la carpeta de destino exista
    if not os.path.isdir(directorio_salida):
        print(f"❌ Error: La carpeta de destino no existe: {directorio_salida}")
        return

    # Pedir el nombre del archivo final
    nombre_archivo = input("Escribe el nombre para el archivo (ej: mi_icono) sin la extensión: ").strip()
    if not nombre_archivo.endswith(".ico"):
        nombre_archivo += ".ico"
        
    # Construir la ruta final completa
    ruta_salida = os.path.join(directorio_salida, nombre_archivo)

    try:
        print("\nProcesando imagen...")
        # 3. Abrir y convertir a RGBA
        img = Image.open(ruta_entrada).convert("RGBA")
        
        # 4. Hacerla cuadrada
        tsize = min(img.size)
        img = img.crop((
            (img.width - tsize) // 2,
            (img.height - tsize) // 2,
            (img.width + tsize) // 2,
            (img.height + tsize) // 2
        ))
        
        # 5. Crear la máscara circular
        mask = Image.new("L", (tsize, tsize), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, tsize, tsize), fill=255)
        
        # 6. Aplicar máscara
        img_circular = Image.new("RGBA", (tsize, tsize))
        img_circular.paste(img, (0, 0), mask=mask)
        
        # 7. Guardar en múltiples tamaños para Windows
        img_circular.save(
            ruta_salida, 
            format="ICO", 
            sizes=[(16, 16), (32, 32), (48, 48), (256, 256)]
        )
        print(f"✨ ¡Éxito! Tu icono circular se guardó en:\n👉 {ruta_salida}\n")
        
    except Exception as e:
        print(f"❌ Ocurrió un error al procesar la imagen: {e}")

# Ejecutar la función
if __name__ == "__main__":
    hacer_ico_circular()