import os
from PIL import Image
import qrcode
from qrcode.constants import ERROR_CORRECT_H

def generar_qr_con_logo(url_destino, ruta_imagen, ruta_salida="qr_con_imagen.png"):
    # 1. Configurar el QR con nivel de corrección alto (H) para soportar la imagen central
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url_destino)
    qr.make(fit=True)

    # Crear la imagen base del QR
    img_qr = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    # 2. Abrir la imagen que quieres dejar en el centro
    try:
        logo = Image.open(ruta_imagen)
    except FileNotFoundError:
        print(f"\n[ERROR] No se encontró la imagen en la ruta especificada: '{ruta_imagen}'")
        return False

    # 3. Calcular el tamaño (aprox 25% del ancho del QR)
    ancho_qr, alto_qr = img_qr.size
    tamanio_logo = int(ancho_qr / 4)
    
    # Redimensionar el logo manteniendo proporciones
    logo = logo.resize((tamanio_logo, tamanio_logo), Image.Resampling.LANCZOS)

    # Si la imagen tiene transparencia (RGBA), ponerle fondo blanco
    if logo.mode in ("RGBA", "LA"):
        fondo_blanco = Image.new("RGBA", logo.size, "WHITE")
        logo = Image.alpha_composite(fondo_blanco, logo).convert("RGB")

    # 4. Calcular la posición para centrarlo
    pos_x = (ancho_qr - tamanio_logo) // 2
    pos_y = (alto_qr - tamanio_logo) // 2

    # 5. Pegar la imagen en el centro
    img_qr.paste(logo, (pos_x, pos_y))

    # 6. Guardar el resultado final
    img_qr.save(ruta_salida)
    print(f"\n¡Éxito! Código QR generado y guardado correctamente como: '{ruta_salida}'")
    return True

if __name__ == "__main__":
    print("=== GENERADOR DE QR CON IMAGEN INTERACTIVO ===")
    
    # Pedir datos por consola
    url = input("1. Ingresa la URL o texto de destino (ej: https://miweb.com): ").strip()
    if not url:
        print("La URL no puede estar vacía.")
        exit()

    ruta_logo = input("2. Ingresa la ruta de la imagen o logo (ej: logo.png): ").strip()
    if not ruta_logo:
        print("La ruta de la imagen no puede estar vacía.")
        exit()

    ruta_out = input("3. Ingresa el nombre del archivo de salida (por defecto 'qr_final.png'): ").strip()
    if not ruta_out:
        ruta_out = "qr_final.png"
    
    # Asegurarnos de que tenga extensión de imagen
    if not ruta_out.lower().endswith(('.png', '.jpg', '.jpeg')):
        ruta_out += ".png"

    print("\nGenerando código QR, por favor espera...")
    generar_qr_con_logo(url, ruta_logo, ruta_out)