import os
from moviepy import ImageClip, concatenate_videoclips, vfx

def crear_gif_profesional():
    print("--- Creador de GIFs Calidad Original (Sin redimensionar) ---")
    
    carpeta_input = input("Ruta de la carpeta: ").replace("'", "").replace('"', "").strip()
    ruta_output = input("Ruta de salida (.gif): ").replace("'", "").replace('"', "").strip()
    if not ruta_output.lower().endswith('.gif'): ruta_output += '.gif'

    try:
        duracion_imagen = float(input("Duración de cada imagen (seg): "))
        duracion_transicion = float(input("Duración de la disolvencia (seg): "))
    except ValueError:
        return

    efectos_disponibles = {"1": (vfx.CrossFadeIn, "Disolver"), "2": (vfx.FadeIn, "FadeIn"), "3": (vfx.FadeOut, "FadeOut")}
    opcion = input("Efecto (1-3): ")
    efecto_clase = efectos_disponibles.get(opcion, efectos_disponibles["1"])[0]

    rutas_imagenes = [os.path.join(raiz, f) for raiz, _, archivos in os.walk(carpeta_input) 
                     for f in sorted(archivos) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]

    clips = []
    print(f"\nProcesando {len(rutas_imagenes)} imágenes en CALIDAD ORIGINAL...")
    
    for ruta in rutas_imagenes:
        # AQUÍ ESTÁ EL CAMBIO: Quitamos totalmente .resized()
        # Esto mantiene la resolución y peso exacto de tus archivos originales
        clip = ImageClip(ruta, duration=duracion_imagen)
        clip = clip.with_effects([efecto_clase(duracion_transicion)])
        clips.append(clip)

    if not clips: return

    primer_clip_loop = clips[0].with_effects([efecto_clase(duracion_transicion)])
    clips.append(primer_clip_loop)

    video_final = concatenate_videoclips(clips, method="compose", padding=-duracion_transicion)
    
    print("\nRenderizando a calidad original (esto puede tardar más)...")
    # Al no usar 'opt' ni redimensionar, MoviePy usará los pixeles puros
    video_final.write_gif(ruta_output, fps=10, loop=0)
    
    print(f"\n¡Listo! Calidad original intacta en: {ruta_output}")

if __name__ == "__main__":
    crear_gif_profesional()