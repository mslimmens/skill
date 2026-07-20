from PIL import Image
import os

def optimizar_gif(img, max_width=800):
    """Redimensiona todos los frames de un GIF."""
    frames = []
    duration = img.info.get('duration', 100) # Mantener duración original
    
    for i in range(img.n_frames):
        img.seek(i)
        # Redimensionar frame individual
        if img.width > max_width:
            ratio = max_width / float(img.width)
            new_height = int(float(img.height) * float(ratio))
            frame = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        else:
            frame = img.copy()
        frames.append(frame)
    
    return frames, duration

def optimizar_archivo():
    path_input = input("Ingresa la ruta completa del archivo (imagen o GIF): ").strip().replace("'", "")
    
    if not os.path.exists(path_input):
        print("Error: Archivo no encontrado.")
        return

    directorio = os.path.dirname(path_input)
    nombre_base, ext = os.path.splitext(os.path.basename(path_input))
    ruta_output = os.path.join(directorio, f"{nombre_base}_v_opt{ext}")

    try:
        with Image.open(path_input) as img:
            if ext.lower() in ['.jpg', '.jpeg']:
                img.save(ruta_output, "JPEG", optimize=True, quality=85)
            
            elif ext.lower() == '.png':
                img.save(ruta_output, "PNG", optimize=True)
            
            elif ext.lower() == '.gif':
                # Si es necesario redimensionar
                if img.width > 800:
                    frames, duration = optimizar_gif(img, 800)
                    # Guardar la lista de frames
                    frames[0].save(ruta_output, save_all=True, append_images=frames[1:], 
                                   optimize=True, duration=duration, loop=0)
                else:
                    # Si no necesita redimensionar, guardamos tal cual
                    img.save(ruta_output, "GIF", optimize=True, save_all=True)
            
            else:
                print("Formato no soportado.")
                return

        print(f"¡Éxito! Archivo guardado en: {ruta_output}")
    except Exception as e:
        print(f"Error al procesar: {e}")

if __name__ == "__main__":
    optimizar_archivo()