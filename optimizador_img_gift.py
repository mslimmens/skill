from PIL import Image
import os

def optimizar_archivo():
    path_input = input("Ingresa la ruta completa del archivo (imagen o GIF): ").strip().replace("'", "")
    
    if not os.path.exists(path_input):
        print("Error: Archivo no encontrado.")
        return

    # Preparar ruta de salida
    directorio = os.path.dirname(path_input)
    nombre_base, ext = os.path.splitext(os.path.basename(path_input))
    ruta_output = os.path.join(directorio, f"{nombre_base}_v_opt{ext}")

    try:
        with Image.open(path_input) as img:
            if ext.lower() in ['.jpg', '.jpeg']:
                # JPG: optimize=True busca el mejor equilibrio calidad/peso
                img.save(ruta_output, "JPEG", optimize=True, quality=85)
            
            elif ext.lower() == '.png':
                # PNG: optimize=True reduce el tamaño sin perder datos
                img.save(ruta_output, "PNG", optimize=True)
            
            elif ext.lower() == '.gif':
                # Si el GIF es muy grande, lo redimensionamos para no saturar la RAM
                if img.width > 800: # Si mide más de 800px de ancho
                    ratio = 800 / float(img.width)
                    new_height = int(float(img.height) * float(ratio))
                    img = img.resize((800, new_height), Image.Resampling.LANCZOS)
                
                # Guardar con optimización de frames
                img.save(ruta_output, "GIF", optimize=True, save_all=True)
            
            else:
                print("Formato no soportado para optimización automática.")
                return

        print(f"¡Éxito! Archivo optimizado guardado en: {ruta_output}")
        # Comparar tamaños
        print(f"Tamaño original: {os.path.getsize(path_input)/1024:.1f} KB")
        print(f"Tamaño nuevo: {os.path.getsize(ruta_output)/1024:.1f} KB")

    except Exception as e:
        print(f"Error al procesar: {e}")

if __name__ == "__main__":
    optimizar_archivo()