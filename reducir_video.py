import ffmpeg

def comprimir_video(video_origen, video_destino, calidad=26):
    """
    Reduce el tamaño de un video usando el códec H.265.
    calidad (CRF): A menor número, mejor calidad pero más pesado. 
                   El rango ideal es entre 22 y 28.
    """
    try:
        print("Comprimiendo... Esto puede tardar unos segundos.")
        
        (
            ffmpeg
            .input(video_origen)
            .output(video_destino, vcodec='libx265', crf=calidad, acodec='aac')
            .run(overwrite_output=True)
        )
        
        print(True, f"¡Video comprimido con éxito guardado en: {video_destino}!")
    except ffmpeg.Error as e:
        print(f"Hubo un error al procesar el video: {e.stderr.decode()}")

# Ejemplo de uso
video_input = "test.mp4"
video_output = "mi_video_comprimido.mp4"

comprimir_video(video_input, video_output, calidad=24)