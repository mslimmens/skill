import os

def listar_directorio(ruta, prefijo=""):
    # Obtenemos el nombre de la carpeta actual
    nombre_carpeta = os.path.basename(os.path.abspath(ruta))
    
    # Si es la raíz de la ejecución, imprimimos el nombre base
    if prefijo == "":
        print(f"[{nombre_carpeta}]")
    
    # Listamos el contenido y filtramos para ignorar archivos ocultos (opcional)
    try:
        items = sorted(os.listdir(ruta))
    except PermissionError:
        print(f"{prefijo}└── [Acceso Denegado]")
        return

    for i, item in enumerate(items):
        ruta_completa = os.path.join(ruta, item)
        es_ultimo = (i == len(items) - 1)
        
        # Seleccionamos el conector visual
        conector = "└── " if es_ultimo else "├── "
        print(f"{prefijo}{conector}{item}")

        # Si el item es un directorio, llamamos a la función recursivamente
        if os.path.isdir(ruta_completa):
            nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")
            listar_directorio(ruta_completa, nuevo_prefijo)

# Uso del script
ruta_objetivo = input("Introduce la ruta del directorio: ")

if os.path.exists(ruta_objetivo):
    listar_directorio(ruta_objetivo)
else:
    print("La ruta no es válida.")