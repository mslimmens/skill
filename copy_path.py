import os
import shutil

def procesar_archivos():
    # 1. Pedir los paths
    path_origen = input("Ingresa el path de la carpeta de origen: ").strip().replace("'", "")
    path_destino = input("Ingresa el path de la carpeta de destino: ").strip().replace("'", "")

    if not os.path.exists(path_origen) or not os.path.exists(path_destino):
        print("Error: Uno de los paths no es válido.")
        return

    # 2. Revisar archivos en origen
    archivos = os.listdir(path_origen)
    
    for nombre_archivo in archivos:
        # Filtramos para ignorar los que ya tienen el sufijo '_copy'
        if "_copy" in nombre_archivo:
            continue
            
        ruta_completa_origen = os.path.join(path_origen, nombre_archivo)
        
        # Solo procesamos si es un archivo (no una carpeta)
        if os.path.isfile(ruta_completa_origen):
            print(f"Procesando: {nombre_archivo}")
            
            # 3. Definir nuevo nombre y ruta de destino
            nombre_base, ext = os.path.splitext(nombre_archivo)
            nuevo_nombre = f"{nombre_base}_copy{ext}"
            ruta_destino = os.path.join(path_destino, nuevo_nombre)
            
            # 4. Copiar
            try:
                shutil.copy2(ruta_completa_origen, ruta_destino)
                
                # 5. Cambiar el nombre al original para marcarlo como procesado
                nuevo_path_origen = os.path.join(path_origen, nuevo_nombre)
                os.rename(ruta_completa_origen, nuevo_path_origen)
                
                print(f" -> Copiado y marcado como: {nuevo_nombre}")
            except Exception as e:
                print(f" -> Error al copiar {nombre_archivo}: {e}")

if __name__ == "__main__":
    procesar_archivos()