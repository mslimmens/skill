from PIL import Image
from PIL.ExifTags import TAGS

def obtener_fecha_exif(ruta_imagen):
    img = Image.open(ruta_imagen)
    exif_data = img._getexif()
    if not exif_data:
        return "No tiene datos EXIF"
    
    for tag_id, value in exif_data.items():
        tag = TAGS.get(tag_id, tag_id)
        if tag == 'DateTimeOriginal':
            return value
    return "No se encontró la fecha original"

ruta = input("Arrastra la imagen: ").replace("'", "").strip()
print(f"Fecha real de captura: {obtener_fecha_exif(ruta)}")